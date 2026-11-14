"""
Adversarial Verification Suite for docs/CULTURAL_ANIMATION_SPEC.md
Empirically tests:
1. Looping Continuity & Boundary Conditions for 14 procedural motion primitives
2. Volume Preservation Integrity
3. Micro-Motion Living Hold Efficacy against Pillow frame coalescing
4. Acceptance Criteria & Verifier Feasibility (Section 7 contract)
"""

import os
import sys
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image, ImageChops

def test_1_looping_continuity():
    print("=" * 80)
    print("TEST 1: LOOPING CONTINUITY & BOUNDARY CONDITIONS (14 PRIMITIVES)")
    print("=" * 80)
    
    findings = []
    
    # Primitives and their mathematical trajectories over t in [0, 1]
    # We sample 24 frames: t_k = k / 24 for k = 0..23, plus t = 1.0 (frame 24 / loop point)
    
    # 1. soca_rag_windmill
    def p1(t):
        th = 2 * math.pi * t
        xh = 256 + 110 * math.cos(th)
        yh = 180 + 38 * math.sin(th)
        xc = 256 + 110 * math.cos(th - 0.52)
        yc = 180 + 38 * math.sin(th - 0.52) + 15 * math.sin(2 * th)
        return {"x_hand": xh, "y_hand": yh, "x_cloth": xc, "y_cloth": yc}
    
    # 2. steups_recoil_burst
    def p2(t):
        def clamp01(u): return max(0.0, min(1.0, u))
        def ease_out_back(u, s=1.8):
            u_ = clamp01(u) - 1.0
            return 1.0 + (s + 1.0) * (u_ ** 3) + s * (u_ ** 2)
        def ease_cubic(u):
            u_ = clamp01(u)
            return 4.0 * u_**3 if u_ < 0.5 else 1.0 - ((-2.0 * u_ + 2.0)**3) / 2.0
            
        t_antic, t_hit, t_hold = 0.14, 0.28, 0.65
        if t < t_antic:
            pt = -0.35 * math.sin((t / t_antic) * math.pi * 0.5)
        elif t < t_hit:
            pt = -0.35 + 1.35 * ease_out_back((t - t_antic) / (t_hit - t_antic), 1.8)
        elif t < t_hold:
            pt = 1.0 + 0.06 * math.sin(((t - t_hit) / (t_hold - t_hit)) * 2 * math.pi)
        else:
            pt = 1.0 - ease_cubic((t - t_hold) / (1.0 - t_hold))
            
        sy = 1.0 + 0.12 * pt
        sx = 1.0 / math.sqrt(sy)
        dy_neck = -16.0 * max(0.0, pt)
        th_head = -12.0 * pt
        r_puff = 0.0
        if 0.28 <= t <= 0.68:
            r_puff = 8.0 + 42.0 * ((t - 0.28) / 0.40)
        return {"pt": pt, "sy": sy, "sx": sx, "dy_neck": dy_neck, "th_head": th_head, "r_puff": r_puff}
        
    # 3. allfours_table_slam
    def p3(t):
        if t < 0.25:
            y_arm = -50.0 * math.sin((t / 0.25) * (math.pi / 2))
        elif t < 0.37:
            y_arm = -50.0 + 85.0 * (((t - 0.25) / 0.12) ** 2)
        else:
            y_arm = 35.0 * math.exp(-12 * (t - 0.37)) * math.cos(8 * math.pi * (t - 0.37))
            
        if t < 0.37:
            sh_x, sh_y = 0.0, 0.0
            sy = 1.0
        elif abs(t - 0.37) < 1e-5:
            sh_x = 12.0 * math.exp(-18 * (t - 0.37)) * math.sin(95 * (t - 0.37))
            sh_y = 8.0 * math.exp(-18 * (t - 0.37)) * math.cos(110 * (t - 0.37))
            sy = 0.68
        else:
            sh_x = 12.0 * math.exp(-18 * (t - 0.37)) * math.sin(95 * (t - 0.37))
            sh_y = 8.0 * math.exp(-18 * (t - 0.37)) * math.cos(110 * (t - 0.37))
            sy = 1.0 + 0.15 * math.exp(-14 * (t - 0.37)) * math.cos(25 * (t - 0.37))
            
        return {"y_arm": y_arm, "sh_x": sh_x, "sh_y": sh_y, "sy": sy}

    # 4. doubles_45_lean_drip
    def p4(t):
        def clamp01(u): return max(0.0, min(1.0, u))
        y_jaw = 6.0 * abs(math.sin(4 * math.pi * t))
        s_jaw = 1.0 + 0.04 * math.sin(4 * math.pi * t)
        l_drip = 10.0 + 35.0 * clamp01((t - 0.20) / 0.50)
        y_bara = 300.0
        if t < 0.70:
            y_drop = y_bara + l_drip
        else:
            y_drop = y_bara + 45.0 + 120.0 * ((t - 0.70) ** 2)
        return {"y_jaw": y_jaw, "s_jaw": s_jaw, "l_drip": l_drip, "y_drop": y_drop}

    # 5. tanty_akumbo_tilt
    def p5(t):
        th_hip = 14.0 * math.sin(2 * math.pi * t)
        th_neck = -18.0 * math.sin(2 * math.pi * t + 0.35)
        dx_pelvis = 16.0 * math.sin(2 * math.pi * t)
        dy_bob = -6.0 * abs(math.cos(2 * math.pi * t))
        th_finger = 22.0 * math.sin(6 * math.pi * t)
        return {"th_hip": th_hip, "th_neck": th_neck, "dx_pelvis": dx_pelvis, "dy_bob": dy_bob, "th_finger": th_finger}

    # 6. bazodee_dazed_spiral
    def p6(t):
        x_sway = 22.0 * math.sin(2 * math.pi * t)
        y_sway = 12.0 * math.sin(4 * math.pi * t)
        star0_x = 256 + 105 * math.cos(2 * math.pi * t)
        star0_y = 90 + 22 * math.sin(2 * math.pi * t)
        return {"x_sway": x_sway, "y_sway": y_sway, "star0_x": star0_x, "star0_y": star0_y}

    # 7. maco_peep_zoom
    def p7(t):
        def ease_in_back(u, s=1.7):
            return (s + 1.0) * (u ** 3) - s * (u ** 2)
        def ease_out_back(u, s=1.8):
            u_ = max(0.0, min(1.0, u)) - 1.0
            return 1.0 + (s + 1.0) * (u_ ** 3) + s * (u_ ** 2)
            
        if t < 0.25:
            y_creep = -30.0 * ((t / 0.25) ** 3)
            s_lens = 1.0
            x_pan = 0.0
        elif t < 0.40:
            y_creep = -30.0
            s_lens = 1.0 + 0.35 * ease_out_back((t - 0.25) / 0.15, 1.8)
            x_pan = 0.0
        elif t < 0.75:
            y_creep = -30.0
            s_lens = 1.35 + 0.05 * math.sin(10 * math.pi * t)
            x_pan = 18.0 * math.sin(((t - 0.40) / 0.35) * 2 * math.pi)
        else:
            y_creep = -30.0 + 30.0 * ease_in_back((t - 0.75) / 0.25, 1.7)
            s_lens = 1.0
            x_pan = 0.0
        return {"y_creep": y_creep, "s_lens": s_lens, "x_pan": x_pan}

    # 8. heat_seeking_slipper_arc
    def p8(t):
        u = t / 0.65 if t < 0.65 else 1.0
        x_pos = 490.0 - 234.0 * u
        y_pos = 280.0 - 180.0 * math.sin(math.pi * u)
        th_spin = 8 * math.pi * u
        r_flash = 0.0 if t < 0.65 else 55.0 * math.sin(((t - 0.65) / 0.35) * math.pi)
        return {"x_pos": x_pos, "y_pos": y_pos, "th_spin": th_spin, "r_flash": r_flash}

    # 9. puncheon_fire_breath
    def p9(t):
        if t < 0.22:
            sy = 1.0 + 0.18 * math.sin((t / 0.22) * (math.pi / 2))
        elif t < 0.34:
            sy = 1.18 - 0.38 * ((t - 0.22) / 0.12)
        else:
            sy = 0.80 + 0.20 * (1.0 - math.exp(-8 * (t - 0.34)))
            
        r_flame = 0.0
        if 0.24 <= t <= 0.69:
            r_flame = 85.0 * math.sin(((t - 0.24) / 0.45) * math.pi)
            
        dx_cough = 0.0
        if t >= 0.69:
            dx_cough = 7.0 * math.sin(16 * math.pi * t) * math.exp(-5 * (t - 0.69))
            
        return {"sy": sy, "r_flame": r_flame, "dx_cough": dx_cough}

    # 10. steelpan_rebound
    def p10(t):
        tau = (t * 3.0) % 1.0
        if tau < 0.3:
            y_mallet = -28.0 * (1.0 - tau / 0.3)
        else:
            y_mallet = -28.0 * math.sin(((tau - 0.3) / 0.7) * math.pi) * math.exp(-3.5 * tau)
            
        r_ring = (t * 180.0) % 120.0
        alpha_ring = 240.0 * (1.0 - r_ring / 120.0)
        return {"tau": tau, "y_mallet": y_mallet, "r_ring": r_ring, "alpha_ring": alpha_ring}

    # 11. killing_dead_collapse
    def p11(t):
        th_torso = -24.0 + 8.0 * math.sin(6 * math.pi * t)
        dy_laugh = 18.0 + 10.0 * abs(math.cos(6 * math.pi * t))
        sy = 1.0 + 0.12 * math.cos(6 * math.pi * t)
        mod2 = (t * 2.0) % 1.0
        x_tear = 256.0 + 25.0 + 110.0 * mod2
        y_tear = 256.0 - 20.0 * math.sin(math.pi * mod2) + 65.0 * (mod2 ** 2)
        return {"th_torso": th_torso, "dy_laugh": dy_laugh, "sy": sy, "x_tear": x_tear, "y_tear": y_tear}

    # 12. ttec_blackout_candle
    def p12(t):
        def clamp01(u): return max(0.0, min(1.0, u))
        if t < 0.16:
            L = 1.0
        elif t < 0.32:
            L = 0.0
        else:
            L = 0.15 + 0.85 * clamp01((t - 0.32) / 0.20)
        r_flash = 45.0 * math.exp(-25 * (t - 0.32)) if t >= 0.32 else 0.0
        th_flame = 4.0 * math.sin(14 * math.pi * t) + 2.0 * math.sin(33 * math.pi * t)
        r_glow = 90.0 + 12.0 * math.sin(8 * math.pi * t)
        return {"L": L, "r_flash": r_flash, "th_flame": th_flame, "r_glow": r_glow}

    # 13. moko_jumbie_stilt_sway
    def p13(t):
        th_sway = 15.0 * math.sin(2 * math.pi * t)
        dy_left = -24.0 * max(0.0, math.sin(2 * math.pi * t))
        dy_right = -24.0 * max(0.0, -math.sin(2 * math.pi * t))
        dx_torso = -12.0 * math.sin(2 * math.pi * t)
        return {"th_sway": th_sway, "dy_left": dy_left, "dy_right": dy_right, "dx_torso": dx_torso}

    # 14. wasa_dry_shower_cough
    def p14(t):
        if t < 0.28:
            sx = 1.0 + 0.16 * math.sin((t / 0.28) * (math.pi / 2))
        elif t < 0.36:
            sx = 1.16 - 0.26 * ((t - 0.28) / 0.08)
        else:
            sx = 0.90 + 0.10 * (1.0 - math.exp(-10 * (t - 0.36)))
            
        if t < 0.36:
            y_drop = 280.0
        elif t <= 0.64:
            y_drop = 280.0 + 190.0 * (((t - 0.36) / 0.28) ** 2)
        else:
            y_drop = 470.0
            
        r_dust = 0.0
        if 0.40 <= t <= 0.85:
            r_dust = 38.0 * math.sin(((t - 0.40) / 0.45) * math.pi)
            
        return {"sx": sx, "y_drop": y_drop, "r_dust": r_dust}

    primitives = [
        ("01_soca_rag_windmill", p1),
        ("02_steups_recoil_burst", p2),
        ("03_allfours_table_slam", p3),
        ("04_doubles_45_lean_drip", p4),
        ("05_tanty_akumbo_tilt", p5),
        ("06_bazodee_dazed_spiral", p6),
        ("07_maco_peep_zoom", p7),
        ("08_heat_seeking_slipper_arc", p8),
        ("09_puncheon_fire_breath", p9),
        ("10_steelpan_rebound", p10),
        ("11_killing_dead_collapse", p11),
        ("12_ttec_blackout_candle", p12),
        ("13_moko_jumbie_stilt_sway", p13),
        ("14_wasa_dry_shower_cough", p14),
    ]

    for name, fn in primitives:
        val0 = fn(0.0)
        val23 = fn(23.0 / 24.0)
        val24 = fn(1.0)
        
        # Check differences
        print(f"\n--- Primitive {name} ---")
        issues = []
        for k in val0.keys():
            v0 = val0[k]
            v23 = val23[k]
            v24 = val24[k]
            diff_loop = abs(v24 - v0)
            diff_seam = abs(v0 - v23)
            
            # Find max step between consecutive frames 0..23
            steps = []
            for f in range(23):
                vf = fn(f / 24.0)[k]
                vnext = fn((f + 1) / 24.0)[k]
                steps.append(abs(vnext - vf))
            max_step = max(steps) if steps else 0.0
            
            print(f"  {k:12s} | t=0: {v0:8.3f} | t=23/24: {v23:8.3f} | t=1.0: {v24:8.3f} | Loop err: {diff_loop:8.3f} | Seam step: {diff_seam:8.3f} | Max inter-frame step: {max_step:8.3f}")
            
            if diff_loop > 0.05:
                issues.append(f"BOUNDARY LOOP MISMATCH in '{k}': |f(1.0) - f(0.0)| = {diff_loop:.3f} > 0.05")
            if diff_seam > 2.5 * max(max_step, 0.01) and diff_seam > 1.0:
                issues.append(f"SEAM VELOCITY DISCONTINUITY in '{k}': jump across loop {diff_seam:.3f} is > 2.5x max normal step ({max_step:.3f})")
                
        if issues:
            print(f"  [!] ISSUES FOUND IN {name}:")
            for iss in issues:
                print(f"      - {iss}")
            findings.append((name, issues))
        else:
            print(f"  [OK] Primitive {name} is continuous.")
            
    return findings

if __name__ == '__main__':
    test_1_looping_continuity()

def test_2_volume_preservation():
    print("\n" + "=" * 80)
    print("TEST 2: VOLUME PRESERVATION INTEGRITY")
    print("=" * 80)
    
    # 1. Theoretical Analysis: 2D vs 3D
    print("1. Theoretical Conservation Law:")
    print("   Spec Section 4.2 & 6.3.2 specifies: Sx = 1.0 / sqrt(Sy)")
    for sy in [0.65, 0.68, 0.80, 1.00, 1.18, 1.35, 1.45]:
        sx = 1.0 / math.sqrt(sy)
        area_2d = sx * sy
        vol_3d = (sx ** 2) * sy
        print(f"   Sy = {sy:.2f} -> Sx = {sx:.4f} | 2D Area (Sx*Sy) = {area_2d:.4f} ({area_2d-1.0:+.2%}) | 3D Vol (Sx^2*Sy) = {vol_3d:.4f} ({vol_3d-1.0:+.2%})")
        
    print("\n2. Verification of Explicit Numerical Pairs in Spec Text vs Equations:")
    test_cases = [
        ("Section 3.2 Gesture 03 (All Fours Table Slam)", 0.68, 1.21, "Sy=0.68, Sx=1.21"),
        ("Section 3.2 Gesture 11 (Lip Point)", 0.85, 0.70, "Sy=0.85, Sx=0.70"),
        ("Section 3.2 Gesture 12 (Slipper Impact)", 0.70, 1.20, "Sy=0.70, Sx=1.20"),
        ("Section 4.4 Primitive 02 Text (Steups Cheek Comp)", None, 0.88, "Sx=0.88 (Text) vs Eq Sy=1+0.12*p(t)"),
        ("Section 4.4 Primitive 09 Text (Puncheon Inhalation)", 1.18, 0.92, "Sy=1.18, Sx=0.92"),
        ("Section 4.4 Primitive 14 (WASA Cough)", None, 1.16, "Sx=1.16, Sy omitted from equations"),
    ]
    
    for label, sy, sx, desc in test_cases:
        print(f"\n   Case: {label} ({desc})")
        if sy is not None and sx is not None:
            expected_sx = 1.0 / math.sqrt(sy)
            err_sx = abs(sx - expected_sx)
            vol_3d = (sx ** 2) * sy
            area_2d = sx * sy
            print(f"     Given: Sy={sy}, Sx={sx}")
            print(f"     Formula Sx = 1/sqrt({sy}) = {expected_sx:.4f} | Delta = {err_sx:.4f}")
            print(f"     3D Volume = {vol_3d:.4f} | 2D Area = {area_2d:.4f}")
            if err_sx > 0.05:
                print(f"     [!] VIOLATION: Given Sx={sx} deviates from formula Sx={expected_sx:.4f} by {err_sx:.4f}")
            else:
                print(f"     [OK] Conforms to 3D volume preservation (error < 0.05).")
        elif label.startswith("Section 4.4 Primitive 02"):
            # Check Primitive 2 formula
            # p(t) ranges in [-0.35, 1.0]
            # Sy = 1 + 0.12 * p(t)
            # Sy_min = 1 - 0.042 = 0.958 -> Sx = 1 / sqrt(0.958) = 1.0216
            # But text says Sx = 0.88!
            print("     Formula in 4.4.2: Sy = 1.0 + 0.12*p(t), Sx = 1/sqrt(Sy)")
            print("     When p(t) = -0.35 (anticipation min): Sy = 0.958 -> Sx = 1.0216")
            print("     Text states: 'Anticipatory cheek compression (Sx = 0.88)'")
            print("     [!] INCONSISTENCY: Formula yields Sx=1.0216 (expansion), but text specifies Sx=0.88 (compression).")
        elif label.startswith("Section 4.4 Primitive 14"):
            print("     Formula in 4.4.14 defines Sx(t) = 1.0 + 0.16*sin(...) = 1.16")
            print("     Sy(t) is completely omitted from the parametric equations!")
            print("     If Sx = 1.16, mass-preserving Sy should be Sy = 1 / (1.16^2) = 0.7432")
            print("     [!] DEFECT: Parametric equations lack Sy(t) formulation.")

def test_3_micro_motion_living_hold():
    print("\n" + "=" * 80)
    print("TEST 3: MICRO-MOTION LIVING HOLD EFFICACY")
    print("=" * 80)
    
    # Import build_animated_stickers functions
    from scripts.build_animated_stickers import prep_breathing_room, warp_mesh
    
    # Pick a sample sticker
    sample_path = os.path.join("assets", "stickers", "slang-link-me.png")
    if not os.path.exists(sample_path):
        sample_path = os.path.join("assets", "stickers", "ah-eh-able.png")
    print(f"Using sample sticker: {sample_path}")
    
    src_img = Image.open(sample_path).convert("RGBA")
    src_prepped = prep_breathing_room(src_img, scale=0.91)
    
    # Experiment A: Static 6-frame hold (dx = 0, dy = 0) without micro-motion
    print("\n--- Experiment A: Static 6-Frame Hold (dx = 0, dy = 0) ---")
    frames_static = []
    for f in range(24):
        # frames 10-15 are completely static (dx=0, dy=0)
        if 10 <= f <= 15:
            disp_fn = lambda x, y: (x, y)
        else:
            disp_fn = lambda x, y, f=f: (x + math.sin(f), y + math.cos(f))
        im_warped = warp_mesh(src_prepped, disp_fn)
        frames_static.append(im_warped)
        
    # Check pixel difference between consecutive static frames 10 and 11
    diff_bbox = ImageChops.difference(frames_static[10], frames_static[11]).getbbox()
    print(f"Pixel difference bbox between frames 10 & 11: {diff_bbox}")
    
    # Save to WebP and GIF
    tmp_static_webp = "temp_test_static.webp"
    tmp_static_gif = "temp_test_static.gif"
    
    frames_static[0].save(
        tmp_static_webp,
        save_all=True,
        append_images=frames_static[1:],
        duration=90,
        loop=0,
        quality=76,
        method=4
    )
    
    # Convert for GIF
    bg_color = (16, 20, 30)
    gif_static_frames = []
    for frm in frames_static:
        bg = Image.new("RGBA", (512, 512), bg_color + (255,))
        bg.alpha_composite(frm)
        pal = bg.convert("RGB").quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        gif_static_frames.append(pal)
        
    gif_static_frames[0].save(
        tmp_static_gif,
        save_all=True,
        append_images=gif_static_frames[1:],
        duration=90,
        loop=0,
        optimize=False
    )
    
    with Image.open(tmp_static_webp) as im:
        n_webp_static = im.n_frames
    with Image.open(tmp_static_gif) as im:
        n_gif_static = im.n_frames
        
    print(f"Exported without micro-motion: WebP frames = {n_webp_static}, GIF frames = {n_gif_static}")
    if n_webp_static < 24:
        print(f"  [CONFIRMED BUG] WebP coalescing occurred! Expected 24 frames, got {n_webp_static} frames.")
    else:
        print(f"  WebP frames: {n_webp_static}")
    if n_gif_static < 24:
        print(f"  [CONFIRMED BUG] GIF coalescing occurred! Expected 24 frames, got {n_gif_static} frames.")
    else:
        print(f"  GIF frames: {n_gif_static}")
        
    # Experiment B: Micro-Motion Living Hold Applied (Ax = 0.8, Ay = 0.5)
    print("\n--- Experiment B: Micro-Motion Living Hold (Ax = 0.8, Ay = 0.5) ---")
    frames_micro = []
    deltas = []
    for f in range(24):
        t = f / 24.0
        # In hold period, inject sinusoidal micro-motion
        dx_idle = 0.8 * math.sin(2 * math.pi * t)
        dy_idle = 0.5 * math.cos(2 * math.pi * t)
        if 10 <= f <= 15:
            disp_fn = lambda x, y, dx=dx_idle, dy=dy_idle: (x + dx, y + dy)
        else:
            disp_fn = lambda x, y, f=f, dx=dx_idle, dy=dy_idle: (x + math.sin(f) + dx, y + math.cos(f) + dy)
        im_warped = warp_mesh(src_prepped, disp_fn)
        frames_micro.append(im_warped)
        
    for f in range(23):
        diff = ImageChops.difference(frames_micro[f], frames_micro[f + 1])
        bbox = diff.getbbox()
        # Find maximum pixel channel difference
        stat = diff.getextrema() # ((min, max), ...)
        max_px_diff = max(st[1] for st in stat)
        deltas.append((f, f+1, bbox, max_px_diff))
        
    print(f"Adjacent frame differences across all 23 frame transitions:")
    zero_diffs = [d for d in deltas if d[2] is None or d[3] == 0]
    min_delta = min(d[3] for d in deltas)
    max_delta = max(d[3] for d in deltas)
    print(f"  Zero-difference frame transitions: {len(zero_diffs)}")
    print(f"  Min channel delta: {min_delta}, Max channel delta: {max_delta}")
    
    tmp_micro_webp = "temp_test_micro.webp"
    tmp_micro_gif = "temp_test_micro.gif"
    
    frames_micro[0].save(
        tmp_micro_webp,
        save_all=True,
        append_images=frames_micro[1:],
        duration=90,
        loop=0,
        quality=76,
        method=4
    )
    
    gif_micro_frames = []
    for frm in frames_micro:
        bg = Image.new("RGBA", (512, 512), bg_color + (255,))
        bg.alpha_composite(frm)
        pal = bg.convert("RGB").quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        gif_micro_frames.append(pal)
        
    gif_micro_frames[0].save(
        tmp_micro_gif,
        save_all=True,
        append_images=gif_micro_frames[1:],
        duration=90,
        loop=0,
        optimize=False
    )
    
    with Image.open(tmp_micro_webp) as im:
        n_webp_micro = im.n_frames
    with Image.open(tmp_micro_gif) as im:
        n_gif_micro = im.n_frames
        
    print(f"Exported WITH micro-motion: WebP frames = {n_webp_micro}, GIF frames = {n_gif_micro}")
    if n_webp_micro == 24 and n_gif_micro == 24:
        print("  [SUCCESS] Micro-Motion Living Hold completely prevented coalescing (24/24 frames preserved on WebP and GIF)!")
    else:
        print(f"  [FAILURE] Frame count mismatch: WebP={n_webp_micro}, GIF={n_gif_micro}")
        
    # Clean up temp files
    for p in [tmp_static_webp, tmp_static_gif, tmp_micro_webp, tmp_micro_gif]:
        if os.path.exists(p):
            os.remove(p)


def test_4_verifier_contract():
    print("\n" + "=" * 80)
    print("TEST 4: ACCEPTANCE CRITERIA & VERIFIER HARNESS FEASIBILITY")
    print("=" * 80)
    
    # Let's inspect the code in Section 7.3.2 against real existing files
    test_webp = os.path.join("assets", "animated", "ah-eh-able.webp")
    test_gif = os.path.join("assets", "animated", "ah-eh-able.gif")
    
    print(f"Testing Section 7.3.2 assertions against {test_webp} and {test_gif}:")
    
    # Test WebP
    try:
        with Image.open(test_webp) as im:
            print(f"  WebP format: {im.format}")
            print(f"  WebP size: {im.size}")
            print(f"  WebP n_frames: {im.n_frames}")
            print(f"  WebP mode: {im.mode}")
            print(f"  WebP loop info: {im.info.get('loop')}")
            
            # Duration test
            durations = []
            for f in range(im.n_frames):
                im.seek(f)
                d = im.info.get('duration', 90)
                durations.append(d)
            print(f"  WebP durations (first 5): {durations[:5]}")
            print(f"  WebP total duration: {sum(durations)}ms")
    except Exception as e:
        print(f"  [!] WebP inspection error: {e}")
        
    # Test GIF
    try:
        with Image.open(test_gif) as im:
            print(f"\n  GIF format: {im.format}")
            print(f"  GIF size: {im.size}")
            print(f"  GIF n_frames: {im.n_frames}")
            print(f"  GIF mode: {im.mode}")
            print(f"  GIF loop info: {im.info.get('loop')}")
            
            corner = im.convert('RGB').getpixel((2, 2))
            print(f"  GIF corner pixel at (2, 2): {corner}")
            expected_corner = (16, 20, 30)
            if corner == expected_corner:
                print(f"  [OK] Corner pixel matches {expected_corner}")
            else:
                print(f"  [!] CORNER MISMATCH: corner pixel {corner} != {expected_corner}")
                
            durations = []
            for f in range(im.n_frames):
                im.seek(f)
                d = im.info.get('duration', 90)
                durations.append(d)
            print(f"  GIF durations (first 5): {durations[:5]}")
            print(f"  GIF total duration: {sum(durations)}ms")
    except Exception as e:
        print(f"  [!] GIF inspection error: {e}")

    # Test Q1-Q11 coverage in Section 7.3.2
    print("\n--- Auditing Q1-Q11 Coverage in Section 7.3.2 Code ---")
    q_audit = [
        ("Q1", "Total Sticker Coverage (188)", "Partially covered in main() comment; main() body is 'pass' stub"),
        ("Q2", "Dual-Stream Production (376)", "Implicit in main() comment; main() body is 'pass' stub"),
        ("Q3", "Non-Zero Byte Audit", "Covered: assert size > 1024"),
        ("Q4", "Frame Count Invariance (24)", "Covered: assert im.n_frames == 24"),
        ("Q5", "Frame Timing (90ms)", "Covered: assert d == 90"),
        ("Q6", "Total Duration (2160ms)", "Covered: assert total_dur == 2160"),
        ("Q7", "Canvas Dimensions (512x512)", "Covered: assert im.size == (512, 512)"),
        ("Q8", "Header Magic Bytes (RIFF/WEBPVP8X, GIF89a)", "NOT rigorously covered: only checks im.format == 'WEBP', does not read raw magic bytes from header!"),
        ("Q9", "Infinite Loop Configuration (loop=0)", "Covered: assert im.info.get('loop', 0) == 0"),
        ("Q10", "WebP Alpha Integrity (Transparent exterior)", "NOT fully covered: only checks im.mode == 'RGBA', does NOT verify alpha==0 on outer border/exterior!"),
        ("Q11", "GIF Studio Card Integrity (#10141E)", "Covered: assert corner == (16, 20, 30)"),
    ]
    for q_id, metric, status in q_audit:
        print(f"  {q_id:5s} | {metric:40s} | {status}")


if __name__ == '__main__':
    test_1_looping_continuity()
    test_2_volume_preservation()
    test_3_micro_motion_living_hold()
    test_4_verifier_contract()
