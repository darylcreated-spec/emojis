# PeelOff E2E Test Infrastructure Specification

**Document Version**: 1.0.0  
**Target Environment**: Python 3.12+ (Pillow 13.0.0)  
**Location**: `TEST_INFRA.md` (Project Root)  
**Author**: E2E Testing Track (`test_writer_e2e_1`)  
**Scope**: 4-Tier End-to-End Opaque-Box Verification Harness for PeelOff Trinidad & Tobago Sticker Redesign

---

## 1. Architecture & Testing Philosophy

PeelOff is a client-side Progressive Web Application (PWA) and cross-platform sticker engine for 188 Trinidad & Tobago 3D cultural emojis and dialect expressions. The E2E test suite provides **opaque-box (black-box)** verification: it tests exclusively against public interfaces, observable artifacts, file format specifications, CLI entry points, and web application contracts without coupling tests to internal generator state or private helper implementations.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PEELOFF E2E TEST RUNNER                         │
│                       (tests/e2e/run_all_tests.py)                     │
│  CLI Flags: --tier [1-4] | --feature [F1-F10] | --strict | --report    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│    Tier 1    │             │    Tier 2    │             │  Tier 3 & 4  │
│Feature Cov   │             │Boundary &    │             │Cross-Feature │
│50 Tests      │             │Corner (50)   │             │& Real-World  │
└──────┬───────┘             └──────┬───────┘             └──────┬───────┘
       │                            │                            │
       └────────────────────────────┼────────────────────────────┘
                                    │
       ┌────────────────────────────┴────────────────────────────┐
       │             OPAQUE-BOX VERIFICATION TARGETS             │
       ├─────────────────────────────────────────────────────────┤
       │ • File Headers: RIFF/WEBP, VP8X, ANIM, ANMF chunks      │
       │ • WebP 3-byte little-endian duration in ANMF chunks     │
       │ • GIF89a header, Netscape 2.0 loop 0, 128-color card   │
       │ • Frame count (24), duration (90ms/frame = 2.16s loop)   │
       │ • Canvas bounds (512x512) and alpha integrity           │
       │ • Catalog schemas: data/packs.js & data/trini-slang.js  │
       │ • WhatsApp manifest: assets/contents.json               │
       │ • Web app contracts: index.html & app.js (?v=9)         │
       │ • Cultural Spec: docs/CULTURAL_ANIMATION_SPEC.md        │
       └─────────────────────────────────────────────────────────┘
```

---

## 2. The 4-Tier Test Matrix

The test suite is structured into four distinct verification tiers totaling **117 test cases**:

| Tier | Category | File | Count | Methodology & Scope |
|---|---|---|---|---|
| **Tier 1** | Feature Coverage | `tests/e2e/test_tier1_feature_coverage.py` | 50 | Category-partition testing covering features F1 through F10 (5 tests per feature). Verifies primary contracts and happy paths. |
| **Tier 2** | Boundary & Corner Cases | `tests/e2e/test_tier2_boundary_corner.py` | 50 | Boundary Value Analysis (BVA) and extreme corner cases for F1 through F10 (5 tests per feature). Tests min/max limits, zero values, overflow conditions, empty inputs. |
| **Tier 3** | Cross-Feature Interactions | `tests/e2e/test_tier3_cross_feature.py` | 12 | Pairwise integration tests validating handoffs, shared contracts, and state consistency across features. |
| **Tier 4** | Real-World Workflows | `tests/e2e/test_tier4_real_world.py` | 5 | End-to-end user workflows, CI build pipelines, sharing simulations, and self-healing recovery scenarios. |
| **Total** | Full E2E Harness | All Suites | **117** | Comprehensive, opaque-box verification exceeding the $\ge 115$ threshold. |

---

## 3. Feature Mapping (F1 through F10)

| ID | Feature Name | Primary Artifacts | Milestone | Scope & Test Focus |
|---|---|---|---|---|
| **F1** | Cultural Reference Guide | `docs/CULTURAL_ANIMATION_SPEC.md` | M1 | Formal documentation of Trini kinesics, emotional registers, comedic tropes, and complete 188-sticker matrix. |
| **F2** | Authentic Motion Primitives | `scripts/build_animated_stickers.py` | M2 | Procedural implementation of 12+ authentic Trini motion routines (soca rag windmill, steups recoil, doubles lean, all-fours slam, etc.). |
| **F3** | Individualized Rig Mapping | `scripts/build_animated_stickers.py` | M2 | Zero generic fallback (`articulated_gesture` count == 0); 100% bespoke mapping for all 188 stickers. |
| **F4** | Micro-Motion Hold & Frame Standardization | `scripts/build_animated_stickers.py`, Assets | M2 | Elimination of frame coalescing; full 24 frames @ 90ms (2.16s loop, loop=0) across all animations. |
| **F5** | Production Asset Generation | `assets/animated/*.webp`, `*.gif` | M3 | Dual-stream generation of 376 non-corrupt, 512×512 animated files (188 WebP + 188 GIF on #10141E card). |
| **F6** | Automated Animation Verifier | `scripts/verify_animated_stickers.py` | M3 | Standalone verification script validating headers, frames, dimensions, and loops with exit code 0/non-zero. |
| **F7** | Web App Animated Integration | `index.html`, `app.js`, `styles.css` | M4 | Smooth loading, toggling (`isAnimatedMode`), card grid rendering, and platform-specific sharing without omissions. |
| **F8** | WhatsApp Manifest Alignment | `assets/contents.json` | M4 | Valid multi-pack JSON schema, `animated_sticker_pack: true`, all 8 packs aligned, 3-30 stickers per pack. |
| **F9** | Comprehensive E2E Test Suite | `tests/e2e/run_all_tests.py` | M5 | Modular Python `unittest` runner executing Tiers 1-4 with summary reporting and pass/fail semantics. |
| **F10** | Adversarial Coverage Hardening | Test suite / generator CLI | M5 | Stress resilience, multi-worker concurrency, corrupt input rejection, memory bounds, and edge handling. |

---

## 4. Authoritative Catalog & Assets Inventory

1. **Catalogs**:
   - `data/packs.js`: Exactly **100 stickers** across 8 cultural packs:
     - Pack 1: `pack-1-social-slang` (18 stickers)
     - Pack 2: `pack-2-reactions-drama` (12 stickers)
     - Pack 3: `pack-3-food-belly` (12 stickers)
     - Pack 4: `pack-4-liming-allfours` (12 stickers)
     - Pack 5: `pack-5-carnival-mas` (12 stickers)
     - Pack 6: `pack-6-folklore` (10 stickers)
     - Pack 7: `pack-7-festivals` (12 stickers)
     - Pack 8: `pack-8-tobago-everyday` (12 stickers)
   - `data/trini-slang.js`: Exactly **88 stickers** across 6 categories:
     - Greetings & Links (14 stickers)
     - Co-Signs & Facts (12 stickers)
     - Disbelief & Comedy (16 stickers)
     - Attitude & Shade (17 stickers)
     - People & Drama (11 stickers)
     - Vibes, Belly & Money (18 stickers)
   - **Total Unique Sticker Catalog**: Exactly **188 stickers**.

2. **Asset Deliverables**:
   - `assets/animated/`: Exactly **376 files** (188 `.webp` + 188 `.gif`).
   - `assets/stickers/`: Exactly **376 static files** (188 `.png` + 188 `.webp`).
   - `assets/trays/`: Exactly **8 tray icons** (96×96 PNG).
   - `assets/contents.json`: Official WhatsApp multi-pack manifest.

---

## 5. Binary Format Specifications & Opaque Extraction

### 5.1 Animated WebP Specification
- Container: RIFF/WEBP.
- Chunk `VP8X`: Canvas size $512 \times 512$ (`width - 1 = 511`, `height - 1 = 511`). Flags: Animation bit (0x02), Alpha bit (0x10).
- Chunk `ANIM`: Background RGBA `(0, 0, 0, 0)`, Loop count `0x0000` (infinite).
- Chunks `ANMF`: Exactly 24 frames.
- **Pillow 13.0.0 Duration Quirk**: Pillow's `im.info.get('duration')` returns `None` for WebP files. The E2E test harness parses the 3-byte duration directly from the binary `ANMF` chunk header:
  ```python
  # ANMF payload starts at chunk_offset + 8
  # Frame duration (uint24 little-endian) is at offset +12 within chunk payload (+20 from chunk start)
  duration_ms = int.from_bytes(data[anmf_offset + 20 : anmf_offset + 23], "little")
  ```
  Expected duration: **90 ms** per frame ($24 \times 90\,\text{ms} = 2,160\,\text{ms}$).

### 5.2 Animated GIF Specification
- Signature: `GIF89a`.
- Logical Screen: $512 \times 512$.
- Palette: $\le 128$ colors quantized on `#10141E` (`(16, 20, 30, 255)`) dark studio card.
- Application Extension: `NETSCAPE2.0` with loop sub-block `0x0000` (infinite).
- Graphic Control Extension (GCE): Delay time = 9 cs = 90 ms (`0x09, 0x00`).
- Frames: Exactly 24 frames.

---

## 6. Progressive Testability Framework

During active milestone development, tests targeting future deliverables skip gracefully with diagnostic milestone tags:

```
Test Execution (Default Mode)
├── Milestone Deliverable Present -> Execute full assertions -> PASS / FAIL
└── Milestone Deliverable Absent  -> raise unittest.SkipTest("[Pending Milestone MX] ...") -> SKIPPED
```

### CLI Modes
1. **Default Progressive Mode**:
   ```bash
   python tests/e2e/run_all_tests.py
   ```
   Tests on uncompleted milestones report `SKIPPED`. Exit code is `0` if all active tests pass.
2. **Strict Release Mode (`--strict`)**:
   ```bash
   python tests/e2e/run_all_tests.py --strict
   ```
   All skips are intercepted and treated as **failures**. Exit code is `1` if any test is skipped or failed. Used as the final Milestone M5 gating mechanism.

---

## 7. Test Runner CLI Interface (`tests/e2e/run_all_tests.py`)

### Usage
```bash
# Run all 117 tests in progressive mode
python tests/e2e/run_all_tests.py

# Run a specific tier (1, 2, 3, or 4)
python tests/e2e/run_all_tests.py --tier 1

# Filter by feature (F1 through F10)
python tests/e2e/run_all_tests.py --feature F4

# Strict gating mode (skips treated as failures)
python tests/e2e/run_all_tests.py --strict

# Custom report output paths
python tests/e2e/run_all_tests.py --json test_summary.json --report test_report.md
```

### Exit Codes
- `0`: All executed tests passed (skips permitted in progressive mode).
- `1`: One or more tests failed or encountered errors (or skips occurred with `--strict`).
- `2`: Invalid CLI arguments or configuration error.

---

## 8. Directory Layout

```
tests/
└── e2e/
    ├── __init__.py                     # Package marker
    ├── test_helpers.py                 # Opaque helpers: binary parsers, catalog loaders, PIL safe ops
    ├── test_tier1_feature_coverage.py   # Tier 1: 50 tests (5 per F1-F10)
    ├── test_tier2_boundary_corner.py    # Tier 2: 50 tests (5 per F1-F10)
    ├── test_tier3_cross_feature.py     # Tier 3: 12 tests (Pairwise feature combinations)
    ├── test_tier4_real_world.py        # Tier 4: 5 tests (End-to-end scenarios & pipelines)
    ├── run_all_tests.py                # Standalone test runner and reporting engine
    ├── test_summary.json               # Generated machine-readable telemetry
    └── test_report.md                  # Generated human-readable markdown report
```
