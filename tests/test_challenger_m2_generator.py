"""
tests/test_challenger_m2_generator.py
=====================================
Empirical Adversarial Stress Test Suite for Milestone 2 Animation Generator:
`scripts/build_animated_stickers.py`.

Author: Challenger M2-1 (Frame Integrity & Generation Challenger)
Constraints:
  1. Generate sample stickers across ALL 14 motion primitives.
  2. Frame Uniqueness Checks: assert strictly 24 unique frames, NO frame coalescing in WebP and GIF outputs.
  3. Verify timing (24 @ 90ms = 2.16s >= 2.0s), dimensions (512x512), loop continuity.
  4. Adversarial corner cases: missing sticker ID, non-square source, RGB vs RGBA source, corrupted source.
"""

import os
import sys
import tempfile
import unittest
import subprocess
from typing import List, Tuple, Dict, Any
from PIL import Image, ImageSequence, ImageChops

# Ensure workspace root is in python path
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from scripts.build_animated_stickers import (
    STICKER_RIG_REGISTRY,
    PRIMITIVE_DISP,
    PRIMITIVE_OVERLAY,
    classify_rig,
    process_one,
    disp_tanty_akumbo_tilt,
)
from tests.e2e.test_helpers import parse_webp_binary, parse_gif_binary


# Map each of the 14 motion primitives to representative stickers
REPRESENTATIVE_STICKERS = {
    "soca_rag_windmill": "rel-bess",
    "steups_recoil_burst": "steups",
    "allfours_table_slam": "hang-jack",
    "doubles_45_lean_drip": "doubles-lean",
    "tanty_akumbo_tilt": "ent",
    "bazodee_dazed_spiral": "pure-bazodee",
    "maco_peep_zoom": "look-trouble",
    "heat_seeking_slipper_arc": "flying-slipper",
    "puncheon_fire_breath": "weyyyy",
    "steelpan_rebound": "steelpan-3d",
    "killing_dead_collapse": "ah-eh-able",
    "ttec_blackout_candle": "ttec-current-gone",
    "moko_jumbie_stilt_sway": "moko-jumbie",
    "wasa_dry_shower_cough": "wasa-water-gone",
}

# Additional stress stickers
ADDITIONAL_STICKERS = [
    "slang-steups",
    "buss-up-shut",
    "deya-parsad",
    "soucouyant",
    "maco",
]


class TestChallengerM2Generator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.python_exe = sys.executable
        cls.script_path = os.path.join(WORKSPACE_DIR, "scripts", "build_animated_stickers.py")
        cls.anim_dir = os.path.join(WORKSPACE_DIR, "assets", "animated")
        cls.stickers_dir = os.path.join(WORKSPACE_DIR, "assets", "stickers")

        # Ensure all representative stickers are built and non-empty
        all_test_sids = list(REPRESENTATIVE_STICKERS.values()) + ADDITIONAL_STICKERS
        print(f"\n[SETUP] Pre-generating {len(all_test_sids)} test stickers across all 14 primitives...")
        for sid in all_test_sids:
            webp_path = os.path.join(cls.anim_dir, f"{sid}.webp")
            gif_path = os.path.join(cls.anim_dir, f"{sid}.gif")
            needs_build = (
                not os.path.exists(webp_path)
                or not os.path.exists(gif_path)
                or os.path.getsize(webp_path) == 0
                or os.path.getsize(gif_path) == 0
            )
            if needs_build:
                print(f"  Generating {sid}...")
                process_one(f"{sid}.png")

    # =========================================================================
    # TEST 1: COVERAGE OF ALL 14 MOTION PRIMITIVES
    # =========================================================================
    def test_01_all_14_primitives_covered(self):
        """TC-CHALLENGER-01: Verify all 14 motion primitives have assigned stickers in registry."""
        primitives_in_registry = set()
        for sid, data in STICKER_RIG_REGISTRY.items():
            primitives_in_registry.add(data["primitive"])

        for prim_name in PRIMITIVE_DISP.keys():
            self.assertIn(
                prim_name,
                primitives_in_registry,
                f"Primitive '{prim_name}' has 0 stickers in STICKER_RIG_REGISTRY!",
            )
        self.assertEqual(len(primitives_in_registry), 14, "Registry must cover exactly 14 primitives")

    # =========================================================================
    # TEST 2: CLI GENERATION ACROSS PRIMITIVES
    # =========================================================================
    def test_02_cli_single_sticker_generation(self):
        """TC-CHALLENGER-02: Test CLI invocation with --sticker across representative primitives."""
        test_samples = ["steups", "hang-jack", "pure-bazodee", "moko-jumbie"]
        for sid in test_samples:
            cmd = [self.python_exe, self.script_path, "--sticker", sid]
            res = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"CLI generation failed for '{sid}': {res.stderr}")
            self.assertIn(f"Generated {sid}", res.stdout)
            self.assertIn("WebP:", res.stdout)
            self.assertIn("GIF:", res.stdout)

    def test_02b_cli_extension_and_whitespace_resilience(self):
        """TC-CHALLENGER-02B: Test CLI robustness with .png extension and whitespace."""
        for raw_arg in ["steups.png", "  steups  ", "STEUPS.PNG"]:
            cmd = [self.python_exe, self.script_path, "--sticker", raw_arg]
            res = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"CLI failed on raw arg '{raw_arg}': {res.stderr}")
            self.assertIn("Generated steups", res.stdout)

    # =========================================================================
    # TEST 3: ADVERSARIAL FRAME UNIQUENESS & INTEGRITY (WEBP)
    # =========================================================================
    def test_03_webp_frame_uniqueness_and_integrity(self):
        """
        TC-CHALLENGER-03: Binary and frame-by-frame uniqueness check for WebP.
        Inspect all 24 frames across all representative stickers.
        Assert strictly 24 unique frames with NO adjacent frame coalescing.
        """
        all_sids = list(REPRESENTATIVE_STICKERS.values()) + ADDITIONAL_STICKERS
        for sid in all_sids:
            webp_path = os.path.join(self.anim_dir, f"{sid}.webp")
            self.assertTrue(os.path.exists(webp_path), f"Missing WebP: {webp_path}")

            # 1. Binary inspection
            b_info = parse_webp_binary(webp_path)
            self.assertTrue(b_info.get("exists"), f"Binary parse failed for {sid}.webp")
            self.assertTrue(b_info.get("has_animation"), f"{sid}.webp missing animation flag")
            self.assertTrue(b_info.get("has_alpha"), f"{sid}.webp missing alpha flag")
            self.assertEqual(b_info.get("width"), 512, f"{sid}.webp width != 512")
            self.assertEqual(b_info.get("height"), 512, f"{sid}.webp height != 512")
            self.assertEqual(b_info.get("frame_count"), 24, f"{sid}.webp frame_count != 24")
            self.assertEqual(b_info.get("total_duration_ms"), 2160, f"{sid}.webp duration != 2160ms")
            for d in b_info.get("durations", []):
                self.assertEqual(d, 90, f"{sid}.webp frame duration != 90ms")

            # 2. Pixel-level frame uniqueness
            with Image.open(webp_path) as im:
                frames = [f.copy().convert("RGBA") for f in ImageSequence.Iterator(im)]
            self.assertEqual(len(frames), 24, f"Pillow loaded {len(frames)} frames for {sid}.webp")

            for i in range(len(frames) - 1):
                f1 = frames[i]
                f2 = frames[i + 1]
                diff = ImageChops.difference(f1, f2)
                extrema = diff.getextrema()
                # Max difference across R, G, B, A
                max_diff = max(e[1] for e in extrema)
                self.assertGreater(
                    max_diff,
                    0,
                    f"ADVERSARIAL COALESCING DETECTED: Frame {i} and {i+1} in {sid}.webp are IDENTICAL! (max_diff=0)",
                )

    # =========================================================================
    # TEST 4: ADVERSARIAL FRAME UNIQUENESS & INTEGRITY (GIF)
    # =========================================================================
    def test_04_gif_frame_uniqueness_and_integrity(self):
        """
        TC-CHALLENGER-04: Binary and frame-by-frame uniqueness check for GIF.
        Inspect all 24 frames across all representative stickers on #10141E dark card.
        Assert strictly 24 unique frames with NO adjacent frame coalescing.
        """
        all_sids = list(REPRESENTATIVE_STICKERS.values()) + ADDITIONAL_STICKERS
        for sid in all_sids:
            gif_path = os.path.join(self.anim_dir, f"{sid}.gif")
            self.assertTrue(os.path.exists(gif_path), f"Missing GIF: {gif_path}")

            # 1. Binary inspection
            b_info = parse_gif_binary(gif_path)
            self.assertTrue(b_info.get("exists"), f"Binary parse failed for {sid}.gif")
            self.assertEqual(b_info.get("width"), 512, f"{sid}.gif width != 512")
            self.assertEqual(b_info.get("height"), 512, f"{sid}.gif height != 512")
            self.assertEqual(b_info.get("frame_count"), 24, f"{sid}.gif frame_count != 24")
            self.assertEqual(b_info.get("total_duration_ms"), 2160, f"{sid}.gif duration != 2160ms")
            for d in b_info.get("durations", []):
                self.assertEqual(d, 90, f"{sid}.gif frame duration != 90ms")

            # 2. Pixel-level frame uniqueness (RGB mode on dark card)
            with Image.open(gif_path) as im:
                frames = [f.copy().convert("RGB") for f in ImageSequence.Iterator(im)]
            self.assertEqual(len(frames), 24, f"Pillow loaded {len(frames)} frames for {sid}.gif")

            for i in range(len(frames) - 1):
                f1 = frames[i]
                f2 = frames[i + 1]
                diff = ImageChops.difference(f1, f2)
                extrema = diff.getextrema()
                max_diff = max(e[1] for e in extrema)
                self.assertGreater(
                    max_diff,
                    0,
                    f"ADVERSARIAL COALESCING DETECTED: Frame {i} and {i+1} in {sid}.gif are IDENTICAL! (max_diff=0)",
                )

    # =========================================================================
    # TEST 5: LIVING HOLD MICRO-MOTION EMPIRICAL ASSERTION
    # =========================================================================
    def test_05_living_hold_micro_motion(self):
        """
        TC-CHALLENGER-05: Stress-test the living hold jitter mechanism.
        Verify that in frames where the macro displacement function is in a static hold phase,
        adjacent frames STILL differ due to living_hold_jitter.
        """
        # maco_peep_zoom has static creep hold between t=0.25 and t=0.75 (Frames 6-18)
        # and static lens scale between t=0.40 and t=0.75
        maco_gif = os.path.join(self.anim_dir, "look-trouble.gif")
        with Image.open(maco_gif) as im:
            frames = [f.copy().convert("RGB") for f in ImageSequence.Iterator(im)]

        # Check adjacent frames in the hold window: frames 7 through 17
        for i in range(7, 17):
            diff = ImageChops.difference(frames[i], frames[i + 1])
            max_diff = max(e[1] for e in diff.getextrema())
            self.assertGreater(
                max_diff,
                0,
                f"Living hold failed: Frame {i} and {i+1} in look-trouble.gif coalesced during hold phase!",
            )

    # =========================================================================
    # TEST 6: MATHEMATICAL LOOP CONTINUITY AND BOUNDARY TRANSITION
    # =========================================================================
    def test_06_loop_continuity_displacement(self):
        """
        TC-CHALLENGER-06: Verify displacement function mathematical loop continuity:
        |disp(x, y, 1.0) - disp(x, y, 0.0)| < 1.0 px across all 14 primitives.
        """
        test_points = [
            (256.0, 256.0),
            (128.0, 128.0),
            (384.0, 384.0),
            (256.0, 480.0),
            (256.0, 100.0),
        ]
        for name, disp_fn in PRIMITIVE_DISP.items():
            for x, y in test_points:
                p0 = disp_fn(x, y, 0.0)
                p1 = disp_fn(x, y, 1.0)
                dx = abs(p0[0] - p1[0])
                dy = abs(p0[1] - p1[1])
                self.assertLess(
                    dx,
                    1.0,
                    f"Primitive {name} loop discontinuity in X at ({x}, {y}): |{p0[0]} - {p1[0]}| = {dx}",
                )
                self.assertLess(
                    dy,
                    1.0,
                    f"Primitive {name} loop discontinuity in Y at ({x}, {y}): |{p0[1]} - {p1[1]}| = {dy}",
                )

    # =========================================================================
    # TEST 7: ADVERSARIAL CORNER CASES & RESILIENCE
    # =========================================================================
    def test_07a_missing_sticker_id_error_handling(self):
        """TC-CHALLENGER-07A: Assert missing sticker ID raises FileNotFoundError and exits non-zero."""
        cmd = [self.python_exe, self.script_path, "--sticker", "non_existent_fake_sticker_999"]
        res = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "CLI must exit non-zero for missing sticker")
        self.assertIn("FileNotFoundError", res.stderr + res.stdout)

    def test_07b_non_square_source_image_handling(self):
        """
        TC-CHALLENGER-07B: Non-square input handling.
        Feed a 300x600 non-square image to process_one and verify output is strictly 512x512.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create synthetic non-square image
            non_square = Image.new("RGBA", (300, 600), (255, 100, 50, 255))
            fake_sid = "test_non_square_sample"
            fake_src = os.path.join(self.stickers_dir, f"{fake_sid}.png")
            try:
                non_square.save(fake_src)
                process_one(f"{fake_sid}.png", out_dir=tmp_dir)

                out_webp = os.path.join(tmp_dir, f"{fake_sid}.webp")
                out_gif = os.path.join(tmp_dir, f"{fake_sid}.gif")
                self.assertTrue(os.path.exists(out_webp))
                self.assertTrue(os.path.exists(out_gif))

                # Check WebP dimensions
                w_info = parse_webp_binary(out_webp)
                self.assertEqual(w_info["width"], 512)
                self.assertEqual(w_info["height"], 512)
                self.assertEqual(w_info["frame_count"], 24)

                # Check GIF dimensions
                g_info = parse_gif_binary(out_gif)
                self.assertEqual(g_info["width"], 512)
                self.assertEqual(g_info["height"], 512)
                self.assertEqual(g_info["frame_count"], 24)
            finally:
                if os.path.exists(fake_src):
                    os.remove(fake_src)

    def test_07c_rgb_source_image_handling(self):
        """
        TC-CHALLENGER-07C: RGB input (no alpha) handling.
        Feed an RGB image and verify it is converted to RGBA and processed cleanly.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            rgb_img = Image.new("RGB", (512, 512), (100, 150, 200))
            fake_sid = "test_rgb_no_alpha_sample"
            fake_src = os.path.join(self.stickers_dir, f"{fake_sid}.png")
            try:
                rgb_img.save(fake_src)
                process_one(f"{fake_sid}.png", out_dir=tmp_dir)

                out_webp = os.path.join(tmp_dir, f"{fake_sid}.webp")
                out_gif = os.path.join(tmp_dir, f"{fake_sid}.gif")
                self.assertTrue(os.path.exists(out_webp))
                self.assertTrue(os.path.exists(out_gif))

                w_info = parse_webp_binary(out_webp)
                self.assertEqual(w_info["frame_count"], 24)
                self.assertEqual(w_info["width"], 512)
                self.assertEqual(w_info["height"], 512)
            finally:
                if os.path.exists(fake_src):
                    os.remove(fake_src)

    def test_07d_corrupted_source_error_handling(self):
        """TC-CHALLENGER-07D: Feed a 0-byte corrupted image and verify clean exception handling."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            fake_sid = "test_corrupted_zero_byte"
            fake_src = os.path.join(self.stickers_dir, f"{fake_sid}.png")
            try:
                with open(fake_src, "wb") as f:
                    f.write(b"NOT_A_PNG_IMAGE_DATA")
                with self.assertRaises(Exception):
                    process_one(f"{fake_sid}.png", out_dir=tmp_dir)
            finally:
                if os.path.exists(fake_src):
                    os.remove(fake_src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
