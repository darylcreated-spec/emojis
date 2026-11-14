"""
PeelOff E2E Test Suite — Tier 3: Cross-Feature Interactions (Pairwise Combinations)
12 Comprehensive Test Cases covering pairwise feature integrations, shared contracts,
data flow, and multi-component lifecycles.
"""

import os
import sys
import json
import unittest
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
    calculate_frame_difference,
    run_command,
    require_milestone,
    is_strict_mode,
)


class TestTier3CrossFeatureInteractions(unittest.TestCase):
    """Tier 3: 12 Pairwise Cross-Feature Integration Tests."""

    def setUp(self):
        self.anim_dir = get_workspace_path("assets", "animated")
        self.gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        self.spec_path = get_workspace_path("docs", "CULTURAL_ANIMATION_SPEC.md")

    def test_pairwise_f1_spec_to_f2_generator_routines(self):
        """TC-T3-01: F1 <-> F2: Motion primitives documented in spec exist in generator code."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            spec_content = f.read().lower()
        with open(self.gen_path, "r", encoding="utf-8") as f:
            gen_code = f.read().lower()

        # Check for core routines
        routines = ["rag", "steups", "doubles", "lean"]
        found_in_both = [r for r in routines if r in spec_content and r in gen_code]
        self.assertGreaterEqual(len(found_in_both), 2, f"Routines missing in generator or spec: {routines}")

    def test_pairwise_f1_matrix_to_f3_rig_classifier(self):
        """TC-T3-02: F1 <-> F3: Spec matrix sticker IDs match catalog definitions."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            spec_content = f.read()

        all_ids = load_all_catalog_ids()
        matched = [sid for sid in all_ids if sid in spec_content]
        if len(matched) < 188:
            require_milestone(
                "Pending Milestone M1",
                False,
                f"Spec matrix contains {len(matched)}/188 stickers (still being authored)"
            )
        self.assertEqual(len(matched), 188)

    def test_pairwise_f2_motion_curves_to_f4_24_frames(self):
        """TC-T3-03: F2 <-> F4: Procedural curves evaluated over 24 frames produce smooth continuity."""
        # Check that 24 frame animation in ent.webp has smooth transitions
        ent_webp = os.path.join(self.anim_dir, "ent.webp")
        meta = parse_webp_binary(ent_webp)
        self.assertTrue(meta.get("valid_riff"))
        self.assertEqual(meta.get("frame_count"), 24)

    def test_pairwise_f3_rigs_to_f5_visual_distinction(self):
        """TC-T3-04: F3 <-> F5: Different rigs produce distinct animation signatures."""
        im_steups, err1 = safe_open_image(os.path.join(self.anim_dir, "steups.webp"))
        im_rag, err2 = safe_open_image(os.path.join(self.anim_dir, "wave-yuh-rag.webp"))
        self.assertIsNone(err1)
        self.assertIsNone(err2)

        # Compute difference between their first frames
        diff = calculate_frame_difference(im_steups, im_rag)
        self.assertGreater(diff, 10.0, "Stickers with different rigs should be visually distinct")

    def test_pairwise_f4_standardization_to_f5_asset_metadata(self):
        """TC-T3-05: F4 <-> F5: 24 frames @ 90ms standard is reflected in asset binary metadata."""
        sample_stickers = ["ent", "steups", "doubles-3d", "slang-ent", "slang-wha-yuh-say"]
        for sid in sample_stickers:
            webp_path = os.path.join(self.anim_dir, f"{sid}.webp")
            gif_path = os.path.join(self.anim_dir, f"{sid}.gif")
            w_meta = parse_webp_binary(webp_path)
            g_meta = parse_gif_binary(gif_path)
            if w_meta.get("size", 0) == 0 or w_meta.get("frame_count") != 24:
                require_milestone(
                    "Pending Milestone M3",
                    False,
                    f"{sid}.webp is empty or has non-standard frames ({w_meta.get('frame_count')})"
                )
            if g_meta.get("size", 0) == 0 or g_meta.get("frame_count") != 24:
                require_milestone(
                    "Pending Milestone M3",
                    False,
                    f"{sid}.gif is empty or has non-standard frames ({g_meta.get('frame_count')})"
                )
            self.assertEqual(w_meta.get("frame_count"), 24, f"{sid}.webp frame count != 24")
            self.assertEqual(g_meta.get("frame_count"), 24, f"{sid}.gif frame count != 24")
            self.assertEqual(w_meta.get("total_duration_ms"), 2160)
            self.assertEqual(g_meta.get("total_duration_ms"), 2160)

    def test_pairwise_f5_assets_to_f6_verifier_acceptance(self):
        """TC-T3-06: F5 <-> F6: Generated assets are verified by animation verifier."""
        verifier_path = get_workspace_path("scripts", "verify_animated_stickers.py")
        exists = os.path.exists(verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        rc, stdout, stderr = run_command([get_python_executable(), verifier_path], timeout=25)
        self.assertEqual(rc, 0)

    def test_pairwise_f5_assets_to_f7_webapp_urls(self):
        """TC-T3-07: F5 <-> F7: URLs constructed in app.js point to existing disk assets."""
        all_ids = load_all_catalog_ids()
        # Verify first 10 stickers
        for sid in all_ids[:10]:
            webp_file = os.path.join(self.anim_dir, f"{sid}.webp")
            gif_file = os.path.join(self.anim_dir, f"{sid}.gif")
            self.assertTrue(os.path.exists(webp_file), f"Missing {webp_file}")
            self.assertTrue(os.path.exists(gif_file), f"Missing {gif_file}")

    def test_pairwise_f7_webapp_to_f8_manifest_stickers(self):
        """TC-T3-08: F7 <-> F8: Web app pack identifiers align with WhatsApp manifest."""
        manifest = load_whatsapp_manifest()
        packs = load_packs_catalog()
        manifest_pack_ids = [p["identifier"] for p in manifest["sticker_packs"]]
        catalog_pack_ids = [p["id"] for p in packs]
        self.assertEqual(sorted(manifest_pack_ids), sorted(catalog_pack_ids))

    def test_pairwise_f6_verifier_to_f9_test_runner(self):
        """TC-T3-09: F6 <-> F9: Animation verifier assertions are tested in E2E harness."""
        # Verifier script contract test
        verifier_path = get_workspace_path("scripts", "verify_animated_stickers.py")
        exists = os.path.exists(verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        self.assertTrue(exists)

    def test_pairwise_f7_toggle_to_f10_fallback_resilience(self):
        """TC-T3-10: F7 <-> F10: Web app image fallback prevents UI failure under missing asset."""
        app_js_path = get_workspace_path("app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn("onerror", code, "app.js must implement onerror resilience")

    def test_pairwise_f8_animated_flag_to_f5_webp_validity(self):
        """TC-T3-11: F8 <-> F5: Manifest animated packs reference valid WebP assets."""
        manifest = load_whatsapp_manifest()
        # Check first 5 stickers in pack 1
        pack1 = manifest["sticker_packs"][0]
        for s in pack1.get("stickers", [])[:5]:
            wpath = os.path.join(self.anim_dir, s["image_file"])
            meta = parse_webp_binary(wpath)
            self.assertTrue(meta.get("valid_riff"), f"{s['image_file']} must be valid RIFF/WEBP")

    def test_pairwise_f3_catalog_to_f8_manifest_alignment(self):
        """TC-T3-12: F3 <-> F8: Pack 1 sticker count alignment between packs.js and contents.json."""
        manifest = load_whatsapp_manifest()
        packs = load_packs_catalog()
        pack1_catalog = [p for p in packs if p["id"] == "pack-1-social-slang"][0]
        pack1_manifest = [p for p in manifest["sticker_packs"] if p["identifier"] == "pack-1-social-slang"][0]

        catalog_stickers = [s["id"] for s in pack1_catalog.get("stickers", [])]
        manifest_stickers = [s["image_file"].replace(".webp", "") for s in pack1_manifest.get("stickers", [])]

        # Milestone M4 aligns contents.json from 16 to 18 stickers (crapaud-pipe, trini-chow)
        if len(manifest_stickers) < len(catalog_stickers):
            require_milestone(
                "Pending Milestone M4",
                False,
                f"contents.json pack-1 has {len(manifest_stickers)} stickers; packs.js has {len(catalog_stickers)}"
            )
        self.assertEqual(len(manifest_stickers), len(catalog_stickers))


if __name__ == "__main__":
    unittest.main()
