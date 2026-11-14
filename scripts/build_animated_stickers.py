"""
scripts/build_animated_stickers.py
==================================
PeelOff Trinidad & Tobago Sticker Animation Generator (Milestone 2 Overhaul).
Implements:
  1. 14 Procedural Motion Primitives with exact math formulas and loop continuity.
  2. Master 188-Sticker Static Registry directly from CULTURAL_ANIMATION_SPEC.md Section 5.
  3. ZERO generic fallbacks (complete elimination of articulated_gesture).
  4. Micro-motion living hold sub-pixel micro-jitter to prevent Pillow frame coalescing
     (guaranteeing strictly 24 frames @ 90ms = 2.16s loop).
  5. Dual-Stream Export:
     - WebP: 512x512 RGBA transparent, Q76, method=4, loop=0
     - GIF: 512x512 solid #10141E dark card, FASTOCTREE 128 colors, dither=NONE, optimize=False, loop=0
  6. Production CLI: --sticker, --pack, --workers, --all.
"""

import os
import sys
import math
import time
import uuid
import shutil
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageDraw

# =============================================================================
# CONSTANTS, PALETTES & DIRECTORY PATHS
# =============================================================================
STICKER_DIR = os.path.join("assets", "stickers")
OUT_DIR = os.path.join("assets", "animated")

INK = (20, 22, 29, 255)
WHITE = (255, 255, 255, 255)
GOLD = (255, 212, 59, 255)
CYAN = (0, 229, 255, 255)
RED = (255, 42, 95, 255)
CARD_BG = (16, 20, 30, 255)


# =============================================================================
# COMIC TIMING & EASING CURVES (12 Principles of Animation)
# =============================================================================
def clamp01(u: float) -> float:
    return 0.0 if u < 0.0 else (1.0 if u > 1.0 else u)


def ease_in_out_cubic(u: float) -> float:
    u = clamp01(u)
    return 4.0 * u * u * u if u < 0.5 else 1.0 - ((-2.0 * u + 2.0) ** 3) / 2.0


def ease_out_back(u: float, s: float = 1.70158) -> float:
    u = clamp01(u) - 1.0
    return 1.0 + (s + 1.0) * (u ** 3) + s * (u ** 2)


def ease_in_back(u: float, s: float = 1.6) -> float:
    u = clamp01(u)
    return (s + 1.0) * (u ** 3) - s * (u ** 2)


def comic_pop_curve(t: float, t_antic: float = 0.16, t_hit: float = 0.32, t_hold: float = 0.68) -> float:
    """Returns signed comic curve: negative anticipation -> snappy overshoot pop -> hold -> settle to 0."""
    if t < t_antic:
        return -0.35 * math.sin((t / t_antic) * math.pi * 0.5)
    if t < t_hit:
        u = (t - t_antic) / (t_hit - t_antic)
        return -0.35 + 1.35 * ease_out_back(u, 1.8)
    if t < t_hold:
        u = (t - t_hit) / (t_hold - t_hit)
        return 1.0 + 0.06 * math.sin(u * math.pi * 2.0)
    u = (t - t_hold) / (1.0 - t_hold)
    return 1.0 - ease_in_out_cubic(u)


def impact_shake(t: float, t_hit: float, amp: float = 10.0, decay: float = 18.0) -> tuple[float, float]:
    dt = t - t_hit
    if dt < 0.0 or dt > 0.25:
        return (0.0, 0.0)
    env = math.exp(-dt * decay)
    return (amp * env * math.sin(dt * 95.0), amp * 0.6 * env * math.cos(dt * 110.0))


# =============================================================================
# MICRO-MOTION LIVING HOLD INJECTION ENGINE
# =============================================================================
def living_hold_jitter(t: float, ax: float = 0.8, ay: float = 0.5) -> tuple[float, float]:
    """
    Injects continuous sub-pixel sinusoidal micro-motion to prevent Pillow frame coalescing.
    The 1-cycle base wave guarantees that all 24 frames at t = f / 24 are strictly unique.
    Loop continuity is preserved with zero boundary jump: dx(0) == dx(1), dy(0) == dy(1).
    """
    ang = 2.0 * math.pi * t
    dx = ax * math.sin(ang) + 0.25 * ax * math.sin(ang * 8.0)
    dy = ay * math.cos(ang) + 0.25 * ay * math.cos(ang * 6.0)
    return (dx, dy)


# =============================================================================
# C-LEVEL MESH WARP & VOLUME PRESERVATION DEFORMERS
# =============================================================================
def prep_breathing_room(im: Image.Image, scale: float = 0.91) -> Image.Image:
    """Keep safety margins inside 512x512 so die-cut borders never clip during comic jumps."""
    w, h = im.size
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    small = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.alpha_composite(small, ((w - nw) // 2, (h - nh) // 2))
    return canvas


def warp_mesh(img: Image.Image, disp_fn, grid_n: int = 18) -> Image.Image:
    w, h = img.size
    step_x = w / grid_n
    step_y = h / grid_n
    verts = [
        [disp_fn(c * step_x, r * step_y) for c in range(grid_n + 1)]
        for r in range(grid_n + 1)
    ]
    mesh = []
    for r in range(grid_n):
        for c in range(grid_n):
            x0 = int(round(c * step_x))
            y0 = int(round(r * step_y))
            x1 = int(round((c + 1) * step_x))
            y1 = int(round((r + 1) * step_y))
            nw = verts[r][c]
            sw = verts[r + 1][c]
            se = verts[r + 1][c + 1]
            ne = verts[r][c + 1]
            mesh.append(((x0, y0, x1, y1), (nw[0], nw[1], sw[0], sw[1], se[0], se[1], ne[0], ne[1])))
    return img.transform((w, h), Image.Transform.MESH, mesh, Image.Resampling.BICUBIC)


def squash_stretch_offset(x: float, y: float, cx: float, cy: float, sy: float) -> tuple[float, float]:
    """3D cylindrical volume preservation: Sx^2 * Sy = 1.0 -> Sx = 1 / sqrt(Sy). Anchor at (cx, cy)."""
    sy_clamped = max(0.65, min(1.45, sy))
    sx = 1.0 / math.sqrt(sy_clamped)
    src_x = cx + (x - cx) / sx
    src_y = cy + (y - cy) / sy_clamped
    return (src_x - x, src_y - y)


def squash_stretch_cylindrical(x: float, y: float, cx: float, cy: float, sx: float) -> tuple[float, float]:
    """3D cylindrical volume preservation: Sx^2 * Sy = 1.0 -> Sy = 1 / (Sx^2). Anchor at (cx, cy)."""
    sx_clamped = max(0.70, min(1.30, sx))
    sy = 1.0 / (sx_clamped ** 2)
    src_x = cx + (x - cx) / sx_clamped
    src_y = cy + (y - cy) / sy
    return (src_x - x, src_y - y)


# =============================================================================
# PROCEDURAL COMIC VECTOR GRAPHIC FX ENGINE
# =============================================================================
def draw_comic_starburst(
    od: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    r_outer: float,
    r_inner: float,
    points: int = 10,
    fill=(255, 212, 59, 255),
    core=(255, 255, 240, 255),
    rot: float = 0.0,
    alpha: int = 255,
):
    if r_outer < 4 or alpha <= 5:
        return
    pts_out = []
    pts_in = []
    for i in range(points * 2):
        a = rot + i * math.pi / points
        r = r_outer if i % 2 == 0 else r_inner
        pts_out.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        pts_in.append((cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55))
    ink_col = (INK[0], INK[1], INK[2], alpha)
    fill_col = (fill[0], fill[1], fill[2], alpha)
    core_col = (core[0], core[1], core[2], alpha)
    od.polygon(pts_out, fill=fill_col, outline=ink_col, width=3)
    od.polygon(pts_in, fill=core_col)


def draw_comic_twinkle(
    od: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    size: float,
    fill=(255, 230, 80, 255),
    rot: float = 0.0,
    alpha: int = 255,
):
    if size < 3 or alpha <= 5:
        return
    pts = []
    for i in range(8):
        a = rot + i * math.pi / 4.0
        r = size if i % 2 == 0 else size * 0.28
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    od.polygon(pts, fill=(fill[0], fill[1], fill[2], alpha), outline=(INK[0], INK[1], INK[2], alpha), width=2)
    c_r = max(2, int(size * 0.22))
    od.ellipse([cx - c_r, cy - c_r, cx + c_r, cy + c_r], fill=(255, 255, 255, alpha))


def draw_comic_droplet(
    od: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    scale: float = 1.0,
    fill=(0, 215, 255, 255),
    alpha: int = 245,
):
    r = 9.0 * scale
    if r < 2 or alpha <= 5:
        return
    pts = [
        (cx, cy - r * 1.45),
        (cx + r * 0.85, cy + r * 0.15),
        (cx + r * 0.65, cy + r * 0.95),
        (cx, cy + r * 1.15),
        (cx - r * 0.65, cy + r * 0.95),
        (cx - r * 0.85, cy + r * 0.15),
    ]
    od.polygon(pts, fill=(fill[0], fill[1], fill[2], alpha), outline=(INK[0], INK[1], INK[2], alpha), width=2)
    od.ellipse(
        [cx - r * 0.42, cy + r * 0.05, cx - r * 0.12, cy + r * 0.48],
        fill=(255, 255, 255, alpha),
    )


def draw_comic_puff(
    od: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    fill=(245, 250, 255, 255),
    alpha: int = 230,
):
    if radius < 4 or alpha <= 5:
        return
    ink_col = (INK[0], INK[1], INK[2], alpha)
    body_col = (fill[0], fill[1], fill[2], alpha)
    lobes = [
        (0.0, 0.0, 1.0),
        (-0.65, 0.18, 0.72),
        (0.65, 0.14, 0.74),
        (-0.28, -0.52, 0.68),
        (0.32, -0.48, 0.66),
    ]
    for ox, oy, sr in lobes:
        rr = radius * sr + 2.5
        od.ellipse([cx + ox * radius - rr, cy + oy * radius - rr, cx + ox * radius + rr, cy + oy * radius + rr], fill=ink_col)
    for ox, oy, sr in lobes:
        rr = radius * sr
        od.ellipse([cx + ox * radius - rr, cy + oy * radius - rr, cx + ox * radius + rr, cy + oy * radius + rr], fill=body_col)


def draw_comic_speed_lines(
    od: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    angles_deg: list[float],
    r1: float,
    r2: float,
    color=(255, 255, 255, 230),
    width: int = 4,
):
    for deg in angles_deg:
        a = math.radians(deg)
        p1 = (cx + math.cos(a) * r1, cy + math.sin(a) * r1)
        p2 = (cx + math.cos(a) * r2, cy + math.sin(a) * r2)
        od.line([p1, p2], fill=(INK[0], INK[1], INK[2], color[3]), width=width + 3)
        od.line([p1, p2], fill=color, width=width)


def draw_comic_anger_vein(od: ImageDraw.ImageDraw, cx: float, cy: float, s: float = 1.0, alpha: int = 240):
    if alpha <= 5:
        return
    d = 12.0 * s
    col = (255, 42, 95, alpha)
    ink_col = (INK[0], INK[1], INK[2], alpha)
    arcs = [
        ([cx - d, cy - d, cx, cy], 0, 90),
        ([cx, cy - d, cx + d, cy], 90, 180),
        ([cx - d, cy, cx, cy + d], 270, 360),
        ([cx, cy, cx + d, cy + d], 180, 270),
    ]
    for box, a0, a1 in arcs:
        od.arc(box, start=a0, end=a1, fill=ink_col, width=6)
        od.arc(box, start=a0, end=a1, fill=col, width=3)


def draw_comic_music_note(
    od: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    scale: float = 1.0,
    fill=(0, 229, 255, 255),
    alpha: int = 245,
):
    if alpha <= 5:
        return
    r = 8.0 * scale
    ink_col = (INK[0], INK[1], INK[2], alpha)
    col = (fill[0], fill[1], fill[2], alpha)
    stem_x = cx + r * 0.7
    od.line([(stem_x, cy), (stem_x, cy - r * 2.8), (stem_x + r * 1.1, cy - r * 2.1)], fill=ink_col, width=7)
    od.line([(stem_x, cy), (stem_x, cy - r * 2.8), (stem_x + r * 1.1, cy - r * 2.1)], fill=col, width=3)
    od.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=col, outline=ink_col, width=2)
    od.ellipse([cx - r * 0.45, cy - r * 0.35, cx - r * 0.1, cy], fill=(255, 255, 255, alpha))

# =============================================================================
# THE 14 AUTHENTIC TRINI PROCEDURAL MOTION PRIMITIVES
# =============================================================================

# --- 1. soca_rag_windmill ---
def disp_soca_rag_windmill(x: float, y: float, t: float) -> tuple[float, float]:
    ang = 2.0 * math.pi * t
    x_cloth = 256.0 + 110.0 * math.cos(ang - 0.52)
    y_cloth = 180.0 + 38.0 * math.sin(ang - 0.52) + 18.0 * math.sin(2.0 * ang)
    w_top = math.exp(-(((y - 140.0) / 95.0) ** 2))
    sy = 1.0 + 0.05 * math.sin(ang)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 360.0, sy)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + w_top * ((x_cloth - 256.0) * 0.25) + dxi
    dy = sq_dy + w_top * ((y_cloth - 180.0) * 0.22) + dyi
    return (x + dx, y + dy)

def overlay_soca_rag_windmill(od: ImageDraw.ImageDraw, fx: str, t: float):
    ang = 2.0 * math.pi * t
    cx = 256.0 + 110.0 * math.cos(ang - 0.52)
    cy = 180.0 + 38.0 * math.sin(ang - 0.52) + 18.0 * math.sin(2.0 * ang)
    trail_deg = math.degrees(ang - 0.52)
    draw_comic_speed_lines(od, cx, cy, [trail_deg - 30, trail_deg, trail_deg + 30], 25, 45, color=(255, 255, 255, 180), width=3)
    if "feather" in fx or "glitter" in fx:
        draw_comic_twinkle(od, cx + 20, cy - 20, 10, fill=(255, 215, 0, 255), rot=ang, alpha=200)


# --- 2. steups_recoil_burst ---
def disp_steups_recoil_burst(x: float, y: float, t: float) -> tuple[float, float]:
    if t < 0.14:
        sx = 1.0 - 0.12 * math.sin((t / 0.14) * (math.pi / 2))
    elif t < 0.28:
        sx = 0.88 + 0.12 * ease_out_back((t - 0.14) / 0.14, 1.8)
    elif t < 0.65:
        sx = 1.0 + 0.02 * math.sin(((t - 0.28) / 0.37) * 2 * math.pi)
    else:
        sx = 1.0
    sy = 1.0 / (sx ** 2)
    p = comic_pop_curve(t, 0.14, 0.28, 0.65)
    dy_neck = -16.0 * max(0.0, p)
    w_face = math.exp(-(((y - 256.0) / 120.0) ** 2))
    src_x = 256.0 + (x - 256.0) / max(0.70, min(1.30, sx))
    src_y = 256.0 + (y - 256.0) / sy
    dxi, dyi = living_hold_jitter(t)
    dx = (src_x - x) * w_face + dxi
    dy = (src_y - y) * w_face + dy_neck * w_face + dyi
    return (x + dx, y + dy)

def overlay_steups_recoil_burst(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.28 <= t <= 0.68:
        u = (t - 0.28) / 0.40
        r_puff = 8.0 + 42.0 * u
        alpha = int(240.0 * ((1.0 - u) ** 2))
        px = 256.0 - 60.0 - 70.0 * u
        py = 310.0 - 10.0 * u
        draw_comic_puff(od, px, py, r_puff, fill=(245, 250, 255, 255), alpha=alpha)
        draw_comic_speed_lines(od, 256.0 - 55.0, 310.0, [160, 180, 200], 25, 25 + 45 * u, color=(255, 255, 255, alpha), width=3)
    if "sideeye" in fx and t < 0.65:
        od.line([(280, 230), (320, 220)], fill=(INK[0], INK[1], INK[2], 220), width=3)


# --- 3. allfours_table_slam ---
def disp_allfours_table_slam(x: float, y: float, t: float) -> tuple[float, float]:
    if t < 0.25:
        y_arm = -50.0 * math.sin((t / 0.25) * (math.pi / 2))
    elif t < 0.35:
        y_arm = -50.0 + 50.0 * (((t - 0.25) / 0.10) ** 2)
    else:
        y_arm = 28.0 * math.exp(-18.0 * (t - 0.35)) * math.sin(16 * math.pi * (t - 0.35))
    
    if t >= 0.35:
        dt = t - 0.35
        sh_x = 10.0 * math.exp(-18.0 * dt) * math.sin(24 * math.pi * dt)
        sh_y = 7.0 * math.exp(-18.0 * dt) * math.cos(28 * math.pi * dt)
        sy = 1.0 - 0.32 * math.exp(-16.0 * dt) * math.cos(20.0 * dt)
    else:
        sh_x = 0.0
        sh_y = 0.0
        sy = 1.0
    
    w_top = math.exp(-(((y - 180.0) / 100.0) ** 2))
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 420.0, sy)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + sh_x + dxi
    dy = sq_dy + y_arm * w_top + sh_y + dyi
    return (x + dx, y + dy)

def overlay_allfours_table_slam(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.35 <= t < 0.65:
        u = (t - 0.35) / 0.30
        r_burst = 60.0 * math.sin(u * math.pi)
        alpha = int(250.0 * (1.0 - u))
        draw_comic_starburst(od, 256.0, 420.0, r_burst, r_burst * 0.45, points=8, fill=(255, 230, 70, 255), alpha=alpha)
        draw_comic_puff(od, 256.0 - 80.0 * u, 420.0, 14.0 * (1.0 - u), fill=(245, 245, 255, 255), alpha=int(alpha * 0.7))
        draw_comic_puff(od, 256.0 + 80.0 * u, 420.0, 14.0 * (1.0 - u), fill=(245, 245, 255, 255), alpha=int(alpha * 0.7))


# --- 4. doubles_45_lean_drip ---
def disp_doubles_45_lean_drip(x: float, y: float, t: float) -> tuple[float, float]:
    cantilever = (y - 512.0) * math.tan(math.radians(8.0)) * clamp01((512.0 - y) / 350.0)
    y_jaw = 4.0 * abs(math.sin(4 * math.pi * t))
    w_head = math.exp(-(((y - 200.0) / 100.0) ** 2))
    dxi, dyi = living_hold_jitter(t)
    dx = cantilever + dxi
    dy = y_jaw * w_head + dyi
    return (x + dx, y + dy)

def overlay_doubles_45_lean_drip(od: ImageDraw.ImageDraw, fx: str, t: float):
    if t < 0.70:
        l_stub = 10.0 + 35.0 * clamp01((t - 0.20) / 0.50)
        y_drop = 360.0 + l_stub
        alpha = 255
    elif t <= 0.92:
        y_drop = 360.0 + 45.0 + 2400.0 * ((t - 0.70) ** 2)
        alpha = 255
    else:
        y_drop = 360.0 + 10.0
        alpha = 0
    if alpha > 0 and y_drop <= 530.0:
        fill_col = (245, 170, 30, 255)
        draw_comic_droplet(od, 280.0, y_drop, scale=1.1, fill=fill_col, alpha=alpha)
        if t < 0.70:
            od.line([(280.0, 360.0), (280.0, y_drop)], fill=(INK[0], INK[1], INK[2], alpha), width=5)
            od.line([(280.0, 360.0), (280.0, y_drop)], fill=(fill_col[0], fill_col[1], fill_col[2], alpha), width=2)


# --- 5. tanty_akumbo_tilt ---
def disp_tanty_akumbo_tilt(x: float, y: float, t: float) -> tuple[float, float]:
    ang = 2.0 * math.pi * t
    th_neck = math.radians(-18.0 * math.sin(ang + 0.35))
    dx_pelvis = 16.0 * math.sin(ang)
    dy_bob = -6.0 * abs(math.cos(ang))
    sy = 1.0 + 0.05 * math.sin(ang)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 380.0, sy)
    w_head = math.exp(-(((y - 180.0) / 90.0) ** 2))
    w_torso = math.exp(-(((y - 320.0) / 110.0) ** 2))
    head_rot_x = (x - 256.0) * (math.cos(th_neck) - 1.0) - (y - 180.0) * math.sin(th_neck)
    head_rot_y = (x - 256.0) * math.sin(th_neck) + (y - 180.0) * (math.cos(th_neck) - 1.0)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + dx_pelvis * w_torso + head_rot_x * w_head + dxi
    dy = sq_dy + dy_bob + head_rot_y * w_head + dyi
    return (x + dx, y + dy)

def overlay_tanty_akumbo_tilt(od: ImageDraw.ImageDraw, fx: str, t: float):
    ang = 2.0 * math.pi * t
    if math.sin(ang) > 0.4:
        draw_comic_twinkle(od, 360.0, 160.0, size=11, fill=(255, 220, 50, 255), rot=ang, alpha=210)


# --- 6. bazodee_dazed_spiral ---
def disp_bazodee_dazed_spiral(x: float, y: float, t: float) -> tuple[float, float]:
    ang = 2.0 * math.pi * t
    x_sway = 22.0 * math.sin(ang)
    y_sway = 12.0 * math.sin(2.0 * ang)
    sy = 1.0 + 0.04 * math.sin(ang)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 256.0, sy)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + x_sway + dxi
    dy = sq_dy + y_sway + dyi
    return (x + dx, y + dy)

def overlay_bazodee_dazed_spiral(od: ImageDraw.ImageDraw, fx: str, t: float):
    for i in range(3):
        a = 2.0 * math.pi * t + (2.0 * math.pi * i / 3.0)
        sx = 256.0 + 105.0 * math.cos(a)
        sy = 110.0 + 22.0 * math.sin(a)
        draw_comic_twinkle(od, sx, sy, size=12.0, fill=(255, 220, 60, 255), rot=a * 2.0, alpha=240)


# --- 7. maco_peep_zoom ---
def disp_maco_peep_zoom(x: float, y: float, t: float) -> tuple[float, float]:
    if t < 0.25:
        y_creep = -30.0 * ((t / 0.25) ** 3)
    elif t < 0.75:
        y_creep = -30.0
    else:
        y_creep = -30.0 + 30.0 * ease_in_back((t - 0.75) / 0.25, 1.7)
    
    if t < 0.25:
        s_lens = 1.0
    elif t < 0.40:
        s_lens = 1.0 + 0.35 * ease_out_back((t - 0.25) / 0.15, 1.8)
    elif t < 0.75:
        s_lens = 1.35 + 0.05 * math.sin(10 * math.pi * t)
    else:
        s_lens = 1.0
    
    if 0.40 <= t <= 0.75:
        x_pan = 18.0 * math.sin(((t - 0.40) / 0.35) * 2 * math.pi)
    else:
        x_pan = 0.0
    
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 240.0, s_lens)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + x_pan + dxi
    dy = sq_dy + y_creep + dyi
    return (x + dx, y + dy)

def overlay_maco_peep_zoom(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.25 <= t <= 0.75:
        alpha = int(200 * math.sin(((t - 0.25) / 0.50) * math.pi))
        od.ellipse([120, 160, 240, 280], outline=(INK[0], INK[1], INK[2], alpha), width=3)
        od.ellipse([272, 160, 392, 280], outline=(INK[0], INK[1], INK[2], alpha), width=3)


# --- 8. heat_seeking_slipper_arc ---
def disp_heat_seeking_slipper_arc(x: float, y: float, t: float) -> tuple[float, float]:
    u = min(1.0, t / 0.65)
    if t < 0.65:
        x_pos = 490.0 - 234.0 * u
        y_pos = 280.0 - 180.0 * math.sin(math.pi * u)
        th = 8.0 * math.pi * u
    elif t < 0.70:
        x_pos = 256.0
        y_pos = 280.0
        th = 8.0 * math.pi
    elif t < 0.85:
        dt = t - 0.70
        x_pos = 256.0 + 4.0 * math.exp(-12.0 * dt) * math.sin(12 * math.pi * dt)
        y_pos = 280.0 - 8.0 * math.exp(-14.0 * dt) * abs(math.sin(16 * math.pi * dt))
        th = 8.0 * math.pi
    elif t < 0.95:
        x_pos = 256.0
        y_pos = 280.0
        th = 8.0 * math.pi
    else:
        norm = (t - 0.95) / 0.05
        x_pos = 256.0 + 234.0 * norm
        y_pos = 280.0
        th = 8.0 * math.pi * (1.0 - norm)
    
    cos_th = math.cos(th)
    sin_th = math.sin(th)
    rx = cos_th * (x - 256.0) + sin_th * (y - 280.0)
    ry = -sin_th * (x - 256.0) + cos_th * (y - 280.0)
    dxi, dyi = living_hold_jitter(t)
    dx = (256.0 + rx - x) + (x_pos - 256.0) + dxi
    dy = (280.0 + ry - y) + (y_pos - 280.0) + dyi
    return (x + dx, y + dy)

def overlay_heat_seeking_slipper_arc(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.65 <= t < 0.85:
        r_flash = 55.0 * math.sin(((t - 0.65) / 0.20) * math.pi)
        alpha = int(255.0 * (r_flash / 55.0))
        draw_comic_starburst(od, 256.0, 280.0, r_flash, r_flash * 0.45, points=10, fill=(255, 60, 40, 255), alpha=alpha)

def apply_slipper_alpha(im: Image.Image, t: float) -> Image.Image:
    if t <= 0.85:
        return im
    elif t <= 0.95:
        fade = (1.0 - (t - 0.85) / 0.10) ** 2
        r, g, b, a = im.split()
        a = a.point(lambda p: int(p * fade))
        return Image.merge("RGBA", (r, g, b, a))
    else:
        return Image.new("RGBA", im.size, (0, 0, 0, 0))


# --- 9. puncheon_fire_breath ---
def disp_puncheon_fire_breath(x: float, y: float, t: float) -> tuple[float, float]:
    if t < 0.22:
        sy = 1.0 + 0.18 * math.sin((t / 0.22) * (math.pi / 2))
    elif t < 0.34:
        sy = 1.18 - 0.38 * ((t - 0.22) / 0.12)
    elif t < 0.70:
        sy = 0.80 + 0.05 * math.sin(((t - 0.34) / 0.36) * 4 * math.pi)
    else:
        sy = 0.80 + 0.20 * ((t - 0.70) / 0.30)
    
    if t >= 0.69:
        sh_x = 7.0 * math.sin(16 * math.pi * t) * math.exp(-5.0 * (t - 0.69))
    else:
        sh_x = 0.0
    
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 360.0, sy)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + sh_x + dxi
    dy = sq_dy + dyi
    return (x + dx, y + dy)

def overlay_puncheon_fire_breath(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.24 <= t <= 0.69:
        u = (t - 0.24) / 0.45
        r_flame = 85.0 * math.sin(u * math.pi)
        alpha = int(250.0 * math.sin(u * math.pi))
        draw_comic_starburst(od, 256.0 + 60.0 + 50.0 * u, 270.0, r_flame, r_flame * 0.45, points=8, fill=(0, 200, 255, 255), core=(255, 255, 255, 255), alpha=alpha)


# --- 10. steelpan_rebound ---
def disp_steelpan_rebound(x: float, y: float, t: float) -> tuple[float, float]:
    tau = (t * 3.0) % 1.0
    if tau < 0.3:
        y_mallet = -28.0 * (1.0 - tau / 0.3)
    elif tau == 0.3:
        y_mallet = 0.0
    else:
        y_mallet = -28.0 * math.sin(((tau - 0.3) / 0.7) * math.pi) * math.exp(-3.5 * tau)
    
    sy = 1.0 + 0.06 * math.sin(6 * math.pi * t)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 360.0, sy)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + dxi
    dy = sq_dy + y_mallet * 0.25 + dyi
    return (x + dx, y + dy)

def overlay_steelpan_rebound(od: ImageDraw.ImageDraw, fx: str, t: float):
    r_ring = (t * 360.0) % 120.0
    alpha = 240.0 * (max(0.0, 1.0 - r_ring / 105.0) ** 2)
    if alpha > 5:
        a_int = int(alpha)
        od.ellipse([256 - r_ring, 320 - r_ring * 0.45, 256 + r_ring, 320 + r_ring * 0.45], outline=(INK[0], INK[1], INK[2], a_int), width=5)
        od.ellipse([256 - r_ring, 320 - r_ring * 0.45, 256 + r_ring, 320 + r_ring * 0.45], outline=(0, 230, 255, a_int), width=2)


# --- 11. killing_dead_collapse ---
def disp_killing_dead_collapse(x: float, y: float, t: float) -> tuple[float, float]:
    th = math.radians(-24.0 + 8.0 * math.sin(6 * math.pi * t))
    dy_laugh = 18.0 + 10.0 * abs(math.cos(6 * math.pi * t))
    sy = 1.0 + 0.12 * math.cos(6 * math.pi * t)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 420.0, sy)
    rx = (x - 256.0) * (math.cos(th) - 1.0) - (y - 420.0) * math.sin(th)
    ry = (x - 256.0) * math.sin(th) + (y - 420.0) * (math.cos(th) - 1.0)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + rx + dxi
    dy = sq_dy + ry + dy_laugh + dyi
    return (x + dx, y + dy)

def overlay_killing_dead_collapse(od: ImageDraw.ImageDraw, fx: str, t: float):
    tau = (2 * t) % 1.0
    x_left = 220.0 - (25.0 + 90.0 * tau)
    x_right = 292.0 + (25.0 + 90.0 * tau)
    y_tear = 240.0 - 20.0 * math.sin(math.pi * tau) + 65.0 * (tau ** 2)
    draw_comic_droplet(od, x_left, y_tear, scale=1.0, fill=(0, 215, 255, 255), alpha=240)
    draw_comic_droplet(od, x_right, y_tear, scale=1.0, fill=(0, 215, 255, 255), alpha=240)


# --- 12. ttec_blackout_candle ---
def disp_ttec_blackout_candle(x: float, y: float, t: float) -> tuple[float, float]:
    ang = 2.0 * math.pi * t
    sy = 1.0 + 0.03 * math.sin(ang)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 320.0, sy)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + dxi
    dy = sq_dy + dyi
    return (x + dx, y + dy)

def get_ttec_lighting(t: float) -> float:
    if t < 0.16: return 1.0
    elif t < 0.32: return 0.0
    elif t < 0.85: return 0.15 + 0.85 * clamp01((t - 0.32) / 0.20)
    elif t < 0.88: return 0.0
    elif t < 0.92: return 0.75
    elif t < 0.95: return 0.30
    else: return 1.0

def overlay_ttec_blackout_candle(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.32 <= t < 0.85:
        r_glow = 90.0 + 12.0 * math.sin(8 * math.pi * t)
        alpha = 255
    elif 0.85 <= t <= 0.95:
        fade = (1.0 - (t - 0.85) / 0.10) ** 2
        r_glow = (90.0 + 12.0 * math.sin(8 * math.pi * t)) * fade
        alpha = int(255 * fade)
    else:
        r_glow = 0.0
        alpha = 0
    
    if alpha > 5:
        od.ellipse([256 - r_glow, 320 - r_glow, 256 + r_glow, 320 + r_glow], fill=(255, 220, 50, int(alpha * 0.25)))
        draw_comic_twinkle(od, 256, 320, size=15, fill=(255, 230, 80, 255), alpha=alpha)
    
    if 0.85 <= t <= 0.95:
        a_smoke = int(180.0 * ((1.0 - (t - 0.85) / 0.10) ** 2))
        if a_smoke > 5:
            draw_comic_puff(od, 256, 300, radius=12, fill=(200, 200, 210, 255), alpha=a_smoke)

def apply_candle_lighting(im: Image.Image, t: float) -> Image.Image:
    light = get_ttec_lighting(t)
    if light >= 0.999:
        return im
    r, g, b, a = im.split()
    r = r.point(lambda p: int(p * light))
    g = g.point(lambda p: int(p * light))
    b = b.point(lambda p: int(p * light))
    return Image.merge("RGBA", (r, g, b, a))


# --- 13. moko_jumbie_stilt_sway ---
def disp_moko_jumbie_stilt_sway(x: float, y: float, t: float) -> tuple[float, float]:
    ang = 2.0 * math.pi * t
    th_sway = math.radians(15.0 * math.sin(ang))
    dx_torso = -12.0 * math.sin(ang)
    dx_fabric = 18.0 * math.sin(ang - 0.015 * y) * ((y - 200.0) / 312.0)
    sy = 1.0 + 0.06 * math.cos(ang)
    sq_dx, sq_dy = squash_stretch_offset(x, y, 256.0, 480.0, sy)
    rx = (x - 256.0) * (math.cos(th_sway) - 1.0) - (y - 480.0) * math.sin(th_sway)
    ry = (x - 256.0) * math.sin(th_sway) + (y - 480.0) * (math.cos(th_sway) - 1.0)
    dxi, dyi = living_hold_jitter(t)
    dx = sq_dx + dx_torso + rx + dx_fabric + dxi
    dy = sq_dy + ry + dyi
    return (x + dx, y + dy)

def overlay_moko_jumbie_stilt_sway(od: ImageDraw.ImageDraw, fx: str, t: float):
    ang = 2.0 * math.pi * t
    draw_comic_twinkle(od, 256.0 + 40.0 * math.sin(ang), 120.0, size=10, fill=(255, 215, 0, 255), rot=ang, alpha=200)


# --- 14. wasa_dry_shower_cough ---
def disp_wasa_dry_shower_cough(x: float, y: float, t: float) -> tuple[float, float]:
    if t < 0.28:
        sx = 1.0 + 0.16 * math.sin((t / 0.28) * (math.pi / 2))
    elif t < 0.36:
        sx = 1.16 - 0.26 * ((t - 0.28) / 0.08)
    else:
        # Normalized exponential decay ensuring exact boundary closure sx=1.0 at t=1.0
        decay_norm = 1.0 - math.exp(-10.0 * 0.64)
        sx = 0.90 + 0.10 * ((1.0 - math.exp(-10.0 * (t - 0.36))) / decay_norm)
    sy = 1.0 / (sx ** 2)
    src_x = 256.0 + (x - 256.0) / sx
    src_y = 280.0 + (y - 280.0) / sy
    dxi, dyi = living_hold_jitter(t)
    dx = (src_x - x) + dxi
    dy = (src_y - y) + dyi
    return (x + dx, y + dy)

def overlay_wasa_dry_shower_cough(od: ImageDraw.ImageDraw, fx: str, t: float):
    if 0.36 <= t <= 0.68:
        y_drop = 280.0 + 2600.0 * ((t - 0.36) ** 2)
        if y_drop <= 530.0:
            draw_comic_droplet(od, 256.0, y_drop, scale=0.9, fill=(180, 120, 50, 255), alpha=255)
    if 0.40 <= t <= 0.85:
        r_dust = 38.0 * math.sin(((t - 0.40) / 0.45) * math.pi)
        alpha = int(220.0 * (r_dust / 38.0))
        draw_comic_puff(od, 256.0, 290.0, r_dust, fill=(210, 195, 175, 255), alpha=alpha)


PRIMITIVE_DISP = {
    "soca_rag_windmill": disp_soca_rag_windmill,
    "steups_recoil_burst": disp_steups_recoil_burst,
    "allfours_table_slam": disp_allfours_table_slam,
    "doubles_45_lean_drip": disp_doubles_45_lean_drip,
    "tanty_akumbo_tilt": disp_tanty_akumbo_tilt,
    "bazodee_dazed_spiral": disp_bazodee_dazed_spiral,
    "maco_peep_zoom": disp_maco_peep_zoom,
    "heat_seeking_slipper_arc": disp_heat_seeking_slipper_arc,
    "puncheon_fire_breath": disp_puncheon_fire_breath,
    "steelpan_rebound": disp_steelpan_rebound,
    "killing_dead_collapse": disp_killing_dead_collapse,
    "ttec_blackout_candle": disp_ttec_blackout_candle,
    "moko_jumbie_stilt_sway": disp_moko_jumbie_stilt_sway,
    "wasa_dry_shower_cough": disp_wasa_dry_shower_cough,
}

PRIMITIVE_OVERLAY = {
    "soca_rag_windmill": overlay_soca_rag_windmill,
    "steups_recoil_burst": overlay_steups_recoil_burst,
    "allfours_table_slam": overlay_allfours_table_slam,
    "doubles_45_lean_drip": overlay_doubles_45_lean_drip,
    "tanty_akumbo_tilt": overlay_tanty_akumbo_tilt,
    "bazodee_dazed_spiral": overlay_bazodee_dazed_spiral,
    "maco_peep_zoom": overlay_maco_peep_zoom,
    "heat_seeking_slipper_arc": overlay_heat_seeking_slipper_arc,
    "puncheon_fire_breath": overlay_puncheon_fire_breath,
    "steelpan_rebound": overlay_steelpan_rebound,
    "killing_dead_collapse": overlay_killing_dead_collapse,
    "ttec_blackout_candle": overlay_ttec_blackout_candle,
    "moko_jumbie_stilt_sway": overlay_moko_jumbie_stilt_sway,
    "wasa_dry_shower_cough": overlay_wasa_dry_shower_cough,
}


# =============================================================================
# MASTER CULTURAL RIG REGISTRY (188 STICKERS, 0 GENERIC FALLBACKS)
# =============================================================================
STICKER_RIG_REGISTRY: dict[str, dict] = {
    "ent": {"num": 1, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Comic punctuation starburst + snappy nod"},
    "steups": {"num": 2, "primitive": "steups_recoil_burst", "rig": "steups_puff", "scale": 0.91, "fx": "Expanding acoustic shockwave + air puff"},
    "ah-eh-able": {"num": 3, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Sweating droplets + fluttering hand fan"},
    "look-trouble": {"num": 4, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Flashing yellow hazard warning lights"},
    "mamaguy": {"num": 5, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Melting syrup drips + floating hearts"},
    "pure-bazodee": {"num": 6, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Orbiting yellow stars and fluttering birds"},
    "weyyyy": {"num": 7, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Comic megaphone shockwave + exclamation marks"},
    "scene": {"num": 8, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.93, "fx": "Specular glint on sunglasses lens"},
    "fuh-real": {"num": 9, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Question mark pop + skeptical head cock"},
    "doh-tote": {"num": 10, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Dust brushed off shoulder + breezy puff"},
    "killing-me-dead": {"num": 11, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Horizontal tear jets + laughing soundwaves"},
    "rel-bess": {"num": 12, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Golden shimmering starbursts + crown bounce"},
    "cyah-take-dat": {"num": 13, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.91, "fx": "Brick wall barrier impact + dust puff"},
    "chupidee": {"num": 14, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Swirling spiral eyes + floppy ear wobble"},
    "freshwater-yankee": {"num": 15, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Floating boarding pass + snowflake sparkles"},
    "just-picong": {"num": 16, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Comic jester bell bounce + teasing tongue"},
    "crapaud-pipe": {"num": 17, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.88, "fx": "Smoke rings rising from pipe + blinking eyes"},
    "trini-chow": {"num": 18, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Rising spicy heat fumes + jumping pepper seeds"},
    "maco": {"num": 19, "primitive": "maco_peep_zoom", "rig": "maco_window_binoculars", "scale": 0.91, "fx": "Optical magnifying lens distortion + iris twitch"},
    "horning": {"num": 20, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Flashing red siren light + broken trust crack"},
    "real-tabanca": {"num": 21, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Dripping blue tear + pulsing cracked heart"},
    "wha-appen": {"num": 22, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Comic impact flash + kinetic speed lines"},
    "bacchanal": {"num": 23, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "High-frequency bass rumble + flying glitter"},
    "carnival-tabanca": {"num": 24, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Floating solitary feather + tear puddle"},
    "yuh-too-fas": {"num": 25, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Sassy head snap + yellow warning tape"},
    "doh-make-joke": {"num": 26, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.91, "fx": "Simmering anger sparks + ground tremble"},
    "vex-pepper": {"num": 27, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Jet of steam from ears/top + flame base"},
    "kicksin": {"num": 28, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Bouncing spring coil + musical giggle notes"},
    "mauvais-langue": {"num": 29, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Hot pink gossip speech bubble + venom drop"},
    "owah": {"num": 30, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Triple question mark vibration + eyebrow bounce"},
    "doubles-3d": {"num": 31, "primitive": "doubles_45_lean_drip", "rig": "culinary_steam_pop", "scale": 0.91, "fx": "Aromatic steam curls + savory channa bounce"},
    "slight-pepper": {"num": 32, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Sizzling chili sparks + fiery splash drop"},
    "doubles-lean": {"num": 33, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Viscous amber curry drip stretching down"},
    "bake-and-shark": {"num": 34, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Crispy bite crunch lines + garlic sauce drip"},
    "buss-up-shut": {"num": 35, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Flaky roti crumbs flying + fragrant curry steam"},
    "sunday-lunch": {"num": 36, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Melted cheese pull + glossy stew shimmer"},
    "sunday-coma": {"num": 37, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Floating 'Zzz' bubbles + fan blade spin"},
    "pelau-pot": {"num": 38, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Slow aromatic steam puffs + pot lid rattle"},
    "corn-soup": {"num": 39, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Floating corn cob bob + swirling split pea steam"},
    "pholourie": {"num": 40, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Tangy brown chutney drizzle + dough bounce"},
    "crix-and-cheese": {"num": 41, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.93, "fx": "Biscuit crumbs popping + soda fizz bubbles"},
    "savannah-coconut": {"num": 42, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Cutlass gleam + refreshing splashing water"},
    "hang-jack": {"num": 43, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Impact shockwave + cards flying in air"},
    "stress-free-liming": {"num": 44, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Gentle hammock swing + clinking ice cubes"},
    "sou-sou-drop": {"num": 45, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Flying green bills + golden coin sparkles"},
    "bullseye-allfours": {"num": 46, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Flying chalk dust puff + broken card shards"},
    "puncheon-fire": {"num": 47, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Expanding blue ethanol flame + coughing puff"},
    "rum-punch": {"num": 48, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Swirling red bitters + sweating condensation"},
    "ddi-boat": {"num": 49, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Ocean spray foam + sun glint on water"},
    "river-lime": {"num": 50, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Crackling wood fire embers + water ripples"},
    "bess-cutters": {"num": 51, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Sizzling oil splatter + aromatic geera steam"},
    "potcake-dog": {"num": 52, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Energetic tail wag + panting tongue bob"},
    "one-for-de-road": {"num": 53, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Liquid slosh + celebratory cheers stars"},
    "cricket-six": {"num": 54, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Blazing ball comet trail + stadium cheers"},
    "steelpan-3d": {"num": 55, "primitive": "steelpan_rebound", "rig": "steelpan_rebound", "scale": 0.91, "fx": "Expanding concentric acoustic rings + glint"},
    "carnival-mas-3d": {"num": 56, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.88, "fx": "Swaying iridescent plumage + body glitter"},
    "dutty-jouvert": {"num": 57, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Wet mud/paint splatters + paint streak trails"},
    "wait-for-riddim": {"num": 58, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Vibrating ground lines + sudden bass jump"},
    "wave-yuh-rag": {"num": 59, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Aerodynamic ribbon trails + confetti shower"},
    "moko-jumbie": {"num": 60, "primitive": "moko_jumbie_stilt_sway", "rig": "moko_jumbie_stilt_sway", "scale": 0.88, "fx": "Dramatic vertical sway + billowing satin cloth"},
    "midnight-robber": {"num": 61, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.88, "fx": "Swirling brimstone smoke + skull gun flash"},
    "dame-lorraine": {"num": 62, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Rhythmic hip bounce + fluttering hand fan"},
    "blue-devil": {"num": 63, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Erupting yellow fireball + clattering tin can"},
    "jab-molassie": {"num": 64, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Dripping black molasses + rattling chains"},
    "pierrot-grenade": {"num": 65, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Fluttering fabric rags + alphabet letter pops"},
    "tassa-chutney": {"num": 66, "primitive": "steelpan_rebound", "rig": "steelpan_rebound", "scale": 0.91, "fx": "High-speed stick blur + sonic shockwaves"},
    "soucouyant": {"num": 67, "primitive": "heat_seeking_slipper_arc", "rig": "heat_seeking_slipper_arc", "scale": 0.88, "fx": "Flaming comet tail + sparks crackling"},
    "salt-in-mortar": {"num": 68, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Burning white sizzling sparks + screaming puff"},
    "la-diablesse": {"num": 69, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Flashing cloven hoof + ghostly blue mist"},
    "mama-dlo": {"num": 70, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Swirling water vortex + glistening scales"},
    "papa-bois": {"num": 71, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Rustling forest leaves + animal call waves"},
    "douen": {"num": 72, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Footprints appearing reversed in mud"},
    "lagahoo": {"num": 73, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Heavy chain dragging sparks + glowing red eyes"},
    "no-maljo": {"num": 74, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Expanding blue protective shield pulse"},
    "bush-tea": {"num": 75, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Spiraling healing herbal steam + floating leaf"},
    "silk-cotton-tree": {"num": 76, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Whispering autumn leaves + mystical aura pulse"},
    "parang-vibes": {"num": 77, "primitive": "steelpan_rebound", "rig": "steelpan_rebound", "scale": 0.91, "fx": "Strumming hand blur + rhythmic music notes"},
    "parang-season": {"num": 78, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Shaking maraca blur + festive green/red stars"},
    "deya-parsad": {"num": 79, "primitive": "ttec_blackout_candle", "rig": "ttec_blackout_candle", "scale": 0.93, "fx": "Warm golden light glow expanding + ghee flicker"},
    "ponche-de-creme": {"num": 80, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Grated nutmeg dusting + rich liquid swirl"},
    "trini-black-cake": {"num": 81, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Glistening dark rum drizzle + sugar holly"},
    "divali-sweet-bag": {"num": 82, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Sweet powdered sugar puff + popping kurma"},
    "eid-sawine": {"num": 83, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Cardamom steam curls + floating almond slice"},
    "phagwa-holi": {"num": 84, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Exploding magenta and cyan powder clouds"},
    "chowtal-jhaal": {"num": 85, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Golden cymbal clash spark + sonic chime wave"},
    "christmas-curtains": {"num": 86, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Fluttering lace hem + sparkling clean sparkles"},
    "emancipation-pride": {"num": 87, "primitive": "steelpan_rebound", "rig": "steelpan_rebound", "scale": 0.91, "fx": "Deep bass pulse rings + vibrant kente flutter"},
    "every-creed-and-race": {"num": 88, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Glowing rainbow/national flag halo pulse"},
    "crab-and-dumpling": {"num": 89, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Thick curry gravy bubbling + claw snap"},
    "maxi-taxi": {"num": 90, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.88, "fx": "Exhaust pipe puff + bumper bounce squash"},
    "buccoo-goat-race": {"num": 91, "primitive": "heat_seeking_slipper_arc", "rig": "heat_seeking_slipper_arc", "scale": 0.88, "fx": "Kicking up dirt clouds + goat bell jingling"},
    "nylon-pool": {"num": 92, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Shimmering caustic water lines + seafoam"},
    "pure-bago-vibes": {"num": 93, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Coconut swaying + gentle tropical breeze wave"},
    "highway-traffic": {"num": 94, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.88, "fx": "Blinking brake lights + frustrated car horn puff"},
    "trini-mom-spoon": {"num": 95, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Ticking panic clock + cold ice vapor smoke"},
    "flying-slipper": {"num": 96, "primitive": "heat_seeking_slipper_arc", "rig": "heat_seeking_slipper_arc", "scale": 0.88, "fx": "Curving motion trail + comic bullseye impact"},
    "wasa-water-gone": {"num": 97, "primitive": "wasa_dry_shower_cough", "rig": "wasa_dry_shower_cough", "scale": 0.91, "fx": "Solitary water droplet drip + dust cloud puff"},
    "ttec-current-gone": {"num": 98, "primitive": "ttec_blackout_candle", "rig": "ttec_blackout_candle", "scale": 0.91, "fx": "Sudden pitch black screen + warm candle flame"},
    "scarlet-ibis-cocrico": {"num": 99, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Crimson and brown feather flutter + sunbeam"},
    "sweet-tt-heart": {"num": 100, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Rhythmic heartbeat thumping + radiant sparkle"},
    "slang-wha-yuh-say": {"num": 101, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Expanding blue acoustic wave ripples"},
    "slang-wha-go-on": {"num": 102, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.93, "fx": "Comic spark burst at contact point"},
    "slang-doh-study-dat": {"num": 103, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Raindrops bouncing off umbrella dome"},
    "slang-leh-we-go": {"num": 104, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Speed dust cloud + fluttering wings"},
    "slang-ah-coming": {"num": 105, "primitive": "heat_seeking_slipper_arc", "rig": "heat_seeking_slipper_arc", "scale": 0.88, "fx": "Spinning clock hands + coffee sloshing"},
    "slang-ah-reach": {"num": 106, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Circular ground ripple + triumphant star"},
    "slang-ah-gone": {"num": 107, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Poof smoke cloud expanding + fading sparkle"},
    "slang-ent": {"num": 108, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Pulsing golden heart glow + snappy nod"},
    "slang-right-dey": {"num": 109, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Crosshair pulse + lock-on beep lines"},
    "slang-just-now": {"num": 110, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Trickling golden sand + floating question marks"},
    "slang-small-ting": {"num": 111, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.93, "fx": "Gentle finger flick + nonchalant sparkle"},
    "slang-no-scene": {"num": 112, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.93, "fx": "Green badge sparkle + gentle bounce"},
    "slang-all-ah-dat": {"num": 113, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.88, "fx": "Wobbling parcels balance + star sparkles"},
    "slang-yuh-good": {"num": 114, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Pulsing golden heart glow + thumbs-up pop"},
    "slang-how-yuh-mean": {"num": 115, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Rhythmic double nod + confirmation checkmark"},
    "slang-doh-start": {"num": 116, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.93, "fx": "Metal zipper sliding + key sparkling away"},
    "slang-watch-nah": {"num": 117, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Eyebrow raise + downward sightline glint"},
    "slang-hear-nah": {"num": 118, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Whispering wave trail + attention sparkle"},
    "slang-for-true": {"num": 119, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Golden heart aura pulse + sincere nod"},
    "slang-real-talk": {"num": 120, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Mic drop shockwave + reverb sound rings"},
    "slang-bet": {"num": 121, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.93, "fx": "Handshake grip spark + coin flip spin"},
    "slang-yuh-mad": {"num": 122, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Mercury shooting out top + fiery sparks"},
    "slang-yuh-jokin": {"num": 123, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Jingling bells bounce + flying question mark"},
    "slang-doh-play": {"num": 124, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Flashing warning blink + firm slam"},
    "slang-lemme-see": {"num": 125, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Optical text enlargement + inquisitive twitch"},
    "slang-nah-man": {"num": 126, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.91, "fx": "Rapid horizontal blur + waving dismissive hands"},
    "slang-boy-please": {"num": 127, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Sassy cut-eye flick + palm pushing away"},
    "slang-steups": {"num": 128, "primitive": "steups_recoil_burst", "rig": "steups_sideeye_emoji", "scale": 0.93, "fx": "Puffed cheek release + dismissive air puff"},
    "slang-tanty": {"num": 129, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Glasses sliding down nose + firm head nod"},
    "slang-gyal": {"num": 130, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Shimmering diamond facets + sassy bounce"},
    "slang-boi": {"num": 131, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Eyebrow lift overshoot + astonished gaze"},
    "slang-yuh-too-lie": {"num": 132, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.91, "fx": "Rapid nose extension shoot + leafy twig pop"},
    "slang-doh-kill-meh": {"num": 133, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Rhythmic laughter torso bounce + tears"},
    "slang-ah-done": {"num": 134, "primitive": "steups_recoil_burst", "rig": "steups_recoil_burst", "scale": 0.91, "fx": "Hand clapping dust cloud + turning away"},
    "slang-is-a-jokes": {"num": 135, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Sputtering laugh wobble + comic squeak"},
    "slang-mad-ting": {"num": 136, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Exploding multicolored fireworks + smoke"},
    "slang-wicked": {"num": 137, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Flaming golden horn tips + mischievous wink"},
    "slang-high-beam": {"num": 138, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Intense white beam cone glare + lens flares"},
    "slang-a-week": {"num": 139, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Melting liquid ripple + laughter notes"},
    "slang-too-much": {"num": 140, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Soundwave rejection barrier + head shake"},
    "slang-dohh-bother": {"num": 141, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Casual shrug drop + dismissive sigh puff"},
    "slang-mash-up": {"num": 142, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.88, "fx": "Flying rock shards + ground impact crater"},
    "slang-real-bad": {"num": 143, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Rotating dual-color siren beams + alarm rings"},
    "slang-ah-screaming": {"num": 144, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.88, "fx": "Vibrating megaphone cone + outward blast rings"},
    "slang-doh-watch-me": {"num": 145, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.93, "fx": "Reflective glare flash + turning away"},
    "slang-mind-yuh-business": {"num": 146, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Golden bubble shield shimmer + straw sip"},
    "slang-stay-in-yuh-lane": {"num": 147, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Solid neon lane lines + car wheel bounce"},
    "slang-yuh-too-bold": {"num": 148, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Dramatic red card thrust + whistle sound rings"},
    "slang-yuh-real-brave": {"num": 149, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Expanding roar soundwaves + golden mane shake"},
    "slang-badmind": {"num": 150, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.88, "fx": "Slit pupil constriction + poisonous green fume"},
    "slang-vex": {"num": 151, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Throbbing red pulse + pressurized steam jets"},
    "slang-dont-hot-up-yuh-head": {"num": 152, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.93, "fx": "Cooling water vapor + soothing blue wave"},
    "slang-take-a-set": {"num": 153, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Spring-loaded chair unfolding + sand puff"},
    "slang-doh-get-on-so": {"num": 154, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Stern finger wag blur + scolding brow"},
    "slang-yuh-feeling-yuhself": {"num": 155, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Mirror specular shine + vanity sparkles"},
    "slang-big-up-yuhself": {"num": 156, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Bursting confetti fountain + trophy gleam"},
    "slang-respect": {"num": 157, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Heartfelt salute snap + golden halo"},
    "slang-liming": {"num": 158, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Clinking straws + floating lime wedge"},
    "slang-doh-be-a-dotish": {"num": 159, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Orbiting yellow stars + spinning spiral eyes"},
    "slang-dotishness": {"num": 160, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Slap impact starburst + wobbling cranium"},
    "slang-fass": {"num": 161, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Telescopic brass extension click + lens glint"},
    "slang-maco": {"num": 162, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Binocular sweep + targeting reticle focus"},
    "slang-tabanca": {"num": 163, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Dripping blue tear + pulsing cracked heart"},
    "slang-horn": {"num": 164, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.91, "fx": "Red warning alarm flash + shivering horns"},
    "slang-wha-yuh-on": {"num": 165, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Flashlight search beam + skeptical squint"},
    "slang-yuh-outside": {"num": 166, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Flashing neon strobes + pumping bass waves"},
    "slang-link-me": {"num": 167, "primitive": "steelpan_rebound", "rig": "steelpan_rebound", "scale": 0.91, "fx": "High-frequency phone vibration lines"},
    "slang-link-up": {"num": 168, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Metallic snap spark + locking click lines"},
    "slang-vibes": {"num": 169, "primitive": "steelpan_rebound", "rig": "steelpan_rebound", "scale": 0.91, "fx": "Pumping speaker cones + pulsing music notes"},
    "slang-good-vibes-only": {"num": 170, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Rotating warm sun rays + radiant sparkle"},
    "slang-the-vibe-different": {"num": 171, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Shivering frost particles + needle wobble"},
    "slang-no-cap": {"num": 172, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Clean slash spark + green verified badge"},
    "slang-cap": {"num": 173, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Cap dropping over eyes + buzzer 'X'"},
    "slang-lowkey": {"num": 174, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Sneaky tip-toe bob + dimming ambient light"},
    "slang-highkey": {"num": 175, "primitive": "puncheon_fire_breath", "rig": "puncheon_fire_breath", "scale": 0.88, "fx": "Crossing sweeping searchlights + beam glare"},
    "slang-im-weak": {"num": 176, "primitive": "killing_dead_collapse", "rig": "killing_dead_collapse", "scale": 0.91, "fx": "Wobbly jelly collapse + soft comic plop"},
    "slang-im-dead": {"num": 177, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Wobbling skull chatter + electric spark arc"},
    "slang-ate": {"num": 178, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Circular belly rub motion + content smile"},
    "slang-ate-and-left-no-crumbs": {"num": 179, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.91, "fx": "Sparkling halo shimmer + twirling golden fork"},
    "slang-its-not-giving": {"num": 180, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.93, "fx": "Drooping thumb + wilted flower petal drop"},
    "slang-be-so-for-real": {"num": 181, "primitive": "allfours_table_slam", "rig": "allfours_table_slam", "scale": 0.93, "fx": "Deadpan stare + dry blinking eyelids"},
    "slang-delulu": {"num": 182, "primitive": "bazodee_dazed_spiral", "rig": "bazodee_dazed_spiral", "scale": 0.91, "fx": "Floating cloud bob + sparkling rainbow arch"},
    "slang-rizz": {"num": 183, "primitive": "tanty_akumbo_tilt", "rig": "tanty_akumbo_tilt", "scale": 0.91, "fx": "Magnetic charm spark lines + cool wink glint"},
    "slang-red-flag": {"num": 184, "primitive": "soca_rag_windmill", "rig": "soca_rag_windmill", "scale": 0.91, "fx": "Sharp fabric ripple snaps + alarm flashes"},
    "slang-soft-launch": {"num": 185, "primitive": "maco_peep_zoom", "rig": "maco_peep_zoom", "scale": 0.91, "fx": "Subtle curtain flutter + discreet wink glint"},
    "slang-hard-lucks-dey": {"num": 186, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Sad empty pot resonance + floating fly"},
    "slang-left-on-read": {"num": 187, "primitive": "doubles_45_lean_drip", "rig": "doubles_45_lean_drip", "scale": 0.91, "fx": "Fluttering moth loop + floating dust cobweb"},
    "slang-the-eagle-has-landed": {"num": 188, "primitive": "heat_seeking_slipper_arc", "rig": "heat_seeking_slipper_arc", "scale": 0.88, "fx": "Flapping wing thrust + falling cash bills"},
}


# Master mapping dictionary alias for test compatibility
STICKER_RIG_MAP: dict[str, str] = {k: v["primitive"] for k, v in STICKER_RIG_REGISTRY.items()}


# =============================================================================
# RIG CLASSIFIER (ZERO GENERIC FALLBACKS ACROSS ALL 188 STICKERS)
# =============================================================================
def classify_rig(sid: str) -> str:
    """
    Classify sticker into its bespoke rig or authentic procedural motion primitive.
    Strictly achieves ZERO generic fallbacks across all 188 stickers.
    Preserves exact backward compatibility with contract test assertions.
    """
    s = sid.lower().strip()
    if s.endswith((".png", ".webp", ".gif")):
        s = s.rsplit(".", 1)[0]
    if s in STICKER_RIG_REGISTRY:
        return STICKER_RIG_REGISTRY[s]["rig"]
    
    # Safe authentic Caribbean default for empty or unknown inputs (never generic articulated_gesture)
    return "tanty_akumbo_tilt"


# =============================================================================
# PICTURE-SPECIFIC COMIC ANIMATION RENDERER
# =============================================================================
def render_picture_specific_frame(im: Image.Image, rig: str, sid: str, f: int, n_frames: int = 24) -> Image.Image:
    sid_clean = sid.lower().strip()
    if sid_clean.endswith((".png", ".webp", ".gif")):
        sid_clean = sid_clean.rsplit(".", 1)[0]
    
    entry = STICKER_RIG_REGISTRY.get(sid_clean, {})
    primitive = entry.get("primitive")
    if not primitive:
        primitive = rig if rig in PRIMITIVE_DISP else "tanty_akumbo_tilt"
    fx = entry.get("fx", "")
    
    t = f / n_frames
    disp_fn_base = PRIMITIVE_DISP.get(primitive, disp_tanty_akumbo_tilt)
    disp_fn = lambda x, y: disp_fn_base(x, y, t)
    
    frame = warp_mesh(im, disp_fn, grid_n=18)
    
    # Custom post-warp effects for ballistic slipper and blackout candle
    if primitive == "heat_seeking_slipper_arc":
        frame = apply_slipper_alpha(frame, t)
    elif primitive == "ttec_blackout_candle":
        frame = apply_candle_lighting(frame, t)
    
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    overlay_fn = PRIMITIVE_OVERLAY.get(primitive, overlay_tanty_akumbo_tilt)
    overlay_fn(od, fx, t)
    
    return Image.alpha_composite(frame, overlay)


# =============================================================================
# EXPORT ANIMATED WEBP & WHATSAPP-COMPATIBLE 24-FRAME GIF
# =============================================================================
def save_with_atomic_retry(save_func, target_path: str, max_retries: int = 5, base_delay: float = 0.12):
    """
    Saves an image to a unique temporary file and atomically replaces target_path.
    Retries with exponential backoff on transient Windows file lock contention (OSError / PermissionError).
    """
    target_dir, target_name = os.path.split(os.path.abspath(target_path))
    os.makedirs(target_dir, exist_ok=True)
    name_part, ext_part = os.path.splitext(target_name)
    token = f"{os.getpid()}_{uuid.uuid4().hex[:8]}"
    tmp_path = os.path.join(target_dir, f".tmp_{name_part}_{token}{ext_part}")
    
    try:
        save_func(tmp_path)
        for attempt in range(max_retries):
            try:
                os.replace(tmp_path, target_path)
                return
            except (PermissionError, OSError):
                if attempt == max_retries - 1:
                    raise
                time.sleep(base_delay * (1.5 ** attempt))
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def copy_with_retry(src: str, dst: str, max_retries: int = 5, base_delay: float = 0.12):
    """
    Copies file with retries on transient Windows file lock contention.
    Uses atomic temporary copy in destination directory to prevent partial files.
    """
    dst_dir, dst_name = os.path.split(os.path.abspath(dst))
    os.makedirs(dst_dir, exist_ok=True)
    name_part, ext_part = os.path.splitext(dst_name)
    token = f"{os.getpid()}_{uuid.uuid4().hex[:8]}"
    tmp_dst = os.path.join(dst_dir, f".tmp_{name_part}_{token}{ext_part}")
    
    try:
        shutil.copy2(src, tmp_dst)
        for attempt in range(max_retries):
            try:
                os.replace(tmp_dst, dst)
                return
            except (PermissionError, OSError):
                if attempt == max_retries - 1:
                    raise
                time.sleep(base_delay * (1.5 ** attempt))
    finally:
        if os.path.exists(tmp_dst):
            try:
                os.remove(tmp_dst)
            except Exception:
                pass


def save_animated_webp_and_gif(base_img: Image.Image, sid: str, rig: str, webp_path: str, gif_path: str):
    n_frames = 24
    duration_ms = 90  # 24 * 90ms = 2.16s (>2.0s so WhatsApp plays it as a looping animation!)
    
    sid_clean = sid.lower().strip()
    if sid_clean.endswith((".png", ".webp", ".gif")):
        sid_clean = sid_clean.rsplit(".", 1)[0]
    
    entry = STICKER_RIG_REGISTRY.get(sid_clean, {})
    scale = entry.get("scale", 0.91)
    
    prepped = prep_breathing_room(base_img, scale=scale)
    rgba_frames = [render_picture_specific_frame(prepped, rig, sid_clean, i, n_frames) for i in range(n_frames)]

    # 1. Save Transparent 512x512 Animated WebP (crisp & lighter weight)
    def _save_webp(target):
        rgba_frames[0].save(
            target,
            format="WEBP",
            save_all=True,
            append_images=rgba_frames[1:],
            duration=duration_ms,
            loop=0,
            lossless=False,
            quality=76,
            method=4,
        )
    save_with_atomic_retry(_save_webp, webp_path)

    # 2. Save WhatsApp-Compatible 512x512 24-Frame Looping GIF on Dark Studio Card (#10141E)
    gif_frames = []
    bg_color = (16, 20, 30, 255)
    for fr in rgba_frames:
        card = Image.new("RGBA", fr.size, bg_color)
        card.alpha_composite(fr)
        rgb = card.convert("RGB")
        p_frame = rgb.quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        gif_frames.append(p_frame)

    def _save_gif(target):
        gif_frames[0].save(
            target,
            format="GIF",
            save_all=True,
            append_images=gif_frames[1:],
            duration=duration_ms,
            loop=0,
            optimize=False,
        )
    save_with_atomic_retry(_save_gif, gif_path)


def process_one(fname: str, out_dir: str = OUT_DIR):
    sid = fname[:-4] if fname.endswith((".png", ".webp", ".gif")) else fname
    png_path = os.path.join(STICKER_DIR, f"{sid}.png")
    if not os.path.exists(png_path):
        png_path = os.path.join(STICKER_DIR, fname)
    if not os.path.exists(png_path):
        raise FileNotFoundError(f"Sticker PNG not found: {png_path}")
    
    os.makedirs(out_dir, exist_ok=True)
    webp_out = os.path.join(out_dir, f"{sid}.webp")
    gif_out = os.path.join(out_dir, f"{sid}.gif")
    
    rig = classify_rig(sid)
    with Image.open(png_path) as im:
        base = im.convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
        save_animated_webp_and_gif(base, sid, rig, webp_out, gif_out)
    
    # Mirror outputs to build/animated_stickers/ for pipeline and verification
    build_webp_dir = os.path.join("build", "animated_stickers", "webp")
    build_gif_dir = os.path.join("build", "animated_stickers", "gif")
    os.makedirs(build_webp_dir, exist_ok=True)
    os.makedirs(build_gif_dir, exist_ok=True)
    copy_with_retry(webp_out, os.path.join(build_webp_dir, f"{sid}.webp"))
    copy_with_retry(gif_out, os.path.join(build_gif_dir, f"{sid}.gif"))
    
    return sid, rig, os.path.getsize(webp_out) / 1024, os.path.getsize(gif_out) / 1024


# =============================================================================
# PRODUCTION CLI ARGUMENT PARSER
# =============================================================================
def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="PeelOff Trinidad & Tobago Sticker Animation Generator (Milestone 2)"
    )
    parser.add_argument(
        "--sticker", "-s",
        type=str,
        default=None,
        help="Build a single sticker by ID (e.g., 'steups', 'doubles-lean', 'hang-jack')"
    )
    parser.add_argument(
        "--pack", "-p",
        type=str,
        default=None,
        help="Build all stickers belonging to a specific pack (e.g., 'pack-1', 'slang')"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=min(8, os.cpu_count() or 4),
        help="Number of concurrent worker processes (clamped between 1 and 16)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        default=False,
        help="Build all 188 stickers across all packs (default if no flag specified)"
    )
    args = parser.parse_args()
    args.workers = max(1, min(16, args.workers))
    return args


def main():
    args = parse_cli_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. Single sticker build
    if args.sticker:
        sid = args.sticker.strip().lower()
        if sid.endswith((".png", ".webp", ".gif")):
            sid = sid.rsplit(".", 1)[0]
        fname = f"{sid}.png"
        t0 = time.time()
        sid_out, rig, w_kb, g_kb = process_one(fname)
        print(f"Generated {sid_out} ({rig}) -> WebP: {w_kb:.1f}KB, GIF: {g_kb:.1f}KB in {time.time() - t0:.2f}s")
        return

    # 2. Pack or catalog build
    files = sorted([f for f in os.listdir(STICKER_DIR) if f.endswith(".png")])
    if args.pack:
        pack_arg = args.pack.strip().lower()
        PACK_RANGES = {
            1: (1, 18),
            2: (19, 30),
            3: (31, 42),
            4: (43, 54),
            5: (55, 66),
            6: (67, 76),
            7: (77, 88),
            8: (89, 100),
            9: (101, 188),
        }
        PACK_ALIASES = {
            "1": 1, "pack-1": 1, "pack1": 1, "pack_1": 1, "pack-1-social-slang": 1, "social-slang": 1,
            "2": 2, "pack-2": 2, "pack2": 2, "pack_2": 2, "pack-2-reactions-drama": 2, "reactions-drama": 2,
            "3": 3, "pack-3": 3, "pack3": 3, "pack_3": 3, "pack-3-food-belly": 3, "food-belly": 3,
            "4": 4, "pack-4": 4, "pack4": 4, "pack_4": 4, "pack-4-liming-allfours": 4, "liming-allfours": 4,
            "5": 5, "pack-5": 5, "pack5": 5, "pack_5": 5, "pack-5-carnival-mas": 5, "carnival-mas": 5,
            "6": 6, "pack-6": 6, "pack6": 6, "pack_6": 6, "pack-6-folklore": 6, "folklore": 6,
            "7": 7, "pack-7": 7, "pack7": 7, "pack_7": 7, "pack-7-festivals": 7, "festivals": 7,
            "8": 8, "pack-8": 8, "pack8": 8, "pack_8": 8, "pack-8-tobago-everyday": 8, "tobago-everyday": 8,
            "9": 9, "pack-9": 9, "pack9": 9, "pack_9": 9, "slang": 9, "pack-slang": 9, "trini-slang": 9,
        }
        
        target_sids = set()
        if pack_arg in PACK_ALIASES:
            pnum = PACK_ALIASES[pack_arg]
            lo, hi = PACK_RANGES[pnum]
            target_sids = {sid for sid, d in STICKER_RIG_REGISTRY.items() if lo <= d["num"] <= hi}
        elif "slang" in pack_arg:
            target_sids = {sid for sid, d in STICKER_RIG_REGISTRY.items() if d["num"] >= 101 or sid.startswith("slang-")}
        else:
            target_sids = {sid for sid in STICKER_RIG_REGISTRY if pack_arg in sid}
        
        files = [f for f in files if (f[:-4] if f.endswith(".png") else f) in target_sids]
        if not files:
            print(f"No stickers found matching pack '{args.pack}'. Available packs: 1-8, slang.")
            return
        print(f"Building {len(files)} stickers for pack '{args.pack}' with {args.workers} workers...")
    else:
        print(f"Building comic-artist articulated animations for {len(files)} stickers with {args.workers} workers...")

    t0 = time.time()
    done = 0
    failed_stickers = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(process_one, f): f for f in files}
        for fut in as_completed(futures):
            f_orig = futures[fut]
            try:
                sid, rig, w_kb, g_kb = fut.result()
                done += 1
                if done % 25 == 0 or done == len(files) or "maco" in sid:
                    print(f"  [{done}/{len(files)}] {sid} ({rig}) -> WebP: {w_kb:.1f}KB, GIF: {g_kb:.1f}KB")
            except Exception as exc:
                print(f"  [ERROR] Worker failed on {f_orig}: {exc}", file=sys.stderr)
                failed_stickers.append(f_orig)

    # Sequential retry pass for any transient multiprocessing failures
    if failed_stickers:
        print(f"\nRetrying {len(failed_stickers)} failed sticker(s) sequentially...")
        time.sleep(0.5)
        still_failed = []
        for f in failed_stickers:
            try:
                time.sleep(0.2)
                sid, rig, w_kb, g_kb = process_one(f)
                done += 1
                print(f"  [RETRY SUCCESS] {sid} ({rig}) -> WebP: {w_kb:.1f}KB, GIF: {g_kb:.1f}KB")
            except Exception as exc:
                print(f"  [RETRY FAILED] {f}: {exc}", file=sys.stderr)
                still_failed.append((f, str(exc)))
        if still_failed:
            print(f"\nFATAL: {len(still_failed)} sticker(s) failed after retry pass:", file=sys.stderr)
            for f, err in still_failed:
                print(f"  - {f}: {err}", file=sys.stderr)
            sys.exit(1)
    print(f"Completed all {len(files)} stickers in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
