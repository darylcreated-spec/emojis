"""Empirical Challenger Test Harness for Milestone 4:
Web App Integration & Manifest Alignment.

Covers:
1. Manifest Stress Testing (assets/contents.json):
   - JSON parsing & schema structure
   - All 8 packs have animated_sticker_pack: True (boolean)
   - Emoji array bounds [1, 3] for all stickers
   - Pack count and per-pack sticker count vs data/packs.js (100 stickers total)
   - Tray icon existence, dimensions (96x96), size (< 50KB), PNG headers
   - Physical asset existence (.webp in assets/stickers/ and assets/animated/, plus .gif in assets/animated/)
2. Web App Query String Stress Testing (app.js):
   - Node.js syntax validity (node --check app.js)
   - Cache buster ?v=9 present on all sticker/animated URLs
   - Absolute absence of ?v=8 or legacy version strings
   - Runtime simulated asset URL resolution for all slang (88) and pure culture (40) stickers
   - Fallback error handling & share sheet routing
3. Dual Catalog & Global Asset Verification:
   - All 188 stickers (100 packs + 88 slang) exist across 4 formats (.webp/.png in stickers, .webp/.gif in animated)
"""

import json
import os
import re
import subprocess
import sys
import unittest
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_path(*parts):
    return os.path.join(PROJECT_ROOT, *parts)

class TestManifestStress(unittest.TestCase):
    """Stress testing WhatsApp manifest assets/contents.json and related assets."""

    @classmethod
    def setUpClass(cls):
        cls.manifest_path = get_path("assets", "contents.json")
        with open(cls.manifest_path, "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_01_manifest_root_structure(self):
        """Verify root-level keys and types."""
        self.assertIn("sticker_packs", self.manifest)
        packs = self.manifest["sticker_packs"]
        self.assertIsInstance(packs, list)
        self.assertEqual(len(packs), 8, f"Expected exactly 8 packs, found {len(packs)}")

    def test_02_all_packs_animated_sticker_pack_is_true(self):
        """Verify all 8 packs have 'animated_sticker_pack': True strictly as a boolean."""
        for p in self.manifest["sticker_packs"]:
            pack_id = p.get("identifier", "unknown")
            self.assertIn("animated_sticker_pack", p, f"Pack {pack_id} missing animated_sticker_pack key")
            val = p["animated_sticker_pack"]
            self.assertIs(val, True, f"Pack {pack_id} animated_sticker_pack must be boolean True, got {type(val)}: {val}")

    def test_03_emojis_array_bounds_and_validity(self):
        """Verify every sticker has between 1 and 3 emojis, and each emoji is non-empty."""
        total_stickers = 0
        for p in self.manifest["sticker_packs"]:
            pack_id = p.get("identifier")
            stickers = p.get("stickers", [])
            for s in stickers:
                total_stickers += 1
                img = s.get("image_file")
                self.assertIsNotNone(img, f"Pack {pack_id} sticker missing image_file")
                self.assertTrue(img.endswith(".webp"), f"Sticker {img} in {pack_id} must be .webp")
                
                emojis = s.get("emojis")
                self.assertIsInstance(emojis, list, f"Sticker {img} emojis must be list")
                self.assertGreaterEqual(len(emojis), 1, f"Sticker {img} in {pack_id} has < 1 emoji ({len(emojis)})")
                self.assertLessEqual(len(emojis), 3, f"Sticker {img} in {pack_id} has > 3 emojis ({len(emojis)})")
                for em in emojis:
                    self.assertIsInstance(em, str, f"Emoji {em} in {img} must be string")
                    self.assertGreater(len(em.strip()), 0, f"Empty emoji string in {img}")
        self.assertEqual(total_stickers, 100, f"Expected 100 total stickers across all packs, got {total_stickers}")

    def test_04_tray_icons_physical_and_specification(self):
        """Verify tray icon for each pack exists, < 50KB, valid PNG header, and exactly 96x96 pixels."""
        tray_dir = get_path("assets", "trays")
        seen_trays = set()
        for p in self.manifest["sticker_packs"]:
            pack_id = p.get("identifier")
            tray_file = p.get("tray_image_file")
            self.assertIsNotNone(tray_file, f"Pack {pack_id} missing tray_image_file")
            self.assertTrue(tray_file.endswith(".png"), f"Tray file {tray_file} must be .png")
            self.assertNotIn(tray_file, seen_trays, f"Duplicate tray icon file {tray_file}")
            seen_trays.add(tray_file)

            tray_path = os.path.join(tray_dir, tray_file)
            self.assertTrue(os.path.isfile(tray_path), f"Tray file does not exist: {tray_path}")
            
            # File size check (< 50,000 bytes)
            file_size = os.path.getsize(tray_path)
            self.assertGreater(file_size, 0, f"Tray file {tray_file} is empty")
            self.assertLess(file_size, 50000, f"Tray file {tray_file} size {file_size} exceeds 50,000 bytes")

            # Binary PNG header check
            with open(tray_path, "rb") as f:
                header = f.read(8)
            self.assertEqual(header, b"\x89PNG\r\n\x1a\n", f"Tray file {tray_file} has invalid PNG header")

            # PIL Image dimension check
            with Image.open(tray_path) as im:
                self.assertEqual(im.format, "PNG", f"Tray file {tray_file} is not PNG format")
                self.assertEqual(im.size, (96, 96), f"Tray file {tray_file} size is {im.size}, expected (96, 96)")

    def test_05_manifest_stickers_disk_presence_and_formats(self):
        """Verify all 100 stickers in manifest exist on disk as static .webp, static .png, animated .webp, animated .gif."""
        static_dir = get_path("assets", "stickers")
        anim_dir = get_path("assets", "animated")

        missing_static_webp = []
        missing_static_png = []
        missing_anim_webp = []
        missing_anim_gif = []

        for p in self.manifest["sticker_packs"]:
            for s in p.get("stickers", []):
                fname = s["image_file"]
                stem = fname[:-5] if fname.endswith(".webp") else fname

                s_webp = os.path.join(static_dir, f"{stem}.webp")
                s_png = os.path.join(static_dir, f"{stem}.png")
                a_webp = os.path.join(anim_dir, f"{stem}.webp")
                a_gif = os.path.join(anim_dir, f"{stem}.gif")

                if not os.path.isfile(s_webp) or os.path.getsize(s_webp) == 0:
                    missing_static_webp.append(f"{stem}.webp")
                if not os.path.isfile(s_png) or os.path.getsize(s_png) == 0:
                    missing_static_png.append(f"{stem}.png")
                if not os.path.isfile(a_webp) or os.path.getsize(a_webp) == 0:
                    missing_anim_webp.append(f"{stem}.webp")
                if not os.path.isfile(a_gif) or os.path.getsize(a_gif) == 0:
                    missing_anim_gif.append(f"{stem}.gif")

        self.assertEqual(missing_static_webp, [], f"Missing static .webp: {missing_static_webp}")
        self.assertEqual(missing_static_png, [], f"Missing static .png: {missing_static_png}")
        self.assertEqual(missing_anim_webp, [], f"Missing anim .webp: {missing_anim_webp}")
        self.assertEqual(missing_anim_gif, [], f"Missing anim .gif: {missing_anim_gif}")

    def test_06_manifest_pack_sticker_counts_and_bounds(self):
        """Verify each pack contains between 3 and 30 stickers (WhatsApp spec)."""
        counts = {}
        for p in self.manifest["sticker_packs"]:
            pid = p["identifier"]
            count = len(p.get("stickers", []))
            counts[pid] = count
            self.assertGreaterEqual(count, 3, f"Pack {pid} has {count} < 3 stickers")
            self.assertLessEqual(count, 30, f"Pack {pid} has {count} > 30 stickers")
        # Pack 1 has 18 stickers
        self.assertEqual(counts["pack-1-social-slang"], 18, f"Pack 1 should have 18 stickers, got {counts['pack-1-social-slang']}")

    def test_07_manifest_vs_packs_js_exact_alignment(self):
        """Cross-check manifest stickers with data/packs.js."""
        packs_js_path = get_path("data", "packs.js")
        self.assertTrue(os.path.isfile(packs_js_path))
        
        # Extract packs from data/packs.js via node
        node_script = """
        const fs = require('fs');
        const code = fs.readFileSync('data/packs.js', 'utf8');
        const sandbox = {};
        const fn = new Function('window', code + '; return window.STICKERBOOM_PACKS;');
        const packs = fn(sandbox);
        console.log(JSON.stringify(packs.map(p => ({
            id: p.id,
            name: p.name,
            stickers: p.stickers.map(s => s.id)
        }))));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
        packs_js_data = json.loads(proc.stdout.strip())

        self.assertEqual(len(packs_js_data), 8, f"packs.js has {len(packs_js_data)} packs")

        manifest_packs = {p["identifier"]: p for p in self.manifest["sticker_packs"]}

        for p_js in packs_js_data:
            pid = p_js["id"]
            self.assertIn(pid, manifest_packs, f"Pack {pid} from packs.js not found in contents.json")
            m_pack = manifest_packs[pid]
            m_sticker_ids = [s["image_file"].replace(".webp", "") for s in m_pack.get("stickers", [])]
            js_sticker_ids = p_js["stickers"]

            self.assertEqual(len(m_sticker_ids), len(js_sticker_ids),
                             f"Pack {pid} count mismatch: manifest={len(m_sticker_ids)}, packs.js={len(js_sticker_ids)}")
            self.assertEqual(set(m_sticker_ids), set(js_sticker_ids),
                             f"Pack {pid} sticker set mismatch: diff={set(m_sticker_ids) ^ set(js_sticker_ids)}")


class TestWebAppQueryStringStress(unittest.TestCase):
    """Stress testing app.js query string versioning, fallback handlers, and runtime execution."""

    @classmethod
    def setUpClass(cls):
        cls.app_js_path = get_path("app.js")
        with open(cls.app_js_path, "r", encoding="utf-8") as f:
            cls.app_js_code = f.read()

    def test_01_app_js_node_syntax_check(self):
        """Check app.js syntax using node --check."""
        proc = subprocess.run(["node", "--check", self.app_js_path], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Syntax error in app.js:\n{proc.stderr}")

    def test_02_no_stray_v8_or_legacy_versions(self):
        """Ensure no ?v=8 or ?v=7 exists in app.js."""
        stray_v8 = re.findall(r"\?v=8\b", self.app_js_code)
        self.assertEqual(len(stray_v8), 0, f"Found stray ?v=8 occurrences: {len(stray_v8)}")

        stray_v7 = re.findall(r"\?v=7\b", self.app_js_code)
        self.assertEqual(len(stray_v7), 0, f"Found stray ?v=7 occurrences: {len(stray_v7)}")

    def test_03_exact_v9_url_occurrences(self):
        """Verify exactly 8 occurrences of ?v=9 in URL constructions."""
        v9_matches = re.findall(r"\?v=9", self.app_js_code)
        self.assertEqual(len(v9_matches), 8, f"Expected exactly 8 occurrences of ?v=9 in app.js, found {len(v9_matches)}")

        # Verify the specific lines
        expected_patterns = [
            r"item\.webpUrl\s*=\s*`assets/stickers/\${item\.id}\.webp\?v=9`;",
            r"item\.pngUrl\s*=\s*`assets/stickers/\${item\.id}\.png\?v=9`;",
            r"item\.animWebpUrl\s*=\s*`assets/animated/\${item\.id}\.webp\?v=9`;",
            r"item\.animGifUrl\s*=\s*`assets/animated/\${item\.id}\.gif\?v=9`;",
            r"webpUrl:\s*`assets/stickers/\${s\.id}\.webp\?v=9`,",
            r"pngUrl:\s*`assets/stickers/\${s\.id}\.png\?v=9`,",
            r"animWebpUrl:\s*`assets/animated/\${s\.id}\.webp\?v=9`,",
            r"animGifUrl:\s*`assets/animated/\${s\.id}\.gif\?v=9`",
        ]
        for pat in expected_patterns:
            self.assertRegex(self.app_js_code, pat, f"Missing expected URL pattern: {pat}")

    def test_04_no_unversioned_sticker_or_animated_asset_urls(self):
        """Check that every line constructing a sticker or animated asset URL in app.js contains ?v=9."""
        lines = self.app_js_code.splitlines()
        for idx, line in enumerate(lines, 1):
            if ("assets/stickers/" in line or "assets/animated/" in line) and ("webp" in line or "gif" in line or "png" in line):
                self.assertIn("?v=9", line, f"Line {idx} constructs sticker/animated URL without ?v=9: {line.strip()}")
                self.assertNotIn("?v=8", line, f"Line {idx} constructs sticker/animated URL with stale ?v=8: {line.strip()}")

    def test_05_runtime_simulated_url_resolution(self):
        """Execute node script directly evaluating app.js enrichment and verify every resolved URL exists on disk."""
        node_script = """
        const fs = require('fs');
        const path = require('path');

        // Load data catalogs
        const packsCode = fs.readFileSync('data/packs.js', 'utf8');
        const slangCode = fs.readFileSync('data/trini-slang.js', 'utf8');
        const appCode = fs.readFileSync('app.js', 'utf8');

        const window = {};
        new Function('window', packsCode)(window);
        new Function('window', slangCode)(window);

        const basePacks = window.STICKERBOOM_PACKS || [];
        const triniSlangList = window.STICKERBOOM_TRINI_SLANG || [];

        // Extract PURE_3D_CULTURE_IDS and enrichment directly from app.js source
        const extractCode = appCode.slice(
            appCode.indexOf('const PURE_3D_CULTURE_IDS'),
            appCode.indexOf('// Group 88 Trini Slang items')
        );

        const fn = new Function('basePacks', 'triniSlangList', extractCode + '; return { triniSlangList, pureCultureStickers };');
        const res = fn(basePacks, triniSlangList);

        const results = [];
        res.triniSlangList.forEach(s => {
            results.push({ id: s.id, type: 'slang', urls: [s.webpUrl, s.pngUrl, s.animWebpUrl, s.animGifUrl] });
        });
        res.pureCultureStickers.forEach(s => {
            results.push({ id: s.id, type: 'culture', urls: [s.webpUrl, s.pngUrl, s.animWebpUrl, s.animGifUrl] });
        });

        console.log(JSON.stringify(results));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
        items = json.loads(proc.stdout.strip())

        self.assertEqual(len(items), 88 + 40, f"Expected 128 items (88 slang + 40 culture), got {len(items)}")

        for item in items:
            for url in item["urls"]:
                self.assertTrue(url.endswith("?v=9"), f"URL {url} does not end with ?v=9")
                # Strip query parameter to check disk existence
                disk_rel = url.split("?")[0]
                disk_path = get_path(disk_rel)
                self.assertTrue(os.path.isfile(disk_path), f"File referenced by URL does not exist on disk: {disk_path}")
                self.assertGreater(os.path.getsize(disk_path), 0, f"File {disk_path} is empty")

    def test_06_app_js_fallback_and_sharing_routines(self):
        """Verify error fallback handler and share sheet routing in app.js."""
        self.assertIn("onerror", self.app_js_code)
        self.assertIn("animGifUrl", self.app_js_code)
        # Check that share sheet uses animGifUrl
        share_match = re.search(r"navigator\.share[\s\S]*?animGifUrl", self.app_js_code)
        self.assertIsNotNone(share_match, "app.js should reference animGifUrl in sharing logic")


class TestGlobalCatalogCompleteness(unittest.TestCase):
    """Stress testing dual catalogs (100 packs + 88 slang = 188 total stickers)."""

    def test_01_all_188_stickers_in_all_four_formats(self):
        """Verify that all 188 stickers across both catalogs exist as static webp, static png, anim webp, anim gif."""
        # Run node to extract all 188 IDs
        node_script = """
        const fs = require('fs');
        const packsCode = fs.readFileSync('data/packs.js', 'utf8');
        const slangCode = fs.readFileSync('data/trini-slang.js', 'utf8');

        const window = {};
        new Function('window', packsCode)(window);
        new Function('window', slangCode)(window);

        const packs = window.STICKERBOOM_PACKS || [];
        const slang = window.STICKERBOOM_TRINI_SLANG || [];

        const packStickers = [];
        packs.forEach(p => p.stickers.forEach(s => packStickers.push(s.id)));
        const slangStickers = slang.map(s => s.id);

        console.log(JSON.stringify({
            packStickers: packStickers,
            slangStickers: slangStickers
        }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout.strip())
        pack_stickers = data["packStickers"]
        slang_stickers = data["slangStickers"]

        self.assertEqual(len(pack_stickers), 100, f"packs.js has {len(pack_stickers)} stickers, expected 100")
        self.assertEqual(len(slang_stickers), 88, f"trini-slang.js has {len(slang_stickers)} stickers, expected 88")

        all_stickers = set(pack_stickers) | set(slang_stickers)
        self.assertEqual(len(all_stickers), 188, f"Expected 188 distinct stickers, found {len(all_stickers)}")

        static_dir = get_path("assets", "stickers")
        anim_dir = get_path("assets", "animated")

        missing = []
        for sid in all_stickers:
            files_to_check = [
                os.path.join(static_dir, f"{sid}.webp"),
                os.path.join(static_dir, f"{sid}.png"),
                os.path.join(anim_dir, f"{sid}.webp"),
                os.path.join(anim_dir, f"{sid}.gif"),
            ]
            for f in files_to_check:
                if not os.path.isfile(f) or os.path.getsize(f) == 0:
                    missing.append(f)

        self.assertEqual(missing, [], f"Total missing or empty asset files: {len(missing)}: {missing[:10]}")


class TestAdversarialIntegrityAndFormatDeepAudit(unittest.TestCase):
    """Deep adversarial audit on headers, distinctness, encoding, and catalog files."""

    def test_01_json_encoding_no_bom(self):
        """Verify assets/contents.json has no UTF-8 BOM."""
        path = get_path("assets", "contents.json")
        with open(path, "rb") as f:
            first_bytes = f.read(4)
        self.assertNotEqual(first_bytes[:3], b"\xef\xbb\xbf", "contents.json has a UTF-8 BOM")

    def test_02_data_catalogs_syntax_validity(self):
        """Verify data/packs.js and data/trini-slang.js have zero syntax errors."""
        for js_file in ["data/packs.js", "data/trini-slang.js"]:
            full_path = get_path(js_file)
            proc = subprocess.run(["node", "--check", full_path], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, f"Syntax error in {js_file}: {proc.stderr}")

    def test_03_tray_icons_distinctness(self):
        """Verify all 8 tray icons have unique contents (no duplicate/placeholder copies)."""
        import hashlib
        tray_hashes = {}
        with open(get_path("assets", "contents.json"), "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for p in manifest["sticker_packs"]:
            tpath = get_path("assets", "trays", p["tray_image_file"])
            with open(tpath, "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            self.assertNotIn(h, tray_hashes, f"Duplicate tray icon detected: {p['tray_image_file']} matches {tray_hashes.get(h)}")
            tray_hashes[h] = p["tray_image_file"]
        self.assertEqual(len(tray_hashes), 8, "Expected 8 unique tray icons")

    def test_04_headers_and_frame_counts_for_all_manifest_stickers(self):
        """Adversarially open all 100 manifest stickers and verify RIFF/WEBP, GIF89a, frames >= 24, size 512x512."""
        with open(get_path("assets", "contents.json"), "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for p in manifest["sticker_packs"]:
            for s in p.get("stickers", []):
                fname = s["image_file"]
                stem = fname[:-5] if fname.endswith(".webp") else fname

                # 1. Static WebP
                s_webp = get_path("assets", "stickers", f"{stem}.webp")
                with open(s_webp, "rb") as f:
                    header = f.read(12)
                self.assertEqual(header[0:4], b"RIFF", f"{s_webp} not RIFF")
                self.assertEqual(header[8:12], b"WEBP", f"{s_webp} not WEBP")

                # 2. Animated WebP
                a_webp = get_path("assets", "animated", f"{stem}.webp")
                with open(a_webp, "rb") as f:
                    header = f.read(12)
                self.assertEqual(header[0:4], b"RIFF", f"{a_webp} not RIFF")
                self.assertEqual(header[8:12], b"WEBP", f"{a_webp} not WEBP")
                with Image.open(a_webp) as im:
                    self.assertEqual(im.size, (512, 512), f"{a_webp} size != 512x512")
                    self.assertGreaterEqual(getattr(im, "n_frames", 1), 24, f"{a_webp} frames < 24")

                # 3. Animated GIF
                a_gif = get_path("assets", "animated", f"{stem}.gif")
                with open(a_gif, "rb") as f:
                    header = f.read(6)
                self.assertEqual(header, b"GIF89a", f"{a_gif} not GIF89a")
                with Image.open(a_gif) as im:
                    self.assertEqual(im.size, (512, 512), f"{a_gif} size != 512x512")
                    self.assertGreaterEqual(getattr(im, "n_frames", 1), 24, f"{a_gif} frames < 24")


if __name__ == "__main__":
    unittest.main()

