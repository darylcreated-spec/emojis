# Project: PeelOff Trinidad & Tobago Sticker Animation Redesign

## Architecture
PeelOff is a pure client-side PWA and cross-platform sticker engine for 188 Trinidad & Tobago 3D emojis and slang expressions.
- **Frontend Layer**: `index.html`, `styles.css`, `app.js` (vanilla ES6+ PWA). Card grids dynamically render animated WebPs (`assets/animated/[id].webp`) when `isAnimatedMode` is active. Mobile OS sharing routes animated GIFs (`assets/animated/[id].gif`) for multi-platform sticker playback.
- **Data Layer**:
  - `data/packs.js`: Defines 100 cultural pack stickers across 8 packs.
  - `data/trini-slang.js`: Defines 88 literal 3D slang stickers across 6 categories.
  - `assets/contents.json`: Official WhatsApp multi-pack manifest.
- **Asset Pipeline Layer**:
  - `scripts/build_animated_stickers.py`: Multiprocessing generator (Pillow 13.0.0) reading `assets/stickers/[id].png`, applying breathing room, procedural mesh warp transformations, comic easing curves, and authentic Trini motion primitives, exporting dual streams (24-frame looping WebP and dark card GIF).
  - `scripts/verify_animated_stickers.py`: Automated verification suite validating RIFF/WEBP and GIF89a headers, frame count (>= 24), timing (>= 2.0s), canvas dimensions (512x512), and zero corruption across all 376 animated files.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Cultural Reference Guide | Authoritative documentation of Trini kinesics, emotional registers, slang terms, comedic tropes, and motion primitives | M1 | ORIGINAL_REQUEST §R1 |
| F2 | Authentic Motion Primitives | Procedural implementation of 12+ authentic Trini motion routines (soca rag windmill, steups recoil, 45° doubles lean, all-fours slam, tanty akumbo, bazodee spiral, etc.) | M2 | ORIGINAL_REQUEST §R1, R2 |
| F3 | Individualized Rig Mapping | Replace generic `articulated_gesture` fallback so all 188 stickers have culturally tailored custom animations | M2 | ORIGINAL_REQUEST §R2 |
| F4 | Micro-Motion Hold & Frame Standardization | Eliminate 20/18-frame coalescing anomaly; ensure all 188 animations have full 24 frames @ 90ms (2.16s loop) | M2 | Survey Finding |
| F5 | Production Asset Generation | Generate all 376 animated files (188 .webp + 188 .gif) in `assets/animated/` with clean looping and visual quality | M3 | ORIGINAL_REQUEST §R3 |
| F6 | Automated Animation Verifier | Script validating headers, frame counts, dimensions, durations, and loop flags for all 376 assets | M3 | Acceptance Criteria |
| F7 | Web App Animated Integration | Ensure `app.js` and `index.html` load, render, toggle, and share all 188 stickers smoothly without omissions | M4 | ORIGINAL_REQUEST §R3 |
| F8 | WhatsApp Manifest Alignment | Update `assets/contents.json` with accurate pack metadata and animated sticker support flags | M4 | Survey Finding |
| F9 | Comprehensive E2E Test Suite | 4-Tier test suite covering feature coverage, boundaries, combinations, and real-world workloads | M5 | Project Pattern Dual Track |
| F10 | Adversarial Coverage Hardening | White-box adversarial testing (Tier 5) auditing uncovered paths and stress-testing performance | M5 | Project Pattern Dual Track |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Cultural Reference Guide & Animation Design Spec | Document full cultural mapping and kinesic motion specifications for all 188 stickers | none | DONE |
| M2 | Animation Generator Overhaul & Rig Redesign | Refactor `scripts/build_animated_stickers.py` with 12+ authentic motion primitives and individualized rigs for all 188 stickers | M1 | IN_PROGRESS |
| M3 | Batch Production & Automated Verification | Render all 376 animated assets (.webp & .gif) and implement automated validator `scripts/verify_animated_stickers.py` | M2 | PLANNED |
| M4 | Web App Integration & Manifest Alignment | Align `app.js`, `index.html`, and `assets/contents.json` for seamless animated sticker rendering and sharing | M3 | PLANNED |
| M5 | E2E Verification & Adversarial Hardening | Validate 100% pass rate across E2E Test Suite (Tiers 1-4) and execute Tier 5 adversarial stress testing | M4, E2E Track | PLANNED |

## Interface Contracts
### `scripts/build_animated_stickers.py` ↔ `assets/animated/`
- **Input**: `assets/stickers/{id}.png` (512×512 RGBA PNG)
- **Output 1**: `assets/animated/{id}.webp` (512×512 RGBA transparent WebP, 24 frames, duration 90ms/frame, loop=0, quality 76)
- **Output 2**: `assets/animated/{id}.gif` (512×512 128-color GIF on #10141E card, 24 frames, duration 90ms/frame, loop=0)
- **CLI**: `python scripts/build_animated_stickers.py [--sticker ID] [--pack PACK_ID] [--workers N]`

### `scripts/verify_animated_stickers.py` ↔ CI / Orchestrator
- **Invocation**: `python scripts/verify_animated_stickers.py`
- **Output**: Exit code 0 if all 376 files pass format, header, frame count (>= 24), timing (>= 2.0s), and dimension checks; non-zero on any defect.

### `app.js` ↔ Assets
- **Animated Mode URL**: `assets/animated/{id}.webp?v=9`
- **Share Sheet URL**: `assets/animated/{id}.gif?v=9`
- **Fallback URL**: `assets/stickers/{id}.webp?v=9`

## Code Layout
- `data/packs.js`: Pack catalog definitions (100 stickers)
- `data/trini-slang.js`: Slang catalog definitions (88 stickers)
- `assets/stickers/`: Master static PNG and WebP files
- `assets/animated/`: Master animated WebP and GIF files
- `scripts/build_animated_stickers.py`: Master animation generator
- `scripts/verify_animated_stickers.py`: Animation verification test runner
- `docs/CULTURAL_ANIMATION_SPEC.md`: Cultural Reference Guide & Animation Design Spec
- `tests/e2e/`: Opaque-box E2E test suite (Tiers 1-4)
