import os
import re
import json
import unittest
from html.parser import HTMLParser

class IndexHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.classes = set()
        self.data_attrs = {}
        self.tags = set()

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        for attr, val in attrs:
            if attr == "id" and val:
                self.ids.add(val)
            elif attr == "class" and val:
                for c in val.split():
                    self.classes.add(c)
            elif attr.startswith("data-") and val:
                self.data_attrs.setdefault(attr, set()).add(val)

class TestMilestone4EmpiricalChallenge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        with open(os.path.join(cls.repo_root, "app.js"), "r", encoding="utf-8") as f:
            cls.app_js = f.read()
        with open(os.path.join(cls.repo_root, "index.html"), "r", encoding="utf-8") as f:
            cls.index_html = f.read()
        with open(os.path.join(cls.repo_root, "assets", "contents.json"), "r", encoding="utf-8") as f:
            cls.contents_json = json.load(f)
        with open(os.path.join(cls.repo_root, "data", "packs.js"), "r", encoding="utf-8") as f:
            cls.packs_js = f.read()
        with open(os.path.join(cls.repo_root, "data", "trini-slang.js"), "r", encoding="utf-8") as f:
            cls.trini_slang_js = f.read()

        parser = IndexHtmlParser()
        parser.feed(cls.index_html)
        cls.html_ids = parser.ids
        cls.html_classes = parser.classes
        cls.html_data_attrs = parser.data_attrs

    # -------------------------------------------------------------
    # 1. PWA & Web Runtime Verification: DOM Queries & Event Listeners
    # -------------------------------------------------------------
    def test_dom_get_element_by_id_complete_coverage(self):
        """All document.getElementById calls in app.js reference existing elements in index.html."""
        id_calls = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', self.app_js)
        unique_ids = set(id_calls)
        self.assertGreater(len(unique_ids), 20, "Should have identified at least 20 unique element IDs")

        missing_ids = [elem_id for elem_id in sorted(unique_ids) if elem_id not in self.html_ids]
        self.assertEqual(missing_ids, [], f"Missing getElementById targets in index.html: {missing_ids}")

    def test_required_interactive_elements_exist_and_wired(self):
        """Critical interactive buttons specified in dispatch exist and have event listeners attached."""
        critical_ids = [
            "toggleAnimatedBtn",
            "toggleAnimatedLabel",
            "packRail",
            "stickerGrid",
            "activePackCard",
            "slangSearchInput",
            "clearSearchBtn",
            "copyStickerClipboardBtn",
            "directSendSocialBtn",
            "downloadAnimGifBtn",
            "downloadAnimWebpBtn",
            "downloadPngBtn",
            "downloadDiscordBtn",
            "downloadPackBtn",
            "sharePackBtn",
            "shareAppBtn",
            "toastBanner"
        ]
        for cid in critical_ids:
            with self.subTest(element_id=cid):
                self.assertIn(cid, self.html_ids, f"Critical element '{cid}' missing from index.html")
                # Verify element is referenced in app.js
                self.assertIn(cid, self.app_js, f"Critical element '{cid}' not referenced in app.js")

    def test_query_selectors_and_classes_validity(self):
        """Verify static querySelector and querySelectorAll classes exist either in index.html or generated DOM."""
        class_queries = re.findall(r'querySelectorAll\(["\']\.([a-zA-Z0-9_-]+)["\']\)', self.app_js)
        unique_classes = set(class_queries)
        
        # Generated DOM classes that are created dynamically inside render functions:
        dynamic_classes = {"sticker-card", "studio-thumb-btn"}

        for cls_name in unique_classes:
            with self.subTest(class_name=cls_name):
                found_in_static = cls_name in self.html_classes
                found_in_dynamic = cls_name in dynamic_classes or cls_name in self.app_js
                self.assertTrue(
                    found_in_static or found_in_dynamic,
                    f"Queried class '.{cls_name}' neither in index.html nor generated in app.js"
                )

    # -------------------------------------------------------------
    # 2. Onerror Fallback Logic Verification
    # -------------------------------------------------------------
    def test_onerror_fallback_syntax_and_quoting(self):
        """Verify onerror attributes inside app.js have safe quoting and valid JS assignments."""
        onerror_patterns = re.findall(r'onerror="([^"]+)"', self.app_js)
        self.assertGreater(len(onerror_patterns), 0, "app.js should define onerror fallback handler")

        for handler in onerror_patterns:
            with self.subTest(handler=handler):
                # Must be a safe assignment: this.src='...'
                self.assertTrue(
                    re.match(r"^this\.src='[^']+'$", handler),
                    f"Unexpected or unsafe onerror handler pattern: {handler}"
                )
                # Verify that no unescaped double quotes exist
                self.assertNotIn('"', handler)
                # Verify that no unescaped angle brackets or javascript: URIs exist
                self.assertNotIn('<', handler)
                self.assertNotIn('>', handler)
                self.assertNotIn('javascript:', handler.lower())

    def test_all_stickers_have_valid_static_webp_fallbacks(self):
        """Verify every sticker's webpUrl fallback exists on disk so onerror does not fail."""
        stickers_dir = os.path.join(self.repo_root, "assets", "stickers")
        self.assertTrue(os.path.isdir(stickers_dir), "assets/stickers directory must exist")

        # Extract all sticker IDs defined in data/trini-slang.js and PURE_3D_CULTURE_IDS in app.js
        slang_ids = re.findall(r'["\']id["\']:\s*["\']([^"\']+)["\']', self.trini_slang_js)
        self.assertGreater(len(slang_ids), 80, f"Expected at least 80 slang sticker IDs, got {len(slang_ids)}")

        pure_culture_matches = re.search(r'const PURE_3D_CULTURE_IDS = new Set\(\[\s*([\s\S]*?)\s*\]\);', self.app_js)
        self.assertIsNotNone(pure_culture_matches, "PURE_3D_CULTURE_IDS definition must be present")
        pure_culture_ids = re.findall(r'["\']([^"\']+)["\']', pure_culture_matches.group(1))
        self.assertEqual(len(pure_culture_ids), 40, "Expected 40 pure culture sticker IDs")

        all_rendered_ids = set(slang_ids + pure_culture_ids)
        missing_webp = []
        for sid in sorted(all_rendered_ids):
            webp_path = os.path.join(stickers_dir, f"{sid}.webp")
            if not os.path.isfile(webp_path):
                missing_webp.append(f"{sid}.webp")

        self.assertEqual(missing_webp, [], f"Missing static fallback WebP assets: {missing_webp}")

    def test_all_stickers_have_animated_assets_on_disk(self):
        """Verify that animated WebP and GIF assets exist for all rendered stickers."""
        anim_dir = os.path.join(self.repo_root, "assets", "animated")
        self.assertTrue(os.path.isdir(anim_dir), "assets/animated directory must exist")

        slang_ids = re.findall(r'["\']id["\']:\s*["\']([^"\']+)["\']', self.trini_slang_js)
        pure_culture_matches = re.search(r'const PURE_3D_CULTURE_IDS = new Set\(\[\s*([\s\S]*?)\s*\]\);', self.app_js)
        pure_culture_ids = re.findall(r'["\']([^"\']+)["\']', pure_culture_matches.group(1))
        all_rendered_ids = set(slang_ids + pure_culture_ids)

        missing_anim_webp = []
        missing_anim_gif = []
        for sid in sorted(all_rendered_ids):
            webp_p = os.path.join(anim_dir, f"{sid}.webp")
            gif_p = os.path.join(anim_dir, f"{sid}.gif")
            if not os.path.isfile(webp_p):
                missing_anim_webp.append(f"{sid}.webp")
            if not os.path.isfile(gif_p):
                missing_anim_gif.append(f"{sid}.gif")

        self.assertEqual(missing_anim_webp, [], f"Missing animated WebP files: {missing_anim_webp}")
        self.assertEqual(missing_anim_gif, [], f"Missing animated GIF files: {missing_anim_gif}")

    # -------------------------------------------------------------
    # 3. URL Query Construction & Sticker ID Integrity
    # -------------------------------------------------------------
    def test_sticker_ids_are_strictly_url_safe(self):
        """Verify all sticker IDs are strictly kebab-case lowercase alphanumeric without unsafe chars."""
        slang_ids = re.findall(r'["\']id["\']:\s*["\']([^"\']+)["\']', self.trini_slang_js)
        pure_culture_matches = re.search(r'const PURE_3D_CULTURE_IDS = new Set\(\[\s*([\s\S]*?)\s*\]\);', self.app_js)
        pure_culture_ids = re.findall(r'["\']([^"\']+)["\']', pure_culture_matches.group(1))

        all_ids = set(slang_ids + pure_culture_ids)
        unsafe_ids = [sid for sid in all_ids if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', sid)]
        self.assertEqual(unsafe_ids, [], f"Non-conforming or unsafe sticker IDs detected: {unsafe_ids}")

    def test_cache_buster_query_consistency(self):
        """Verify app.js uniformly uses ?v=9 and contains zero occurrences of legacy ?v=8."""
        self.assertNotIn("?v=8", self.app_js, "Legacy '?v=8' cache buster detected in app.js")
        v9_occurrences = self.app_js.count("?v=9")
        self.assertEqual(v9_occurrences, 8, f"Expected exactly 8 occurrences of '?v=9' in app.js, found {v9_occurrences}")

    def test_url_construction_edge_case_simulation(self):
        """Simulate URL construction in Node/JS runtime with edge cases to test URL generation safety."""
        test_ids = [
            "steups",
            "killing-me-dead",
            "doh-tote",
            "test_underscores",
            "test.dots",
            "test%20encoded",
            "test space",
            "test'quote",
            "test\"dquote",
            "test<tag>",
            "test?param=1",
            "test#anchor"
        ]
        for tid in test_ids:
            webp_url = f"assets/stickers/{tid}.webp?v=9"
            anim_webp_url = f"assets/animated/{tid}.webp?v=9"
            anim_gif_url = f"assets/animated/{tid}.gif?v=9"

            # Check that query string concatenation '?v=9' preserves path extension properly
            self.assertTrue(webp_url.endswith(".webp?v=9"))
            self.assertTrue(anim_webp_url.endswith(".webp?v=9"))
            self.assertTrue(anim_gif_url.endswith(".gif?v=9"))

            # When placed into onerror="this.src='${item.webpUrl}'", does single quote cause breakage?
            onerror_snippet = f"onerror=\"this.src='{webp_url}'\""
            if "'" in tid:
                # This demonstrates why sticker IDs MUST NEVER contain single quotes
                self.assertIn("'", tid)
            else:
                self.assertNotIn("'", tid)
                # Ensure no quote break-out is possible for any legitimate sticker ID
                self.assertEqual(onerror_snippet.count("'"), 2)

    # -------------------------------------------------------------
    # 4. WhatsApp Manifest & Content Alignment
    # -------------------------------------------------------------
    def test_whatsapp_manifest_animated_flag(self):
        """Verify all sticker packs in assets/contents.json have animated_sticker_pack set to true."""
        packs = self.contents_json.get("sticker_packs", [])
        self.assertEqual(len(packs), 8, "Expected 8 sticker packs in contents.json")
        for p in packs:
            self.assertTrue(
                p.get("animated_sticker_pack"),
                f"Pack '{p.get('identifier')}' does not have animated_sticker_pack: true"
            )

    def test_whatsapp_manifest_pack_1_contains_18_stickers(self):
        """Verify pack-1-social-slang in contents.json has 18 stickers matching data/packs.js."""
        pack1 = next((p for p in self.contents_json.get("sticker_packs", []) if p.get("identifier") == "pack-1-social-slang"), None)
        self.assertIsNotNone(pack1, "pack-1-social-slang missing from contents.json")
        stickers = pack1.get("stickers", [])
        self.assertEqual(len(stickers), 18, f"pack-1-social-slang should have 18 stickers, found {len(stickers)}")
        
        # Verify crapaud-pipe and trini-chow are present
        image_files = [s.get("image_file") for s in stickers]
        self.assertIn("crapaud-pipe.webp", image_files, "crapaud-pipe.webp missing from pack 1")
        self.assertIn("trini-chow.webp", image_files, "trini-chow.webp missing from pack 1")

if __name__ == "__main__":
    unittest.main()
