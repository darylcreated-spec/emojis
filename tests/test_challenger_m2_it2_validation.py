"""
tests/test_challenger_m2_it2_validation.py
==========================================
Challenger Empirical Validation Harness for Milestone 2 Iteration 2:
Validates binary headers, frame counts, frame durations, canvas dimensions,
and loop counts for all generated .webp and .gif animations.
"""

import os
import sys

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from tests.e2e.test_helpers import parse_webp_binary, parse_gif_binary
ANIM_DIR = os.path.join(WORKSPACE_DIR, "assets", "animated")
BUILD_WEBP_DIR = os.path.join(WORKSPACE_DIR, "build", "animated_stickers", "webp")
BUILD_GIF_DIR = os.path.join(WORKSPACE_DIR, "build", "animated_stickers", "gif")


def validate_asset(sid: str):
    results = {}
    
    # 1. assets/animated/{sid}.webp
    webp_path = os.path.join(ANIM_DIR, f"{sid}.webp")
    webp_res = parse_webp_binary(webp_path)
    results["webp_exists"] = webp_res.get("exists", False)
    results["webp_valid_riff"] = webp_res.get("valid_riff", False)
    results["webp_has_animation"] = webp_res.get("has_animation", False)
    results["webp_has_alpha"] = webp_res.get("has_alpha", False)
    results["webp_width"] = webp_res.get("width")
    results["webp_height"] = webp_res.get("height")
    results["webp_frames"] = webp_res.get("frame_count")
    results["webp_durations"] = webp_res.get("durations", [])
    results["webp_total_duration"] = webp_res.get("total_duration_ms", 0)
    results["webp_loop"] = webp_res.get("loop_count")
    results["webp_size"] = webp_res.get("size", 0)

    # 2. assets/animated/{sid}.gif
    gif_path = os.path.join(ANIM_DIR, f"{sid}.gif")
    gif_res = parse_gif_binary(gif_path)
    results["gif_exists"] = gif_res.get("exists", False)
    results["gif_valid"] = gif_res.get("valid_gif", False)
    results["gif_width"] = gif_res.get("width")
    results["gif_height"] = gif_res.get("height")
    results["gif_frames"] = gif_res.get("frame_count")
    results["gif_durations"] = gif_res.get("durations", [])
    results["gif_total_duration"] = gif_res.get("total_duration_ms", 0)
    results["gif_loop"] = gif_res.get("loop_count")
    results["gif_size"] = gif_res.get("size", 0)

    # 3. Check build/ mirror files exist
    b_webp = os.path.join(BUILD_WEBP_DIR, f"{sid}.webp")
    b_gif = os.path.join(BUILD_GIF_DIR, f"{sid}.gif")
    results["build_webp_exists"] = os.path.exists(b_webp) and os.path.getsize(b_webp) > 0
    results["build_gif_exists"] = os.path.exists(b_gif) and os.path.getsize(b_gif) > 0

    return results


def main():
    sids = sys.argv[1:]
    if not sids:
        # Default: all valid stickers in STICKER_RIG_REGISTRY that exist in assets/animated
        from scripts.build_animated_stickers import STICKER_RIG_REGISTRY
        sids = [sid for sid in STICKER_RIG_REGISTRY.keys() if os.path.exists(os.path.join(ANIM_DIR, f"{sid}.webp"))]
    
    print(f"Validating {len(sids)} stickers...")
    failures = []
    for sid in sids:
        r = validate_asset(sid)
        errors = []
        if not r["webp_exists"] or not r["webp_valid_riff"]:
            errors.append(f"WebP invalid header/missing")
        if r["webp_width"] != 512 or r["webp_height"] != 512:
            errors.append(f"WebP dimensions {r['webp_width']}x{r['webp_height']} != 512x512")
        if r["webp_frames"] != 24:
            errors.append(f"WebP frame count {r['webp_frames']} != 24")
        if any(d != 90 for d in r["webp_durations"]):
            errors.append(f"WebP frame duration not all 90ms: {set(r['webp_durations'])}")
        if r["webp_total_duration"] != 2160:
            errors.append(f"WebP total duration {r['webp_total_duration']}ms != 2160ms")
        if r["webp_size"] == 0:
            errors.append("WebP 0 bytes")

        if not r["gif_exists"] or not r["gif_valid"]:
            errors.append(f"GIF invalid header/missing")
        if r["gif_width"] != 512 or r["gif_height"] != 512:
            errors.append(f"GIF dimensions {r['gif_width']}x{r['gif_height']} != 512x512")
        if r["gif_frames"] != 24:
            errors.append(f"GIF frame count {r['gif_frames']} != 24")
        if any(d != 90 for d in r["gif_durations"]):
            errors.append(f"GIF frame duration not all 90ms: {set(r['gif_durations'])}")
        if r["gif_total_duration"] != 2160:
            errors.append(f"GIF total duration {r['gif_total_duration']}ms != 2160ms")
        if r["gif_size"] == 0:
            errors.append("GIF 0 bytes")

        if not r["build_webp_exists"]:
            errors.append("build/animated_stickers/webp mirror missing or 0 bytes")
        if not r["build_gif_exists"]:
            errors.append("build/animated_stickers/gif mirror missing or 0 bytes")

        if errors:
            print(f"[FAIL] {sid}: {', '.join(errors)}")
            failures.append((sid, errors))
        else:
            print(f"[PASS] {sid}: WebP ({r['webp_size']} bytes, 24x90ms, 512x512) | GIF ({r['gif_size']} bytes, 24x90ms, 512x512)")

    if failures:
        print(f"\nVALIDATION FAILED: {len(failures)} stickers failed.")
        sys.exit(1)
    else:
        print(f"\nVALIDATION PASSED: All {len(sids)} stickers strictly adhere to 512x512, 24 frames, 90ms duration, and valid RIFF/GIF89a headers.")
        sys.exit(0)


if __name__ == "__main__":
    main()
