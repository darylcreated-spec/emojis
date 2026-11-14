"""
Milestone 1 Gate 2 Adversarial Verification Suite
Empirical challenger tests for patched docs/CULTURAL_ANIMATION_SPEC.md

Tests:
1. ID Sequential Matching: 188 sticker IDs in Section 5 match packs.js (100) and trini-slang.js (88) 100% in exact sequential order.
2. Table Schema Integrity: exactly 188 rows, each having exactly 9 non-empty pipe-delimited columns.
3. Fallback Zero-Tolerance: 0 occurrences of 'articulated_gesture' or generic bounce in Section 5.
4. Completeness & Formatting: 0 TODO, TBD, [placeholder], and 0 unclosed markdown blocks/fences.
5. Iteration 2 Patch Verification: loop boundary math, volume preservation, Gaussian envelope, and Section 7.3.2 verification script.
"""

import os
import sys
import re
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

        if "## SECTION 5:" in line_str or "### 5.2" in line_str:
            in_sec5 = True
        elif "## SECTION 6:" in line_str:
            in_sec5 = False
            break

        if not in_sec5:
            continue

        if not line_str.startswith("|"):
            continue

        raw_cols = [c.strip() for c in line_str.split("|")]
        if raw_cols and raw_cols[0] == "":
            raw_cols = raw_cols[1:]
        if raw_cols and raw_cols[-1] == "":
            raw_cols = raw_cols[:-1]

        # Ignore markdown separator line (|---|---|...)
        if all(re.match(r"^:?-+:?$", c) for c in raw_cols):
            continue

        # Header check
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


class TestMilestone1Gate2Adversarial(unittest.TestCase):

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

    def test_01_id_sequential_matching(self):
        """Assert 188 sticker IDs in Section 5 match packs.js (100) and trini-slang.js (88) 100% in exact sequential order."""
        self.assertEqual(len(self.expected_pack_ids), 100, "Pack stickers count in data/packs.js must be 100")
        self.assertEqual(len(self.expected_slang_ids), 88, "Slang stickers count in data/trini-slang.js must be 88")
        self.assertEqual(len(self.expected_all_ids), 188, "Total expected stickers must be 188")
        self.assertEqual(len(self.sec5_rows), 188, f"Section 5 must have exactly 188 rows, got {len(self.sec5_rows)}")

        spec_ids = [r["id"] for r in self.sec5_rows]

        # 1. Exact 100% match
        self.assertEqual(spec_ids, self.expected_all_ids, "Section 5 IDs do not match expected 188 IDs sequentially")

        # 2. Check no duplicates
        self.assertEqual(len(set(spec_ids)), 188, "Section 5 must have 188 distinct IDs")

        # 3. Check Pack 1..8 ordering in rows 1..100
        for idx, (exp, act) in enumerate(zip(self.expected_pack_ids, spec_ids[:100]), 1):
            self.assertEqual(exp, act, f"Row {idx} pack sticker ID mismatch: expected {exp}, got {act}")

        # 4. Check Slang 1..88 ordering in rows 101..188
        for idx, (exp, act) in enumerate(zip(self.expected_slang_ids, spec_ids[100:]), 101):
            self.assertEqual(exp, act, f"Row {idx} slang sticker ID mismatch: expected {exp}, got {act}")

    def test_02_table_schema_and_non_empty_columns(self):
        """Assert exactly 188 rows, each with 9 non-empty pipe-delimited columns and 10 pipes per line."""
        self.assertEqual(self.sec5_header_errors, [])
        self.assertEqual(len(self.sec5_rows), 188)

        empty_cell_violations = []
        col_count_violations = []
        numbering_violations = []

        for idx, r in enumerate(self.sec5_rows, 1):
            # Row numbering check
            if r["num"] != idx:
                numbering_violations.append(f"Row {idx}: expected #{idx}, got #{r['num']}")

            # Column count check
            if r["col_count"] != 9:
                col_count_violations.append(f"Row {r['num']} (Line {r['line_num']}): expected 9 cols, got {r['col_count']}")

            # Non-empty cell check
            for col_idx, col_val in enumerate(r["raw_cols"]):
                if not col_val.strip():
                    empty_cell_violations.append(f"Row {r['num']} (Line {r['line_num']}): Column {col_idx+1} is empty")

        self.assertEqual(numbering_violations, [], f"Row numbering sequence broken: {numbering_violations}")
        self.assertEqual(col_count_violations, [], f"Column count violations: {col_count_violations}")
        self.assertEqual(empty_cell_violations, [], f"Empty cell violations: {empty_cell_violations}")

        # Pipe delimiter count check (exactly 10 pipes per line in Section 5 tables)
        in_sec5 = False
        pipe_errors = []
        for line_num, line in enumerate(self.spec_lines, 1):
            line_str = line.strip()
            if "## SECTION 5:" in line_str or "### 5.2" in line_str:
                in_sec5 = True
            elif "## SECTION 6:" in line_str:
                in_sec5 = False
                break
            if in_sec5 and line_str.startswith("|"):
                pipes = line_str.count("|")
                if pipes != 10:
                    pipe_errors.append(f"Line {line_num}: {pipes} pipes found (expected 10)")

        self.assertEqual(pipe_errors, [], f"Section 5 table rows must each have 10 pipe delimiters: {pipe_errors}")

    def test_03_zero_tolerance_fallback_and_generic_bounce(self):
        """Assert 0 occurrences of 'articulated_gesture' or generic bounce descriptions in Section 5."""
        forbidden_in_sec5 = [
            "articulated_gesture",
            "generic_bounce",
            "generic bounce",
            "simple bounce",
            "default bounce",
            "basic bounce",
            "basic warp",
            "fallback_warp",
            "unassigned",
        ]

        sec5_violations = []
        for r in self.sec5_rows:
            full_row_str = " | ".join(r["raw_cols"]).lower()
            for term in forbidden_in_sec5:
                if term in full_row_str:
                    sec5_violations.append(f"Row {r['num']} ({r['id']}): contains '{term}'")

        self.assertEqual(sec5_violations, [], f"Forbidden fallback terms found in Section 5:\n" + "\n".join(sec5_violations))

        # Check document-wide occurrences of articulated_gesture: only allowed in deprecation mandates
        lines_with_ag = []
        for line_num, line in enumerate(self.spec_lines, 1):
            if "articulated_gesture" in line:
                lines_with_ag.append((line_num, line.strip()))

        for ln, text in lines_with_ag:
            lower = text.lower()
            self.assertTrue(
                "eliminate" in lower or "legacy" in lower or "deprecated" in lower or "replacement" in lower or "was" in lower or "zero" in lower,
                f"Line {ln} mentions articulated_gesture without deprecation context: {text}"
            )

    def test_04_completeness_and_unclosed_markdown_blocks(self):
        """Assert 0 occurrences of TODO, TBD, [placeholder], or unclosed markdown blocks."""
        # 1. Placeholders
        placeholder_regex = re.compile(r"\b(TODO|TBD|FIXME|XXX|WIP|REPLACE_ME)\b|\[placeholder\]", re.IGNORECASE)
        placeholder_matches = []
        for line_num, line in enumerate(self.spec_lines, 1):
            m = placeholder_regex.search(line)
            if m:
                placeholder_matches.append(f"Line {line_num}: matched '{m.group(0)}' in '{line.strip()[:80]}'")

        self.assertEqual(placeholder_matches, [], f"Unresolved placeholders found:\n" + "\n".join(placeholder_matches))

        # 2. Balanced markdown code fences (```)
        code_fence_count = 0
        fence_lines = []
        for line_num, line in enumerate(self.spec_lines, 1):
            if line.strip().startswith("```"):
                code_fence_count += 1
                fence_lines.append((line_num, line.strip()))

        self.assertEqual(
            code_fence_count % 2, 0,
            f"Unclosed markdown code block! Total code fence tags count is odd ({code_fence_count}). Fences: {fence_lines[-5:]}"
        )

        # 3. Check all python code blocks compile with 0 syntax errors
        py_blocks = re.findall(r"(?s)```python\n(.*?)```", self.spec_content)
        self.assertGreater(len(py_blocks), 0, "Expected at least one python code block in spec")
        for i, block in enumerate(py_blocks, 1):
            try:
                compile(block, f"<embedded_python_block_{i}>", "exec")
            except SyntaxError as e:
                self.fail(f"Embedded Python code block {i} failed to compile: {e}")

        # 4. Check for unclosed HTML tags outside code blocks
        # Strip all code blocks first
        non_code_text = re.sub(r"(?s)```.*?```", "", self.spec_content)
        non_code_text = re.sub(r"`[^`\n]+`", "", non_code_text)
        raw_html_open = re.findall(r"<(div|span|p|b|i|table|tr|td|th)\b[^>]*>", non_code_text, re.IGNORECASE)
        raw_html_close = re.findall(r"</(div|span|p|b|i|table|tr|td|th)>", non_code_text, re.IGNORECASE)
        self.assertEqual(len(raw_html_open), len(raw_html_close), f"Mismatched HTML tags: {len(raw_html_open)} open vs {len(raw_html_close)} close")

    def test_05_iteration2_patches_verification(self):
        """Verify the specific patches applied in Iteration 2."""
        # 1. Check Section 7.3.2 verification script is complete and has zero 'pass' stubs
        sec7_match = re.search(r"#### 7\.3\.2 Verification Test Routine Structure.*?(```python\n.*?\n```)", self.spec_content, re.DOTALL)
        self.assertIsNotNone(sec7_match, "Section 7.3.2 verification script block not found")
        sec7_code = sec7_match.group(1)
        for line in sec7_code.splitlines():
            self.assertFalse(
                re.match(r"^\s*pass\s*(#.*)?$", line),
                f"Section 7.3.2 verification script contains unexecutable pass stub: '{line}'"
            )
        self.assertIn("def verify_animated_file", sec7_code)
        self.assertIn("parse_webp_anmf_durations", sec7_code)

        # 2. Check Primitive 02 squash range updated to 0.82 – 1.29 in Table 4.4
        self.assertIn("0.82 – 1.29", self.spec_content, "Primitive 02 squash range not updated to 0.82 – 1.29 in Section 4.4 summary table")

        # 3. Check Gesture 11 (Lip Point) localized Gaussian envelope
        self.assertIn("w_{\\text{mouth}}(x, y)", self.spec_content, "Gesture 11 missing Gaussian oral envelope formula")
        self.assertIn("1.6807", self.spec_content, "Gesture 11 missing 3D z-axis extension commentary")

        # 4. Check Primitive 04 (doubles_45_lean_drip) loop boundary & snapback
        self.assertIn("L_{\\text{stub}}", self.spec_content, "Primitive 04 missing elastic wrapper stub snapback")
        self.assertIn("\\alpha_{\\text{drop}}", self.spec_content, "Primitive 04 missing alpha drop reset")

        # 5. Check Primitive 08 (heat_seeking_slipper_arc) zero-alpha trajectory reset
        self.assertIn("R_{\\text{flash}}", self.spec_content, "Primitive 08 missing flash radius specification")

        # 6. Check Primitive 10 (steelpan_rebound) 360 frequency multiplier
        self.assertIn("360.0", self.spec_content, "Primitive 10 missing 360.0 degree wave frequency multiplier")
        self.assertIn("\\alpha_{\\text{ring}}", self.spec_content, "Primitive 10 missing alpha ring reset")

        # 7. Check Primitive 12 (ttec_blackout_candle) T&TEC grid restoration
        self.assertIn("R_{\\text{glow}}", self.spec_content, "Primitive 12 missing candle glow specification")

        # 8. Check Primitive 14 (wasa_dry_shower_cough) off-canvas acceleration
        self.assertIn("2600.0", self.spec_content, "Primitive 14 missing gravity acceleration clearing canvas")


if __name__ == "__main__":
    unittest.main(verbosity=2)
