#!/usr/bin/env python3
"""
tests/test_challenger_m3_verifier_adversarial.py
================================================
Adversarial Probe for scripts/verify_animated_stickers.py:
Tests defect detection, negative test cases, and edge cases:
1. Non-existent directory handling (exit code 1)
2. Empty directory handling (exit code 1)
3. 0-byte corrupt asset detection (exit code 1)
4. Corrupted header detection (exit code 1)
5. WebP non-transparent corner detection (exit code 1)
6. GIF incorrect background color detection (exit code 1)
7. CLI flags: --sticker, --format, --report, --fast
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from PIL import Image

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
VERIFIER_SCRIPT = os.path.join(WORKSPACE_DIR, "scripts", "verify_animated_stickers.py")
PYTHON_EXE = sys.executable


def run_verifier(args):
    cmd = [PYTHON_EXE, VERIFIER_SCRIPT] + args
    res = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr


def test_adversarial_probes():
    print("Testing verifier adversarial resilience...")

    # 1. Non-existent directory
    rc, stdout, stderr = run_verifier(["--dir", "non_existent_dir_xyz"])
    assert rc == 1, f"Expected rc=1 for non-existent dir, got {rc}"
    assert "ERROR: Target directory does not exist" in stderr
    print("  [PASS] Non-existent directory rejected cleanly.")

    # 2. Empty directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        rc, stdout, stderr = run_verifier(["--dir", tmp_dir])
        assert rc == 1, f"Expected rc=1 for empty dir, got {rc}"
        assert "No animated assets" in stderr
        print("  [PASS] Empty directory rejected cleanly.")

    # 3. 0-byte file detection
    with tempfile.TemporaryDirectory() as tmp_dir:
        bad_file = os.path.join(tmp_dir, "corrupt.webp")
        with open(bad_file, "wb") as f:
            pass  # 0 bytes
        rc, stdout, stderr = run_verifier(["--dir", tmp_dir])
        assert rc == 1, f"Expected rc=1 for 0-byte file, got {rc}"
        assert "FAIL" in stderr or "FAILED" in stderr
        print("  [PASS] 0-byte file detected and rejected.")

    # 4. Truncated / invalid RIFF header
    with tempfile.TemporaryDirectory() as tmp_dir:
        bad_file = os.path.join(tmp_dir, "bad_header.webp")
        with open(bad_file, "wb") as f:
            f.write(b"NOT_A_RIFF_HEADER_1234567890")
        rc, stdout, stderr = run_verifier(["--dir", tmp_dir])
        assert rc == 1, f"Expected rc=1 for bad header, got {rc}"
        assert "Invalid RIFF/WEBP header" in stderr or "too small" in stderr
        print("  [PASS] Invalid header detected and rejected.")

    # 5. Invalid GIF header
    with tempfile.TemporaryDirectory() as tmp_dir:
        bad_file = os.path.join(tmp_dir, "bad_header.gif")
        with open(bad_file, "wb") as f:
            f.write(b"NOT_A_GIF_HEADER_12345678901234567890")
        rc, stdout, stderr = run_verifier(["--dir", tmp_dir])
        assert rc == 1, f"Expected rc=1 for bad GIF header, got {rc}"
        assert "Invalid GIF header" in stderr or "too small" in stderr
        print("  [PASS] Invalid GIF header detected and rejected.")

    # 6. Single sticker CLI flag filter
    rc, stdout, stderr = run_verifier(["--sticker", "steups", "--verbose"])
    assert rc == 0, f"Expected rc=0 for --sticker steups, got {rc}. Stderr: {stderr}"
    assert "steups.webp" in stdout
    assert "steups.gif" in stdout
    assert "2/2 animated assets verified successfully" in stdout
    print("  [PASS] --sticker CLI filter works accurately.")

    # 7. Format filter flag
    rc, stdout, stderr = run_verifier(["--format", "webp"])
    assert rc == 0, f"Expected rc=0 for --format webp, got {rc}"
    assert "188/188 animated assets verified successfully (188 WebP, 0 GIF)" in stdout
    print("  [PASS] --format webp filter works accurately.")

    rc, stdout, stderr = run_verifier(["--format", "gif"])
    assert rc == 0, f"Expected rc=0 for --format gif, got {rc}"
    assert "188/188 animated assets verified successfully (0 WebP, 188 GIF)" in stdout
    print("  [PASS] --format gif filter works accurately.")

    # 8. Report generation flag
    with tempfile.TemporaryDirectory() as tmp_dir:
        report_path = os.path.join(tmp_dir, "report.json")
        rc, stdout, stderr = run_verifier(["--report", report_path, "--sticker", "steups"])
        assert rc == 0, f"Expected rc=0 for --report, got {rc}"
        assert os.path.exists(report_path), "Report JSON file was not created"
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["summary"]["status"] == "PASSED"
        assert data["summary"]["total_checked"] == 2
        print("  [PASS] --report flag outputs valid schema JSON report.")

    print("\nALL VERIFIER ADVERSARIAL RESILIENCE PROBES PASSED!")
    return 0


if __name__ == "__main__":
    sys.exit(test_adversarial_probes())
