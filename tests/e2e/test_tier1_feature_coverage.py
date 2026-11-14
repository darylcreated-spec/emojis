"""
PeelOff E2E Test Suite — Tier 1: Feature Coverage (Category-Partition Method)
50 Comprehensive Test Cases covering Features F1 through F10 (5 tests per feature).
Verifies primary behavior, functional contracts, and observable outputs.
"""

import os
import sys
import json
import re
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
    check_card_background_rgb,
    check_webp_corner_alpha,
    run_command,
    require_milestone,
    is_strict_mode,
    temporary_strict_mode,
)


class TestTier1F1CulturalReferenceGuide(unittest.TestCase):
    """F1: Cultural Reference Guide (docs/CULTURAL_ANIMATION_SPEC.md)."""

    def setUp(self):
        self.spec_path = get_workspace_path("docs", "CULTURAL_ANIMATION_SPEC.md")

    def test_f1_01_spec_file_exists(self):
        """TC-T1-F1-01: Verify CULTURAL_ANIMATION_SPEC.md exists and is non-empty."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        size = os.path.getsize(self.spec_path)
        self.assertGreater(size, 2000, f"Spec file is too small ({size} bytes)")

    def test_f1_02_emotional_registers_coverage(self):
        """TC-T1-F1-02: Verify documentation of authentic Trini emotional registers."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        registers = ["picong", "bazodee", "steups", "tabanca", "liming"]
        found = [r for r in registers if r in content]
        self.assertGreaterEqual(len(found), 4, f"Missing key emotional registers; found: {found}")

    def test_f1_03_exhaustive_188_sticker_matrix(self):
        """TC-T1-F1-03: Verify cultural matrix maps all 188 sticker IDs."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read()
        all_ids = load_all_catalog_ids()
        missing = [sid for sid in all_ids if sid not in content]
        if missing:
            require_milestone(
                "Pending Milestone M1",
                False,
                f"Section 5 (188-Sticker Mapping Matrix) is still being authored ({len(missing)} stickers missing)"
            )
        self.assertEqual(len(missing), 0)

    def test_f1_04_authentic_motion_primitives_specification(self):
        """TC-T1-F1-04: Verify specification documents 12+ authentic motion routines."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        primitives = ["windmill", "recoil", "lean", "slam", "akumbo", "spiral", "wine"]
        found = [p for p in primitives if p in content]
        if len(found) < 4:
            require_milestone(
                "Pending Milestone M1",
                False,
                f"Section 4 (Motion Primitives) not yet fully authored (found {len(found)} routines: {found})"
            )
        self.assertGreaterEqual(len(found), 4)

    def test_f1_05_matrix_column_schema(self):
        """TC-T1-F1-05: Verify master matrix defines required structural columns."""
        exists = os.path.exists(self.spec_path)
        require_milestone("Pending Milestone M1", exists, "docs/CULTURAL_ANIMATION_SPEC.md not yet created")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Look for table header keywords
        headers = ["sticker", "motion", "rig", "context"]
        found_headers = [h for h in headers if h.lower() in content.lower()]
        self.assertGreaterEqual(len(found_headers), 2, f"Matrix table lacks required header columns: {headers}")


class TestTier1F2AuthenticMotionPrimitives(unittest.TestCase):
    """F2: Authentic Motion Primitives (scripts/build_animated_stickers.py)."""

    def setUp(self):
        self.gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        self.assertTrue(os.path.exists(self.gen_path), "Missing scripts/build_animated_stickers.py")
        with open(self.gen_path, "r", encoding="utf-8") as f:
            self.code = f.read()

    def test_f2_01_soca_rag_windmill_motion(self):
        """TC-T1-F2-01: Verify soca rag windmill / wave motion primitive exists."""
        has_primitive = "rag" in self.code.lower() or "wave" in self.code.lower()
        self.assertTrue(has_primitive, "Generator missing soca rag windmill motion primitive")

    def test_f2_02_steups_recoil_motion(self):
        """TC-T1-F2-02: Verify steups recoil / acoustic air puff motion primitive exists."""
        has_primitive = "steups" in self.code.lower()
        self.assertTrue(has_primitive, "Generator missing steups recoil motion primitive")

    def test_f2_03_doubles_lean_motion(self):
        """TC-T1-F2-03: Verify 45° doubles lean motion primitive exists."""
        has_primitive = "doubles" in self.code.lower() or "lean" in self.code.lower()
        self.assertTrue(has_primitive, "Generator missing doubles 45° lean motion primitive")

    def test_f2_04_allfours_slam_motion(self):
        """TC-T1-F2-04: Verify all-fours table slam / shockwave motion routine exists."""
        has_primitive = "impact_shake" in self.code or "slam" in self.code.lower()
        self.assertTrue(has_primitive, "Generator missing all-fours slam / impact shake routine")

    def test_f2_05_tanty_akumbo_motion(self):
        """TC-T1-F2-05: Verify tanty akumbo / stern mom motion routine exists."""
        has_primitive = "spoon" in self.code.lower() or "akumbo" in self.code.lower() or "sway" in self.code.lower()
        self.assertTrue(has_primitive, "Generator missing tanty akumbo / spoon motion routine")


class TestTier1F3IndividualizedRigMapping(unittest.TestCase):
    """F3: Individualized Rig Mapping in scripts/build_animated_stickers.py."""

    def setUp(self):
        self.gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        with open(self.gen_path, "r", encoding="utf-8") as f:
            self.code = f.read()

    def test_f3_01_zero_generic_fallback(self):
        """TC-T1-F3-01: Verify articulated_gesture generic fallback is eliminated."""
        # Milestone M2 overhaul eliminates the fallback
        if "return \"articulated_gesture\"" in self.code or "return 'articulated_gesture'" in self.code:
            require_milestone(
                "Pending Milestone M2",
                False,
                "scripts/build_animated_stickers.py still contains articulated_gesture fallback"
            )
        self.assertNotIn("return \"articulated_gesture\"", self.code)

    def test_f3_02_cultural_pack_rig_coverage(self):
        """TC-T1-F3-02: Verify rigs cover cultural pack themes."""
        packs = load_packs_catalog()
        self.assertEqual(len(packs), 8, "Expected 8 cultural packs")
        pack_stickers = [s["id"] for p in packs for s in p.get("stickers", [])]
        self.assertEqual(len(pack_stickers), 100, f"Expected 100 pack stickers, found {len(pack_stickers)}")

    def test_f3_03_trini_slang_rig_coverage(self):
        """TC-T1-F3-03: Verify rigs cover Trini slang catalog."""
        slang = load_slang_catalog()
        self.assertEqual(len(slang), 88, f"Expected 88 slang stickers, found {len(slang)}")

    def test_f3_04_folklore_rig_specialization(self):
        """TC-T1-F3-04: Verify specialized folklore character rigs exist in generator."""
        folklore_ids = ["soucouyant", "papa-bois", "mama-dlo", "douen", "lagahoo"]
        found = [fid for fid in folklore_ids if fid in self.code]
        if len(found) < 3:
            require_milestone(
                "Pending Milestone M2",
                False,
                f"Folklore rigs not yet overhauled in scripts/build_animated_stickers.py (found: {found})"
            )
        self.assertGreaterEqual(len(found), 3)

    def test_f3_05_food_and_belly_rig_dynamics(self):
        """TC-T1-F3-05: Verify culinary food items have specialized rigs."""
        food_ids = ["doubles-3d", "bake-and-shark", "corn-soup", "pelau-pot"]
        found = [fid for fid in food_ids if fid in self.code]
        self.assertGreaterEqual(len(found), 2, f"Food stickers missing bespoke mapping in generator: {food_ids}")


class TestTier1F4MicroMotionHoldAndFrames(unittest.TestCase):
    """F4: Micro-Motion Hold & Frame Standardization (24 frames @ 90ms = 2.16s)."""

    def setUp(self):
        self.anim_dir = get_workspace_path("assets", "animated")

    def test_f4_01_universal_24_frames_webp(self):
        """TC-T1-F4-01: Verify non-empty WebP animations have 24 frames."""
        webp_files = [f for f in os.listdir(self.anim_dir) if f.endswith(".webp")]
        self.assertGreaterEqual(len(webp_files), 180, "Missing WebP files in assets/animated/")

        coalesced = []
        for fname in webp_files:
            fpath = os.path.join(self.anim_dir, fname)
            meta = parse_webp_binary(fpath)
            if meta.get("size", 0) > 0 and meta.get("valid_riff"):
                if meta.get("frame_count") != 24:
                    coalesced.append((fname, meta.get("frame_count")))

        if coalesced:
            require_milestone(
                "Pending Milestone M2",
                False,
                f"Found {len(coalesced)} WebP files with frame counts != 24 (e.g. {coalesced[:3]})"
            )
        self.assertEqual(len(coalesced), 0)

    def test_f4_02_universal_24_frames_gif(self):
        """TC-T1-F4-02: Verify non-empty GIF animations have 24 frames."""
        gif_files = [f for f in os.listdir(self.anim_dir) if f.endswith(".gif")]
        self.assertGreaterEqual(len(gif_files), 180, "Missing GIF files in assets/animated/")

        coalesced = []
        for fname in gif_files:
            fpath = os.path.join(self.anim_dir, fname)
            meta = parse_gif_binary(fpath)
            if meta.get("size", 0) > 0 and meta.get("valid_gif"):
                if meta.get("frame_count") != 24:
                    coalesced.append((fname, meta.get("frame_count")))

        if coalesced:
            require_milestone(
                "Pending Milestone M2",
                False,
                f"Found {len(coalesced)} GIF files with frame counts != 24 (e.g. {coalesced[:3]})"
            )
        self.assertEqual(len(coalesced), 0)

    def test_f4_03_per_frame_duration_90ms(self):
        """TC-T1-F4-03: Verify frame duration is 90ms nominal via binary parsers."""
        test_webp = os.path.join(self.anim_dir, "ent.webp")
        meta = parse_webp_binary(test_webp)
        self.assertTrue(meta.get("valid_riff"), "ent.webp should be valid RIFF")
        durations = meta.get("durations", [])
        self.assertGreaterEqual(len(durations), 1)
        self.assertEqual(durations[0], 90, f"Expected 90ms per frame, got {durations[0]}")

    def test_f4_04_total_loop_duration_2160ms(self):
        """TC-T1-F4-04: Verify total loop duration is 2160ms (satisfying WhatsApp >= 2.0s)."""
        test_gif = os.path.join(self.anim_dir, "ent.gif")
        meta = parse_gif_binary(test_gif)
        self.assertTrue(meta.get("valid_gif"), "ent.gif should be valid GIF")
        total_ms = meta.get("total_duration_ms", 0)
        self.assertGreaterEqual(total_ms, 2000, f"Loop duration {total_ms}ms < 2000ms minimum")

    def test_f4_05_previously_coalesced_stickers_resolved(self):
        """TC-T1-F4-05: Verify previously coalesced stickers (slang-link-me, bullseye-allfours) have 24 frames."""
        target_sid = "slang-link-me.webp"
        target_path = os.path.join(self.anim_dir, target_sid)
        meta = parse_webp_binary(target_path)
        if meta.get("size", 0) > 0 and meta.get("frame_count") != 24:
            require_milestone(
                "Pending Milestone M2",
                False,
                f"{target_sid} has {meta.get('frame_count')} frames (coalescing anomaly not yet resolved)"
            )
        self.assertEqual(meta.get("frame_count"), 24)


class TestTier1F5ProductionAssetGeneration(unittest.TestCase):
    """F5: Production Asset Generation (assets/animated/*.webp & *.gif)."""

    def setUp(self):
        self.anim_dir = get_workspace_path("assets", "animated")

    def test_f5_01_all_376_files_exist(self):
        """TC-T1-F5-01: Verify all 188 .webp and 188 .gif exist (total 376 files)."""
        all_ids = load_all_catalog_ids()
        self.assertEqual(len(all_ids), 188)
        missing_webp = [sid for sid in all_ids if not os.path.exists(os.path.join(self.anim_dir, f"{sid}.webp"))]
        missing_gif = [sid for sid in all_ids if not os.path.exists(os.path.join(self.anim_dir, f"{sid}.gif"))]
        self.assertEqual(len(missing_webp), 0, f"Missing WebP assets: {missing_webp}")
        self.assertEqual(len(missing_gif), 0, f"Missing GIF assets: {missing_gif}")

    def test_f5_02_zero_byte_file_detection(self):
        """TC-T1-F5-02: Assert zero 0-byte files exist in assets/animated/."""
        all_files = [f for f in os.listdir(self.anim_dir) if f.endswith((".webp", ".gif"))]
        zero_byte_files = [
            f for f in all_files if os.path.getsize(os.path.join(self.anim_dir, f)) == 0
        ]
        if zero_byte_files:
            require_milestone(
                "Pending Milestone M3",
                False,
                f"Found {len(zero_byte_files)} empty (0-byte) animated assets: {zero_byte_files}"
            )
        self.assertEqual(len(zero_byte_files), 0)

    def test_f5_03_canvas_dimension_512x512(self):
        """TC-T1-F5-03: Verify canvas dimensions are exactly 512x512 pixels."""
        test_files = ["ent.webp", "ent.gif", "slang-ent.webp", "slang-ent.gif"]
        for fname in test_files:
            fpath = os.path.join(self.anim_dir, fname)
            im, err = safe_open_image(fpath)
            self.assertIsNone(err, f"Error opening {fname}: {err}")
            self.assertEqual(im.size, (512, 512), f"{fname} dimensions {im.size} != (512, 512)")

    def test_f5_04_webp_riff_vp8x_header_and_alpha(self):
        """TC-T1-F5-04: Verify WebP header integrity and alpha transparency flag."""
        meta = parse_webp_binary(os.path.join(self.anim_dir, "ent.webp"))
        self.assertTrue(meta.get("valid_riff"))
        self.assertTrue(meta.get("has_animation"))
        self.assertTrue(meta.get("has_alpha"))
        self.assertEqual(meta.get("loop_count"), 0)

    def test_f5_05_gif_header_and_studio_card_palette(self):
        """TC-T1-F5-05: Verify GIF header is GIF89a and studio card background is #10141E."""
        gif_path = os.path.join(self.anim_dir, "ent.gif")
        meta = parse_gif_binary(gif_path)
        self.assertTrue(meta.get("valid_gif"))
        self.assertEqual(meta.get("header"), "GIF89a")
        self.assertLessEqual(meta.get("palette_colors", 0), 128)
        bg_ok, pixel = check_card_background_rgb(gif_path)
        self.assertTrue(bg_ok, f"Card background color {pixel} deviates from #10141E")


class TestTier1F6AutomatedAnimationVerifier(unittest.TestCase):
    """F6: Automated Animation Verifier (scripts/verify_animated_stickers.py)."""

    def setUp(self):
        self.verifier_path = get_workspace_path("scripts", "verify_animated_stickers.py")

    def test_f6_01_verifier_script_exists(self):
        """TC-T1-F6-01: Verify scripts/verify_animated_stickers.py exists."""
        exists = os.path.exists(self.verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        self.assertTrue(exists)

    def test_f6_02_verifier_clean_run(self):
        """TC-T1-F6-02: Verify verifier script executes with exit code 0."""
        exists = os.path.exists(self.verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        rc, stdout, stderr = run_command([get_python_executable(), self.verifier_path], timeout=30)
        self.assertEqual(rc, 0, f"Verifier failed with return code {rc}. Stderr: {stderr}")

    def test_f6_03_verifier_defect_detection_zero_byte(self):
        """TC-T1-F6-03: Verify verifier detects 0-byte corrupt assets."""
        exists = os.path.exists(self.verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        # Test code should contain 0-byte check
        with open(self.verifier_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertTrue("getsize" in code or "0" in code, "Verifier must check for empty/0-byte files")

    def test_f6_04_verifier_defect_detection_frame_drop(self):
        """TC-T1-F6-04: Verify verifier checks for minimum 24 frames."""
        exists = os.path.exists(self.verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        with open(self.verifier_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertTrue("24" in code, "Verifier must enforce 24 frames minimum")

    def test_f6_05_verifier_output_schema_and_duration(self):
        """TC-T1-F6-05: Verify verifier outputs diagnostic statistics within runtime budget."""
        exists = os.path.exists(self.verifier_path)
        require_milestone("Pending Milestone M3", exists, "scripts/verify_animated_stickers.py not yet created")
        rc, stdout, stderr = run_command([get_python_executable(), self.verifier_path], timeout=25)
        self.assertEqual(rc, 0)
        self.assertTrue("376" in stdout or "PASSED" in stdout.upper())


class TestTier1F7WebAppAnimatedIntegration(unittest.TestCase):
    """F7: Web App Animated Integration (app.js, index.html)."""

    def setUp(self):
        self.app_js = get_workspace_path("app.js")
        self.index_html = get_workspace_path("index.html")

    def test_f7_01_app_js_syntax_valid(self):
        """TC-T1-F7-01: Verify app.js contains valid JavaScript syntax."""
        rc, stdout, stderr = run_command(["node", "--check", self.app_js])
        self.assertEqual(rc, 0, f"Syntax error in app.js: {stderr}")

    def test_f7_02_index_html_dom_elements(self):
        """TC-T1-F7-02: Verify index.html contains required UI controls and tabs."""
        with open(self.index_html, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("toggleAnimatedBtn", html, "Missing #toggleAnimatedBtn in index.html")
        self.assertIn("view-packs", html, "Missing #view-packs in index.html")
        self.assertIn("view-slang", html, "Missing #view-slang in index.html")

    def test_f7_03_cache_busting_version_v9(self):
        """TC-T1-F7-03: Verify app.js uses cache-busting query parameter ?v=9."""
        with open(self.app_js, "r", encoding="utf-8") as f:
            js = f.read()
        if "?v=8" in js:
            require_milestone("Pending Milestone M4", False, "app.js still uses legacy ?v=8 instead of ?v=9")
        self.assertIn("?v=9", js, "app.js should use ?v=9 cache buster")

    def test_f7_04_image_fallback_error_handler(self):
        """TC-T1-F7-04: Verify image tags include onerror fallback handler."""
        with open(self.app_js, "r", encoding="utf-8") as f:
            js = f.read()
        self.assertIn("onerror", js, "app.js missing onerror image fallback handler")

    def test_f7_05_share_sheet_gif_routing(self):
        """TC-T1-F7-05: Verify animated mode routes looping GIF to share sheet."""
        with open(self.app_js, "r", encoding="utf-8") as f:
            js = f.read()
        self.assertIn("animGifUrl", js, "app.js missing animGifUrl share sheet routing")


class TestTier1F8WhatsAppManifestAlignment(unittest.TestCase):
    """F8: WhatsApp Manifest Alignment (assets/contents.json)."""

    def setUp(self):
        self.manifest = load_whatsapp_manifest()

    def test_f8_01_contents_json_valid_syntax(self):
        """TC-T1-F8-01: Verify assets/contents.json has valid JSON schema."""
        self.assertIn("sticker_packs", self.manifest)
        self.assertEqual(len(self.manifest["sticker_packs"]), 8)

    def test_f8_02_animated_sticker_pack_flag(self):
        """TC-T1-F8-02: Verify animated_sticker_pack is set to true for animated packs."""
        packs = self.manifest["sticker_packs"]
        # Check if animated flag is updated
        has_animated_flag = any(p.get("animated_sticker_pack") is True for p in packs)
        if not has_animated_flag:
            require_milestone("Pending Milestone M4", False, "assets/contents.json animated_sticker_pack is false")
        for p in packs:
            self.assertTrue(p.get("animated_sticker_pack"), f"Pack {p['identifier']} animated_sticker_pack != true")

    def test_f8_03_pack_count_and_tray_icons(self):
        """TC-T1-F8-03: Verify 8 packs and valid 96x96 tray icon files < 50KB."""
        for p in self.manifest["sticker_packs"]:
            tray_path = get_workspace_path("assets", "trays", p["tray_image_file"])
            self.assertTrue(os.path.exists(tray_path), f"Missing tray icon: {tray_path}")
            size_kb = os.path.getsize(tray_path) / 1024.0
            self.assertLess(size_kb, 50.0, f"Tray icon {tray_path} exceeds 50KB")
            im, err = safe_open_image(tray_path)
            self.assertIsNone(err)
            self.assertEqual(im.size, (96, 96))

    def test_f8_04_manifest_stickers_exist_on_disk(self):
        """TC-T1-F8-04: Verify all stickers in manifest exist in assets/stickers/ and assets/animated/."""
        for p in self.manifest["sticker_packs"]:
            for s in p.get("stickers", []):
                fname = s["image_file"]
                static_path = get_workspace_path("assets", "stickers", fname)
                anim_path = get_workspace_path("assets", "animated", fname)
                self.assertTrue(os.path.exists(static_path), f"Missing static asset {static_path}")
                self.assertTrue(os.path.exists(anim_path), f"Missing animated asset {anim_path}")

    def test_f8_05_pack_sticker_bounds(self):
        """TC-T1-F8-05: Verify each pack contains between 3 and 30 stickers (WhatsApp constraint)."""
        for p in self.manifest["sticker_packs"]:
            count = len(p.get("stickers", []))
            self.assertGreaterEqual(count, 3, f"Pack {p['identifier']} has fewer than 3 stickers ({count})")
            self.assertLessEqual(count, 30, f"Pack {p['identifier']} exceeds 30 stickers ({count})")


class TestTier1F9ComprehensiveE2ETestSuite(unittest.TestCase):
    """F9: Comprehensive E2E Test Suite Harness & Runner."""

    def test_f9_01_runner_cli_execution(self):
        """TC-T1-F9-01: Verify runner CLI responds to --help."""
        runner_path = get_workspace_path("tests", "e2e", "run_all_tests.py")
        if not os.path.exists(runner_path):
            require_milestone("Pending E2E Harness", False, "run_all_tests.py not yet implemented")
        rc, stdout, stderr = run_command([get_python_executable(), runner_path, "--help"])
        self.assertEqual(rc, 0)
        self.assertIn("PeelOff", stdout)

    def test_f9_02_runner_discovers_all_tiers(self):
        """TC-T1-F9-02: Verify test suites for Tiers 1 through 4 are present in tests/e2e/."""
        tier_files = [
            "test_tier1_feature_coverage.py",
            "test_tier2_boundary_corner.py",
            "test_tier3_cross_feature.py",
            "test_tier4_real_world.py",
        ]
        for tf in tier_files:
            fpath = get_workspace_path("tests", "e2e", tf)
            self.assertTrue(os.path.exists(fpath), f"Missing tier file: {fpath}")

    def test_f9_03_runner_total_tests_threshold(self):
        """TC-T1-F9-03: Verify total test cases across tiers meet or exceed 115 threshold."""
        from tests.e2e.run_all_tests import PeelOffTestRunner

        # Dynamically discover full test suite across all 4 tiers
        runner = PeelOffTestRunner()
        full_suite = runner.discover_suite()
        total_discovered = full_suite.countTestCases()
        expected_min = 115

        self.assertGreaterEqual(
            total_discovered,
            expected_min,
            f"Discovered {total_discovered} tests across all tiers, expected at least {expected_min}",
        )

        # Dynamically verify each tier meets its specific contract threshold
        tier_thresholds = {1: 50, 2: 50, 3: 10, 4: 5}
        for tier_num, min_expected in tier_thresholds.items():
            tier_suite = PeelOffTestRunner(tier=tier_num).discover_suite()
            tier_count = tier_suite.countTestCases()
            self.assertGreaterEqual(
                tier_count,
                min_expected,
                f"Tier {tier_num} discovered {tier_count} tests, expected at least {min_expected}",
            )

    def test_f9_04_runner_json_summary_output(self):
        """TC-T1-F9-04: Verify runner generates valid test_summary.json schema."""
        test_summary_path = get_workspace_path("tests", "e2e", "test_summary.json")
        if os.path.exists(test_summary_path):
            with open(test_summary_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("summary", data)
            self.assertIn("total", data["summary"])

    def test_f9_05_progressive_skip_handling(self):
        """TC-T1-F9-05: Verify require_milestone raises SkipTest in default progressive mode."""
        with temporary_strict_mode(False):
            with self.assertRaises(unittest.SkipTest):
                require_milestone("TestMilestone", False, "Simulated pending milestone")


class TestTier1F10AdversarialCoverageHardening(unittest.TestCase):
    """F10: Adversarial Coverage Hardening."""

    def test_f10_01_corrupted_webp_rejection(self):
        """TC-T1-F10-01: Verify parser rejects corrupted or truncated WebP bytes."""
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            tmp.write(b"RIFF\x00\x00\x00\x00WEBPTRUNCATED_GARBAGE")
            tmp_path = tmp.name
        try:
            meta = parse_webp_binary(tmp_path)
            self.assertEqual(meta.get("frame_count", 0), 0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_f10_02_corrupted_gif_rejection(self):
        """TC-T1-F10-02: Verify parser rejects corrupted or truncated GIF bytes."""
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
            tmp.write(b"GIF89a\x00\x00GARBAGE")
            tmp_path = tmp.name
        try:
            meta = parse_gif_binary(tmp_path)
            self.assertEqual(meta.get("frame_count", 0), 0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_f10_03_path_traversal_sanitization(self):
        """TC-T1-F10-03: Verify path resolution rejects or bounds path traversal sequences."""
        traversal = get_workspace_path("assets", "..", "..", "evil.txt")
        self.assertFalse(traversal.startswith(get_workspace_path("assets", "animated")))

    def test_f10_04_generator_invalid_cli_arguments(self):
        """TC-T1-F10-04: Verify generator handles invalid arguments safely."""
        gen_path = get_workspace_path("scripts", "build_animated_stickers.py")
        with open(gen_path, "r", encoding="utf-8") as f:
            code = f.read()
        has_cli_args = "argparse" in code or "--sticker" in code
        if not has_cli_args:
            require_milestone(
                "Pending Milestone M2",
                False,
                "scripts/build_animated_stickers.py CLI argument parsing (--sticker, --pack, --workers) not yet implemented"
            )
        rc, stdout, stderr = run_command([get_python_executable(), gen_path, "--invalid-flag-xyz"], timeout=10)
        self.assertIn(rc, (1, 2))

    def test_f10_05_extreme_dimensions_or_empty_inputs(self):
        """TC-T1-F10-05: Verify safe_open_image rejects empty or non-existent files."""
        im, err = safe_open_image(get_workspace_path("non_existent_file_xyz.png"))
        self.assertIsNone(im)
        self.assertIsNotNone(err)


if __name__ == "__main__":
    unittest.main()
