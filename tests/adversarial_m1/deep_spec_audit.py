import re

spec_path = "docs/CULTURAL_ANIMATION_SPEC.md"
with open(spec_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in spec: {len(lines)}")

# 1. Search for placeholders
placeholders = ["TODO", "TBD", "[placeholder]", "FIXME", "XXX", "WIP", "REPLACE_ME", "DRAFT", "LOREM IPSUM"]
found_placeholders = []
for i, line in enumerate(lines, 1):
    for ph in placeholders:
        if ph in line:
            found_placeholders.append((i, ph, line.strip()))

print(f"Found placeholders count: {len(found_placeholders)}")
for fp in found_placeholders:
    print(f"  Line {fp[0]}: [{fp[1]}] {fp[2]}")

# 2. Check all markdown tables in the entire file
table_errors = []
in_table = False
expected_cols = None
table_start = 0

for i, line in enumerate(lines, 1):
    line_s = line.strip()
    if line_s.startswith("|"):
        cols = [c.strip() for c in line_s.split("|")]
        if cols and cols[0] == "":
            cols = cols[1:]
        if cols and cols[-1] == "":
            cols = cols[:-1]
        
        if not in_table:
            in_table = True
            table_start = i
            expected_cols = len(cols)
            # print(f"Table starting at line {i} with {expected_cols} columns")
        else:
            # Check separator row or data row
            if all(re.match(r"^:?-+:?$", c) for c in cols):
                if len(cols) != expected_cols:
                    table_errors.append(f"Line {i}: Separator has {len(cols)} columns, expected {expected_cols} (table started at {table_start})")
            else:
                if len(cols) != expected_cols:
                    table_errors.append(f"Line {i}: Data row has {len(cols)} columns, expected {expected_cols} (table started at {table_start})")
    else:
        in_table = False
        expected_cols = None

print(f"\nMarkdown Table Consistency Errors across ENTIRE document: {len(table_errors)}")
for te in table_errors:
    print(f"  {te}")

# 3. Check Section Structure and Table of Contents Alignment
toc_anchors = []
for line in lines[14:50]:
    matches = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", line)
    for title, anchor in matches:
        toc_anchors.append((title, anchor))

print(f"\nFound {len(toc_anchors)} Table of Contents links.")
# Verify headings exist in text
full_text = "".join(lines)
missing_anchors = []
for title, anchor in toc_anchors:
    # generate anchor from actual headings
    # simple check: check if anchor slug words exist in document
    anchor_words = anchor.split("-")
    if not all(w in full_text.lower() for w in anchor_words if len(w) > 2):
        missing_anchors.append((title, anchor))

print(f"Missing anchor topics: {missing_anchors}")
