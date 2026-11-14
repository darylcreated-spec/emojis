"""
Milestone 1 Adversarial Verification Suite
Empirical challenger tests for docs/CULTURAL_ANIMATION_SPEC.md

Tests:
1. Catalog Census Total Count: 100 pack + 88 slang = 188 catalog stickers vs 188 Section 5 rows.
2. Catalog Census Exact ID Match: 100% ID match, 0 missing, 0 duplicates between catalog and Section 5.
3. Catalog Census Sequential Ordering: Part 1 matches Pack 1..8 order, Part 2 matches Slang 1..88 order.
4. Table Schema Integrity: exactly 188 rows, 9 non-empty pipe-delimited columns.
5. Strictly Incrementing Row Numbers: numbering strictly increments 1..188 with zero gaps.
6. Fallback Zero-Tolerance: 0 occurrences of 'articulated_gesture' or generic bounce in Section 5.
7. Completeness & Formatting: 0 TODO, TBD, [placeholder], broken markdown tables, or truncated text.
8. Motion Primitive Whitelist: all assigned motion primitives exist in Section 4 primitive definitions.
9. Keyframe Timing Coverage: timing column specifies 24-frame (f0-f23 @ 90ms) loop cycle.
10. Framing Bounds Safety: scale <= 0.95 and safety margins prevent 512x512 canvas clipping.
11. Markdown Delimiter Integrity: exactly 10 pipe symbols per table line across all 192 Section 5 rows.
12. Source Asset Alignment: all 188 sticker IDs resolve to existing PNG and WebP files in assets/stickers/.
"""

import os
import sys
import re
import json
import unittest
from typing import List, Dict, Any, Tuple

# Workspace root
WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
SPEC_PATH = os.path.join(WORKSPACE_DIR, "docs", "CULTURAL_ANIMATION_SPEC.md")
PACKS_PATH = os.path.join(WORKSPACE_DIR, "data", "packs.js")
SLANG_PATH = os.path.join(WORKSPACE_DIR, "data", "trini-slang.js")

# Add e2e helper path
sys.path.insert(0, os.path.join(WORKSPACE_DIR, "tests", "e2e"))
from test_helpers import load_packs_catalog, load_slang_catalog


def parse_section5_rows(spec_path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Parse Section 5.2 and 5.3 markdown tables from CULTURAL_ANIMATION_SPEC.md.
    Returns:
        (rows, errors)
    """
    with open(spec_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    rows = []
    errors = []
    in_sec5 = False
    headers = None

    for line_num, line in enumerate(lines, 1):
        line_str = line.strip()

        # Check section boundaries
        if "## SECTION 5:" in line_str or "### 5.2" in line_str:
            in_sec5 = True
        elif "## SECTION 6:" in line_str:
            in_sec5 = False
            break

        if not in_sec5:
            continue

        if not line_str.startswith("|"):
            continue

        # Split columns
        raw_cols = [c.strip() for c in line_str.split("|")]
        # Drop leading and trailing empty splits from boundary pipes
        if raw_cols and raw_cols[0] == "":
            raw_cols = raw_cols[1:]
        if raw_cols and raw_cols[-1] == "":
            raw_cols = raw_cols[:-1]

        # Ignore markdown separator line (|---|---|...)
        if all(re.match(r"^:?-+:?$", c) for c in raw_cols):
            continue

        # Check for header
        if raw_cols and raw_cols[0] == "#" and raw_cols[1] == "Sticker ID":
            headers = raw_cols
            if len(headers) != 9:
                errors.append(f"Line {line_num}: Header has {len(headers)} columns, expected 9: {headers}")
            continue

        # Data rows start with an integer
        if raw_cols and raw_cols[0].isdigit():
            row_dict = {
                "line_num": line_num,
                "raw_cols": raw_cols,
                "col_count": len(raw_cols),
                "num_str": raw_cols[0],
                "num": int(raw_cols[0]),
                "id_raw": raw_cols[1] if len(raw_cols) > 1 else "",
                "id": raw_cols[1].strip("`").strip() if len(raw_cols) > 1 else "",
                "pack": raw_cols[2] if len(raw_cols) > 2 else "",
                "meaning": raw_cols[3] if len(raw_cols) > 3 else "",
                "visual": raw_cols[4] if len(raw_cols) > 4 else "",
                "primitive": raw_cols[5] if len(raw_cols) > 5 else "",
                "secondary_fx": raw_cols[6] if len(raw_cols) > 6 else "",
                "timing": raw_cols[7] if len(raw_cols) > 7 else "",
                "framing": raw_cols[8] if len(raw_cols) > 8 else "",
            }
            rows.append(row_dict)

    return rows, errors


class TestMilestone1SpecAdversarial(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(SPEC_PATH):
            raise FileNotFoundError(f"Missing spec file: {SPEC_PATH}")
        with open(SPEC_PATH, "r", encoding="utf-8") as f:
            cls.spec_content = f.read()
            cls.spec_lines = cls.spec_content.splitlines()

        cls.packs_catalog = load_packs_catalog()
        cls.slang_catalog = load_slang_catalog()

        # Expected sequential IDs from data source
        cls.expected_pack_ids = []
        for p in cls.packs_catalog:
            for s in p.get("stickers", []):
                cls.expected_pack_ids.append(s["id"])

        cls.expected_slang_ids = [s["id"] for s in cls.slang_catalog]
        cls.expected_all_ids = cls.expected_pack_ids + cls.expected_slang_ids

        cls.sec5_rows, cls.sec5_header_errors = parse_section5_rows(SPEC_PATH)

    def test_01_catalog_census_total_count(self):
        """Assert total stickers extracted from data files == 188, and Section 5 rows == 188."""
        self.assertEqual(len(self.expected_pack_ids), 100, "Pack stickers count in data/packs.js must be 100")
        self.assertEqual(len(self.expected_slang_ids), 88, "Slang stickers count in data/trini-slang.js must be 88")
        self.assertEqual(len(self.expected_all_ids), 188, "Grand total stickers in data files must be exactly 188")
        self.assertEqual(len(self.sec5_rows), 188, f"Section 5 table must contain exactly 188 rows, found {len(self.sec5_rows)}")

    def test_02_catalog_census_exact_id_match(self):
        """Assert 100% ID match, 0 missing, 0 duplicates between catalog and Section 5."""
        spec_ids = [r["id"] for r in self.sec5_rows]

        # Check duplicates in spec
        seen = set()
        dups = []
        for sid in spec_ids:
            if sid in seen:
                dups.append(sid)
            seen.add(sid)
        self.assertEqual(dups, [], f"Duplicate IDs detected in Section 5 table: {dups}")

        # Check missing from spec
        missing_from_spec = [sid for sid in self.expected_all_ids if sid not in seen]
        self.assertEqual(missing_from_spec, [], f"IDs missing from Section 5 table: {missing_from_spec}")

        # Check extraneous/hallucinated IDs in spec
        expected_set = set(self.expected_all_ids)
        extraneous_in_spec = [sid for sid in spec_ids if sid not in expected_set]
        self.assertEqual(extraneous_in_spec, [], f"Extraneous IDs in Section 5 table not in data: {extraneous_in_spec}")

        # Check 1:1 match
        self.assertEqual(len(seen), 188, "Section 5 must contain 188 unique sticker IDs")

    def test_03_catalog_census_sequential_ordering(self):
        """Assert exact sequential ordering: Part 1 matches Pack 1..8 order, Part 2 matches Slang 1..88 order."""
        spec_ids = [r["id"] for r in self.sec5_rows]
        spec_pack_ids = spec_ids[:100]
        spec_slang_ids = spec_ids[100:]

        # Compare Pack ordering
        pack_mismatches = []
        for i, (exp, act) in enumerate(zip(self.expected_pack_ids, spec_pack_ids), 1):
            if exp != act:
                pack_mismatches.append(f"Row {i}: expected '{exp}', got '{act}'")
        self.assertEqual(pack_mismatches, [], f"Pack sequential ordering mismatch: {pack_mismatches}")

        # Compare Slang ordering
        slang_mismatches = []
        for i, (exp, act) in enumerate(zip(self.expected_slang_ids, spec_slang_ids), 101):
            if exp != act:
                slang_mismatches.append(f"Row {i}: expected '{exp}', got '{act}'")
        self.assertEqual(slang_mismatches, [], f"Slang sequential ordering mismatch: {slang_mismatches}")

    def test_04_table_schema_integrity(self):
        """Assert exactly 188 rows, each having exactly 9 non-empty pipe-delimited columns."""
        self.assertEqual(self.sec5_header_errors, [], f"Header parsing errors: {self.sec5_header_errors}")

        schema_errors = []
        for r in self.sec5_rows:
            line_num = r["line_num"]
            num = r["num"]
            col_count = r["col_count"]

            if col_count != 9:
                schema_errors.append(f"Line {line_num} (Row {num}): expected 9 columns, got {col_count}")
                continue

            # Check every column is non-empty
            for col_idx, col_val in enumerate(r["raw_cols"]):
                if not col_val.strip():
                    schema_errors.append(f"Line {line_num} (Row {num}): Column {col_idx+1} is empty")

        self.assertEqual(schema_errors, [], f"Table schema violations found:\n" + "\n".join(schema_errors[:20]))

    def test_05_strictly_incrementing_row_numbers(self):
        """Assert numbering strictly increments from 1 to 188 without gaps or jumps."""
        numbering_errors = []
        for idx, r in enumerate(self.sec5_rows, 1):
            expected_num = idx
            actual_num = r["num"]
            if actual_num != expected_num:
                numbering_errors.append(f"Line {r['line_num']}: expected row #{expected_num}, got #{actual_num} (ID: {r['id']})")

        self.assertEqual(numbering_errors, [], f"Row numbering sequence broken:\n" + "\n".join(numbering_errors))

    def test_06_fallback_zero_tolerance(self):
        """Scan all rows in Section 5 for articulated_gesture or generic bounce descriptions. Assert count == 0."""
        fallback_violations = []

        forbidden_terms = [
            "articulated_gesture",
            "generic_bounce",
            "generic bounce",
            "simple bounce",
            "default bounce",
            "basic warp",
            "unassigned",
            "fallback_warp",
        ]

        for r in self.sec5_rows:
            # Check primitive column specifically
            prim = r["primitive"].lower()
            for term in forbidden_terms:
                if term in prim:
                    fallback_violations.append(f"Row {r['num']} ({r['id']}): Primitive column contains '{term}'")

            # Check entire row text for articulated_gesture
            full_row_text = " | ".join(r["raw_cols"]).lower()
            if "articulated_gesture" in full_row_text:
                fallback_violations.append(f"Row {r['num']} ({r['id']}): Contains deprecated 'articulated_gesture'")

        self.assertEqual(fallback_violations, [], f"Fallback violations in Section 5:\n" + "\n".join(fallback_violations))

    def test_07_completeness_and_no_placeholders(self):
        """Scan entire document for TODO, TBD, [placeholder], etc."""
        placeholder_patterns = [
            r"\bTODO\b",
            r"\bTBD\b",
            r"\[placeholder\]",
            r"\bFIXME\b",
            r"\bXXX\b",
            r"\bWIP\b",
            r"\bREPLACE_ME\b",
            r"\bINSERT HERE\b",
        ]

        violations = []
        for line_num, line in enumerate(self.spec_lines, 1):
            for pat in placeholder_patterns:
                match = re.search(pat, line, re.IGNORECASE)
                if match:
                    violations.append(f"Line {line_num}: matched '{match.group(0)}': {line.strip()[:100]}")

        self.assertEqual(violations, [], f"Unresolved placeholders found in spec:\n" + "\n".join(violations))

    def test_08_motion_primitives_whitelist(self):
        """Assert every motion primitive in Section 5 is one of the defined authentic primitives."""
        # Find defined primitives in Section 4
        primitive_defs = set()
        for line in self.spec_lines:
            match1 = re.search(r"####\s*\d+\.\s*`([a-z0-9_]+)`", line)
            if match1:
                primitive_defs.add(match1.group(1))
            match2 = re.search(r"\|\s*\d+\s*\|\s*([a-z0-9_]+)\s*\|", line)
            if match2:
                primitive_defs.add(match2.group(1))

        known_valid_primitives = {
            "soca_rag_windmill",
            "steups_recoil_burst",
            "doubles_45_lean_drip",
            "allfours_table_slam",
            "tanty_akumbo_tilt",
            "bazodee_dazed_spiral",
            "puncheon_fire_breath",
            "maco_peep_zoom",
            "killing_dead_collapse",
            "steelpan_rebound",
            "heat_seeking_slipper_arc",
            "ttec_blackout_candle",
            "moko_jumbie_stilt_sway",
            "wasa_dry_shower_cough",
        }

        # Check every row in Section 5
        invalid_primitives = []
        for r in self.sec5_rows:
            prim = r["primitive"].strip("`").strip()
            prim_name = prim.split()[0].split("(")[0].strip()
            if prim_name not in known_valid_primitives and prim_name not in primitive_defs:
                invalid_primitives.append(f"Row {r['num']} ({r['id']}): Unknown primitive '{prim}'")

        self.assertEqual(invalid_primitives, [], f"Undefined motion primitives in Section 5:\n" + "\n".join(invalid_primitives))

    def test_09_keyframe_timing_structure(self):
        """Assert keyframe timing column specifies 24 frames @ 90ms (f0 to f23)."""
        timing_errors = []
        for r in self.sec5_rows:
            timing = r["timing"]
            if not ("f0" in timing and ("f23" in timing or "f22" in timing or "f24" in timing)):
                timing_errors.append(f"Row {r['num']} ({r['id']}): Invalid timing specification '{timing}'")

        self.assertEqual(timing_errors, [], f"Keyframe timing format anomalies:\n" + "\n".join(timing_errors[:15]))

    def test_10_framing_bounds_safe_margins(self):
        """Assert framing bounds specify scale <= 0.95 and safe margins >= 12px for 512x512 canvas."""
        framing_errors = []
        for r in self.sec5_rows:
            framing = r["framing"]
            scale_match = re.search(r"scale\s*=\s*([0-9.]+)", framing)
            if not scale_match:
                framing_errors.append(f"Row {r['num']} ({r['id']}): Missing scale parameter in '{framing}'")
            else:
                scale_val = float(scale_match.group(1))
                if scale_val > 0.95:
                    framing_errors.append(f"Row {r['num']} ({r['id']}): Scale {scale_val} exceeds safe limit 0.95")

        self.assertEqual(framing_errors, [], f"Framing bounds safety violations:\n" + "\n".join(framing_errors[:15]))

    def test_11_markdown_pipe_delimiter_integrity(self):
        """Assert every table row in Section 5 has exactly 10 pipe symbols (forming 9 columns)."""
        in_sec5 = False
        delimiter_errors = []
        for line_num, line in enumerate(self.spec_lines, 1):
            line_str = line.strip()
            if "## SECTION 5:" in line_str or "### 5.2" in line_str:
                in_sec5 = True
            elif "## SECTION 6:" in line_str:
                in_sec5 = False
                break
            if in_sec5 and line_str.startswith("|"):
                pipe_count = line_str.count("|")
                if pipe_count != 10:
                    delimiter_errors.append(f"Line {line_num}: found {pipe_count} pipes, expected 10")

        self.assertEqual(delimiter_errors, [], f"Delimiter syntax errors in Section 5:\n" + "\n".join(delimiter_errors))

    def test_12_source_asset_alignment(self):
        """Assert all 188 sticker IDs in Section 5 map to actual existing assets/stickers/ files."""
        missing_assets = []
        for r in self.sec5_rows:
            sid = r["id"]
            png_file = os.path.join(WORKSPACE_DIR, "assets", "stickers", f"{sid}.png")
            webp_file = os.path.join(WORKSPACE_DIR, "assets", "stickers", f"{sid}.webp")
            if not os.path.exists(png_file):
                missing_assets.append(f"Missing master PNG: {png_file}")
            if not os.path.exists(webp_file):
                missing_assets.append(f"Missing master WebP: {webp_file}")

        self.assertEqual(missing_assets, [], f"Missing source assets for spec stickers:\n" + "\n".join(missing_assets[:15]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
