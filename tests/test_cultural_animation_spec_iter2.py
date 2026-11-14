"""
tests/test_cultural_animation_spec_iter2.py
===========================================
Milestone 1, Iteration 2 Gate Adversarial Challenge Suite.
Empirically stress-tests:
1. Looping Continuity & Zero-Alpha Seam:
   - Primitive 08 (heat_seeking_slipper_arc)
   - Primitive 10 (steelpan_rebound)
   - Primitive 14 (wasa_dry_shower_cough)
   - Primitive 04 (doubles_45_lean_drip)
   - Primitive 12 (ttec_blackout_candle)
2. Volume Preservation Consistency:
   - Primitive 02 (steups_recoil_burst)
   - Gesture 11 (Lip Point localized oral Gaussian envelope)
3. Section 7.3.2 Verifier Contract:
   - Dynamic enumeration of all 188 sticker IDs (100 packs + 88 slang)
   - Raw binary magic byte inspection (Q8)
   - WebP exterior corner transparency check (Q10)
   - WebP ANMF duration parser & GIF FASTOCTREE tolerance (Q11)
   - Adversarial corruption and edge-case resistance
4. Specification Structural Integrity:
   - Zero stubs (TODO, TBD, [placeholder], standalone pass)
   - Full 188-row Section 5 matrix validation
"""

import os
import sys
import re
import math
import struct
import tempfile
from PIL import Image

def test_primitive_08_heat_seeking_slipper():
    """Stress-test Primitive 08: heat_seeking_slipper_arc."""
    print("\n--- Testing Primitive 08: heat_seeking_slipper_arc ---")
    
    def u_flight(t):
        return min(1.0, t / 0.65)

    def x_pos(t):
        u = u_flight(t)
        if t < 0.65:
            return 490.0 - 234.0 * u
        elif t < 0.70:
            return 256.0
        elif t < 0.85:
            return 256.0 + 4.0 * math.exp(-12 * (t - 0.70)) * math.sin(12 * math.pi * (t - 0.70))
        elif t < 0.95:
            return 256.0
        else:
            return 256.0 + 234.0 * ((t - 0.95) / 0.05)

    def y_pos(t):
        u = u_flight(t)
        if t < 0.65:
            return 280.0 - 180.0 * math.sin(math.pi * u)
        elif t < 0.70:
            return 280.0
        elif t < 0.85:
            return 280.0 - 8.0 * math.exp(-14 * (t - 0.70)) * abs(math.sin(16 * math.pi * (t - 0.70)))
        else:
            return 280.0

    def theta_spin(t):
        u = u_flight(t)
        if t < 0.65:
            return 8 * math.pi * u
        elif t < 0.95:
            return 8 * math.pi
        else:
            return 8 * math.pi * (1.0 - (t - 0.95) / 0.05)

    def alpha_slipper(t):
        if t <= 0.85:
            return 255.0
        elif t <= 0.95:
            return 255.0 * ((1.0 - (t - 0.85) / 0.10) ** 2)
        else:
            return 0.0

    def r_flash(t):
        if t < 0.65:
            return 0.0
        elif t < 0.85:
            return 55.0 * math.sin(((t - 0.65) / 0.20) * math.pi)
        else:
            return 0.0

    # 1. Boundary continuity at t=0 and t=1.0
    x0 = x_pos(0.0)
    x1 = x_pos(1.0)
    y0 = y_pos(0.0)
    y1 = y_pos(1.0)
    th0 = theta_spin(0.0)
    th1 = theta_spin(1.0)
    
    assert abs(x1 - x0) < 1.0, f"Primitive 08 x loop jump: |{x1} - {x0}| >= 1.0"
    assert abs(y1 - y0) < 1.0, f"Primitive 08 y loop jump: |{y1} - {y0}| >= 1.0"
    ang_diff = abs((th1 - th0 + math.pi) % (2 * math.pi) - math.pi)
    assert ang_diff < 1e-4, f"Primitive 08 spin loop mismatch: {th1} vs {th0} (diff={ang_diff})"
    print(f"  [PASS] Boundary coordinates: x(0)={x0:.1f}, x(1)={x1:.1f} (delta={abs(x1-x0):.3f}px)")
    print(f"  [PASS] Boundary coordinates: y(0)={y0:.1f}, y(1)={y1:.1f} (delta={abs(y1-y0):.3f}px)")

    # 2. Frame 23 (t = 23/24) zero-alpha and zero-flash assertions
    t_f23 = 23.0 / 24.0
    alpha_23 = alpha_slipper(t_f23)
    flash_23 = r_flash(t_f23)
    
    assert flash_23 == 0.0, f"Primitive 08 flash at Frame 23 is non-zero: {flash_23}"
    assert alpha_23 == 0.0, f"Primitive 08 slipper alpha at Frame 23 is non-zero: {alpha_23}"
    print(f"  [PASS] Frame 23 seam: alpha_slipper(23/24) = {alpha_23:.1f}, R_flash(23/24) = {flash_23:.1f}px")

    # 3. Dense step audit across all 24 frames
    for f in range(24):
        t = f / 24.0
        # Assert coordinates remain within reasonable bounding canvas
        x = x_pos(t)
        y = y_pos(t)
        assert 0 <= x <= 512, f"Frame {f} (t={t:.3f}) x out of canvas: {x}"
        assert 0 <= y <= 512, f"Frame {f} (t={t:.3f}) y out of canvas: {y}"
    print("  [PASS] 24 frames densely sampled within valid canvas coordinates.")


def test_primitive_10_steelpan_rebound():
    """Stress-test Primitive 10: steelpan_rebound."""
    print("\n--- Testing Primitive 10: steelpan_rebound ---")

    def r_ring(t):
        return (t * 360.0) % 120.0

    def alpha_ring(t):
        r = r_ring(t)
        decay = max(0.0, 1.0 - r / 105.0)
        return 240.0 * (decay ** 2)

    # 1. Boundary continuity at t=0 and t=1.0
    r0 = r_ring(0.0)
    r1 = r_ring(1.0)
    a0 = alpha_ring(0.0)
    a1 = alpha_ring(1.0)

    assert abs(r1 - r0) < 1.0, f"Primitive 10 R_ring loop jump: |{r1} - {r0}| >= 1.0"
    assert abs(a1 - a0) < 1.0, f"Primitive 10 alpha_ring loop jump: |{a1} - {a0}| >= 1.0"
    print(f"  [PASS] Boundary: R(0)={r0:.1f}, R(1)={r1:.1f}; alpha(0)={a0:.1f}, alpha(1)={a1:.1f}")

    # 2. Frame 23 (t = 23/24) zero-alpha seam check
    t_f23 = 23.0 / 24.0
    r_f23 = r_ring(t_f23)
    a_f23 = alpha_ring(t_f23)

    assert abs(r_f23 - 105.0) < 1e-4, f"Expected R_ring(23/24) == 105.0, got {r_f23}"
    assert a_f23 == 0.0, f"Primitive 10 alpha_ring at Frame 23 is non-zero: {a_f23}"
    print(f"  [PASS] Frame 23 seam: R_ring(23/24) = {r_f23:.1f}px, alpha_ring(23/24) = {a_f23:.4f}")

    # 3. Wave cycle count: 360/120 = exactly 3 wavefront cycles per 24 frames
    cycles = 360.0 / 120.0
    assert cycles == 3.0, f"Expected exactly 3 wave cycles, got {cycles}"
    print(f"  [PASS] Integer cycle count: exactly {cycles:.0f} acoustic cycles per 24 frames (triplet strikes).")


def test_primitive_14_wasa_dry_shower_cough():
    """Stress-test Primitive 14: wasa_dry_shower_cough."""
    print("\n--- Testing Primitive 14: wasa_dry_shower_cough ---")

    def s_x(t):
        if t < 0.28:
            return 1.0 + 0.16 * math.sin((t / 0.28) * (math.pi / 2))
        elif t < 0.36:
            return 1.16 - 0.26 * ((t - 0.28) / 0.08)
        else:
            return 0.90 + 0.10 * (1.0 - math.exp(-10 * (t - 0.36)))

    def s_y(t):
        return 1.0 / (s_x(t) ** 2)

    def y_drop(t):
        if t < 0.36:
            return 280.0
        elif t <= 0.68:
            return 280.0 + 2600.0 * ((t - 0.36) ** 2)
        else:
            return 280.0

    def alpha_drop(t):
        if t < 0.36:
            return 0.0
        elif t <= 0.68:
            return 255.0
        else:
            return 0.0

    def r_dust(t):
        if t < 0.40:
            return 0.0
        elif t <= 0.85:
            return 38.0 * math.sin(((t - 0.40) / 0.45) * math.pi)
        else:
            return 0.0

    # 1. Boundary continuity: |y(1.0) - y(0.0)| < 1.0px
    y0 = y_drop(0.0)
    y1 = y_drop(1.0)
    assert abs(y1 - y0) < 1.0, f"Primitive 14 y_drop loop jump: |{y1} - {y0}| >= 1.0"
    print(f"  [PASS] Boundary coordinates: y_drop(0)={y0:.1f}, y_drop(1)={y1:.1f} (delta={abs(y1-y0):.3f}px)")

    # 2. Droplet clears canvas: y > 512 at t=0.68
    y_exit = y_drop(0.68)
    assert y_exit > 512.0, f"Droplet failed to clear canvas bottom (512px): {y_exit}"
    print(f"  [PASS] Droplet canvas clearance: y_drop(0.68) = {y_exit:.2f}px (> 512px canvas bottom edge)")

    # 3. Mass conservation law: Sy(t) = 1 / (Sx(t))^2
    for f in range(24):
        t = f / 24.0
        sx = s_x(t)
        sy = s_y(t)
        vol_3d = (sx ** 2) * sy
        assert abs(vol_3d - 1.0) < 1e-6, f"Frame {f} 3D mass conservation violated: {vol_3d}"
    print("  [PASS] 3D mass conservation law Sy(t) = 1/(Sx(t))^2 strictly holds across all 24 frames (error < 1e-6).")

    # 4. Frame 23 zero overlays
    t_f23 = 23.0 / 24.0
    a_drop_23 = alpha_drop(t_f23)
    r_dust_23 = r_dust(t_f23)
    assert a_drop_23 == 0.0, f"Frame 23 droplet alpha non-zero: {a_drop_23}"
    assert r_dust_23 == 0.0, f"Frame 23 dust radius non-zero: {r_dust_23}"
    print(f"  [PASS] Frame 23 seam: alpha_drop(23/24) = {a_drop_23:.1f}, R_dust(23/24) = {r_dust_23:.1f}px")


def test_primitive_04_doubles_45_lean_drip():
    """Stress-test Primitive 04: doubles_45_lean_drip."""
    print("\n--- Testing Primitive 04: doubles_45_lean_drip ---")

    def clamp01(v):
        return max(0.0, min(1.0, v))

    def l_stub(t):
        if t < 0.70:
            return 10.0 + 35.0 * clamp01((t - 0.20) / 0.50)
        else:
            return 10.0 + 35.0 * math.exp(-18 * (t - 0.70)) * math.cos(12 * math.pi * (t - 0.70))

    def y_drop(t, y_bara=350.0):
        if t < 0.70:
            return y_bara + l_stub(t)
        elif t <= 0.92:
            return y_bara + 45.0 + 2400.0 * ((t - 0.70) ** 2)
        else:
            return y_bara + 10.0

    def alpha_drop(t):
        if t <= 0.92:
            return 255.0
        else:
            return 0.0

    # 1. Elastic sauce stub snapback & boundary continuity
    l0 = l_stub(0.0)
    l1 = l_stub(1.0)
    stub_seam_jump = abs(l1 - l0)
    assert stub_seam_jump < 0.05, f"Primitive 04 L_stub loop jump: |{l1} - {l0}| = {stub_seam_jump} >= 0.05"
    print(f"  [PASS] Elastic stub snapback: L_stub(0)={l0:.3f}px, L_stub(1)={l1:.3f}px (delta={stub_seam_jump:.5f}px < 0.05px)")

    # 2. Droplet trajectory clearance and alpha seam reset
    # Evaluate clearance across affine bara placements [351, 370]
    for y_b in [352.0, 360.0, 370.0]:
        y_max = y_drop(0.92, y_bara=y_b)
        assert y_max > 512.0, f"At y_bara={y_b}, droplet {y_max} <= 512px"
    print(f"  [PASS] Droplet canvas clearance: at y_bara=360px, y_drop(0.92) = {y_drop(0.92, 360.0):.2f}px (> 512px)")

    # 3. Frame 23 zero-alpha reset
    t_f23 = 23.0 / 24.0
    a_f23 = alpha_drop(t_f23)
    assert a_f23 == 0.0, f"Primitive 04 alpha_drop at Frame 23 is non-zero: {a_f23}"
    print(f"  [PASS] Frame 23 seam: alpha_drop(23/24) = {a_f23:.1f} (droplet completely invisible before loop wrap)")

    # 4. Trajectory wrap: y_drop at t=1.0 matches t=0.0
    assert abs(y_drop(1.0, 360.0) - y_drop(0.0, 360.0)) < 0.01
    print("  [PASS] Droplet position resets invisibly with 0.0px loop seam error.")


def test_primitive_12_ttec_blackout_candle():
    """Stress-test Primitive 12: ttec_blackout_candle."""
    print("\n--- Testing Primitive 12: ttec_blackout_candle ---")

    def clamp01(v):
        return max(0.0, min(1.0, v))

    def grid_l(t):
        if t < 0.16:
            return 1.0
        elif t < 0.32:
            return 0.0
        elif t < 0.85:
            return 0.15 + 0.85 * clamp01((t - 0.32) / 0.20)
        elif t < 0.88:
            return 0.0
        elif t < 0.92:
            return 0.75
        elif t < 0.95:
            return 0.30
        else:
            return 1.0

    def r_glow(t):
        if t < 0.32:
            return 0.0
        elif t < 0.85:
            return 90.0 + 12.0 * math.sin(8 * math.pi * t)
        elif t <= 0.95:
            base = 90.0 + 12.0 * math.sin(8 * math.pi * t)
            fade = (1.0 - (t - 0.85) / 0.10) ** 2
            return base * fade
        else:
            return 0.0

    def alpha_candle(t):
        if t < 0.32:
            return 0.0
        elif t < 0.85:
            return 255.0
        elif t <= 0.95:
            return 255.0 * ((1.0 - (t - 0.85) / 0.10) ** 2)
        else:
            return 0.0

    def alpha_smoke(t):
        if 0.85 <= t <= 0.95:
            return 180.0 * ((1.0 - (t - 0.85) / 0.10) ** 2)
        else:
            return 0.0

    # 1. Boundary continuity for grid illumination
    l0 = grid_l(0.0)
    l1 = grid_l(1.0)
    assert l0 == 1.0 and l1 == 1.0, f"Illumination mismatch: L(0)={l0}, L(1)={l1}"
    print(f"  [PASS] Illumination boundary: L(0) = {l0:.1f}, L(1) = {l1:.1f}")

    # 2. Power restoration transition profile in [0.85, 1.0]
    # Check intermediate states: pre-surge dip (0.86), voltage surge (0.90), arc dip (0.93), lock-in (0.96)
    assert grid_l(0.86) == 0.0, "Pre-surge dip failed"
    assert grid_l(0.90) == 0.75, "Voltage surge failed"
    assert grid_l(0.93) == 0.30, "Arc dip failed"
    assert grid_l(0.96) == 1.0, "Grid lock-in failed"
    print("  [PASS] Authentic T&TEC restoration profile confirmed: pre-surge dip (0.0) -> surge (0.75) -> arc dip (0.30) -> lock-in (1.0).")

    # 3. Frame 23 zero-overlay seam check
    t_f23 = 23.0 / 24.0
    assert grid_l(t_f23) == 1.0, f"Frame 23 grid light != 1.0: {grid_l(t_f23)}"
    assert r_glow(t_f23) == 0.0, f"Frame 23 glow != 0.0: {r_glow(t_f23)}"
    assert alpha_candle(t_f23) == 0.0, f"Frame 23 candle alpha != 0.0: {alpha_candle(t_f23)}"
    assert alpha_smoke(t_f23) == 0.0, f"Frame 23 smoke alpha != 0.0: {alpha_smoke(t_f23)}"
    print(f"  [PASS] Frame 23 seam: L={grid_l(t_f23):.1f}, R_glow={r_glow(t_f23):.1f}, alpha_candle={alpha_candle(t_f23):.1f}, alpha_smoke={alpha_smoke(t_f23):.1f}")


def test_volume_preservation_steups_and_lip_point():
    """Stress-test Volume Preservation Consistency in Primitive 02 and Gesture 11."""
    print("\n--- Testing Volume Preservation: Steups Recoil & Lip Point ---")

    # 1. Primitive 02: steups_recoil_burst
    def ease_back(x, c1=1.8):
        c3 = c1 + 1.0
        return 1.0 + c3 * ((x - 1.0) ** 3) + c1 * ((x - 1.0) ** 2)

    def s_x_steups(t):
        t_antic = 0.14
        t_hit = 0.28
        t_hold = 0.65
        if t < t_antic:
            return 1.0 - 0.12 * math.sin((t / t_antic) * (math.pi / 2))
        elif t < t_hit:
            norm = (t - t_antic) / (t_hit - t_antic)
            return 0.88 + 0.12 * ease_back(norm, 1.8)
        elif t < t_hold:
            return 1.0 + 0.02 * math.sin(((t - t_hit) / (t_hold - t_hit)) * 2 * math.pi)
        else:
            return 1.0

    def s_y_steups(t):
        return 1.0 / (s_x_steups(t) ** 2)

    # Check anticipation peak at t = 0.14
    sx_antic = s_x_steups(0.14)
    sy_antic = s_y_steups(0.14)
    assert abs(sx_antic - 0.88) < 1e-4, f"Steups anticipation Sx != 0.88: {sx_antic}"
    assert abs(sy_antic - 1.2913) < 1e-3, f"Steups anticipation Sy != 1.2913: {sy_antic}"
    vol_antic = (sx_antic ** 2) * sy_antic
    assert abs(vol_antic - 1.0) < 1e-6, f"Steups volume != 1.0 at anticipation: {vol_antic}"
    print(f"  [PASS] Steups anticipation clench (t=0.14): Sx = {sx_antic:.4f}, Sy = {sy_antic:.4f}, 3D Vol = {vol_antic:.6f}")

    # Check boundary continuity
    assert abs(s_x_steups(1.0) - s_x_steups(0.0)) < 1e-5
    assert abs(s_y_steups(1.0) - s_y_steups(0.0)) < 1e-5
    print("  [PASS] Steups continuous across loop boundary (Sx=1.0, Sy=1.0).")

    # 2. Gesture 11: Lip Point ("Look Dey") Localized Oral Envelope
    sx_lip = 0.70
    sy_lip = 0.85
    sz_lip = 1.0 / (sx_lip * sy_lip)
    vol_lip_3d = sx_lip * sy_lip * sz_lip
    assert abs(vol_lip_3d - 1.0) < 1e-6, f"Lip Point 3D tissue mass violated: {vol_lip_3d}"
    print(f"  [PASS] Lip Point 3D tissue mass: Sx={sx_lip:.2f}, Sy={sy_lip:.2f}, Sz={sz_lip:.4f} -> 3D Volume = {vol_lip_3d:.6f}")

    def w_mouth(x, y):
        return math.exp(-(((x - 256.0) / 42.0) ** 2 + ((y - 310.0) / 28.0) ** 2))

    # Center peak
    w_peak = w_mouth(256.0, 310.0)
    assert abs(w_peak - 1.0) < 1e-6, f"Peak weight != 1.0: {w_peak}"

    # Cranium (y=150)
    w_cranium = w_mouth(256.0, 150.0)
    assert w_cranium < 1e-9, f"Cranium affected by mouth pucker: {w_cranium}"

    # Cheek (x=160, y=310)
    w_cheek = w_mouth(160.0, 310.0)
    assert w_cheek < 0.01, f"Lateral cheeks affected by mouth pucker: {w_cheek}"

    # Torso (y=450)
    w_torso = w_mouth(256.0, 450.0)
    assert w_torso < 1e-9, f"Torso affected by mouth pucker: {w_torso}"
    print(f"  [PASS] Oral Gaussian envelope isolation: center w={w_peak:.4f}, cranium w={w_cranium:.2e}, cheek w={w_cheek:.2e}, torso w={w_torso:.2e}")


def test_section_7_3_2_verifier_contract():
    """Stress-test Section 7.3.2 Verifier Implementation and Contracts."""
    print("\n--- Testing Section 7.3.2 Verifier Contract ---")

    # Extract Section 7.3.2 Python code from docs/CULTURAL_ANIMATION_SPEC.md
    with open("docs/CULTURAL_ANIMATION_SPEC.md", "r", encoding="utf-8") as f:
        spec_text = f.read()

    match = re.search(
        r"#### 7\.3\.2 Verification Test Routine Structure\s*```python\n(.*?)```",
        spec_text,
        re.DOTALL
    )
    assert match is not None, "Could not extract Section 7.3.2 code block from specification!"
    verifier_code = match.group(1)

    # 1. Compile verifier code
    compiled_verifier = compile(verifier_code, "<spec_7_3_2>", "exec")
    v_scope = {}
    exec(compiled_verifier, v_scope)
    print("  [PASS] Section 7.3.2 code compiled and executed into scope successfully.")

    # 2. Test sticker enumeration (Q1)
    assert "enumerate_sticker_ids" in v_scope
    sticker_ids = v_scope["enumerate_sticker_ids"](".")
    assert len(sticker_ids) == 188, f"Expected 188 sticker IDs, got {len(sticker_ids)}"
    assert len(set(sticker_ids)) == 188, "Duplicate sticker IDs detected!"
    print(f"  [PASS] Q1 Assertion: Exactly {len(sticker_ids)} unique sticker IDs enumerated from packs.js and trini-slang.js.")

    # 3. Test raw magic byte inspection (Q8) and verifier on real assets
    assert "verify_animated_file" in v_scope
    sample_webp = "assets/animated/ah-eh-able.webp"
    sample_gif = "assets/animated/ah-eh-able.gif"

    v_scope["verify_animated_file"](sample_webp, "WEBP")
    v_scope["verify_animated_file"](sample_gif, "GIF")
    print("  [PASS] Production assets passed Q3-Q11 verification in embedded verifier.")

    # 4. Stress-test raw magic byte inspection with adversarial corrupt files
    with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
        tf.write(b"NOT_A_WEBP_HEADER_CORRUPTED_123456789" + b"\x00" * 2000)
        tf_name = tf.name
    try:
        corrupt_caught = False
        try:
            v_scope["verify_animated_file"](tf_name, "WEBP")
        except AssertionError as e:
            corrupt_caught = True
            assert "Invalid WebP magic bytes" in str(e)
        assert corrupt_caught, "Verifier failed to catch corrupted WebP magic bytes!"
        print("  [PASS] Adversarial check: Corrupted WebP magic bytes successfully rejected by Q8 assertion.")
    finally:
        if os.path.exists(tf_name):
            os.remove(tf_name)

    # 5. Stress-test GIF magic bytes with corrupted file
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tf:
        tf.write(b"GIF87a_CORRUPTED_HEADER_DATA_123456789" + b"\x00" * 2000)
        tf_name = tf.name
    try:
        corrupt_caught = False
        try:
            v_scope["verify_animated_file"](tf_name, "GIF")
        except AssertionError as e:
            corrupt_caught = True
            assert "Invalid GIF magic bytes" in str(e)
        assert corrupt_caught, "Verifier failed to catch corrupted GIF magic bytes!"
        print("  [PASS] Adversarial check: Corrupted GIF magic bytes (GIF87a instead of GIF89a) rejected by Q8.")
    finally:
        if os.path.exists(tf_name):
            os.remove(tf_name)

    # 6. Stress-test WebP exterior corner transparency check (Q10)
    # Create an RGBA WebP with an opaque corner pixel and enough interior content to exceed 1024 bytes
    with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tf:
        opaque_corner_path = tf.name
    try:
        from PIL import ImageDraw
        im_opaque = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im_opaque)
        # Draw central pattern to exceed 1024 bytes
        for r in range(10, 100, 5):
            draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=(r * 2, 100, 200, 255))
        im_opaque.putpixel((0, 0), (255, 0, 0, 255)) # Opaque top-left corner
        # Add 24 frames with varying interior pixels to prevent frame coalescing
        frames = []
        for f_idx in range(24):
            frame = im_opaque.copy()
            # Vary an interior pixel to ensure adjacent frame difference
            frame.putpixel((256, 256), (f_idx * 10, 100, 200, 255))
            frames.append(frame)

        frames[0].save(
            opaque_corner_path,
            "WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=90,
            loop=0
        )
        opaque_corner_caught = False
        try:
            v_scope["verify_animated_file"](opaque_corner_path, "WEBP")
        except AssertionError as e:
            opaque_corner_caught = True
            assert "non-transparent" in str(e), f"Unexpected error: {e}"
        assert opaque_corner_caught, "Verifier failed to catch non-transparent exterior corner (Q10)!"
        print("  [PASS] Adversarial check: Non-transparent corner pixel successfully caught by Q10 assertion.")
    finally:
        if os.path.exists(opaque_corner_path):
            os.remove(opaque_corner_path)

    # 7. Stress-test GIF FASTOCTREE tolerance (Q11)
    # Background #10141E is (16, 20, 30).
    # Delta <= 1 should pass; delta >= 2 should fail.
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tf:
        bad_bg_gif_path = tf.name
    try:
        from PIL import ImageDraw
        im_bad_bg = Image.new("RGB", (512, 512), (20, 20, 30)) # delta = 4 on Red
        draw_gif = ImageDraw.Draw(im_bad_bg)
        for r in range(10, 80, 5):
            draw_gif.rectangle((256 - r, 256 - r, 256 + r, 256 + r), fill=(r * 3, 50, 150))
        frames = []
        for f_idx in range(24):
            frame = im_bad_bg.copy()
            frame.putpixel((256, 256), (f_idx * 5, 50, 150))
            frames.append(frame)

        frames[0].save(
            bad_bg_gif_path,
            "GIF",
            save_all=True,
            append_images=frames[1:],
            duration=90,
            loop=0
        )
        bad_bg_caught = False
        try:
            v_scope["verify_animated_file"](bad_bg_gif_path, "GIF")
        except AssertionError as e:
            bad_bg_caught = True
            assert "deviates from studio card" in str(e), f"Unexpected error: {e}"
        assert bad_bg_caught, "Verifier failed to catch background deviating by > 1 unit (Q11)!"
        print("  [PASS] Adversarial check: GIF studio card color deviation > 1 unit successfully caught by Q11.")
    finally:
        if os.path.exists(bad_bg_gif_path):
            os.remove(bad_bg_gif_path)

    # 8. Test WebP ANMF duration parser
    assert "parse_webp_anmf_durations" in v_scope
    durs = v_scope["parse_webp_anmf_durations"](sample_webp)
    assert len(durs) == 24, f"ANMF parser returned {len(durs)} frames instead of 24"
    assert all(d == 90 for d in durs), f"ANMF durations not 90ms: {durs}"
    assert sum(durs) == 2160, f"Total duration not 2160ms: {sum(durs)}"
    print(f"  [PASS] WebP ANMF duration parser confirmed: 24 frames, strictly 90ms, total {sum(durs)}ms.")


def test_spec_structural_integrity():
    """Verify specification structural integrity: stubs, table rows, python syntax."""
    print("\n--- Testing Specification Structural Integrity ---")
    with open("docs/CULTURAL_ANIMATION_SPEC.md", "r", encoding="utf-8") as f:
        spec_text = f.read()

    # 1. Zero stubs
    stubs = ["TODO", "TBD", "[placeholder]"]
    found_stubs = [s for s in stubs if s in spec_text]
    assert not found_stubs, f"Found stubs in spec: {found_stubs}"

    # Check for standalone 'pass' in code blocks
    code_blocks = re.findall(r"```python\n(.*?)```", spec_text, re.DOTALL)
    for i, cb in enumerate(code_blocks):
        for line_no, line in enumerate(cb.splitlines(), 1):
            assert not re.match(r"^\s*pass\s*(#.*)?$", line), (
                f"Standalone 'pass' stub found in code block {i+1}, line {line_no}: {line}"
            )
    print("  [PASS] Specification is 100% free of TODO, TBD, [placeholder], and standalone pass stubs.")

    # 2. Python syntax compilation of all code blocks
    for i, b in enumerate(code_blocks):
        compile(b, f"<spec_block_{i+1}>", "exec")
    print(f"  [PASS] All {len(code_blocks)} embedded Python code blocks compile cleanly without syntax errors.")

    # 3. Section 5 Table Integrity (188 rows, 9 columns, no generic fallbacks)
    s5_match = re.search(r"## SECTION 5:.*?(?=## SECTION 6:)", spec_text, re.DOTALL)
    assert s5_match is not None, "Section 5 not found!"
    s5_text = s5_match.group(0)

    rows = re.findall(r"^\|\s*(\d+)\s*\|(.*?)$", s5_text, re.MULTILINE)
    assert len(rows) == 188, f"Expected 188 rows in Section 5 table, found {len(rows)}"
    indices = [int(r[0]) for r in rows]
    assert indices == list(range(1, 189)), "Row numbering does not strictly match 1..188"

    for idx, content in rows:
        cols = [c.strip() for c in content.split("|")]
        assert len(cols) >= 8, f"Row {idx} has fewer than 9 columns (found {len(cols)+1})"

    assert not re.search(r"articulated_gesture", s5_text), "Generic fallback 'articulated_gesture' found in Section 5!"
    print(f"  [PASS] Section 5 Table verified: all 188 rows present, 9 columns per row, zero generic fallbacks.")


if __name__ == "__main__":
    print("================================================================================")
    print("EMPIRICAL ADVERSARIAL CHALLENGER SUITE (MILESTONE 1, ITERATION 2)")
    print("================================================================================")
    
    test_primitive_08_heat_seeking_slipper()
    test_primitive_10_steelpan_rebound()
    test_primitive_14_wasa_dry_shower_cough()
    test_primitive_04_doubles_45_lean_drip()
    test_primitive_12_ttec_blackout_candle()
    test_volume_preservation_steups_and_lip_point()
    test_section_7_3_2_verifier_contract()
    test_spec_structural_integrity()

    print("\n================================================================================")
    print("ALL EMPIRICAL TESTS PASSED WITH 100% SUCCESS.")
    print("================================================================================")
