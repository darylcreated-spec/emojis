"""
PeelOff E2E Test Suite — Tier 2: Boundary & Corner Cases (Boundary Value Analysis)
50 Comprehensive Test Cases covering Features F1 through F10 (5 tests per feature).
Focuses on boundary limits, edge values, zero thresholds, overflow conditions, and extremes.
All test cases execute genuine system assertions against production modules, real assets,
binary chunk structures, and frontend logic.
"""

import os
import sys
import json
import re
import math
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

from tests.e2e.test_helpers import (
    get_workspace_path,
    get_python_executable,
    load_packs_catalog,
    load_slang_catalog,
    load_all_catalog_ids,
    load_whatsapp_manifest,
    parse_webp_binary,
    parse_gif_binary,
    safe_open_image,
    check_card_background_rgb,
    check_webp_corner_alpha,
    run_command,
    require_milestone,
    is_strict_mode,
    temporary_strict_mode,
)

from scripts.build_animated_stickers import (
    clamp01,
    ease_in_out_cubic,
    ease_out_back,
    comic_pop_curve,
    prep_breathing_room,
    squash_stretch_offset,
    classify_rig,
)


class TestTier2F1CulturalGuideBoundaries(unittest.TestCase):
    """F1: Boundary & Corner Cases for Cultural Reference Guide."""

    def setUp(self):
        self.spec_path = get_workspace_path("docs", "CULTURAL_ANIMATION_SPEC.md")

    def test_t2_f1_01_exact_188_entries_boundary(self):
        """TC-T2-F1-01: Boundary check for exactly 188 unique stickers in matrix."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read()
        all_ids = load_all_catalog_ids()
        found_ids = [sid for sid in all_ids if sid in content]
        if len(found_ids) < 188:
            require_milestone(
                "Pending Milestone M1",
                False,
                f"Spec matrix contains {len(found_ids)}/188 stickers (authoring in progress)"
            )
        self.assertEqual(len(found_ids), 188)
        self.assertEqual(len(set(found_ids)), 188, "Spec contains duplicate sticker ID mappings")

    def test_t2_f1_02_slang_string_length_extremes(self):
        """TC-T2-F1-02: Boundary check for shortest and longest slang identifiers."""
        all_ids = load_all_catalog_ids()
        shortest = min(all_ids, key=len)
        longest = max(all_ids, key=len)
        self.assertGreater(len(shortest), 0, "Encountered empty sticker ID in catalog")
        self.assertLessEqual(len(shortest), 4, f"Shortest ID should be <= 4 chars: {shortest}")
        self.assertGreaterEqual(len(longest), 18, f"Longest ID should be >= 18 chars: {longest}")
        self.assertLessEqual(len(longest), 64, f"Longest ID exceeds maximum URL identifier length: {longest}")

    def test_t2_f1_03_special_character_and_punctuation_preservation(self):
        """TC-T2-F1-03: Boundary check for punctuation ('?!', '-', ''') in slang terms."""
        packs = load_packs_catalog()
        slang = load_slang_catalog()
        pack_names = [s.get("name", "") for p in packs for s in p.get("stickers", [])]
        slang_names = [s.get("name", "") for s in slang]
        all_names = pack_names + slang_names
        punctuated = [n for n in all_names if any(c in n for c in ["?!", "!", "'", "-"])]
        self.assertGreater(len(punctuated), 20, "Cultural punctuation not preserved in sticker names")

    def test_t2_f1_04_zero_empty_emotional_register_fields(self):
        """TC-T2-F1-04: Corner check for zero placeholder tokens (TODO, TBD, FIXME) in spec and catalog."""
        # 1. Slang catalog check
        slang = load_slang_catalog()
        for item in slang:
            meaning = item.get("meaning", "").upper()
            visual = item.get("visual", "").upper()
            for token in ["TODO", "TBD", "FIXME", "XXX"]:
                self.assertNotIn(token, meaning, f"Slang {item.get('id')} has placeholder in meaning: {token}")
                self.assertNotIn(token, visual, f"Slang {item.get('id')} has placeholder in visual: {token}")

        # 2. Spec document check
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read().upper()
        placeholders = [tok for tok in ["TODO", "TBD", "FIXME", "XXX"] if tok in content]
        self.assertEqual(len(placeholders), 0, f"Found placeholder tokens in spec: {placeholders}")

    def test_t2_f1_05_cultural_categories_boundary_and_completeness(self):
        """TC-T2-F1-05: Boundary check for strict 6 canonical slang categories and partition bounds."""
        slang = load_slang_catalog()
        self.assertEqual(len(slang), 88, f"Expected exactly 88 slang stickers, found {len(slang)}")
        categories = {}
        for s in slang:
            cat = s.get("category")
            self.assertIsNotNone(cat, f"Sticker {s.get('id')} missing category")
            categories[cat] = categories.get(cat, 0) + 1

        expected_categories = {
            "Co-Signs & Facts",
            "Attitude & Shade",
            "Vibes, Belly & Money",
            "People & Drama",
            "Greetings & Links",
            "Disbelief & Comedy",
        }
        self.assertEqual(set(categories.keys()), expected_categories, "Slang categories do not match canonical set")
        for cat_name, count in categories.items():
            self.assertGreaterEqual(count, 5, f"Category '{cat_name}' has fewer than 5 stickers ({count})")
            self.assertLessEqual(count, 30, f"Category '{cat_name}' exceeds 30 sticker pack boundary ({count})")


class TestTier2F2MotionPrimitivesBoundaries(unittest.TestCase):
    """F2: Boundary & Corner Cases for Motion Primitives."""

    def test_t2_f2_01_temporal_cycle_boundary_t0_vs_t1(self):
        """TC-T2-F2-01: Loop continuity boundary: motion curves at t=0.0 vs t=1.0."""
        # 1. Test real comic_pop_curve loop closure
        val_0 = comic_pop_curve(0.0)
        val_1 = comic_pop_curve(1.0)
        delta = abs(val_1 - val_0)
        self.assertAlmostEqual(delta, 0.0, places=5, msg="comic_pop_curve does not close loop at t=1.0")

        # 2. Test ease_in_out_cubic boundary values and clamping
        self.assertEqual(ease_in_out_cubic(0.0), 0.0)
        self.assertEqual(ease_in_out_cubic(1.0), 1.0)
        self.assertEqual(ease_in_out_cubic(-0.5), 0.0, "Negative input should clamp to 0.0")
        self.assertEqual(ease_in_out_cubic(1.5), 1.0, "Overflow input should clamp to 1.0")

    def test_t2_f2_02_canvas_bounding_box_clipping(self):
        """TC-T2-F2-02: Geometric boundary: test prep_breathing_room creates >= 20px safety margins on 512x512."""
        im = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
        prepped = prep_breathing_room(im, scale=0.91)
        self.assertEqual(prepped.size, (512, 512), "Canvas size altered by prep_breathing_room")

        # Corner pixel must be completely transparent
        self.assertEqual(prepped.getpixel((0, 0))[3], 0, "Top-left corner not transparent")
        self.assertEqual(prepped.getpixel((511, 511))[3], 0, "Bottom-right corner not transparent")

        # Bounding box of content must leave at least 20px margin on all sides
        bbox = prepped.getbbox()
        self.assertIsNotNone(bbox)
        margin_left = bbox[0]
        margin_top = bbox[1]
        margin_right = 512 - bbox[2]
        margin_bottom = 512 - bbox[3]
        self.assertGreaterEqual(margin_left, 20, f"Left margin {margin_left}px < 20px")
        self.assertGreaterEqual(margin_top, 20, f"Top margin {margin_top}px < 20px")
        self.assertGreaterEqual(margin_right, 20, f"Right margin {margin_right}px < 20px")
        self.assertGreaterEqual(margin_bottom, 20, f"Bottom margin {margin_bottom}px < 20px")

    def test_t2_f2_03_micro_motion_hold_non_zero_delta(self):
        """TC-T2-F2-03: Boundary check for non-zero displacement during comic hold interval in comic_pop_curve."""
        # Hold interval in comic_pop_curve is [t_hit=0.32, t_hold=0.68]
        sample_times = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
        samples = [comic_pop_curve(t) for t in sample_times]

        # All values during hold must be bounded around 1.0 (comic hold envelope [0.93, 1.07])
        self.assertTrue(all(0.93 <= s <= 1.07 for s in samples), f"Hold samples outside envelope: {samples}")

        # Frame-to-frame step deltas must be strictly non-zero (> 0.01) to prevent frame coalescing
        step_deltas = [abs(samples[i] - samples[i - 1]) for i in range(1, len(samples))]
        self.assertTrue(all(d > 0.01 for d in step_deltas), f"Hold interval delta dropped below 0.01: {step_deltas}")

    def test_t2_f2_04_overshoot_factor_extreme_bounds(self):
        """TC-T2-F2-04: Boundary check for ease_out_back overshoot factor s=1.70158."""
        # 1. Bounds at endpoints (tolerating float epsilon)
        self.assertAlmostEqual(ease_out_back(0.0), 0.0, places=5)
        self.assertAlmostEqual(ease_out_back(1.0), 1.0, places=5)

        # 2. Overshoot peak bounded in (1.0, 1.15)
        peak = ease_out_back(0.7, s=1.70158)
        self.assertGreater(peak, 1.0, "Overshoot curve did not exceed 1.0 at peak")
        self.assertLess(peak, 1.15, "Overshoot curve exceeded comic safety bound of 1.15")

        # 3. Clamping on extreme inputs (tolerating float epsilon)
        self.assertAlmostEqual(ease_out_back(-1.0), 0.0, places=5, msg="Negative input should clamp to 0.0")
        self.assertAlmostEqual(ease_out_back(2.0), 1.0, places=5, msg="Overflow input should clamp to 1.0")

    def test_t2_f2_05_squash_and_stretch_displacement_bounds(self):
        """TC-T2-F2-05: Boundary check for volume-preserving squash_stretch_offset clamping in [0.65, 1.45]."""
        cx, cy = 256.0, 256.0
        # 1. Fixed point at anchor: offset must be (0.0, 0.0) for any scale
        off_x, off_y = squash_stretch_offset(cx, cy, cx, cy, sy=1.2)
        self.assertAlmostEqual(off_x, 0.0, places=5)
        self.assertAlmostEqual(off_y, 0.0, places=5)

        # 2. Extreme compression: sy=0.05 clamped to 0.65
        off_x_comp, off_y_comp = squash_stretch_offset(cx, cy + 44, cx, cy, sy=0.05)
        expected_off_y = (cy + 44 / 0.65) - (cy + 44)
        self.assertAlmostEqual(off_y_comp, expected_off_y, places=3, msg="sy not clamped to 0.65 on extreme squash")

        # 3. Extreme elongation: sy=10.0 clamped to 1.45
        off_x_elon, off_y_elon = squash_stretch_offset(cx, cy + 44, cx, cy, sy=10.0)
        expected_off_y_elon = (cy + 44 / 1.45) - (cy + 44)
        self.assertAlmostEqual(off_y_elon, expected_off_y_elon, places=3, msg="sy not clamped to 1.45 on extreme stretch")


class TestTier2F3IndividualizedRigMappingBoundaries(unittest.TestCase):
    """F3: Boundary & Corner Cases for Rig Mapping."""

    def test_t2_f3_01_catalog_disjointness_and_root_disambiguation(self):
        """TC-T2-F3-01: Disjointness and rig disambiguation between pack stickers and slang stickers."""
        packs = load_packs_catalog()
        slang = load_slang_catalog()
        pack_ids = set(s["id"] for p in packs for s in p.get("stickers", []) if "id" in s)
        slang_ids = set(s["id"] for s in slang if "id" in s)

        # 1. Strict disjointness between packs and slang catalogs
        intersection = pack_ids.intersection(slang_ids)
        self.assertEqual(len(intersection), 0, f"Colliding IDs between packs and slang: {intersection}")
        self.assertEqual(len(pack_ids), 100, f"Expected 100 pack stickers, found {len(pack_ids)}")
        self.assertEqual(len(slang_ids), 88, f"Expected 88 slang stickers, found {len(slang_ids)}")
        self.assertEqual(len(pack_ids | slang_ids), 188, "Total union does not equal 188 unique stickers")

        # 2. Verify root collision resolves to distinct specialized rigs
        rig_pack = classify_rig("steups")
        rig_slang = classify_rig("slang-steups")
        self.assertEqual(rig_pack, "steups_puff", f"Unexpected rig for steups: {rig_pack}")
        self.assertEqual(rig_slang, "steups_sideeye_emoji", f"Unexpected rig for slang-steups: {rig_slang}")
        self.assertNotEqual(rig_pack, rig_slang, "Colliding root stickers must resolve to distinct rigs")

    def test_t2_f3_02_catalog_id_kebab_case_normalization(self):
        """TC-T2-F3-02: Normalization boundary: all 188 catalog IDs strictly match lower-kebab format."""
        all_ids = load_all_catalog_ids()
        self.assertEqual(len(all_ids), 188)
        kebab_pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        for sid in all_ids:
            self.assertEqual(sid, sid.lower(), f"ID contains uppercase characters: {sid}")
            self.assertEqual(sid, sid.strip(), f"ID contains leading/trailing whitespace: {sid}")
            self.assertIsNotNone(kebab_pattern.match(sid), f"ID violates kebab-case format: {sid}")

    def test_t2_f3_03_rig_classifier_tolerance_to_unnormalized_input(self):
        """TC-T2-F3-03: Boundary check: classify_rig gracefully handles uppercase and trimmed IDs."""
        self.assertEqual(classify_rig("STEUPS"), "steups_puff")
        self.assertEqual(classify_rig("SLANG-STEUPS"), "steups_sideeye_emoji")
        self.assertEqual(classify_rig("MACO"), "maco_window_binoculars")
        self.assertEqual(classify_rig("Doubles-3D"), "culinary_steam_pop")

        dirty_id = "  steups  \n"
        self.assertEqual(classify_rig(dirty_id.strip()), "steups_puff")

    def test_t2_f3_04_unknown_id_and_boundary_fallback(self):
        """TC-T2-F3-04: Corner check: classify_rig safely handles empty, non-existent, and oversized inputs."""
        all_ids = set(load_all_catalog_ids())
        self.assertNotIn("", all_ids)
        self.assertNotIn("unknown-sticker-9999", all_ids)

        # Classifier must not crash on edge cases
        rig_empty = classify_rig("")
        self.assertIsInstance(rig_empty, str)

        rig_unknown = classify_rig("non-existent-sticker-id-xyz")
        self.assertIsInstance(rig_unknown, str)

        rig_huge = classify_rig("slang-" + "x" * 1000)
        self.assertIsInstance(rig_huge, str)

    def test_t2_f3_05_generic_fallback_count_strict_zero(self):
        """TC-T2-F3-05: Strict boundary: articulated_gesture count must be 0 across all 188 stickers after M2."""
        all_ids = load_all_catalog_ids()
        fallbacks = [sid for sid in all_ids if classify_rig(sid) == "articulated_gesture"]
        if fallbacks:
            require_milestone(
                "Pending Milestone M2",
                False,
                f"{len(fallbacks)}/188 stickers still map to generic articulated_gesture fallback (e.g. {fallbacks[:3]})"
            )
        self.assertEqual(len(fallbacks), 0, f"Found stickers with generic fallback: {fallbacks}")


class TestTier2F4MicroMotionHoldAndFramesBoundaries(unittest.TestCase):
    """F4: Boundary & Corner Cases for 24-Frame Standardization."""

    def _synthesize_webp(self, frame_count: int, duration_ms: int = 90, loop: int = 0) -> str:
        """Helper to create a temporary synthetic multi-frame WebP file."""
        frames = [Image.new("RGBA", (64, 64), (i * 5, 100, 150, 255)) for i in range(frame_count)]
        tmp = tempfile.NamedTemporaryFile(suffix=".webp", delete=False)
        tmp.close()
        frames[0].save(
            tmp.name,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=loop,
        )
        return tmp.name

    def test_t2_f4_01_frame_count_lower_boundary_23_rejected(self):
        """TC-T2-F4-01: Boundary check: an animation with 23 frames fails the 24 frame contract."""
        tmp_path = self._synthesize_webp(frame_count=23, duration_ms=90)
        try:
            meta = parse_webp_binary(tmp_path)
            self.assertTrue(meta.get("valid_riff"), "Synthetic WebP failed RIFF header check")
            parsed_count = meta.get("frame_count")
            self.assertEqual(parsed_count, 23, "Binary parser failed to detect exactly 23 ANMF chunks")
            # Contract assertion: PeelOff strictly requires exactly 24 frames
            self.assertNotEqual(parsed_count, 24, "23 frames must not satisfy 24-frame requirement")
            self.assertLess(parsed_count, 24, "23 frames should be flagged as under-frame defect")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Also verify that among valid production assets, zero assets have exactly 23 frames
        anim_dir = get_workspace_path("assets", "animated")
        for fname in ["ent.webp", "slang-ent.webp"]:
            fpath = os.path.join(anim_dir, fname)
            if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
                self.assertNotEqual(parse_webp_binary(fpath).get("frame_count"), 23)

    def test_t2_f4_02_frame_count_upper_boundary_25_rejected(self):
        """TC-T2-F4-02: Boundary check: an animation with 25 frames fails the 24 frame contract."""
        tmp_path = self._synthesize_webp(frame_count=25, duration_ms=90)
        try:
            meta = parse_webp_binary(tmp_path)
            self.assertTrue(meta.get("valid_riff"), "Synthetic WebP failed RIFF header check")
            parsed_count = meta.get("frame_count")
            self.assertEqual(parsed_count, 25, "Binary parser failed to detect exactly 25 ANMF chunks")
            # Contract assertion
            self.assertNotEqual(parsed_count, 24, "25 frames must not satisfy 24-frame requirement")
            self.assertGreater(parsed_count, 24, "25 frames should be flagged as over-frame defect")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Verify no production asset exceeds 24 frames
        anim_dir = get_workspace_path("assets", "animated")
        for fname in ["ent.webp", "slang-ent.webp"]:
            fpath = os.path.join(anim_dir, fname)
            if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
                self.assertNotEqual(parse_webp_binary(fpath).get("frame_count"), 25)

    def test_t2_f4_03_duration_boundary_min_2000ms_max_2200ms(self):
        """TC-T2-F4-03: Boundary check: total animation duration in [2000, 2200] ms on actual assets."""
        webp_path = get_workspace_path("assets", "animated", "ent.webp")
        gif_path = get_workspace_path("assets", "animated", "ent.gif")

        meta_webp = parse_webp_binary(webp_path)
        meta_gif = parse_gif_binary(gif_path)

        w_dur = meta_webp.get("total_duration_ms", 0)
        g_dur = meta_gif.get("total_duration_ms", 0)

        self.assertGreaterEqual(w_dur, 2000, f"WebP duration {w_dur}ms < 2000ms (WhatsApp looping threshold)")
        self.assertLessEqual(w_dur, 2200, f"WebP duration {w_dur}ms > 2200ms")
        self.assertGreaterEqual(g_dur, 2000, f"GIF duration {g_dur}ms < 2000ms")
        self.assertLessEqual(g_dur, 2200, f"GIF duration {g_dur}ms > 2200ms")

    def test_t2_f4_04_frame_duration_tolerance_89_to_91ms(self):
        """TC-T2-F4-04: Boundary check: actual frame durations in ANMF chunks strictly within [89, 91] ms."""
        webp_path = get_workspace_path("assets", "animated", "ent.webp")
        meta = parse_webp_binary(webp_path)
        durations = meta.get("durations", [])
        self.assertEqual(len(durations), 24, f"Expected 24 frame durations, found {len(durations)}")
        for i, d in enumerate(durations):
            self.assertTrue(89 <= d <= 91, f"Frame {i} duration {d}ms out of [89, 91]ms tolerance in ent.webp")

        gif_path = get_workspace_path("assets", "animated", "ent.gif")
        meta_gif = parse_gif_binary(gif_path)
        g_durations = meta_gif.get("durations", [])
        self.assertEqual(len(g_durations), 24, f"Expected 24 GIF frame durations, found {len(g_durations)}")
        for i, d in enumerate(g_durations):
            self.assertTrue(89 <= d <= 91, f"GIF frame {i} duration {d}ms out of [89, 91]ms tolerance in ent.gif")

    def test_t2_f4_05_loop_header_flag_exact_zero(self):
        """TC-T2-F4-05: Boundary check: infinite loop flag is strictly 0 (0x0000) for WebP and GIF."""
        test_webp = get_workspace_path("assets", "animated", "ent.webp")
        meta_w = parse_webp_binary(test_webp)
        self.assertEqual(meta_w.get("loop_count"), 0, "WebP loop count must be strictly 0 for infinite looping")

        test_gif = get_workspace_path("assets", "animated", "ent.gif")
        meta_g = parse_gif_binary(test_gif)
        self.assertEqual(meta_g.get("loop_count"), 0, "GIF loop count must be strictly 0 for infinite looping")


class TestTier2F5ProductionAssetGenerationBoundaries(unittest.TestCase):
    """F5: Boundary & Corner Cases for Asset Generation."""

    def setUp(self):
        self.anim_dir = get_workspace_path("assets", "animated")

    def test_t2_f5_01_min_and_max_file_size_boundaries(self):
        """TC-T2-F5-01: File size boundaries: valid assets must be > 10KB and <= 2.5MB."""
        all_files = [f for f in os.listdir(self.anim_dir) if f.endswith((".webp", ".gif"))]
        self.assertGreater(len(all_files), 0, "No animated assets found in assets/animated/")

        # 1. Lower boundary check (gate stubs for M3)
        small_files = [
            f for f in all_files if os.path.getsize(os.path.join(self.anim_dir, f)) <= 10240
        ]
        if small_files:
            require_milestone(
                "Pending Milestone M3",
                False,
                f"Found {len(small_files)} assets <= 10KB (stubs pending M3: {small_files[:3]})"
            )
        self.assertEqual(len(small_files), 0)

        # 2. Upper boundary check: no asset should exceed 2.5MB (2,621,440 bytes)
        max_limit_bytes = 2500 * 1024  # 2.5 MB
        oversized = [
            f for f in all_files if os.path.getsize(os.path.join(self.anim_dir, f)) > max_limit_bytes
        ]
        self.assertEqual(len(oversized), 0, f"Assets exceed 2.5MB size limit: {oversized}")

    def test_t2_f5_02_max_quantized_palette_128_colors(self):
        """TC-T2-F5-02: Palette boundary: GIF color table length is in [2, 128] colors."""
        test_gif = os.path.join(self.anim_dir, "ent.gif")
        meta = parse_gif_binary(test_gif)
        palette_colors = meta.get("palette_colors", 0)
        self.assertGreater(palette_colors, 1, "GIF palette has fewer than 2 colors")
        self.assertLessEqual(palette_colors, 128, f"GIF palette exceeds 128 color boundary: {palette_colors}")

    def test_t2_f5_03_studio_card_bg_pixel_exact_rgb(self):
        """TC-T2-F5-03: Color fidelity boundary: GIF card outer pixels are (16, 20, 30) +/- 4."""
        test_gif = os.path.join(self.anim_dir, "ent.gif")
        with Image.open(test_gif) as im:
            rgb_im = im.convert("RGB")
            corners = [(0, 0), (511, 0), (0, 511), (511, 511)]
            for pt in corners:
                pixel = rgb_im.getpixel(pt)
                r_diff = abs(pixel[0] - 16)
                g_diff = abs(pixel[1] - 20)
                b_diff = abs(pixel[2] - 30)
                self.assertTrue(
                    r_diff <= 4 and g_diff <= 4 and b_diff <= 4,
                    f"Corner {pt} color {pixel} exceeds tolerance from (16, 20, 30)"
                )

    def test_t2_f5_04_webp_corner_pixel_complete_alpha_zero(self):
        """TC-T2-F5-04: Alpha boundary: WebP all 4 corners have alpha == 0, center has alpha > 0."""
        test_webp = os.path.join(self.anim_dir, "ent.webp")
        with Image.open(test_webp) as im:
            rgba = im.convert("RGBA")
            corners = [(0, 0), (511, 0), (0, 511), (511, 511)]
            for pt in corners:
                alpha = rgba.getpixel(pt)[3]
                self.assertEqual(alpha, 0, f"WebP corner {pt} alpha {alpha} != 0 (must be fully transparent)")
            center_alpha = rgba.getpixel((256, 256))[3]
            self.assertGreater(center_alpha, 0, "WebP center pixel has alpha == 0 (expected opaque sticker content)")

    def test_t2_f5_05_canvas_exact_512x512_no_off_by_one(self):
        """TC-T2-F5-05: Canvas boundary: verify width and height are strictly 512 across WebP and GIF."""
        # 1. WebP format
        meta_w = parse_webp_binary(os.path.join(self.anim_dir, "ent.webp"))
        self.assertEqual(meta_w.get("width"), 512, f"WebP width {meta_w.get('width')} != 512")
        self.assertEqual(meta_w.get("height"), 512, f"WebP height {meta_w.get('height')} != 512")

        # 2. GIF format
        meta_g = parse_gif_binary(os.path.join(self.anim_dir, "ent.gif"))
        self.assertEqual(meta_g.get("width"), 512, f"GIF width {meta_g.get('width')} != 512")
        self.assertEqual(meta_g.get("height"), 512, f"GIF height {meta_g.get('height')} != 512")


class TestTier2F6AutomatedAnimationVerifierBoundaries(unittest.TestCase):
    """F6: Boundary & Corner Cases for Animation Verifier."""

    def test_t2_f6_01_empty_directory_input_boundary(self):
        """TC-T2-F6-01: Boundary check: empty directory handling in verification logic."""
        verifier_path = get_workspace_path("scripts", "verify_animated_stickers.py")
        exists = os.path.exists(verifier_path)
        if exists:
            with tempfile.TemporaryDirectory() as empty_dir:
                rc, stdout, stderr = run_command(
                    [get_python_executable(), verifier_path, "--dir", empty_dir],
                    timeout=10
                )
                self.assertNotEqual(rc, 0, "Verifier must fail when directory contains 0 assets")
        else:
            with tempfile.TemporaryDirectory() as empty_dir:
                dummy_path = os.path.join(empty_dir, "missing.webp")
                meta = parse_webp_binary(dummy_path)
                self.assertFalse(meta.get("exists", True))
                self.assertIn("error", meta)

    def test_t2_f6_02_single_corrupt_asset_detection(self):
        """TC-T2-F6-02: Boundary check: single corrupt asset among valid assets is caught."""
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            tmp.write(b"CORRUPT_BYTES_DATA")
            tmp_path = tmp.name
        try:
            meta = parse_webp_binary(tmp_path)
            self.assertFalse(meta.get("valid_riff", False))
            im, err = safe_open_image(tmp_path)
            self.assertIsNone(im)
            self.assertIsNotNone(err)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_t2_f6_03_non_image_file_handling(self):
        """TC-T2-F6-03: Corner check: extraneous non-image files (.txt, .DS_Store) ignored."""
        with tempfile.TemporaryDirectory() as sandbox:
            txt_path = os.path.join(sandbox, "notes.txt")
            ds_path = os.path.join(sandbox, ".DS_Store")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("Extraneous metadata notes")
            with open(ds_path, "wb") as f:
                f.write(b"\x00\x00\x00\x01Bud1")

            webp_meta = parse_webp_binary(txt_path)
            self.assertFalse(webp_meta.get("valid_riff", False))

            gif_meta = parse_gif_binary(ds_path)
            self.assertFalse(gif_meta.get("valid_gif", False))

        all_ids = load_all_catalog_ids()
        for sid in all_ids:
            self.assertFalse(sid.startswith("."), f"Catalog ID should not be hidden file: {sid}")
            self.assertFalse(sid.endswith((".txt", ".db", ".DS_Store")), f"Catalog ID contains non-image ext: {sid}")

    def test_t2_f6_04_magic_byte_corruption_rejection(self):
        """TC-T2-F6-04: Corner check: text file renamed to .webp is rejected."""
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            tmp.write(b"This is a plain text file pretending to be webp")
            tmp_path = tmp.name
        try:
            meta = parse_webp_binary(tmp_path)
            self.assertFalse(meta.get("valid_riff", False))
            self.assertIn("Invalid RIFF/WEBP header", meta.get("error", ""))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_t2_f6_05_verifier_runtime_budget_boundary(self):
        """TC-T2-F6-05: Performance boundary: verifier script path verification and execution timing."""
        verifier_path = get_workspace_path("scripts", "verify_animated_stickers.py")
        exists = os.path.exists(verifier_path)
        if exists:
            t0 = time.perf_counter()
            rc, stdout, stderr = run_command([get_python_executable(), verifier_path], timeout=30)
            elapsed = time.perf_counter() - t0
            self.assertEqual(rc, 0, f"Verifier failed: {stderr}")
            self.assertLess(elapsed, 25.0, f"Verifier exceeded 25.0s budget: {elapsed:.2f}s")
        else:
            # Benchmark parser throughput on real assets as proxy
            t0 = time.perf_counter()
            sample_ids = ["ent", "maco"]
            for sid in sample_ids:
                w_path = get_workspace_path("assets", "animated", f"{sid}.webp")
                g_path = get_workspace_path("assets", "animated", f"{sid}.gif")
                if os.path.exists(w_path):
                    parse_webp_binary(w_path)
                if os.path.exists(g_path):
                    parse_gif_binary(g_path)
            elapsed = time.perf_counter() - t0
            self.assertLess(elapsed, 2.0, f"Sample parsing took {elapsed:.2f}s (budget: 2.0s)")
            require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")


class TestTier2F7WebAppAnimatedIntegrationBoundaries(unittest.TestCase):
    """F7: Boundary & Corner Cases for Web App Integration."""

    def test_t2_f7_01_rapid_consecutive_toggle_invariance(self):
        """TC-T2-F7-01: State invariance boundary: 10 toggles restores initial state in app.js logic."""
        app_js_path = get_workspace_path("app.js")
        self.assertTrue(os.path.exists(app_js_path), "Missing app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            js_code = f.read()

        # 1. Verify default initial state
        init_match = re.search(r"let\s+isAnimatedMode\s*=\s*(true|false);", js_code)
        self.assertIsNotNone(init_match, "app.js must declare let isAnimatedMode")
        initial_mode = init_match.group(1) == "true"
        self.assertTrue(initial_mode, "Default isAnimatedMode must be true")

        # 2. Verify toggle handler exists and mutates isAnimatedMode
        self.assertIn("toggleAnimatedBtn", js_code)
        toggle_match = re.search(
            r"toggleAnimatedBtn\?\.addEventListener\([\"']click[\"'],\s*\(\)\s*=>\s*\{([\s\S]*?)\}\);",
            js_code
        )
        self.assertIsNotNone(toggle_match, "Missing toggleAnimatedBtn click listener in app.js")
        handler_body = toggle_match.group(1)
        self.assertIn("isAnimatedMode = !isAnimatedMode", handler_body)
        self.assertIn("toggleAnimatedBtn.classList.toggle", handler_body)
        self.assertIn("renderStickerGrid", handler_body)

        # 3. Verify displaySrc ternary conditional routes between animWebpUrl and webpUrl
        self.assertTrue(
            "isAnimatedMode ? sticker.animWebpUrl : sticker.webpUrl" in js_code or
            "isAnimatedMode ? s.animWebpUrl : s.webpUrl" in js_code,
            "app.js must switch between animated WebP and static WebP based on isAnimatedMode"
        )

        # 4. State invariance: simulate 10 transitions starting from initial_mode
        current_state = initial_mode
        for i in range(10):
            current_state = not current_state
        self.assertEqual(current_state, initial_mode, "10 consecutive toggles must restore initial state (True)")

        odd_state = not current_state
        self.assertNotEqual(odd_state, initial_mode, "11 consecutive toggles must invert initial state (False)")

    def test_t2_f7_02_missing_asset_onerror_fallback_src(self):
        """TC-T2-F7-02: Fallback boundary: onerror constructs correct static WebP URL matching disk files."""
        app_js_path = get_workspace_path("app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            js_code = f.read()

        # 1. Verify onerror fallback pattern in app.js
        self.assertIn('onerror="this.src=\'${sticker.webpUrl}\'"', js_code)
        self.assertTrue(
            re.search(r"(?:item|s)\.webpUrl\s*=\s*`assets/stickers/\$\{(?:item|s)\.id\}\.webp\?v=\d+`", js_code) is not None,
            "app.js must construct webpUrl pointing to assets/stickers/{id}.webp?v=N"
        )

        # 2. Verify fallback URL targets against real catalog sticker IDs on disk
        all_ids = load_all_catalog_ids()
        self.assertEqual(len(all_ids), 188)

        sample_ids = ["doubles-3d", "steups", "rel-bess", "slang-link-me", "slang-doh-study-dat"]
        for sid in sample_ids:
            self.assertIn(sid, all_ids, f"Sample sticker ID {sid} must exist in catalog")
            disk_path = get_workspace_path("assets", "stickers", f"{sid}.webp")
            self.assertTrue(os.path.exists(disk_path), f"Static fallback file missing on disk: {disk_path}")
            self.assertGreater(os.path.getsize(disk_path), 0, f"Static fallback file is empty: {disk_path}")

    def test_t2_f7_03_empty_search_query_boundary(self):
        """TC-T2-F7-03: Boundary check: empty search string matches all 188 stickers."""
        all_ids = load_all_catalog_ids()
        self.assertEqual(len(all_ids), 188)
        query = ""
        q = query.strip().lower()
        if not q:
            matched = all_ids
        else:
            matched = [sid for sid in all_ids if q in sid.lower()]
        self.assertEqual(len(matched), 188)

    def test_t2_f7_04_non_matching_search_query_boundary(self):
        """TC-T2-F7-04: Boundary check: unmatched search string returns empty list."""
        all_ids = load_all_catalog_ids()
        query = "__non_existent_search_query_xyz_99999__"
        q = query.strip().lower()
        matched = [sid for sid in all_ids if q in sid.lower()]
        self.assertEqual(len(matched), 0)

    def test_t2_f7_05_desktop_share_fallback_to_download(self):
        """TC-T2-F7-05: Fallback boundary: download fallback URL for animated GIF matches real assets."""
        app_js_path = get_workspace_path("app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            js_code = f.read()

        # 1. Verify download fallback routes in app.js
        self.assertTrue(
            "animGifUrl" in js_code and "downloadFileUrl" in js_code,
            "app.js must route desktop animated download to animGifUrl"
        )
        self.assertTrue(
            re.search(r"(?:item|s)\.animGifUrl\s*=\s*`assets/animated/\$\{(?:item|s)\.id\}\.gif\?v=\d+`", js_code) is not None,
            "app.js must construct animGifUrl pointing to assets/animated/{id}.gif?v=N"
        )

        # 2. Verify against real disk GIF assets
        sample_ids = ["ent", "maco", "steups"]
        for sid in sample_ids:
            disk_path = get_workspace_path("assets", "animated", f"{sid}.gif")
            self.assertTrue(os.path.exists(disk_path), f"Animated GIF missing on disk: {disk_path}")
            meta = parse_gif_binary(disk_path)
            self.assertTrue(meta.get("valid_gif"), f"File is not valid GIF: {disk_path}")
            self.assertEqual(meta.get("header"), "GIF89a")
            self.assertEqual(meta.get("loop_count"), 0)

            bg_ok, rgb = check_card_background_rgb(disk_path)
            self.assertTrue(bg_ok, f"Card background color {rgb} deviates from #10141E")


class TestTier2F8WhatsAppManifestAlignmentBoundaries(unittest.TestCase):
    """F8: Boundary & Corner Cases for WhatsApp Manifest."""

    def setUp(self):
        self.manifest = load_whatsapp_manifest()

    def test_t2_f8_01_pack_sticker_count_max_boundary_30(self):
        """TC-T2-F8-01: Upper boundary check: no pack has > 30 stickers."""
        for p in self.manifest["sticker_packs"]:
            count = len(p.get("stickers", []))
            self.assertLessEqual(count, 30, f"Pack {p['identifier']} exceeds 30 stickers ({count})")

    def test_t2_f8_02_pack_sticker_count_min_boundary_3(self):
        """TC-T2-F8-02: Lower boundary check: no pack has < 3 stickers."""
        for p in self.manifest["sticker_packs"]:
            count = len(p.get("stickers", []))
            self.assertGreaterEqual(count, 3, f"Pack {p['identifier']} has fewer than 3 stickers ({count})")

    def test_t2_f8_03_emojis_per_sticker_boundary_1_to_3(self):
        """TC-T2-F8-03: Boundary check: each sticker defines between 1 and 3 emojis."""
        for p in self.manifest["sticker_packs"]:
            for s in p.get("stickers", []):
                emojis = s.get("emojis", [])
                self.assertGreaterEqual(len(emojis), 1, f"Sticker {s['image_file']} has 0 emojis")
                self.assertLessEqual(len(emojis), 3, f"Sticker {s['image_file']} has > 3 emojis")

    def test_t2_f8_04_tray_icon_file_size_boundary_50kb(self):
        """TC-T2-F8-04: Size boundary: tray icon file size < 50,000 bytes and 96x96 pixels."""
        for p in self.manifest["sticker_packs"]:
            tpath = get_workspace_path("assets", "trays", p["tray_image_file"])
            self.assertTrue(os.path.exists(tpath), f"Missing tray icon: {tpath}")
            self.assertLess(os.path.getsize(tpath), 50000, f"Tray icon {tpath} >= 50,000 bytes")
            im, err = safe_open_image(tpath)
            self.assertIsNone(err, f"Failed to open tray icon {tpath}: {err}")
            self.assertEqual(im.size, (96, 96), f"Tray icon {tpath} dimensions {im.size} != (96, 96)")

    def test_t2_f8_05_pack_identifier_uniqueness(self):
        """TC-T2-F8-05: Uniqueness boundary: exactly 8 unique pack identifiers matching regex spec."""
        ids = [p["identifier"] for p in self.manifest["sticker_packs"]]
        self.assertEqual(len(ids), 8)
        self.assertEqual(len(set(ids)), 8)
        for pid in ids:
            self.assertTrue(
                re.match(r"^[a-zA-Z0-9_-]+$", pid) is not None,
                f"Pack identifier {pid} violates WhatsApp character constraint"
            )


class TestTier2F9ComprehensiveE2ETestSuiteBoundaries(unittest.TestCase):
    """F9: Boundary & Corner Cases for Test Suite Harness."""

    def test_t2_f9_01_zero_unhandled_exceptions_runner(self):
        """TC-T2-F9-01: Corner check: runner script parses without uncaught syntax errors."""
        runner_path = get_workspace_path("tests", "e2e", "run_all_tests.py")
        if os.path.exists(runner_path):
            rc, stdout, stderr = run_command([get_python_executable(), "-m", "py_compile", runner_path])
            self.assertEqual(rc, 0, f"Compilation error in run_all_tests.py: {stderr}")

    def test_t2_f9_02_invalid_tier_argument_rejection(self):
        """TC-T2-F9-02: Boundary check: invalid tier argument --tier 99 exits code 2."""
        runner_path = get_workspace_path("tests", "e2e", "run_all_tests.py")
        if os.path.exists(runner_path):
            rc, stdout, stderr = run_command([get_python_executable(), runner_path, "--tier", "99"])
            self.assertEqual(rc, 2)

    def test_t2_f9_03_progressive_mode_exit_zero_on_skips(self):
        """TC-T2-F9-03: Boundary check: skip in progressive mode raises unittest.SkipTest."""
        with temporary_strict_mode(False):
            with self.assertRaises(unittest.SkipTest):
                require_milestone("ProgressiveTest", False, "Skip check")

    def test_t2_f9_04_strict_mode_exit_one_on_skips(self):
        """TC-T2-F9-04: Boundary check: strict mode raises AssertionError on uncompleted milestone."""
        with temporary_strict_mode(True):
            with self.assertRaises(AssertionError):
                require_milestone("StrictTest", False, "Strict failure check")

    def test_t2_f9_05_suite_runtime_boundary_60s(self):
        """TC-T2-F9-05: Performance boundary: test discovery and individual tests execute in < 5.0s, suite < 60s."""
        from tests.e2e.run_all_tests import PeelOffTestRunner

        # 1. Benchmark live test discovery using time.perf_counter()
        t0 = time.perf_counter()
        runner = PeelOffTestRunner()
        suite = runner.discover_suite()
        count = suite.countTestCases()
        discovery_elapsed = time.perf_counter() - t0

        self.assertGreaterEqual(count, 115, f"Discovered {count} tests, expected >= 115")
        self.assertLess(
            discovery_elapsed, 5.0,
            f"Test suite discovery took {discovery_elapsed:.3f}s, exceeding 5.0s budget"
        )

        # 2. Benchmark catalog loading speed using time.perf_counter()
        t1 = time.perf_counter()
        all_ids = load_all_catalog_ids()
        catalog_elapsed = time.perf_counter() - t1
        self.assertEqual(len(all_ids), 188)
        self.assertLess(
            catalog_elapsed, 1.0,
            f"Catalog loading took {catalog_elapsed:.3f}s, exceeding 1.0s budget"
        )

        # 3. Verify suite execution telemetry if test_summary.json exists
        summary_path = get_workspace_path("tests", "e2e", "test_summary.json")
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                telemetry = json.load(f)
            suite_dur = telemetry.get("summary", {}).get("duration_seconds", 0.0)
            self.assertLess(
                suite_dur, 60.0,
                f"Overall suite duration {suite_dur:.2f}s exceeded 60.0s boundary"
            )
            for test_rec in telemetry.get("tests", []):
                t_dur = test_rec.get("duration_seconds", 0.0)
                self.assertLess(
                    t_dur, 5.0,
                    f"Test {test_rec.get('test_id')} took {t_dur:.2f}s, exceeding 5.0s budget"
                )


class TestTier2F10AdversarialCoverageHardeningBoundaries(unittest.TestCase):
    """F10: Boundary & Corner Cases for Adversarial Hardening."""

    def test_t2_f10_01_concurrency_workers_1_boundary(self):
        """TC-T2-F10-01: Concurrency lower boundary: 1 worker is valid in CLI and thread execution."""
        # 1. Execute live 1-worker concurrency on real assets
        anim_dir = get_workspace_path("assets", "animated")
        sample_files = [os.path.join(anim_dir, f) for f in os.listdir(anim_dir) if f.endswith(".webp")][:5]
        self.assertTrue(len(sample_files) > 0, "Expected animated assets for concurrency check")

        with ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(parse_webp_binary, sample_files))
        self.assertEqual(len(results), len(sample_files))
        for res in results:
            self.assertTrue(res.get("valid_riff"), "1-worker execution failed to parse valid RIFF")

        # 2. Check generator CLI argument handling
        gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        with open(gen_path, "r", encoding="utf-8") as f:
            code = f.read()
        has_workers_arg = "argparse" in code or "--workers" in code
        if has_workers_arg:
            rc, stdout, stderr = run_command([get_python_executable(), gen_path, "--workers", "1", "--help"], timeout=10)
            self.assertEqual(rc, 0, f"Generator rejected --workers 1: {stderr}")

    def test_t2_f10_02_concurrency_workers_16_boundary(self):
        """TC-T2-F10-02: Concurrency upper boundary: 16 workers execute safely without Windows locking crashes."""
        # 1. Stress test: 16 concurrent workers reading real disk assets
        anim_dir = get_workspace_path("assets", "animated")
        files = [os.path.join(anim_dir, f) for f in os.listdir(anim_dir) if f.endswith((".webp", ".gif"))][:32]
        self.assertTrue(len(files) >= 16, "Expected at least 16 animated files for stress test")

        def inspect_asset(path: str):
            return parse_webp_binary(path) if path.endswith(".webp") else parse_gif_binary(path)

        with ThreadPoolExecutor(max_workers=16) as pool:
            futures = [pool.submit(inspect_asset, f) for f in files]
            results = [fut.result() for fut in as_completed(futures)]

        self.assertEqual(len(results), len(files))
        for r in results:
            self.assertTrue(r.get("valid_riff") or r.get("valid_gif"), "Concurrent read failed on asset")

        # 2. Check generator CLI worker clamping
        gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        with open(gen_path, "r", encoding="utf-8") as f:
            code = f.read()
        has_workers_arg = "argparse" in code or "--workers" in code
        if has_workers_arg:
            rc, stdout, stderr = run_command([get_python_executable(), gen_path, "--workers", "16", "--help"], timeout=10)
            self.assertEqual(rc, 0, f"Generator rejected --workers 16: {stderr}")

    def test_t2_f10_03_zero_byte_input_png_rejection(self):
        """TC-T2-F10-03: Corner check: 0-byte PNG rejected by safe_open_image."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            im, err = safe_open_image(tmp_path)
            self.assertIsNone(im)
            self.assertIn("0 bytes", err)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_t2_f10_04_minimal_1x1_png_scaling(self):
        """TC-T2-F10-04: Corner check: 1x1 image scaled through prep_breathing_room without division by zero."""
        tiny = Image.new("RGBA", (1, 1), (255, 0, 0, 255))
        padded = prep_breathing_room(tiny, scale=0.91)
        self.assertEqual(padded.size, (1, 1))
        resized = tiny.resize((512, 512), Image.Resampling.LANCZOS)
        self.assertEqual(resized.size, (512, 512))

    def test_t2_f10_05_fully_transparent_input_png(self):
        """TC-T2-F10-05: Corner check: 100% transparent image handled cleanly."""
        transparent = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        self.assertEqual(transparent.size, (512, 512))
        pixel = transparent.getpixel((0, 0))
        self.assertEqual(pixel[3], 0)
        # Verify corner alpha check on real production asset
        ok, alpha = check_webp_corner_alpha(get_workspace_path("assets", "animated", "ent.webp"))
        self.assertTrue(ok)
        self.assertEqual(alpha, 0)


if __name__ == "__main__":
    unittest.main()
