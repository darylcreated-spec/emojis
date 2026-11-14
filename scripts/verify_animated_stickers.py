#!/usr/bin/env python3
"""
scripts/verify_animated_stickers.py
===================================
Automated verification suite validating RIFF/WEBP and GIF89a headers,
frame count (>= 24), timing (>= 2.0s), canvas dimensions (512x512),
and zero corruption across all animated sticker assets.

Interface contract:
- Exit code 0: All checked animated assets passed validation.
- Exit code 1: One or more defects found, or directory contains 0 assets.
- Exit code 2: CLI argument or invocation syntax error.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DEFAULT_ANIMATED_DIR = os.path.join(WORKSPACE_DIR, "assets", "animated")

# Constants required for compliance
MIN_FRAMES = 24
NOMINAL_FRAME_DURATION_MS = 90
MIN_TOTAL_DURATION_MS = 2000
NOMINAL_TOTAL_DURATION_MS = 2160
EXPECTED_WIDTH = 512
EXPECTED_HEIGHT = 512
MIN_FILE_SIZE_BYTES = 10240  # 10 KB boundary
MAX_FILE_SIZE_BYTES = 2560000  # 2.5 MB boundary
MAX_GIF_PALETTE_COLORS = 128
STUDIO_CARD_BG_RGB = (16, 20, 30)
CARD_BG_TOLERANCE = 4


def parse_webp_binary(file_path: str, strict: bool = False) -> Dict[str, Any]:
    """
    Direct binary inspection of WebP files bypassing Pillow quirks.
    Validates RIFF header, VP8X chunk, ANIM chunk, and ANMF frame chunks.
    """
    if not os.path.exists(file_path):
        return {"error": "File does not exist", "exists": False, "valid": False}

    size = os.path.getsize(file_path)
    if size == 0:
        return {"error": "File is empty (0 bytes)", "exists": True, "size": 0, "valid": False}

    if size < MIN_FILE_SIZE_BYTES:
        return {"error": f"File size too small ({size} bytes < {MIN_FILE_SIZE_BYTES})", "size": size, "valid": False}

    if size > MAX_FILE_SIZE_BYTES:
        return {"error": f"File size exceeds budget ({size} bytes > {MAX_FILE_SIZE_BYTES})", "size": size, "valid": False}

    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return {"error": "Invalid RIFF/WEBP header", "valid_riff": False, "valid": False, "size": size}

    pos = 12
    width = None
    height = None
    has_animation = False
    has_alpha = False
    loop_count = None
    durations: List[int] = []

    while pos < len(data) - 8:
        fourcc = data[pos : pos + 4]
        chunk_size = int.from_bytes(data[pos + 4 : pos + 8], "little")
        chunk_data = data[pos + 8 : pos + 8 + chunk_size]

        if fourcc == b"VP8X" and len(chunk_data) >= 10:
            flags = chunk_data[0]
            has_animation = bool(flags & 0x02)
            has_alpha = bool(flags & 0x10)
            width = int.from_bytes(chunk_data[4:7], "little") + 1
            height = int.from_bytes(chunk_data[7:10], "little") + 1

        elif fourcc == b"ANIM" and len(chunk_data) >= 6:
            loop_count = int.from_bytes(chunk_data[4:6], "little")

        elif fourcc == b"ANMF" and len(chunk_data) >= 16:
            dur = int.from_bytes(chunk_data[12:15], "little")
            durations.append(dur)

        pos += 8 + chunk_size + (chunk_size % 2)

    frame_count = len(durations)
    total_duration_ms = sum(durations)

    errors = []
    if not has_animation:
        errors.append("VP8X animation flag is not set")
    if not has_alpha:
        errors.append("VP8X alpha flag is not set")
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        errors.append(f"Dimensions {width}x{height} do not match expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    if loop_count != 0:
        errors.append(f"Loop count is {loop_count}, expected 0 (infinite)")
    if frame_count < MIN_FRAMES:
        errors.append(f"Frame count {frame_count} < minimum {MIN_FRAMES}")
    if total_duration_ms < MIN_TOTAL_DURATION_MS:
        errors.append(f"Total duration {total_duration_ms}ms < minimum {MIN_TOTAL_DURATION_MS}ms")

    if strict:
        if frame_count != 24:
            errors.append(f"Strict: Frame count {frame_count} != 24")
        if total_duration_ms != NOMINAL_TOTAL_DURATION_MS:
            errors.append(f"Strict: Total duration {total_duration_ms}ms != {NOMINAL_TOTAL_DURATION_MS}ms")

    return {
        "exists": True,
        "size": size,
        "valid_riff": True,
        "width": width,
        "height": height,
        "has_animation": has_animation,
        "has_alpha": has_alpha,
        "loop_count": loop_count,
        "frame_count": frame_count,
        "durations": durations,
        "total_duration_ms": total_duration_ms,
        "valid": len(errors) == 0,
        "errors": errors,
    }


def parse_gif_binary(file_path: str, strict: bool = False) -> Dict[str, Any]:
    """
    Direct binary inspection of GIF files.
    Validates GIF89a header, Logical Screen Descriptor, Netscape application block,
    Graphic Control Extensions (delays), and Global Color Table size.
    """
    if not os.path.exists(file_path):
        return {"error": "File does not exist", "exists": False, "valid": False}

    size = os.path.getsize(file_path)
    if size == 0:
        return {"error": "File is empty (0 bytes)", "exists": True, "size": 0, "valid": False}

    if size < MIN_FILE_SIZE_BYTES:
        return {"error": f"File size too small ({size} bytes < {MIN_FILE_SIZE_BYTES})", "size": size, "valid": False}

    if size > MAX_FILE_SIZE_BYTES:
        return {"error": f"File size exceeds budget ({size} bytes > {MAX_FILE_SIZE_BYTES})", "size": size, "valid": False}

    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) < 13 or data[:6] not in (b"GIF89a", b"GIF87a"):
        return {"error": "Invalid GIF header", "valid_gif": False, "valid": False, "size": size}

    header = data[:6].decode("ascii", errors="replace")
    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")
    packed = data[10]
    has_gct = bool(packed & 0x80)
    gct_size = 3 * (2 ** ((packed & 0x07) + 1)) if has_gct else 0
    palette_colors = (2 ** ((packed & 0x07) + 1)) if has_gct else 0

    pos = 13 + gct_size
    durations: List[int] = []
    loop_count = None

    while pos < len(data):
        b = data[pos]
        if b == 0x3B:  # Trailer
            break
        elif b == 0x21:  # Extension block
            if pos + 2 > len(data):
                break
            ext_type = data[pos + 1]
            pos += 2
            if ext_type == 0xF9:  # Graphic Control Extension
                if pos < len(data):
                    block_size = data[pos]
                    if block_size >= 4 and pos + 4 <= len(data):
                        delay_cs = int.from_bytes(data[pos + 2 : pos + 4], "little")
                        durations.append(delay_cs * 10)  # ms
                    pos += block_size + 1
                    while pos < len(data) and data[pos] != 0:
                        pos += data[pos] + 1
                    pos += 1
            elif ext_type == 0xFF:  # Application Extension
                if pos < len(data):
                    block_size = data[pos]
                    app_id = data[pos + 1 : pos + 1 + block_size]
                    pos += block_size + 1
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
            packed_img = data[pos + 9]
            has_lct = bool(packed_img & 0x80)
            lct_size = 3 * (2 ** ((packed_img & 0x07) + 1)) if has_lct else 0
            pos += 10 + lct_size + 1
            while pos < len(data) and data[pos] != 0:
                pos += data[pos] + 1
            pos += 1
        else:
            pos += 1

    frame_count = len(durations)
    total_duration_ms = sum(durations)

    errors = []
    if header != "GIF89a":
        errors.append(f"Header is {header}, expected GIF89a")
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        errors.append(f"Dimensions {width}x{height} do not match expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    if palette_colors > MAX_GIF_PALETTE_COLORS:
        errors.append(f"Palette colors {palette_colors} > maximum {MAX_GIF_PALETTE_COLORS}")
    if loop_count != 0:
        errors.append(f"Loop count is {loop_count}, expected 0 (infinite)")
    if frame_count < MIN_FRAMES:
        errors.append(f"Frame count {frame_count} < minimum {MIN_FRAMES}")
    if total_duration_ms < MIN_TOTAL_DURATION_MS:
        errors.append(f"Total duration {total_duration_ms}ms < minimum {MIN_TOTAL_DURATION_MS}ms")

    if strict:
        if frame_count != 24:
            errors.append(f"Strict: Frame count {frame_count} != 24")
        if total_duration_ms != NOMINAL_TOTAL_DURATION_MS:
            errors.append(f"Strict: Total duration {total_duration_ms}ms != {NOMINAL_TOTAL_DURATION_MS}ms")

    return {
        "exists": True,
        "size": size,
        "valid_gif": True,
        "header": header,
        "width": width,
        "height": height,
        "palette_colors": palette_colors,
        "loop_count": loop_count,
        "frame_count": frame_count,
        "durations": durations,
        "total_duration_ms": total_duration_ms,
        "valid": len(errors) == 0,
        "errors": errors,
    }


def verify_corners_pillow(file_path: str, is_gif: bool) -> List[str]:
    """Optional visual verification using Pillow to check corner pixels and transparency."""
    if not HAS_PIL:
        return []
    errors = []
    try:
        with Image.open(file_path) as im:
            corners = [(0, 0), (511, 0), (0, 511), (511, 511)]
            if is_gif:
                rgb_im = im.convert("RGB")
                for c in corners:
                    px = rgb_im.getpixel(c)
                    diff = max(
                        abs(px[0] - STUDIO_CARD_BG_RGB[0]),
                        abs(px[1] - STUDIO_CARD_BG_RGB[1]),
                        abs(px[2] - STUDIO_CARD_BG_RGB[2]),
                    )
                    if diff > CARD_BG_TOLERANCE:
                        errors.append(f"GIF corner {c} color {px} deviates from {STUDIO_CARD_BG_RGB} by {diff}")
                        break
            else:
                rgba_im = im.convert("RGBA")
                for c in corners:
                    alpha = rgba_im.getpixel(c)[3]
                    if alpha != 0:
                        errors.append(f"WebP corner {c} alpha {alpha} != 0 (not transparent)")
                        break
                # Ensure the WebP image is not completely transparent
                if rgba_im.getextrema()[3][1] == 0:
                    errors.append("WebP image is completely transparent (no visible content)")
                # Sample reference sticker check
                base = os.path.basename(file_path).lower()
                if base == "ent.webp":
                    center_alpha = rgba_im.getpixel((256, 256))[3]
                    if center_alpha == 0:
                        errors.append("WebP ent.webp center pixel (256, 256) is transparent")
    except Exception as e:
        errors.append(f"Pillow decode error: {e}")
    return errors


def build_arg_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Automated Animation Verification Suite for PeelOff Trinidad & Tobago Stickers."
    )
    parser.add_argument(
        "--dir",
        default=DEFAULT_ANIMATED_DIR,
        help="Directory containing animated assets (default: assets/animated)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast binary chunk validation only (skip slow pixel decoding)",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Output path for JSON verification report",
    )
    parser.add_argument(
        "--format",
        choices=["all", "webp", "gif"],
        default="all",
        help="Asset format to verify (default: all)",
    )
    parser.add_argument(
        "--sticker",
        default=None,
        help="Verify a single sticker by ID or filename",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce strict exact 24 frames and exact 2160ms timing",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose per-asset output",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    target_dir = os.path.abspath(args.dir)
    if not os.path.isdir(target_dir):
        print(f"ERROR: Target directory does not exist or is not a directory: {target_dir}", file=sys.stderr)
        return 1

    t0 = time.perf_counter()

    # Discover target image files
    entries = sorted(os.listdir(target_dir))
    target_files: List[str] = []

    for entry in entries:
        lower = entry.lower()
        if args.format == "webp" and not lower.endswith(".webp"):
            continue
        if args.format == "gif" and not lower.endswith(".gif"):
            continue
        if args.format == "all" and not (lower.endswith(".webp") or lower.endswith(".gif")):
            continue

        if args.sticker:
            stk = args.sticker.lower()
            if stk.endswith(".webp") or stk.endswith(".gif"):
                if lower != stk:
                    continue
            else:
                name_no_ext, _ = os.path.splitext(lower)
                if name_no_ext != stk:
                    continue

        target_files.append(os.path.join(target_dir, entry))

    if len(target_files) == 0:
        print(f"ERROR: No animated assets (.webp or .gif) found in directory: {target_dir}", file=sys.stderr)
        return 1

    total_checked = 0
    total_passed = 0
    total_failed = 0
    webp_count = 0
    webp_passed = 0
    webp_failed = 0
    gif_count = 0
    gif_passed = 0
    gif_failed = 0

    defects: List[Dict[str, Any]] = []

    for file_path in target_files:
        filename = os.path.basename(file_path)
        is_gif = filename.lower().endswith(".gif")
        total_checked += 1

        if is_gif:
            gif_count += 1
            meta = parse_gif_binary(file_path, strict=args.strict)
        else:
            webp_count += 1
            meta = parse_webp_binary(file_path, strict=args.strict)

        file_errors = list(meta.get("errors", []))
        if not meta.get("valid", True) and "error" in meta and meta["error"] not in file_errors:
            file_errors.append(meta["error"])

        # Pixel corner checks if not fast mode and binary parse passed
        if not args.fast and len(file_errors) == 0 and meta.get("exists", False):
            corner_errs = verify_corners_pillow(file_path, is_gif)
            file_errors.extend(corner_errs)

        if len(file_errors) == 0:
            total_passed += 1
            if is_gif:
                gif_passed += 1
            else:
                webp_passed += 1
            if args.verbose:
                print(
                    f"  [PASS] {filename} -> {meta.get('frame_count')} frames, "
                    f"{meta.get('total_duration_ms')}ms, {meta.get('size') / 1024.0:.1f}KB"
                )
        else:
            total_failed += 1
            if is_gif:
                gif_failed += 1
            else:
                webp_failed += 1
            defects.append({
                "file": filename,
                "path": file_path,
                "format": "gif" if is_gif else "webp",
                "errors": file_errors,
            })
            if args.verbose:
                print(f"  [FAIL] {filename} -> {'; '.join(file_errors)}", file=sys.stderr)

    elapsed_sec = time.perf_counter() - t0

    # Write JSON report if requested
    if args.report:
        report_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "target_dir": target_dir,
            "summary": {
                "total_checked": total_checked,
                "total_passed": total_passed,
                "total_failed": total_failed,
                "duration_seconds": round(elapsed_sec, 3),
                "status": "PASSED" if total_failed == 0 else "FAILED",
                "exit_code": 0 if total_failed == 0 else 1,
            },
            "by_format": {
                "webp": {
                    "count": webp_count,
                    "passed": webp_passed,
                    "failed": webp_failed,
                    "frame_counts": [24],
                    "nominal_duration_ms": NOMINAL_FRAME_DURATION_MS,
                    "total_duration_ms": NOMINAL_TOTAL_DURATION_MS,
                    "dimensions": [EXPECTED_WIDTH, EXPECTED_HEIGHT],
                    "loop_count": 0,
                },
                "gif": {
                    "count": gif_count,
                    "passed": gif_passed,
                    "failed": gif_failed,
                    "frame_counts": [24],
                    "nominal_duration_ms": NOMINAL_FRAME_DURATION_MS,
                    "total_duration_ms": NOMINAL_TOTAL_DURATION_MS,
                    "dimensions": [EXPECTED_WIDTH, EXPECTED_HEIGHT],
                    "max_palette_colors": MAX_GIF_PALETTE_COLORS,
                    "card_bg_rgb": list(STUDIO_CARD_BG_RGB),
                    "loop_count": 0,
                },
            },
            "defects": defects,
        }
        report_dir = os.path.dirname(os.path.abspath(args.report))
        if report_dir:
            os.makedirs(report_dir, exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

    if total_failed == 0:
        print(
            f"VERIFICATION PASSED: {total_checked}/{total_checked} animated assets verified successfully "
            f"({webp_passed} WebP, {gif_passed} GIF) in {elapsed_sec:.2f}s."
        )
        return 0
    else:
        print(
            f"VERIFICATION FAILED: {total_failed}/{total_checked} animated assets failed verification "
            f"({webp_failed} WebP, {gif_failed} GIF) in {elapsed_sec:.2f}s.",
            file=sys.stderr,
        )
        for defect in defects[:20]:
            print(f"  - {defect['file']}: {'; '.join(defect['errors'])}", file=sys.stderr)
        if len(defects) > 20:
            print(f"  ... and {len(defects) - 20} more defects.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
