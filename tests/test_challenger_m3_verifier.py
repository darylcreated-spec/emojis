"""
tests/test_challenger_m3_verifier.py
====================================
Adversarial Empirical Challenge Suite for Milestone 3 Automated Verifier:
`scripts/verify_animated_stickers.py`.

Author: Challenger 1 (Milestone 3 Empirical Challenger)
Scope:
  1. Empty Directory Attack (exit code != 0)
  2. 0-Byte Corrupt Asset Attack (detects 0-byte WebP & GIF, exit code 1)
  3. Magic Byte / Truncated Header Attack (corrupted magic bytes / fake headers, exit code 1)
  4. Dropped Frame Attack (18 or 20 frames instead of 24, exit code 1)
  5. Canvas Dimension Attack (256x256, 512x256 instead of 512x512, exit code 1)
  6. Non-Image File Handling (.txt, .DS_Store alongside valid assets, no unhandled crash)
  7. Loop Count & Timing Defects (loop_count != 0, total_duration < 2000ms, exit code 1)
  8. Visual Integrity Defects (opaque WebP corners, invalid GIF studio card background)
  9. Production Assets Conformance Baseline (376 assets, strict mode, exit code 0)
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import Dict, Any, List

from PIL import Image, ImageSequence

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
VERIFIER_SCRIPT = os.path.join(WORKSPACE_DIR, "scripts", "verify_animated_stickers.py")
ANIMATED_DIR = os.path.join(WORKSPACE_DIR, "assets", "animated")
SAMPLE_WEBP = os.path.join(ANIMATED_DIR, "ent.webp")
SAMPLE_GIF = os.path.join(ANIMATED_DIR, "ent.gif")
PYTHON_EXE = sys.executable


def run_verifier(args: List[str]) -> subprocess.CompletedProcess:
    """Helper to run verify_animated_stickers.py with given CLI args."""
    cmd = [PYTHON_EXE, VERIFIER_SCRIPT] + args
    return subprocess.run(cmd, capture_output=True, text=True)


class TestChallengerM3Verifier(unittest.TestCase):
    """Empirical adversarial stress test suite for verify_animated_stickers.py."""

    @classmethod
    def setUpClass(cls):
        assert os.path.exists(VERIFIER_SCRIPT), f"Verifier missing: {VERIFIER_SCRIPT}"
        assert os.path.exists(SAMPLE_WEBP), f"Sample WebP missing: {SAMPLE_WEBP}"
        assert os.path.exists(SAMPLE_GIF), f"Sample GIF missing: {SAMPLE_GIF}"

    # -------------------------------------------------------------------------
    # ATTACK 1: Empty Directory Attack
    # -------------------------------------------------------------------------
    def test_01_empty_directory_attack(self):
        """Verify python scripts/verify_animated_stickers.py --dir <empty_dir> exits with code 1."""
        with tempfile.TemporaryDirectory() as td:
            res = run_verifier(["--dir", td])
            self.assertEqual(res.returncode, 1, f"Expected RC 1 for empty directory, got {res.returncode}")
            self.assertIn("No animated assets", res.stderr)

    def test_01b_non_existent_directory_attack(self):
        """Verify non-existent directory path exits with code 1."""
        ghost_dir = os.path.join(WORKSPACE_DIR, "ghost_dir_challenge_nonexistent_xyz")
        res = run_verifier(["--dir", ghost_dir])
        self.assertEqual(res.returncode, 1, f"Expected RC 1 for non-existent directory, got {res.returncode}")
        self.assertIn("does not exist", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 2: 0-Byte Corrupt Asset Attack
    # -------------------------------------------------------------------------
    def test_02_zero_byte_corrupt_asset_attack(self):
        """Verify verifier detects 0-byte .webp and .gif files alongside valid assets and exits with code 1."""
        with tempfile.TemporaryDirectory() as td:
            # Seed with valid assets
            shutil.copy(SAMPLE_WEBP, os.path.join(td, "valid.webp"))
            shutil.copy(SAMPLE_GIF, os.path.join(td, "valid.gif"))

            # Inject 0-byte assets
            corrupt_webp = os.path.join(td, "corrupt_empty.webp")
            corrupt_gif = os.path.join(td, "corrupt_empty.gif")
            open(corrupt_webp, "wb").close()
            open(corrupt_gif, "wb").close()

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1, f"Expected RC 1 on 0-byte assets, got {res.returncode}")
            self.assertIn("corrupt_empty.webp: File is empty (0 bytes)", res.stderr)
            self.assertIn("corrupt_empty.gif: File is empty (0 bytes)", res.stderr)
            self.assertIn("[PASS] valid.webp", res.stdout)
            self.assertIn("[PASS] valid.gif", res.stdout)

    # -------------------------------------------------------------------------
    # ATTACK 3: Magic Byte / Truncated Header Attack
    # -------------------------------------------------------------------------
    def test_03a_corrupt_magic_bytes_webp(self):
        """Verify invalid RIFF/WEBP magic bytes are rejected with exit code 1."""
        with tempfile.TemporaryDirectory() as td:
            with open(SAMPLE_WEBP, "rb") as f:
                data = bytearray(f.read())
            # Mutate 'RIFF' -> 'NOPE'
            data[:4] = b"NOPE"
            with open(os.path.join(td, "bad_magic.webp"), "wb") as f:
                f.write(data)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Invalid RIFF/WEBP header", res.stderr)

    def test_03b_corrupt_riff_type_webp(self):
        """Verify valid RIFF but invalid type (RIFF...JPEG instead of RIFF...WEBP) is rejected."""
        with tempfile.TemporaryDirectory() as td:
            with open(SAMPLE_WEBP, "rb") as f:
                data = bytearray(f.read())
            # Mutate 'WEBP' (offset 8..12) -> 'JPEG'
            data[8:12] = b"JPEG"
            with open(os.path.join(td, "fake_webp.webp"), "wb") as f:
                f.write(data)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Invalid RIFF/WEBP header", res.stderr)

    def test_03c_corrupt_header_gif(self):
        """Verify corrupted GIF header (BADGIF instead of GIF89a) is rejected with exit code 1."""
        with tempfile.TemporaryDirectory() as td:
            with open(SAMPLE_GIF, "rb") as f:
                data = bytearray(f.read())
            data[:6] = b"BADGIF"
            with open(os.path.join(td, "bad_header.gif"), "wb") as f:
                f.write(data)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Invalid GIF header", res.stderr)

    def test_03d_plain_text_renamed_to_image(self):
        """Verify ASCII text file renamed to .webp or .gif is rejected with exit code 1."""
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "ascii.webp"), "w", encoding="utf-8") as f:
                f.write("This is definitely not a webp image file.\n" * 100)
            with open(os.path.join(td, "ascii.gif"), "w", encoding="utf-8") as f:
                f.write("This is definitely not a gif image file.\n" * 100)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("ascii.webp", res.stderr)
            self.assertIn("ascii.gif", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 4: Dropped Frame Attack
    # -------------------------------------------------------------------------
    def test_04a_dropped_frames_webp_18_and_20(self):
        """Verify WebP animation with 18 and 20 frames is rejected with exit code 1."""
        with Image.open(SAMPLE_WEBP) as im:
            frames = [f.copy() for f in ImageSequence.Iterator(im)]
        self.assertEqual(len(frames), 24, "Sample WebP does not have 24 frames")

        with tempfile.TemporaryDirectory() as td:
            p18 = os.path.join(td, "dropped_18.webp")
            frames[:18][0].save(p18, format="WEBP", save_all=True, append_images=frames[:18][1:], duration=90, loop=0)

            p20 = os.path.join(td, "dropped_20.webp")
            frames[:20][0].save(p20, format="WEBP", save_all=True, append_images=frames[:20][1:], duration=90, loop=0)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Frame count 18 < minimum 24", res.stderr)
            self.assertIn("Frame count 20 < minimum 24", res.stderr)

    def test_04b_dropped_frames_gif_18_and_20(self):
        """Verify GIF animation with 18 and 20 frames is rejected with exit code 1."""
        with Image.open(SAMPLE_GIF) as im:
            frames = [f.copy() for f in ImageSequence.Iterator(im)]
        self.assertEqual(len(frames), 24, "Sample GIF does not have 24 frames")

        with tempfile.TemporaryDirectory() as td:
            p18 = os.path.join(td, "dropped_18.gif")
            frames[:18][0].save(p18, format="GIF", save_all=True, append_images=frames[:18][1:], duration=90, loop=0)

            p20 = os.path.join(td, "dropped_20.gif")
            frames[:20][0].save(p20, format="GIF", save_all=True, append_images=frames[:20][1:], duration=90, loop=0)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Frame count 18 < minimum 24", res.stderr)
            self.assertIn("Frame count 20 < minimum 24", res.stderr)

    def test_04c_extra_frames_in_strict_mode(self):
        """Verify 25 distinct frames animation is rejected when --strict flag is active."""
        with Image.open(SAMPLE_WEBP) as im:
            frames = [f.copy() for f in ImageSequence.Iterator(im)]
        # Append 1 distinct extra frame (to prevent Pillow frame-coalescing)
        f_extra = frames[-1].copy()
        f_extra.putpixel((200, 200), (255, 128, 64, 255))
        frames_25 = frames + [f_extra]

        with tempfile.TemporaryDirectory() as td:
            p25 = os.path.join(td, "extra_25.webp")
            frames_25[0].save(p25, format="WEBP", save_all=True, append_images=frames_25[1:], duration=90, loop=0)

            res = run_verifier(["--dir", td, "--strict", "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Strict: Frame count 25 != 24", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 5: Canvas Dimension Attack
    # -------------------------------------------------------------------------
    def test_05a_canvas_dimension_webp(self):
        """Verify 256x256 and 512x256 WebP animations are rejected with exit code 1."""
        with Image.open(SAMPLE_WEBP) as im:
            frames_256 = [f.resize((256, 256)).copy() for f in ImageSequence.Iterator(im)]
            frames_rect = [f.resize((512, 256)).copy() for f in ImageSequence.Iterator(im)]

        with tempfile.TemporaryDirectory() as td:
            p_sq = os.path.join(td, "dim_256.webp")
            frames_256[0].save(p_sq, format="WEBP", save_all=True, append_images=frames_256[1:], duration=90, loop=0)

            p_rect = os.path.join(td, "dim_512x256.webp")
            frames_rect[0].save(p_rect, format="WEBP", save_all=True, append_images=frames_rect[1:], duration=90, loop=0)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Dimensions 256x256 do not match expected 512x512", res.stderr)
            self.assertIn("Dimensions 512x256 do not match expected 512x512", res.stderr)

    def test_05b_canvas_dimension_gif(self):
        """Verify 256x256 and 512x256 GIF animations are rejected with exit code 1."""
        with Image.open(SAMPLE_GIF) as im:
            frames_256 = [f.resize((256, 256)).copy() for f in ImageSequence.Iterator(im)]
            frames_rect = [f.resize((512, 256)).copy() for f in ImageSequence.Iterator(im)]

        with tempfile.TemporaryDirectory() as td:
            p_sq = os.path.join(td, "dim_256.gif")
            frames_256[0].save(p_sq, format="GIF", save_all=True, append_images=frames_256[1:], duration=90, loop=0)

            p_rect = os.path.join(td, "dim_512x256.gif")
            frames_rect[0].save(p_rect, format="GIF", save_all=True, append_images=frames_rect[1:], duration=90, loop=0)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Dimensions 256x256 do not match expected 512x512", res.stderr)
            self.assertIn("Dimensions 512x256 do not match expected 512x512", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 6: Non-Image File Handling
    # -------------------------------------------------------------------------
    def test_06a_extraneous_files_ignored_without_crash(self):
        """Verify non-image files (.txt, .DS_Store, .tmp, .json) do not crash the verifier."""
        with tempfile.TemporaryDirectory() as td:
            shutil.copy(SAMPLE_WEBP, os.path.join(td, "ent.webp"))
            shutil.copy(SAMPLE_GIF, os.path.join(td, "ent.gif"))

            with open(os.path.join(td, ".DS_Store"), "wb") as f:
                f.write(b"\x00\x00\x00\x01Bud1\x00")
            with open(os.path.join(td, "notes.txt"), "w") as f:
                f.write("Ignore this text note")
            with open(os.path.join(td, "temp.tmp"), "w") as f:
                f.write("temporary buffer")
            with open(os.path.join(td, "meta.json"), "w") as f:
                f.write('{"key": "value"}')

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 0, f"Expected RC 0 with extraneous files, got {res.returncode}. Stderr: {res.stderr}")
            self.assertIn("VERIFICATION PASSED: 2/2 animated assets verified successfully", res.stdout)

    def test_06b_only_extraneous_files_returns_exit_1(self):
        """Verify directory with only non-image files exits cleanly with code 1."""
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, ".DS_Store"), "wb") as f:
                f.write(b"\x00\x00\x00\x01Bud1\x00")
            with open(os.path.join(td, "notes.txt"), "w") as f:
                f.write("No images here")

            res = run_verifier(["--dir", td])
            self.assertEqual(res.returncode, 1)
            self.assertIn("No animated assets", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 7: Loop Count & Timing Defects
    # -------------------------------------------------------------------------
    def test_07a_non_zero_loop_count_rejected(self):
        """Verify animations with loop_count > 0 (not infinite) are rejected with exit code 1."""
        with tempfile.TemporaryDirectory() as td:
            # WebP ANIM chunk loop count mutation
            with open(SAMPLE_WEBP, "rb") as f:
                data_w = bytearray(f.read())
            anim_idx = data_w.find(b"ANIM")
            self.assertNotEqual(anim_idx, -1)
            # ANIM chunk data: 4 bytes bg_color, 2 bytes loop_count
            data_w[anim_idx + 12 : anim_idx + 14] = (5).to_bytes(2, "little")
            with open(os.path.join(td, "loop_5.webp"), "wb") as f:
                f.write(data_w)

            # GIF NETSCAPE chunk loop count mutation
            with open(SAMPLE_GIF, "rb") as f:
                data_g = bytearray(f.read())
            netscape_idx = data_g.find(b"NETSCAPE2.0")
            self.assertNotEqual(netscape_idx, -1)
            data_g[netscape_idx + 13 : netscape_idx + 15] = (3).to_bytes(2, "little")
            with open(os.path.join(td, "loop_3.gif"), "wb") as f:
                f.write(data_g)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Loop count is 5, expected 0 (infinite)", res.stderr)
            self.assertIn("Loop count is 3, expected 0 (infinite)", res.stderr)

    def test_07b_fast_timing_under_2000ms_rejected(self):
        """Verify animations under 2000ms duration (e.g. 50ms * 24 = 1200ms) are rejected."""
        with Image.open(SAMPLE_WEBP) as im:
            frames = [f.copy() for f in ImageSequence.Iterator(im)]

        with tempfile.TemporaryDirectory() as td:
            p_fast = os.path.join(td, "fast_1200ms.webp")
            frames[0].save(p_fast, format="WEBP", save_all=True, append_images=frames[1:], duration=50, loop=0)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("Total duration 1200ms < minimum 2000ms", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 8: Visual Integrity Defects
    # -------------------------------------------------------------------------
    def test_08a_opaque_corner_pixel_webp_rejected(self):
        """Verify WebP image with non-transparent corner (alpha > 0) is rejected."""
        with Image.open(SAMPLE_WEBP) as im:
            frames = [f.copy() for f in ImageSequence.Iterator(im)]
        for f in frames:
            f.putpixel((0, 0), (255, 0, 0, 255))  # Opaque red corner

        with tempfile.TemporaryDirectory() as td:
            p_opaque = os.path.join(td, "opaque_corner.webp")
            frames[0].save(p_opaque, format="WEBP", save_all=True, append_images=frames[1:], duration=90, loop=0)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("WebP corner (0, 0) alpha 255 != 0 (not transparent)", res.stderr)

    # -------------------------------------------------------------------------
    # ATTACK 9: File Size Budget & CLI Options
    # -------------------------------------------------------------------------
    def test_09a_file_size_exceeding_budget_rejected(self):
        """Verify files exceeding 2.5 MB (2560000 bytes) are rejected with exit code 1."""
        with tempfile.TemporaryDirectory() as td:
            with open(SAMPLE_WEBP, "rb") as f:
                data = f.read()
            data_padded = data + (b"\x00" * (2700000 - len(data)))
            with open(os.path.join(td, "oversized.webp"), "wb") as f:
                f.write(data_padded)

            res = run_verifier(["--dir", td, "-v"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("File size exceeds budget (2700000 bytes > 2560000)", res.stderr)

    def test_09b_invalid_cli_syntax_exit_code_2(self):
        """Verify invalid CLI flag triggers standard argparse exit code 2."""
        res = run_verifier(["--completely-bogus-argument-xyz"])
        self.assertEqual(res.returncode, 2)
        self.assertIn("usage:", res.stderr)

    def test_09c_json_report_generation(self):
        """Verify --report output writes a valid conforming JSON summary."""
        with tempfile.TemporaryDirectory() as td:
            report_path = os.path.join(td, "verification_report.json")
            res = run_verifier(["--dir", ANIMATED_DIR, "--sticker", "ent", "--report", report_path, "--strict"])
            self.assertEqual(res.returncode, 0)
            self.assertTrue(os.path.exists(report_path))
            with open(report_path, "r", encoding="utf-8") as f:
                rep = json.load(f)
            self.assertEqual(rep["summary"]["status"], "PASSED")
            self.assertEqual(rep["summary"]["total_checked"], 2)
            self.assertEqual(rep["by_format"]["webp"]["count"], 1)
            self.assertEqual(rep["by_format"]["gif"]["count"], 1)

    # -------------------------------------------------------------------------
    # ATTACK 10: Production Conformance Baseline
    # -------------------------------------------------------------------------
    def test_10_production_assets_strict_baseline(self):
        """Verify all 376 production assets pass strict verification."""
        res = run_verifier(["--dir", ANIMATED_DIR, "--strict"])
        self.assertEqual(res.returncode, 0, f"Production assets failed strict verification: {res.stderr}")
        self.assertIn("376/376 animated assets verified successfully", res.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
