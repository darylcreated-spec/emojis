import os
import sys

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
SPEC_PATH = os.path.join(WORKSPACE_DIR, "docs", "CULTURAL_ANIMATION_SPEC.md")

sys.path.insert(0, os.path.join(WORKSPACE_DIR, "tests", "adversarial_m1"))
from test_spec_adversarial import parse_section5_rows

sys.path.insert(0, os.path.join(WORKSPACE_DIR, "tests", "e2e"))
from test_helpers import load_packs_catalog, load_slang_catalog

packs = load_packs_catalog()
slang = load_slang_catalog()
rows, _ = parse_section5_rows(SPEC_PATH)

print("--- Sample Pack Stickers (Rows 1-5) ---")
for r in rows[:5]:
    print(f"#{r['num']:>3} ID={r['id']:<20} Pack={r['pack']:<40} Prim={r['primitive']}")

print("\n--- Sample Pack Stickers (Rows 96-100) ---")
for r in rows[95:100]:
    print(f"#{r['num']:>3} ID={r['id']:<20} Pack={r['pack']:<40} Prim={r['primitive']}")

print("\n--- Sample Slang Stickers (Rows 101-105) ---")
for r in rows[100:105]:
    print(f"#{r['num']:>3} ID={r['id']:<30} SlangCat={r['pack']:<30} Prim={r['primitive']}")

print("\n--- Sample Slang Stickers (Rows 184-188) ---")
for r in rows[183:188]:
    print(f"#{r['num']:>3} ID={r['id']:<30} SlangCat={r['pack']:<30} Prim={r['primitive']}")
