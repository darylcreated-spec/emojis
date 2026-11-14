"""
tests/test_challenger_m2_it2_rapid_overwrite.py
===============================================
Challenger Rapid Overwrite & Concurrency Collision Test Harness:
1. 10 consecutive builds of 'mamaguy'
2. 10 consecutive builds of 'steups'
3. Concurrent overwrite race: simultaneous execution of builds targeting the same sticker.
Checks exit codes, file sizes, and 0 lock collisions.
"""

import os
import sys
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
PYTHON_EXE = os.path.join(WORKSPACE_DIR, ".venv", "Scripts", "python.exe")
SCRIPT_PATH = os.path.join(WORKSPACE_DIR, "scripts", "build_animated_stickers.py")


def run_single_sticker(sid: str) -> tuple[int, str, str]:
    cmd = [PYTHON_EXE, SCRIPT_PATH, "--sticker", sid]
    p = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    print("=== TEST PART 1: 10 CONSECUTIVE BUILDS OF MAMAGUY ===")
    mamaguy_errors = []
    for i in range(1, 11):
        t0 = time.time()
        code, out, err = run_single_sticker("mamaguy")
        dur = time.time() - t0
        if code != 0 or "OSError" in err or "PermissionError" in err or "Error" in err:
            print(f"  [RUN {i}/10 FAIL] mamaguy (exit {code}, {dur:.2f}s): {err.strip()}")
            mamaguy_errors.append((i, code, err))
        else:
            print(f"  [RUN {i}/10 PASS] mamaguy (exit {code}, {dur:.2f}s)")
    
    print("\n=== TEST PART 2: 10 CONSECUTIVE BUILDS OF STEUPS ===")
    steups_errors = []
    for i in range(1, 11):
        t0 = time.time()
        code, out, err = run_single_sticker("steups")
        dur = time.time() - t0
        if code != 0 or "OSError" in err or "PermissionError" in err or "Error" in err:
            print(f"  [RUN {i}/10 FAIL] steups (exit {code}, {dur:.2f}s): {err.strip()}")
            steups_errors.append((i, code, err))
        else:
            print(f"  [RUN {i}/10 PASS] steups (exit {code}, {dur:.2f}s)")

    print("\n=== TEST PART 3: CONCURRENT ADVERSARIAL OVERWRITE RACE (4 SIMULTANEOUS WORKERS ON STEUPS) ===")
    race_errors = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(run_single_sticker, "steups") for _ in range(4)]
        for idx, f in enumerate(futs):
            code, out, err = f.result()
            if code != 0 or "OSError" in err or "PermissionError" in err:
                print(f"  [RACE {idx+1}/4 FAIL] (exit {code}): {err.strip()}")
                race_errors.append((idx, code, err))
            else:
                print(f"  [RACE {idx+1}/4 PASS] (exit {code})")

    # Check files exist and non-zero
    for sid in ["mamaguy", "steups"]:
        w = os.path.join(WORKSPACE_DIR, "assets", "animated", f"{sid}.webp")
        g = os.path.join(WORKSPACE_DIR, "assets", "animated", f"{sid}.gif")
        if not os.path.exists(w) or os.path.getsize(w) == 0:
            print(f"[FATAL] {w} missing or 0 bytes!")
            sys.exit(1)
        if not os.path.exists(g) or os.path.getsize(g) == 0:
            print(f"[FATAL] {g} missing or 0 bytes!")
            sys.exit(1)

    total_failures = len(mamaguy_errors) + len(steups_errors) + len(race_errors)
    if total_failures > 0:
        print(f"\n[OVERWRITE STRESS FAILED]: {total_failures} runs failed!")
        sys.exit(1)
    else:
        print(f"\n[OVERWRITE STRESS PASSED]: All 20 consecutive runs + 4 concurrent race runs succeeded with 0 lock collisions or errors!")
        sys.exit(0)


if __name__ == "__main__":
    main()
