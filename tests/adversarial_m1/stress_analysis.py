import os
import sys
from collections import Counter

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
SPEC_PATH = os.path.join(WORKSPACE_DIR, "docs", "CULTURAL_ANIMATION_SPEC.md")

sys.path.insert(0, os.path.join(WORKSPACE_DIR, "tests", "adversarial_m1"))
from test_spec_adversarial import parse_section5_rows

rows, errors = parse_section5_rows(SPEC_PATH)

print(f"Total rows parsed: {len(rows)}")
primitives = [r["primitive"] for r in rows]
prim_counts = Counter(primitives)

print("\n--- Distribution of Primary Motion Primitives across 188 Stickers ---")
for prim, count in prim_counts.most_common():
    pct = (count / len(rows)) * 100
    print(f"{prim:<30}: {count:>3} ({pct:>5.1f}%)")

print(f"\nTotal distinct primitives used: {len(prim_counts)}")

# Check visual style tags and length metrics
print("\n--- Content Depth Metrics ---")
meaning_lengths = [len(r["meaning"]) for r in rows]
visual_lengths = [len(r["visual"]) for r in rows]
timing_lengths = [len(r["timing"]) for r in rows]
fx_lengths = [len(r["secondary_fx"]) for r in rows]

print(f"Meaning character length: min={min(meaning_lengths)}, max={max(meaning_lengths)}, avg={sum(meaning_lengths)/len(rows):.1f}")
print(f"Visual metaphor length: min={min(visual_lengths)}, max={max(visual_lengths)}, avg={sum(visual_lengths)/len(rows):.1f}")
print(f"Secondary FX length: min={min(fx_lengths)}, max={max(fx_lengths)}, avg={sum(fx_lengths)/len(rows):.1f}")
print(f"Keyframe timing length: min={min(timing_lengths)}, max={max(timing_lengths)}, avg={sum(timing_lengths)/len(rows):.1f}")

# Check uniqueness of meanings
unique_meanings = len(set(r["meaning"] for r in rows))
print(f"Unique cultural meanings: {unique_meanings} / {len(rows)}")

# Check uniqueness of visual metaphors
unique_visuals = len(set(r["visual"] for r in rows))
print(f"Unique visual metaphors: {unique_visuals} / {len(rows)}")

# Check uniqueness of secondary FX
unique_fx = len(set(r["secondary_fx"] for r in rows))
print(f"Unique secondary FX: {unique_fx} / {len(rows)}")
