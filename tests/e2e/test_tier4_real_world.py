"""
PeelOff E2E Test Suite — Tier 4: Real-World Scenarios & Production Pipelines
5 End-to-End Simulation Scenarios covering full developer pipelines, user web app journeys,
slang catalog browsing, WhatsApp sticker importing, and defect quarantine/recovery.
"""

import os
import sys
import json
import tempfile
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
    run_command,
    require_milestone,
    is_strict_mode,
)


class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: 5 Real-World End-to-End Workflow Scenarios."""

    def test_scenario_01_asset_build_to_verify_pipeline(self):
        """TC-T4-01: Full developer / CI asset pipeline execution & verification simulation."""
        # 1. Verify generator exists
        gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        self.assertTrue(os.path.exists(gen_path), "Generator scripts/build_animated_stickers.py must exist")

        # 2. Verify WhatsApp specs verifier executes cleanly
        wa_verifier = get_workspace_path("scripts", "verify_whatsapp_specs.py")
        rc, stdout, stderr = run_command([get_python_executable(), wa_verifier])
        self.assertEqual(rc, 0, f"WhatsApp spec verifier failed: {stderr}")
        self.assertIn("VERIFICATION PASSED", stdout)

        # 3. Verify animated verifier contract
        anim_verifier = get_workspace_path("scripts", "verify_animated_stickers.py")
        if not os.path.exists(anim_verifier):
            require_milestone(
                "Pending Milestone M3",
                False,
                "scripts/verify_animated_stickers.py not yet created"
            )
        rc2, out2, err2 = run_command([get_python_executable(), anim_verifier])
        self.assertEqual(rc2, 0)

    def test_scenario_02_user_browsing_and_toggle_workflow(self):
        """TC-T4-02: End-to-end web app user journey (explore, toggle, search, preview, share)."""
        app_js_path = get_workspace_path("app.js")
        index_html_path = get_workspace_path("index.html")

        # 1. User loads PWA root
        self.assertTrue(os.path.exists(index_html_path))
        with open(index_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Check required DOM elements
        self.assertIn("toggleAnimatedBtn", html)
        self.assertTrue("slangSearchInput" in html or "triniSlangSearchInput" in html)
        self.assertIn("triniSlangGrid", html)

        # 2. Check app.js logic
        with open(app_js_path, "r", encoding="utf-8") as f:
            js = f.read()

        # Check toggleAnimatedBtn event listener
        self.assertIn("toggleAnimatedBtn", js)
        # Check Animated URL routing
        self.assertIn("assets/animated", js)

        # 3. Simulate user searching for "steups"
        all_ids = load_all_catalog_ids()
        matched = [sid for sid in all_ids if "steups" in sid.lower()]
        self.assertGreaterEqual(len(matched), 2, "Search for 'steups' should match pack and slang items")
        self.assertIn("steups", matched)
        self.assertIn("slang-steups", matched)

    def test_scenario_03_slang_catalog_exploration_and_sharing(self):
        """TC-T4-03: Slang catalog exploration, filtering, and cross-platform sharing workflow."""
        slang = load_slang_catalog()
        self.assertEqual(len(slang), 88, "Expected 88 slang catalog items")

        # 1. Filter by category "Co-Signs & Facts"
        cosigns = [s for s in slang if s.get("category") == "Co-Signs & Facts"]
        self.assertGreaterEqual(len(cosigns), 10, "Expected at least 10 items in Co-Signs & Facts")

        # 2. Select sticker "slang-doh-study-dat"
        target = [s for s in cosigns if s.get("slug") == "doh-study-dat"]
        self.assertTrue(len(target) > 0, "Missing slang-doh-study-dat in catalog")
        item = target[0]

        # 3. Verify static and animated asset references
        anim_dir = get_workspace_path("assets", "animated")
        static_dir = get_workspace_path("assets", "stickers")

        png_path = os.path.join(static_dir, f"{item['id']}.png")
        webp_path = os.path.join(anim_dir, f"{item['id']}.webp")
        gif_path = os.path.join(anim_dir, f"{item['id']}.gif")

        self.assertTrue(os.path.exists(png_path), f"Missing {png_path}")
        self.assertTrue(os.path.exists(webp_path), f"Missing {webp_path}")
        self.assertTrue(os.path.exists(gif_path), f"Missing {gif_path}")

        # Check GIF share format (GIF89a on dark card)
        g_meta = parse_gif_binary(gif_path)
        self.assertTrue(g_meta.get("valid_gif"))
        self.assertEqual(g_meta.get("header"), "GIF89a")

    def test_scenario_04_whatsapp_multipack_import_simulation(self):
        """TC-T4-04: WhatsApp multi-pack import parsing and asset constraint validation."""
        manifest = load_whatsapp_manifest()
        packs = manifest.get("sticker_packs", [])
        self.assertEqual(len(packs), 8, "WhatsApp import expects 8 packs")

        total_stickers = 0
        for p in packs:
            stickers = p.get("stickers", [])
            total_stickers += len(stickers)
            self.assertGreaterEqual(len(stickers), 3, f"Pack {p['identifier']} below WhatsApp min 3")
            self.assertLessEqual(len(stickers), 30, f"Pack {p['identifier']} exceeds WhatsApp max 30")

            # Validate tray icon
            tray_path = get_workspace_path("assets", "trays", p["tray_image_file"])
            self.assertTrue(os.path.exists(tray_path))
            tray_size = os.path.getsize(tray_path)
            self.assertLess(tray_size, 50000, f"Tray icon {tray_path} >= 50KB")

        self.assertGreaterEqual(total_stickers, 98)

    def test_scenario_05_defect_quarantine_and_recovery(self):
        """TC-T4-05: Defect detection in quarantine sandbox and recovery verification."""
        # 1. Create a simulated corrupt asset in a sandbox
        with tempfile.TemporaryDirectory() as sandbox:
            corrupt_webp = os.path.join(sandbox, "test_corrupt.webp")
            with open(corrupt_webp, "wb") as f:
                f.write(b"")  # 0-byte file

            # 2. Verify opaque binary parser detects the defect
            meta = parse_webp_binary(corrupt_webp)
            self.assertEqual(meta.get("size", -1), 0)
            self.assertFalse(meta.get("valid_riff", False))

            # 3. Verify safe_open_image flags error without crashing
            im, err = safe_open_image(corrupt_webp)
            self.assertIsNone(im)
            self.assertIn("0 bytes", err)

            # 4. Verify recovery: when valid WebP is written, parser succeeds
            valid_source = get_workspace_path("assets", "animated", "ent.webp")
            with open(valid_source, "rb") as src, open(corrupt_webp, "wb") as dst:
                dst.write(src.read())

            rec_meta = parse_webp_binary(corrupt_webp)
            self.assertTrue(rec_meta.get("valid_riff"))
            self.assertEqual(rec_meta.get("frame_count"), 24)


if __name__ == "__main__":
    unittest.main()
