with open("docs/CULTURAL_ANIMATION_SPEC.md", "r", encoding="utf-8") as f:
    text = f.read()

for term in ["ttec_blackout_candle", "moko_jumbie_stilt_sway", "wasa_dry_shower_cough", "wasa_taps_dry_rattle"]:
    count = text.count(term)
    print(f"Occurrences of '{term}': {count}")
    # find lines where it appears
    lines = [i+1 for i, line in enumerate(text.splitlines()) if term in line]
    print(f"  Lines: {lines}")
