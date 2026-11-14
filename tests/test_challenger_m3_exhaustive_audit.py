#!/usr/bin/env python3
"""
tests/test_challenger_m3_exhaustive_audit.py
============================================
Adversarial Challenger 2 Test Harness for Milestone 3:
1. Exhaustive 376-Asset Scan (188 .webp, 188 .gif in assets/animated/)
   - Exact 512x512 canvas dimensions
   - Strictly 24 frames @ 90ms duration (2160ms total)
   - Valid RIFF/WEBP and GIF89a headers
   - WebP: alpha transparency present, corner alpha == 0, loop count == 0
   - GIF: card background #10141E (16, 20, 30 +- 4), <= 128 colors, loop count == 0
   - File size between 10 KB and 2.5 MB
2. Build Mirror Synchronization
   - Byte-for-byte SHA-256 hash match between assets/animated/ and build/animated_stickers/
3. Concurrency Stress
   - 5 rapid consecutive runs of scripts/verify_animated_stickers.py
   - 5 parallel concurrent runs of scripts/verify_animated_stickers.py on Windows
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageSequence

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets", "animated")
BUILD_DIR = os.path.join(WORKSPACE_DIR, "build", "animated_stickers")
BUILD_WEBP_DIR = os.path.join(BUILD_DIR, "webp")
BUILD_GIF_DIR = os.path.join(BUILD_DIR, "gif")
PYTHON_EXE = sys.executable

STUDIO_BG_RGB = (16, 20, 30)
BG_TOLERANCE = 4
MIN_SIZE = 10 * 1024  # 10 KB
MAX_SIZE = 2500 * 1024  # 2.5 MB (2,560,000 bytes)


# Use established project test_helpers
sys.path.insert(0, WORKSPACE_DIR)
from tests.e2e.test_helpers import load_all_catalog_ids


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def audit_webp_binary_and_pillow(path: str) -> List[str]:
    errors = []
    if not os.path.exists(path):
        return [f"File missing: {path}"]

    size = os.path.getsize(path)
    if size < MIN_SIZE:
        errors.append(f"Size too small ({size} < {MIN_SIZE})")
    if size > MAX_SIZE:
        errors.append(f"Size too large ({size} > {MAX_SIZE})")

    # Binary check
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        errors.append("Invalid RIFF/WEBP header")
        return errors

    pos = 12
    width = None
    height = None
    has_anim = False
    has_alpha = False
    loop_count = None
    durations = []

    while pos < len(data) - 8:
        fourcc = data[pos : pos + 4]
        chunk_len = int.from_bytes(data[pos + 4 : pos + 8], "little")
        chunk_data = data[pos + 8 : pos + 8 + chunk_len]

        if fourcc == b"VP8X" and len(chunk_data) >= 10:
            flags = chunk_data[0]
            has_anim = bool(flags & 0x02)
            has_alpha = bool(flags & 0x10)
            width = int.from_bytes(chunk_data[4:7], "little") + 1
            height = int.from_bytes(chunk_data[7:10], "little") + 1
        elif fourcc == b"ANIM" and len(chunk_data) >= 6:
            loop_count = int.from_bytes(chunk_data[4:6], "little")
        elif fourcc == b"ANMF" and len(chunk_data) >= 16:
            dur = int.from_bytes(chunk_data[12:15], "little")
            durations.append(dur)

        pos += 8 + chunk_len + (chunk_len % 2)

    if not has_anim:
        errors.append("VP8X missing animation flag")
    if not has_alpha:
        errors.append("VP8X missing alpha flag")
    if width != 512 or height != 512:
        errors.append(f"Dimensions {width}x{height} != 512x512")
    if loop_count != 0:
        errors.append(f"Loop count {loop_count} != 0")
    if len(durations) != 24:
        errors.append(f"Frame count {len(durations)} != 24")
    total_dur = sum(durations)
    if total_dur != 2160:
        errors.append(f"Total duration {total_dur} != 2160ms")
    for idx, d in enumerate(durations):
        if d != 90:
            errors.append(f"Frame {idx} duration {d}ms != 90ms")

    # Pillow check
    try:
        with Image.open(path) as im:
            if im.format != "WEBP":
                errors.append(f"Pillow format {im.format} != WEBP")
            if im.size != (512, 512):
                errors.append(f"Pillow size {im.size} != (512, 512)")

            # Check frames
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            if len(frames) != 24:
                errors.append(f"Pillow frame count {len(frames)} != 24")

            # Check corners on first frame
            frame0 = frames[0].convert("RGBA")
            corners = [(0, 0), (511, 0), (0, 511), (511, 511)]
            for c in corners:
                a = frame0.getpixel(c)[3]
                if a != 0:
                    errors.append(f"Corner {c} alpha {a} != 0")

            # Check not fully transparent
            alpha_ext = frame0.getextrema()[3]
            if alpha_ext[1] == 0:
                errors.append("Frame 0 is completely transparent")
    except Exception as e:
        errors.append(f"Pillow exception: {e}")

    return errors


def audit_gif_binary_and_pillow(path: str) -> List[str]:
    errors = []
    if not os.path.exists(path):
        return [f"File missing: {path}"]

    size = os.path.getsize(path)
    if size < MIN_SIZE:
        errors.append(f"Size too small ({size} < {MIN_SIZE})")
    if size > MAX_SIZE:
        errors.append(f"Size too large ({size} > {MAX_SIZE})")

    # Binary check
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 13 or data[:6] != b"GIF89a":
        errors.append(f"Header {data[:6]!r} != GIF89a")
        return errors

    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")
    packed = data[10]
    has_gct = bool(packed & 0x80)
    gct_colors = (2 ** ((packed & 0x07) + 1)) if has_gct else 0
    gct_size = 3 * gct_colors if has_gct else 0

    if width != 512 or height != 512:
        errors.append(f"Dimensions {width}x{height} != 512x512")
    if gct_colors > 128:
        errors.append(f"GCT colors {gct_colors} > 128")

    pos = 13 + gct_size
    durations = []
    loop_count = None

    while pos < len(data):
        b = data[pos]
        if b == 0x3B:
            break
        elif b == 0x21:
            if pos + 2 > len(data):
                break
            ext_type = data[pos + 1]
            pos += 2
            if ext_type == 0xF9:  # Graphic Control
                if pos < len(data):
                    blk = data[pos]
                    if blk >= 4 and pos + 4 <= len(data):
                        delay_cs = int.from_bytes(data[pos + 2 : pos + 4], "little")
                        durations.append(delay_cs * 10)
                    pos += blk + 1
                    while pos < len(data) and data[pos] != 0:
                        pos += data[pos] + 1
                    pos += 1
            elif ext_type == 0xFF:  # Application
                if pos < len(data):
                    blk = data[pos]
                    app_id = data[pos + 1 : pos + 1 + blk]
                    pos += blk + 1
                    if b"NETSCAPE" in app_id and pos < len(data):
                        sub_size = data[pos]
                        if sub_size == 3 and pos + 4 <= len(data) and data[pos + 1] == 1:
                            loop_count = int.from_bytes(data[pos + 2 : pos + 4], "little")
                    while pos < len(data) and data[pos] != 0:
                        pos += data[pos] + 1
                    pos += 1
            else:
                while pos < len(data) and data[pos] != 0:
                    pos += data[pos] + 1
                pos += 1
        elif b == 0x2C:  # Image Descriptor
            if pos + 10 > len(data):
                break
            p_img = data[pos + 9]
            has_lct = bool(p_img & 0x80)
            lct_colors = (2 ** ((p_img & 0x07) + 1)) if has_lct else 0
            if has_lct and lct_colors > 128:
                errors.append(f"LCT colors {lct_colors} > 128")
            lct_size = 3 * lct_colors if has_lct else 0
            pos += 10 + lct_size + 1
            while pos < len(data) and data[pos] != 0:
                pos += data[pos] + 1
            pos += 1
        else:
            pos += 1

    if loop_count != 0:
        errors.append(f"Loop count {loop_count} != 0")
    if len(durations) != 24:
        errors.append(f"Frame count {len(durations)} != 24")
    total_dur = sum(durations)
    if total_dur != 2160:
        errors.append(f"Total duration {total_dur} != 2160ms")
    for idx, d in enumerate(durations):
        if d != 90:
            errors.append(f"Frame {idx} delay {d}ms != 90ms")

    # Pillow check
    try:
        with Image.open(path) as im:
            if im.format != "GIF":
                errors.append(f"Pillow format {im.format} != GIF")
            if im.size != (512, 512):
                errors.append(f"Pillow size {im.size} != (512, 512)")

            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            if len(frames) != 24:
                errors.append(f"Pillow frame count {len(frames)} != 24")

            frame0_rgb = frames[0].convert("RGB")
            corners = [(0, 0), (511, 0), (0, 511), (511, 511)]
            for c in corners:
                px = frame0_rgb.getpixel(c)
                diff = max(
                    abs(px[0] - STUDIO_BG_RGB[0]),
                    abs(px[1] - STUDIO_BG_RGB[1]),
                    abs(px[2] - STUDIO_BG_RGB[2]),
                )
                if diff > BG_TOLERANCE:
                    errors.append(f"Corner {c} color {px} deviates from {STUDIO_BG_RGB} by {diff}")
    except Exception as e:
        errors.append(f"Pillow exception: {e}")

    return errors


def run_single_verifier_run(run_idx: int) -> Tuple[int, float, str, str]:
    verifier_script = os.path.join(WORKSPACE_DIR, "scripts", "verify_animated_stickers.py")
    t0 = time.perf_counter()
    res = subprocess.run(
        [PYTHON_EXE, verifier_script, "--strict"],
        capture_output=True,
        text=True,
    )
    duration = time.perf_counter() - t0
    return res.returncode, duration, res.stdout, res.stderr


def main():
    print("=" * 80)
    print("CHALLENGER 2 EMPIRICAL AUDIT & CONCURRENCY STRESS SUITE (MILESTONE 3)")
    print("=" * 80)

    # Step 1: Catalog IDs
    catalog_ids = load_all_catalog_ids()
    print(f"Loaded {len(catalog_ids)} catalog IDs from packs.js and trini-slang.js.")
    assert len(catalog_ids) == 188, f"Expected 188 catalog IDs, found {len(catalog_ids)}"

    # Step 2: Exhaustive 376-Asset Scan
    print("\n--- PHASE 1: EXHAUSTIVE 376-ASSET BINARY & PILLOW SCAN ---")
    webp_errors = {}
    gif_errors = {}
    webp_sizes = []
    gif_sizes = []

    for sid in catalog_ids:
        webp_path = os.path.join(ASSETS_DIR, f"{sid}.webp")
        gif_path = os.path.join(ASSETS_DIR, f"{sid}.gif")

        w_err = audit_webp_binary_and_pillow(webp_path)
        if w_err:
            webp_errors[sid] = w_err
        else:
            webp_sizes.append(os.path.getsize(webp_path))

        g_err = audit_gif_binary_and_pillow(gif_path)
        if g_err:
            gif_errors[sid] = g_err
        else:
            gif_sizes.append(os.path.getsize(gif_path))

    print(f"WebP Audit: {len(webp_sizes)}/188 passed cleanly. Failures: {len(webp_errors)}")
    if webp_errors:
        for sid, errs in list(webp_errors.items())[:10]:
            print(f"  FAIL {sid}.webp: {'; '.join(errs)}")

    print(f"GIF Audit:  {len(gif_sizes)}/188 passed cleanly. Failures: {len(gif_errors)}")
    if gif_errors:
        for sid, errs in list(gif_errors.items())[:10]:
            print(f"  FAIL {sid}.gif: {'; '.join(errs)}")

    if webp_sizes:
        print(f"WebP Size Stats: Min={min(webp_sizes)/1024:.1f}KB, Max={max(webp_sizes)/1024:.1f}KB, Avg={sum(webp_sizes)/len(webp_sizes)/1024:.1f}KB")
    if gif_sizes:
        print(f"GIF Size Stats:  Min={min(gif_sizes)/1024:.1f}KB, Max={max(gif_sizes)/1024:.1f}KB, Avg={sum(gif_sizes)/len(gif_sizes)/1024:.1f}KB")

    # Step 3: Build Mirror Synchronization
    print("\n--- PHASE 2: BUILD MIRROR SYNCHRONIZATION AUDIT ---")
    missing_mirror_webp = []
    missing_mirror_gif = []
    hash_mismatches = []

    for sid in catalog_ids:
        orig_webp = os.path.join(ASSETS_DIR, f"{sid}.webp")
        orig_gif = os.path.join(ASSETS_DIR, f"{sid}.gif")
        mirror_webp = os.path.join(BUILD_WEBP_DIR, f"{sid}.webp")
        mirror_gif = os.path.join(BUILD_GIF_DIR, f"{sid}.gif")

        if not os.path.exists(mirror_webp):
            missing_mirror_webp.append(sid)
        else:
            h_orig = sha256_file(orig_webp)
            h_mirr = sha256_file(mirror_webp)
            if h_orig != h_mirr:
                hash_mismatches.append(f"WebP {sid}: {h_orig} != {h_mirr}")

        if not os.path.exists(mirror_gif):
            missing_mirror_gif.append(sid)
        else:
            h_orig = sha256_file(orig_gif)
            h_mirr = sha256_file(mirror_gif)
            if h_orig != h_mirr:
                hash_mismatches.append(f"GIF {sid}: {h_orig} != {h_mirr}")

    print(f"Mirrored WebP missing: {len(missing_mirror_webp)}/188")
    print(f"Mirrored GIF missing:  {len(missing_mirror_gif)}/188")
    print(f"Hash mismatches:       {len(hash_mismatches)}")
    if hash_mismatches:
        for m in hash_mismatches[:10]:
            print(f"  MISMATCH: {m}")

    # Check for extraneous files in build
    mirror_webp_files = set(os.listdir(BUILD_WEBP_DIR)) if os.path.exists(BUILD_WEBP_DIR) else set()
    mirror_gif_files = set(os.listdir(BUILD_GIF_DIR)) if os.path.exists(BUILD_GIF_DIR) else set()
    expected_webp_files = {f"{sid}.webp" for sid in catalog_ids}
    expected_gif_files = {f"{sid}.gif" for sid in catalog_ids}

    extra_webp = mirror_webp_files - expected_webp_files
    extra_gif = mirror_gif_files - expected_gif_files
    print(f"Extraneous mirrored WebP files: {len(extra_webp)}")
    print(f"Extraneous mirrored GIF files:  {len(extra_gif)}")

    # Step 4: Concurrency Stress
    print("\n--- PHASE 3: CONCURRENCY STRESS (5 RAPID CONSECUTIVE RUNS) ---")
    sequential_results = []
    for r in range(1, 6):
        rc, dur, out, err = run_single_verifier_run(r)
        passed = (rc == 0 and "VERIFICATION PASSED" in out)
        sequential_results.append((r, rc, dur, passed))
        print(f"  Run {r}: ReturnCode={rc}, Duration={dur:.3f}s, Passed={passed}")

    print("\n--- PHASE 4: ADVERSARIAL PARALLEL STRESS (5 CONCURRENT PROCESSES) ---")
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_single_verifier_run, i) for i in range(1, 6)]
        parallel_results = [f.result() for f in futures]
    total_par_time = time.perf_counter() - t0

    all_par_passed = True
    for idx, (rc, dur, out, err) in enumerate(parallel_results, 1):
        p = (rc == 0 and "VERIFICATION PASSED" in out)
        if not p:
            all_par_passed = False
        print(f"  Concurrent Process {idx}: ReturnCode={rc}, Duration={dur:.3f}s, Passed={p}")
    print(f"Total concurrent elapsed: {total_par_time:.3f}s (All 5 passed: {all_par_passed})")

    # Step 5: Overall Verdict
    phase1_pass = (len(webp_errors) == 0 and len(gif_errors) == 0)
    phase2_pass = (len(missing_mirror_webp) == 0 and len(missing_mirror_gif) == 0 and len(hash_mismatches) == 0 and len(extra_webp) == 0 and len(extra_gif) == 0)
    phase3_pass = all(res[3] for res in sequential_results)
    phase4_pass = all_par_passed

    print("\n" + "=" * 80)
    print("SUMMARY OF EMPIRICAL FINDINGS:")
    print(f"1. 376-Asset Scan:             {'PASS' if phase1_pass else 'FAIL'}")
    print(f"2. Build Mirror Synchronization: {'PASS' if phase2_pass else 'FAIL'}")
    print(f"3. Sequential Concurrency (5x): {'PASS' if phase3_pass else 'FAIL'}")
    print(f"4. Parallel Concurrency (5x):   {'PASS' if phase4_pass else 'FAIL'}")
    print("=" * 80)

    final_pass = phase1_pass and phase2_pass and phase3_pass and phase4_pass
    return 0 if final_pass else 1


if __name__ == "__main__":
    sys.exit(main())
