"""
tests/test_tier5_adversarial_c1.py
==================================
Tier 5 Adversarial Coverage Hardening Suite: Asset Pipeline & Verification Engines.

Author: Challenger 1 (Milestone 5 Phase 2 Empirical Challenger)
Focus Area:
  1. `scripts/build_animated_stickers.py`:
     - Mathematical stability of comic timing curves, 14 motion primitives, and living hold jitter.
     - Squash & stretch cylindrical and volume-preserving offset bounds under adversarial parameters.
     - RGBA-to-RGB card composition on #10141E, alpha mask handling, and PIL quantize palette clamping (<= 128 colors).
     - Multiprocessing argument clamping, single sticker error recovery, and failure handling.
  2. `scripts/verify_animated_stickers.py`:
     - Binary chunk parsing edge cases (truncated ANMF chunks, non-standard RIFF sizes, non-square frames, zero durations).
     - Strict mode vs normal mode behavior on malformed and boundary inputs.
     - Fault injection: synthetic corruptions across WebP and GIF binary containers and visual corner checks.
"""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from typing import Any, Dict, List
from unittest.mock import patch

from PIL import Image, ImageDraw, ImageSequence

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

import scripts.build_animated_stickers as builder
import scripts.verify_animated_stickers as verifier
PYTHON_EXE = sys.executable
SAMPLE_WEBP = os.path.join(WORKSPACE_DIR, "assets", "animated", "ent.webp")
SAMPLE_GIF = os.path.join(WORKSPACE_DIR, "assets", "animated", "ent.gif")
VERIFIER_SCRIPT = os.path.join(WORKSPACE_DIR, "scripts", "verify_animated_stickers.py")
BUILDER_SCRIPT = os.path.join(WORKSPACE_DIR, "scripts", "build_animated_stickers.py")


def run_verifier_cmd(args: List[str]) -> subprocess.CompletedProcess:
    """Helper to run verify_animated_stickers.py via subprocess."""
    cmd = [PYTHON_EXE, VERIFIER_SCRIPT] + args
    return subprocess.run(cmd, capture_output=True, text=True)


def run_builder_cmd(args: List[str]) -> subprocess.CompletedProcess:
    """Helper to run build_animated_stickers.py via subprocess."""
    cmd = [PYTHON_EXE, BUILDER_SCRIPT] + args
    return subprocess.run(cmd, capture_output=True, text=True)


# =============================================================================
# SUITE 1: MATHEMATICAL STABILITY & MOTION PRIMITIVES
# =============================================================================
class TestMathematicalStabilityAndMotionPrimitives(unittest.TestCase):
    """Stress tests verifying mathematical stability, boundary handling, and continuity."""

    def test_01_easing_curves_out_of_bounds(self):
        """Verify comic timing and easing curves handle extreme out-of-bound inputs safely."""
        extreme_inputs = [-1e9, -100.0, -1.0, -0.001, 1.001, 2.0, 100.0, 1e9]
        for u in extreme_inputs:
            c = builder.clamp01(u)
            self.assertTrue(0.0 <= c <= 1.0, f"clamp01 failed for {u}: {c}")

            cubic = builder.ease_in_out_cubic(u)
            self.assertTrue(math.isfinite(cubic), f"ease_in_out_cubic non-finite for {u}")

            back_out = builder.ease_out_back(u)
            self.assertTrue(math.isfinite(back_out), f"ease_out_back non-finite for {u}")

            back_in = builder.ease_in_back(u)
            self.assertTrue(math.isfinite(back_in), f"ease_in_back non-finite for {u}")

            pop = builder.comic_pop_curve(u)
            self.assertTrue(math.isfinite(pop), f"comic_pop_curve non-finite for {u}")

    def test_02_comic_pop_curve_c0_continuity(self):
        """Verify comic pop curve achieves C0 continuity at all internal segment transitions."""
        # Boundaries: t_antic=0.16, t_hit=0.32, t_hold=0.68
        eps = 1e-6
        for t_split in [0.16, 0.32, 0.68]:
            val_left = builder.comic_pop_curve(t_split - eps)
            val_right = builder.comic_pop_curve(t_split + eps)
            self.assertAlmostEqual(
                val_left,
                val_right,
                places=3,
                msg=f"Discontinuity detected at t={t_split}: {val_left} vs {val_right}",
            )

    def test_03_squash_stretch_bounds_and_zero_prevention(self):
        """Verify squash/stretch functions clamp scaling factors to prevent division by zero or negative roots."""
        adversarial_s = [-1000.0, -1.0, 0.0, 1e-12, 0.001, 0.65, 1.0, 1.45, 10.0, 1000.0]
        for s in adversarial_s:
            # squash_stretch_offset
            dx, dy = builder.squash_stretch_offset(256.0, 256.0, 256.0, 256.0, s)
            self.assertTrue(math.isfinite(dx) and math.isfinite(dy), f"Offset failed for s={s}")

            # squash_stretch_cylindrical
            cdx, cdy = builder.squash_stretch_cylindrical(256.0, 256.0, 256.0, 256.0, s)
            self.assertTrue(math.isfinite(cdx) and math.isfinite(cdy), f"Cylindrical failed for s={s}")

    def test_04_living_hold_jitter_uniqueness_and_continuity(self):
        """Verify living hold jitter generates 24 strictly unique frames and exact loop closure at t=0 and t=1."""
        jitters = [builder.living_hold_jitter(f / 24.0) for f in range(24)]
        self.assertEqual(len(jitters), 24)
        self.assertEqual(len(set(jitters)), 24, "Micro-motion jitter produced duplicate frames")

        j0 = builder.living_hold_jitter(0.0)
        j1 = builder.living_hold_jitter(1.0)
        self.assertAlmostEqual(j0[0], j1[0], places=7, msg="Living hold dx loop discontinuity")
        self.assertAlmostEqual(j0[1], j1[1], places=7, msg="Living hold dy loop discontinuity")

    def test_05_all_14_primitives_finite_at_extreme_coordinates(self):
        """Verify all 14 motion primitives remain finite when queried at extreme canvas coordinates."""
        test_points = [
            (-1000.0, -1000.0),
            (0.0, 0.0),
            (256.0, 256.0),
            (511.0, 511.0),
            (1000.0, 1000.0),
            (10000.0, -5000.0),
        ]
        test_t = [0.0, 0.14, 0.25, 0.5, 0.75, 0.99, 1.0]

        for name, disp_fn in builder.PRIMITIVE_DISP.items():
            for x, y in test_points:
                for t in test_t:
                    res_x, res_y = disp_fn(x, y, t)
                    self.assertTrue(
                        math.isfinite(res_x) and math.isfinite(res_y),
                        f"Primitive '{name}' produced non-finite output at ({x}, {y}, {t}): ({res_x}, {res_y})",
                    )

    def test_06_all_14_primitives_loop_closure(self):
        """Verify all 14 motion primitives satisfy loop continuity |P(t=0) - P(t=1)| <= 0.005 pixels."""
        sample_grid = [(x, y) for x in range(0, 513, 128) for y in range(0, 513, 128)]
        for name, disp_fn in builder.PRIMITIVE_DISP.items():
            max_drift = 0.0
            for x, y in sample_grid:
                p0 = disp_fn(x, y, 0.0)
                p1 = disp_fn(x, y, 1.0)
                drift = max(abs(p0[0] - p1[0]), abs(p0[1] - p1[1]))
                if drift > max_drift:
                    max_drift = drift
            self.assertLessEqual(
                max_drift,
                0.005,
                f"Primitive '{name}' failed loop continuity: max drift {max_drift:.6f}px > 0.005px",
            )

    def test_07_post_warp_effects_lighting_and_alpha(self):
        """Verify custom post-warp functions (candle lighting & slipper alpha) handle edge timestamps."""
        # ttec lighting curve
        for t in [0.0, 0.15, 0.20, 0.32, 0.50, 0.85, 0.87, 0.90, 0.93, 0.98, 1.0]:
            light = builder.get_ttec_lighting(t)
            self.assertTrue(0.0 <= light <= 1.0, f"Lighting out of bounds at t={t}: {light}")

        # Candle lighting transformation on RGBA
        test_im = Image.new("RGBA", (10, 10), (200, 150, 100, 255))
        lit_im = builder.apply_candle_lighting(test_im, 0.25)  # Pitch black
        self.assertEqual(lit_im.getpixel((5, 5))[:3], (0, 0, 0))

        # Slipper alpha fade
        alpha_im = builder.apply_slipper_alpha(test_im, 1.0)
        self.assertEqual(alpha_im.getpixel((5, 5))[3], 0)


# =============================================================================
# SUITE 2: ASSET PIPELINE WARP & CARD COMPOSITION STRESS TESTING
# =============================================================================
class TestAssetPipelineMeshAndComposition(unittest.TestCase):
    """Stress tests targeting mesh warping, breathing room, and dual-stream card composition."""

    def test_01_prep_breathing_room_adversarial_scales(self):
        """Verify prep_breathing_room behaves predictably on boundary scales and non-square sizes."""
        im = Image.new("RGBA", (512, 512), (255, 100, 50, 255))

        # Scale 0.0 -> clamps to minimum 1x1 resize, returns 512x512
        res0 = builder.prep_breathing_room(im, scale=0.0)
        self.assertEqual(res0.size, (512, 512))

        # Scale 2.0 -> returns 512x512 without crash
        res2 = builder.prep_breathing_room(im, scale=2.0)
        self.assertEqual(res2.size, (512, 512))

        # Non-square input (256x512)
        im_rect = Image.new("RGBA", (256, 512), (0, 255, 0, 255))
        res_rect = builder.prep_breathing_room(im_rect, scale=0.91)
        self.assertEqual(res_rect.size, (256, 512))

    def test_02_warp_mesh_adversarial_displacements(self):
        """Verify warp_mesh handles extreme displacement offsets without crashing Pillow."""
        im = Image.new("RGBA", (512, 512), (50, 150, 250, 255))

        # Extreme positive displacement
        def extreme_disp(x, y):
            return (x + 2000.0, y - 2000.0)

        warped = builder.warp_mesh(im, extreme_disp, grid_n=4)
        self.assertEqual(warped.size, (512, 512))
        self.assertEqual(warped.mode, "RGBA")

    def test_03_render_picture_specific_frame_all_primitives(self):
        """Verify render_picture_specific_frame executes cleanly for a representative sticker of every primitive."""
        base = Image.new("RGBA", (512, 512), (100, 200, 50, 255))
        # Select one sticker for each unique primitive in registry
        seen_primitives = set()
        test_stickers = []
        for sid, entry in builder.STICKER_RIG_REGISTRY.items():
            prim = entry["primitive"]
            if prim not in seen_primitives:
                seen_primitives.add(prim)
                test_stickers.append((sid, entry["rig"], prim))

        self.assertEqual(len(seen_primitives), 14, "Registry missing one or more of the 14 primitives")

        for sid, rig, prim in test_stickers:
            frame = builder.render_picture_specific_frame(base, rig, sid, f=6, n_frames=24)
            self.assertEqual(frame.size, (512, 512), f"Frame size mismatch for {sid}")
            self.assertEqual(frame.mode, "RGBA", f"Frame mode mismatch for {sid}")

    def test_04_card_composition_and_palette_clamping(self):
        """Verify card composition on #10141E clamps palette to <= 128 colors and matches card background."""
        # 1. Fully transparent frame -> solid #10141E card
        trans_frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        card1 = Image.new("RGBA", (512, 512), (16, 20, 30, 255))
        card1.alpha_composite(trans_frame)
        rgb1 = card1.convert("RGB")
        p1 = rgb1.quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        self.assertEqual(len(p1.getcolors()), 1)
        for c in [(0, 0), (511, 0), (0, 511), (511, 511), (256, 256)]:
            self.assertEqual(rgb1.getpixel(c), (16, 20, 30))

        # 2. Multi-color image with 500+ distinct colors
        complex_frame = Image.new("RGBA", (512, 512), (16, 20, 30, 255))
        draw = ImageDraw.Draw(complex_frame)
        for i in range(256):
            draw.line([(0, i * 2), (512, i * 2)], fill=(i, 255 - i, (i * 3) % 256, 255), width=2)
        card2 = Image.new("RGBA", (512, 512), (16, 20, 30, 255))
        card2.alpha_composite(complex_frame)
        rgb2 = card2.convert("RGB")
        p2 = rgb2.quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        palette_colors_used = len(p2.getcolors())
        self.assertLessEqual(
            palette_colors_used,
            128,
            f"GIF palette colors {palette_colors_used} exceeded 128 boundary",
        )

    def test_05_atomic_save_retry_backoff(self):
        """Verify save_with_atomic_retry succeeds and cleans up temporary files even under simulated retry."""
        with tempfile.TemporaryDirectory() as td:
            target = os.path.join(td, "test_atomic.webp")
            attempt_count = 0

            def dummy_saver(path):
                nonlocal attempt_count
                attempt_count += 1
                with open(path, "wb") as f:
                    f.write(b"SAMPLE_DATA_ATOMIC")

            builder.save_with_atomic_retry(dummy_saver, target, max_retries=3, base_delay=0.01)
            self.assertTrue(os.path.exists(target))
            with open(target, "rb") as f:
                self.assertEqual(f.read(), b"SAMPLE_DATA_ATOMIC")

            # Check that no leftover .tmp_* files remain in directory
            leftovers = [f for f in os.listdir(td) if f.startswith(".tmp_")]
            self.assertEqual(leftovers, [], f"Leftover temp files found: {leftovers}")


# =============================================================================
# SUITE 3: MULTIPROCESSING & CLI STRESS TESTING
# =============================================================================
class TestMultiprocessingAndCLIStress(unittest.TestCase):
    """Stress tests targeting CLI argument parsing, worker bounds, and fault recovery."""

    def test_01_worker_count_clamping(self):
        """Verify parse_cli_args clamps workers to [1, 16] regardless of adversarial inputs."""
        test_inputs = [
            (["build.py", "--workers", "-10"], 1),
            (["build.py", "--workers", "0"], 1),
            (["build.py", "--workers", "1"], 1),
            (["build.py", "--workers", "8"], 8),
            (["build.py", "--workers", "16"], 16),
            (["build.py", "--workers", "64"], 16),
            (["build.py", "--workers", "9999"], 16),
        ]
        for argv, expected in test_inputs:
            with patch.object(sys, "argv", argv):
                args = builder.parse_cli_args()
                self.assertEqual(args.workers, expected, f"Failed for {argv}: got {args.workers}")

    def test_02_missing_sticker_process_one_exception(self):
        """Verify process_one raises FileNotFoundError when target sticker PNG does not exist."""
        ghost_name = "ghost_sticker_not_found_12345.png"
        with self.assertRaises(FileNotFoundError) as ctx:
            builder.process_one(ghost_name)
        self.assertIn("Sticker PNG not found", str(ctx.exception))

    def test_03_cli_single_sticker_nonexistent_exit_code(self):
        """Verify running build_animated_stickers.py --sticker <nonexistent> exits with code 1."""
        res = run_builder_cmd(["--sticker", "non_existent_ghost_sticker_xyz"])
        self.assertEqual(res.returncode, 1, f"Expected RC 1 for nonexistent sticker, got {res.returncode}")
        self.assertIn("FileNotFoundError", res.stderr)

    def test_04_cli_pack_nonexistent_graceful_exit(self):
        """Verify running build_animated_stickers.py --pack <nonexistent> reports 0 stickers and exits gracefully."""
        res = run_builder_cmd(["--pack", "nonexistent_pack_xyz"])
        self.assertEqual(res.returncode, 0, f"Expected RC 0 for unmatched pack, got {res.returncode}")
        self.assertIn("No stickers found matching pack", res.stdout)

    def test_05_classify_rig_robustness(self):
        """Verify classify_rig never returns generic fallback, handles extensions, casing, and unknown inputs."""
        # Known sticker
        self.assertEqual(builder.classify_rig("ent"), "tanty_akumbo_tilt")
        self.assertEqual(builder.classify_rig("ent.png"), "tanty_akumbo_tilt")
        self.assertEqual(builder.classify_rig("ENT.WEBP"), "tanty_akumbo_tilt")

        # Unknown sticker -> falls back to authentic tanty_akumbo_tilt, NEVER articulated_gesture
        unknown_rig = builder.classify_rig("completely_unknown_sid_xyz")
        self.assertEqual(unknown_rig, "tanty_akumbo_tilt")
        self.assertNotEqual(unknown_rig, "articulated_gesture")

        # Empty string
        empty_rig = builder.classify_rig("")
        self.assertEqual(empty_rig, "tanty_akumbo_tilt")


# =============================================================================
# SUITE 4: VERIFIER BINARY CHUNK PARSING & FAULT INJECTION
# =============================================================================
class TestVerifierBinaryChunkEdgeCases(unittest.TestCase):
    """Stress tests targeting verify_animated_stickers.py binary chunk parsing."""

    @classmethod
    def setUpClass(cls):
        assert os.path.exists(SAMPLE_WEBP), f"Missing baseline sample WebP: {SAMPLE_WEBP}"
        assert os.path.exists(SAMPLE_GIF), f"Missing baseline sample GIF: {SAMPLE_GIF}"
        with open(SAMPLE_WEBP, "rb") as f:
            cls.baseline_webp_bytes = f.read()
        with open(SAMPLE_GIF, "rb") as f:
            cls.baseline_gif_bytes = f.read()

    def test_01_webp_truncated_anmf_chunk(self):
        """Fault Injection: Truncated ANMF chunk size (< 16 bytes) causes verifier to flag frame count defect."""
        data = bytearray(self.baseline_webp_bytes)
        pos = 12
        while pos < len(data) - 8:
            fourcc = data[pos : pos + 4]
            if fourcc == b"ANMF":
                # Set ANMF chunk length to 10 bytes (< 16)
                data[pos + 4 : pos + 8] = (10).to_bytes(4, "little")
                break
            c_sz = int.from_bytes(data[pos + 4 : pos + 8], "little")
            pos += 8 + c_sz + (c_sz % 2)

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            meta = verifier.parse_webp_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertTrue(
                any("Frame count" in e for e in meta["errors"]),
                f"Expected frame count error, got: {meta['errors']}",
            )
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_02_webp_non_square_dimensions_vp8x(self):
        """Fault Injection: Mutate VP8X dimensions to non-square 256x512, verifier flags mismatch."""
        data = bytearray(self.baseline_webp_bytes)
        pos = 12
        while pos < len(data) - 8:
            if data[pos : pos + 4] == b"VP8X":
                # Width is at pos + 8 + 4 (3 bytes), set to 255 (value + 1 = 256)
                data[pos + 12 : pos + 15] = (255).to_bytes(3, "little")
                break
            c_sz = int.from_bytes(data[pos + 4 : pos + 8], "little")
            pos += 8 + c_sz + (c_sz % 2)

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            meta = verifier.parse_webp_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertTrue(
                any("Dimensions 256x512" in e for e in meta["errors"]),
                f"Expected dimension mismatch error, got: {meta['errors']}",
            )
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_03_webp_missing_animation_or_alpha_flag(self):
        """Fault Injection: Clear animation and alpha flags in VP8X chunk, verifier flags defects."""
        data = bytearray(self.baseline_webp_bytes)
        pos = 12
        while pos < len(data) - 8:
            if data[pos : pos + 4] == b"VP8X":
                # Clear all flags (byte 0 of VP8X chunk data)
                data[pos + 8] = 0x00
                break
            c_sz = int.from_bytes(data[pos + 4 : pos + 8], "little")
            pos += 8 + c_sz + (c_sz % 2)

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            meta = verifier.parse_webp_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertTrue(any("animation flag" in e for e in meta["errors"]))
            self.assertTrue(any("alpha flag" in e for e in meta["errors"]))
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_04_webp_zero_duration_strict_vs_normal(self):
        """Fault Injection: Setting single frame duration to 0ms passes Normal (>=2000ms) but fails Strict (2070ms != 2160ms)."""
        data = bytearray(self.baseline_webp_bytes)
        pos = 12
        while pos < len(data) - 8:
            if data[pos : pos + 4] == b"ANMF":
                # Zero out first frame's duration (bytes 12:15 in ANMF chunk data)
                data[pos + 20 : pos + 23] = b"\x00\x00\x00"
                break
            c_sz = int.from_bytes(data[pos + 4 : pos + 8], "little")
            pos += 8 + c_sz + (c_sz % 2)

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            normal_meta = verifier.parse_webp_binary(tpath, strict=False)
            strict_meta = verifier.parse_webp_binary(tpath, strict=True)

            self.assertTrue(normal_meta["valid"], "Normal mode should pass when total >= 2000ms")
            self.assertFalse(strict_meta["valid"], "Strict mode must fail when total != 2160ms")
            self.assertTrue(any("Strict: Total duration 2070ms != 2160ms" in e for e in strict_meta["errors"]))
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_05_webp_non_zero_loop_count(self):
        """Fault Injection: Set loop count to 5 in ANIM chunk, verifier flags loop count defect."""
        data = bytearray(self.baseline_webp_bytes)
        pos = 12
        while pos < len(data) - 8:
            if data[pos : pos + 4] == b"ANIM":
                # Loop count is at pos + 8 + 4 (2 bytes little endian)
                data[pos + 12 : pos + 14] = (5).to_bytes(2, "little")
                break
            c_sz = int.from_bytes(data[pos + 4 : pos + 8], "little")
            pos += 8 + c_sz + (c_sz % 2)

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            meta = verifier.parse_webp_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertTrue(any("Loop count is 5" in e for e in meta["errors"]))
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_06_webp_corrupt_riff_size_fast_mode_gap(self):
        """Empirical Discovery: Verifies that --fast skips Pillow and bypasses un-decodable zero RIFF size."""
        data = bytearray(self.baseline_webp_bytes)
        data[4:8] = b"\x00\x00\x00\x00"  # Corrupt RIFF length

        with tempfile.TemporaryDirectory() as td:
            bad_path = os.path.join(td, "bad_riff.webp")
            with open(bad_path, "wb") as f:
                f.write(data)

            # Normal mode executes Pillow corner checks -> catches decoder crash
            res_normal = run_verifier_cmd(["--dir", td, "--format", "webp"])
            self.assertEqual(res_normal.returncode, 1)
            self.assertIn("Pillow decode error", res_normal.stderr)

            # Fast mode bypasses Pillow -> demonstrates documented gap in binary chunk verifier
            res_fast = run_verifier_cmd(["--dir", td, "--format", "webp", "--fast"])
            self.assertEqual(res_fast.returncode, 0)
            self.assertIn("VERIFICATION PASSED", res_fast.stdout)

    def test_07_gif_truncated_logical_screen_descriptor(self):
        """Fault Injection: Truncating GIF to 10 bytes (< 13 required for LSD) fails validation."""
        truncated_gif = self.baseline_gif_bytes[:10]
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tf:
            tf.write(truncated_gif)
            tpath = tf.name

        try:
            meta = verifier.parse_gif_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertIn("File size too small", meta.get("error", ""))
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_08_gif_palette_overflow_256_colors(self):
        """Fault Injection: Mutate GIF LSD to declare 256 colors (> 128 allowed), verifier flags error."""
        data = bytearray(self.baseline_gif_bytes)
        # Byte 10 is packed fields: bit 7 (has GCT) | bits 0-2 (GCT size)
        # 0x87 -> GCT present, 2^(7+1) = 256 colors
        data[10] = 0x87

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            meta = verifier.parse_gif_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertTrue(any("Palette colors 256 > maximum 128" in e for e in meta["errors"]))
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)

    def test_09_gif_non_zero_loop_count(self):
        """Fault Injection: Mutate Netscape extension loop count in GIF to 3, verifier flags defect."""
        data = bytearray(self.baseline_gif_bytes)
        netscape_idx = data.find(b"NETSCAPE2.0")
        self.assertNotEqual(netscape_idx, -1, "NETSCAPE extension block not found in baseline GIF")

        # In Netscape sub-block: sub-block size (1 byte = 3), sub-block ID (1 byte = 1), loop count (2 bytes LE)
        # Offset: netscape_idx + len("NETSCAPE2.0") is start of sub-block:
        sub_pos = netscape_idx + len(b"NETSCAPE2.0")
        data[sub_pos + 2 : sub_pos + 4] = (3).to_bytes(2, "little")

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tf:
            tf.write(data)
            tpath = tf.name

        try:
            meta = verifier.parse_gif_binary(tpath)
            self.assertFalse(meta["valid"])
            self.assertTrue(any("Loop count is 3, expected 0" in e for e in meta["errors"]))
        finally:
            if os.path.exists(tpath):
                os.remove(tpath)


# =============================================================================
# SUITE 5: FAULT INJECTION, VISUAL INTEGRITY & CLI RECOVERY
# =============================================================================
class TestVerifierFaultInjectionAndVisualIntegrity(unittest.TestCase):
    """Stress tests targeting visual corner verification, file boundaries, and CLI exit codes."""

    def test_01_webp_visual_corner_opaque_rejection(self):
        """Fault Injection: Mutate corner (0, 0) of WebP to opaque red; verify_corners_pillow flags it."""
        with tempfile.TemporaryDirectory() as td:
            target = os.path.join(td, "bad_corner.webp")
            with Image.open(SAMPLE_WEBP) as im:
                frames = []
                for i, fr in enumerate(ImageSequence.Iterator(im)):
                    f_copy = fr.copy().convert("RGBA")
                    if i == 0:
                        f_copy.putpixel((0, 0), (255, 0, 0, 255))
                    frames.append(f_copy)
                frames[0].save(
                    target,
                    format="WEBP",
                    save_all=True,
                    append_images=frames[1:],
                    duration=90,
                    loop=0,
                )

            errs = verifier.verify_corners_pillow(target, is_gif=False)
            self.assertTrue(
                any("alpha 255 != 0 (not transparent)" in e for e in errs),
                f"Expected opaque corner rejection, got: {errs}",
            )

    def test_02_webp_completely_transparent_rejection(self):
        """Fault Injection: Construct completely blank/transparent WebP; verify_corners_pillow flags it."""
        with tempfile.TemporaryDirectory() as td:
            blank_path = os.path.join(td, "blank.webp")
            frames = [Image.new("RGBA", (512, 512), (0, 0, 0, 0)) for _ in range(24)]
            frames[0].save(
                blank_path,
                format="WEBP",
                save_all=True,
                append_images=frames[1:],
                duration=90,
                loop=0,
            )

            errs = verifier.verify_corners_pillow(blank_path, is_gif=False)
            self.assertTrue(
                any("completely transparent" in e for e in errs),
                f"Expected completely transparent rejection, got: {errs}",
            )

    def test_03_gif_visual_corner_studio_card_divergence(self):
        """Fault Injection: Mutate GIF corner to bright red (255, 0, 0); verify_corners_pillow flags deviation."""
        with tempfile.TemporaryDirectory() as td:
            target = os.path.join(td, "bad_bg.gif")
            with Image.open(SAMPLE_GIF) as im:
                frames = []
                for i, fr in enumerate(ImageSequence.Iterator(im)):
                    f_copy = fr.copy().convert("RGB")
                    if i == 0:
                        f_copy.putpixel((0, 0), (255, 0, 0))
                    frames.append(f_copy.quantize(colors=128))
                frames[0].save(
                    target,
                    format="GIF",
                    save_all=True,
                    append_images=frames[1:],
                    duration=90,
                    loop=0,
                )

            errs = verifier.verify_corners_pillow(target, is_gif=True)
            self.assertTrue(
                any("deviates from (16, 20, 30)" in e for e in errs),
                f"Expected studio card color deviation rejection, got: {errs}",
            )

    def test_04_file_size_budget_boundary_violations(self):
        """Fault Injection: WebP files below 10KB or above 2.5MB are rejected by binary parsers."""
        with tempfile.TemporaryDirectory() as td:
            # 1. Undersized file (500 bytes with RIFF/WEBP header)
            tiny_path = os.path.join(td, "tiny.webp")
            with open(tiny_path, "wb") as f:
                f.write(b"RIFF" + (492).to_bytes(4, "little") + b"WEBP" + b"\x00" * 488)

            meta_tiny = verifier.parse_webp_binary(tiny_path)
            self.assertFalse(meta_tiny["valid"])
            self.assertIn("File size too small", meta_tiny.get("error", ""))

            # 2. Oversized file (2.6 MB)
            huge_path = os.path.join(td, "huge.webp")
            with open(huge_path, "wb") as f:
                f.write(b"RIFF" + (2600000).to_bytes(4, "little") + b"WEBP" + b"\x00" * 2600000)

            meta_huge = verifier.parse_webp_binary(huge_path)
            self.assertFalse(meta_huge["valid"])
            self.assertIn("File size exceeds budget", meta_huge.get("error", ""))

    def test_05_verifier_cli_nonexistent_and_empty_directory(self):
        """Verify CLI exits with code 1 on non-existent or empty asset directories."""
        # Non-existent directory
        res1 = run_verifier_cmd(["--dir", os.path.join(WORKSPACE_DIR, "nonexistent_dir_challenge")])
        self.assertEqual(res1.returncode, 1)
        self.assertIn("does not exist", res1.stderr)

        # Empty directory
        with tempfile.TemporaryDirectory() as td:
            res2 = run_verifier_cmd(["--dir", td])
            self.assertEqual(res2.returncode, 1)
            self.assertIn("No animated assets", res2.stderr)

    def test_06_verifier_json_report_schema_and_metrics(self):
        """Verify verifier generates valid JSON telemetry report with correct summary metrics."""
        with tempfile.TemporaryDirectory() as td:
            # Copy sample valid assets
            shutil.copy(SAMPLE_WEBP, os.path.join(td, "ent.webp"))
            shutil.copy(SAMPLE_GIF, os.path.join(td, "ent.gif"))
            report_path = os.path.join(td, "nested", "telemetry_report.json")

            res = run_verifier_cmd(["--dir", td, "--report", report_path])
            self.assertEqual(res.returncode, 0, f"Verifier failed: {res.stderr}")
            self.assertTrue(os.path.exists(report_path))

            with open(report_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            summary = data.get("summary", {})
            self.assertEqual(summary.get("total_checked"), 2)
            self.assertEqual(summary.get("total_passed"), 2)
            self.assertEqual(summary.get("total_failed"), 0)
            self.assertEqual(summary.get("status"), "PASSED")
            self.assertEqual(summary.get("exit_code"), 0)
            self.assertIn("by_format", data)
            self.assertIn("webp", data["by_format"])
            self.assertIn("gif", data["by_format"])

    def test_07_verifier_single_sticker_filter(self):
        """Verify verifier --sticker flag correctly isolates a single sticker asset."""
        # Run on production directory for 'ent'
        res = run_verifier_cmd(["--sticker", "ent", "-v"])
        self.assertEqual(res.returncode, 0, f"Failed on single sticker: {res.stderr}")
        self.assertIn("[PASS] ent.webp", res.stdout)
        self.assertIn("[PASS] ent.gif", res.stdout)
        self.assertIn("2/2 animated assets verified successfully", res.stdout)


if __name__ == "__main__":
    unittest.main()
