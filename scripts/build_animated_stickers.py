import os
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageDraw

STICKER_DIR = os.path.join("assets", "stickers")
OUT_DIR = os.path.join("assets", "animated")

INK = (20, 22, 29, 255)
WHITE = (255, 255, 255, 255)


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
# C-LEVEL MESH WARP & VOLUME-PRESERVING SQUASH & STRETCH
# =============================================================================
def prep_breathing_room(im: Image.Image, scale: float = 0.91) -> Image.Image:
    """Keep a slight safety margin inside 512x512 so die-cut borders never clip during comic jumps."""
    w, h = im.size
    nw, nh = int(round(w * scale)), int(round(h * scale))
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
    """Volume-preserving squash & stretch around anchor (cx, cy). sy > 1 stretches vertically & narrows X."""
    sy_clamped = max(0.65, min(1.45, sy))
    sx = 1.0 / math.sqrt(sy_clamped)
    # Inverse mapping: src = center + (dst - center) / scale
    src_x = cx + (x - cx) / sx
    src_y = cy + (y - cy) / sy_clamped
    return (src_x - x, src_y - y)


# =============================================================================
# PRO COMIC-BOOK & 3D GRAPHIC FX PRIMITIVES (Ink Outlines + Speculars)
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
    # Ink silhouette first, then clean filled interior so lobes merge seamlessly!
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
# RIG CLASSIFICATION (ALL 128+ STICKERS MAPPED TO PICTURE-SPECIFIC PERSONALITIES)
# =============================================================================
def classify_rig(sid: str) -> str:
    s = sid.lower()
    if "maco" in s:
        return "maco_window_binoculars"
    if s == "steups":
        return "steups_puff"
    if s == "slang-steups":
        return "steups_sideeye_emoji"
    if "ah-eh-able" in s:
        return "fan_and_sweat"
    if "savannah-coconut" in s:
        return "coconut_chop"
    if any(k in s for k in ("red-flag", "flag", "rag")):
        return "flag_on_rigid_pole"
    if "yuh-too-lie" in s:
        return "pinocchio_nose_grow"
    if "doh-start" in s:
        return "zipper_lips_slide"
    if "ah-gone" in s:
        return "ninja_poof"
    if "mad-ting" in s:
        return "mind_blown_fireworks"
    if any(k in s for k in ("doh-be-a-dotish", "chupidee")):
        return "dizzy_spiral_spin"
    if "dotishness" in s:
        return "facepalm_smack"
    if "tabanca" in s:
        return "broken_heart_tear"
    if "left-on-read" in s or "hard-lucks-dey" in s:
        return "broke_pockets_moth"
    if "link-me" in s:
        return "phone_ring_vibrate"
    if "real-bad" in s:
        return "siren_alarm_flash"
    if "trini-mom-spoon" in s:
        return "frozen_chicken_clock"
    if "ttec-current-gone" in s:
        return "ttec_blackout_candle"
    if "wasa-water-gone" in s:
        return "wasa_dry_shower"
    if "crapaud-pipe" in s:
        return "crapaud_smoke_pipe"
    if "flying-slipper" in s:
        return "slipper_missile"
    if "just-now" in s:
        return "hourglass_sand"
    if any(k in s for k in ("eagle", "sou-sou")):
        return "eagle_wing_flap"
    if any(k in s for k in ("liming", "soft-launch", "wha-go-on", "bet", "link-up", "too-much", "ah-done")):
        return "two_part_clink"
    if any(k in s for k in ("doh-study-dat", "no-maljo", "mind-yuh-business", "delulu")):
        return "shield_deflect"
    if any(k in s for k in ("highway-traffic", "maxi-taxi", "stay-in-yuh-lane")):
        return "wheel_pothole_swerve"
    if any(k in s for k in ("bullseye-allfours", "hang-jack", "mash-up", "real-talk", "ah-reach", "right-dey", "no-cap")):
        return "overhead_hand_slam"
    if any(k in s for k in ("blue-devil", "soucouyant", "vex", "yuh-mad", "wicked", "horn", "badmind", "im-dead")):
        return "fire_breath_and_steam"
    if "moko-jumbie" in s or "carnival-mas" in s:
        return "moko_stilt_walk"
    if any(k in s for k in ("tassa-chutney", "steelpan-3d", "parang-season", "vibes")):
        return "drumstick_double_beat"
    if any(k in s for k in ("freshwater-yankee", "doh-tote", "leh-we-go", "ah-coming", "lowkey")):
        return "jet_and_toss_flight"
    if any(k in s for k in ("weyyyy", "ah-screaming", "wha-yuh-say", "hear-nah", "yuh-outside", "highkey")):
        return "megaphone_cone_blast"
    if any(k in s for k in ("killing-me-dead", "doh-kill-meh", "a-week", "im-weak", "just-picong", "is-a-jokes", "yuh-jokin")):
        return "laugh_tears_and_spin"
    if any(k in s for k in ("rizz", "doh-watch-me", "potcake-dog", "good-vibes-only", "take-a-set", "dont-hot-up-yuh-head", "the-vibe-different", "yuh-real-brave", "big-up-yuhself")):
        return "sunglasses_cool_nod"
    if any(k in s for k in ("fass", "lemme-see", "wha-yuh-on", "high-beam", "watch-nah", "how-yuh-mean")):
        return "optical_spy_zoom"
    if any(k in s for k in ("trini-chow", "crix-and-cheese", "buss-up-shut", "sunday-lunch", "corn-soup", "doubles-3d", "slight-pepper", "bake-and-shark", "crab-and-dumpling", "deya-parsad", "ate", "rel-bess", "small-ting")):
        return "culinary_steam_pop"
    return "articulated_gesture"


# =============================================================================
# PICTURE-SPECIFIC COMIC ANIMATION RENDERER
# =============================================================================
def render_picture_specific_frame(im: Image.Image, rig: str, sid: str, f: int, n_frames: int = 24) -> Image.Image:
    W, H = im.size
    t = f / n_frames
    ang = 2.0 * math.pi * t
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # -------------------------------------------------------------------------
    # 1. MACO: Shaded Comic Window Blinds Snap Up -> Guy Pops Forward -> Double-Take Binocular Scan!
    # -------------------------------------------------------------------------
    if rig == "maco_window_binoculars":
        if t < 0.18:
            # Blinds closed, quick anticipation tug right before snapping up
            open_p = 0.0
            cord_pull = math.sin((t / 0.18) * math.pi) * 14.0
            bino_zoom = 0.0
            scan = 0.0
            pop_y = 0.0
        elif t < 0.30:
            u = (t - 0.18) / 0.12
            open_p = clamp01(ease_out_back(u, 1.3))
            cord_pull = -8.0 * (1.0 - u)
            bino_zoom = clamp01(u)
            scan = 0.0
            pop_y = ease_out_back(u, 2.0)
        elif t < 0.78:
            open_p = 1.0
            cord_pull = 0.0
            sub_t = (t - 0.30) / 0.48
            # Comic scan: look left, pause, SNAP double-take right!
            if sub_t < 0.42:
                scan = -ease_in_out_cubic(sub_t / 0.42)
                bino_zoom = 0.85 + 0.15 * math.sin(sub_t * math.pi)
            elif sub_t < 0.58:
                scan = -1.0 + 2.0 * ease_out_back((sub_t - 0.42) / 0.16, 1.8)
                bino_zoom = 1.15
            else:
                scan = 1.0 * (1.0 - ease_in_out_cubic((sub_t - 0.58) / 0.42))
                bino_zoom = 1.0 - 0.15 * ((sub_t - 0.58) / 0.42)
            pop_y = 1.0
        else:
            close_u = (t - 0.78) / 0.22
            open_p = 1.0 - ease_in_out_cubic(close_u)
            cord_pull = 0.0
            bino_zoom = max(0.0, 1.0 - close_u * 2.5)
            scan = 0.0
            pop_y = max(0.0, 1.0 - close_u * 2.0)

        bino_cx = 290.0 + scan * 22.0
        bino_cy = 205.0

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Curtains part outward softly
            wy_c = math.exp(-((y - 265.0) / 130.0) ** 4)
            wx_l = math.exp(-((x - 145.0) / 45.0) ** 2) * wy_c
            wx_r = math.exp(-((x - 367.0) / 45.0) ** 2) * wy_c
            dx += -(1.0 - open_p) * 22.0 * wx_l + (1.0 - open_p) * 22.0 * wx_r

            # Subtle character pop-forward (squash & stretch) + binocular zoom & scan
            if pop_y > 0.01:
                w_guy = math.exp(-((x - 256.0) / 110.0) ** 2 - ((y - 260.0) / 120.0) ** 2)
                sx, sy = squash_stretch_offset(x, y, 256.0, 360.0, 1.0 + 0.07 * pop_y)
                dx += sx * w_guy
                dy += sy * w_guy

            if bino_zoom > 0.01:
                dist2 = ((x - bino_cx) / 110.0) ** 2 + ((y - bino_cy) / 78.0) ** 2
                w_b = math.exp(-dist2 * 1.35)
                sf = 1.0 / (1.0 + 0.34 * bino_zoom * w_b)
                dx += (x - bino_cx) * (sf - 1.0) - scan * 28.0 * w_b
                dy += (y - bino_cy) * (sf - 1.0) + bino_zoom * 7.0 * w_b

            # Coffee steam curl
            w_st = math.exp(-((x - 260.0) / 22.0) ** 2 - ((y - 335.0) / 28.0) ** 2)
            dx += math.sin(ang * 2.0 + y * 0.14) * 6.0 * w_st
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=18)

        # Comic-inked 3D shaded wooden Venetian blinds inside the window frame
        blind_top = 104
        blind_bottom = int(blind_top + (1.0 - open_p) * 298)
        if blind_bottom > blind_top + 6:
            # Cast shadow behind blinds
            od.rectangle([156, blind_top, 358, min(408, blind_bottom + 8)], fill=(14, 16, 22, 110))
            slat_h = 18
            for sy in range(blind_top, blind_bottom, slat_h):
                y2 = min(sy + slat_h - 2, blind_bottom)
                # Warm shaded slat with dark comic ink outline + top specular bevel
                od.rounded_rectangle([154, sy, 358, y2], radius=3, fill=(208, 146, 78, 252), outline=(66, 36, 14, 255), width=2)
                if y2 - sy >= 6:
                    od.line([(158, sy + 3), (354, sy + 3)], fill=(252, 214, 152, 235), width=2)
                    od.line([(158, y2 - 2), (354, y2 - 2)], fill=(148, 92, 38, 210), width=2)
            # Bottom weighted wooden rail
            od.rounded_rectangle([150, blind_bottom - 5, 362, blind_bottom + 5], radius=4, fill=(172, 108, 44, 255), outline=(58, 30, 10, 255), width=2)
            # Swing pull-cord + tassel
            cord_x = int(256 + scan * 8)
            cord_y2 = int(blind_bottom + 24 + cord_pull)
            od.line([(256, blind_top), (cord_x, cord_y2)], fill=(58, 30, 10, 240), width=4)
            od.line([(256, blind_top), (cord_x, cord_y2)], fill=(250, 240, 215, 245), width=2)
            od.ellipse([cord_x - 6, cord_y2 - 2, cord_x + 6, cord_y2 + 10], fill=(255, 196, 36, 255), outline=(58, 30, 10, 255), width=2)

        # Comic lens gleam + double-take "PEEK!" speed-lines
        if bino_zoom > 0.4:
            lx = int(342 + scan * 22)
            ly = int(196 - bino_zoom * 3)
            tw_s = 13.0 * min(1.2, bino_zoom)
            draw_comic_twinkle(od, lx, ly, tw_s, fill=(140, 245, 255, 255), rot=ang * 0.5, alpha=int(235 * min(1.0, bino_zoom)))
            if abs(scan) > 0.65:
                draw_comic_speed_lines(od, lx + (25 if scan > 0 else -45), ly, [-20, 0, 20] if scan > 0 else [160, 180, 200], 18, 36, color=(255, 212, 59, 220), width=3)

        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 2. STEUPS (3D Side-Eye Character with Air Puff)
    # -------------------------------------------------------------------------
    if rig == "steups_puff":
        p = comic_pop_curve(t, 0.18, 0.34, 0.68)
        puff = max(0.0, p)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            sx, sy = squash_stretch_offset(x, y, 256.0, 280.0, 1.0 - 0.06 * p)
            dx += sx
            dy += sy
            w_eyes = math.exp(-((x - 245.0) / 100.0) ** 2 - ((y - 210.0) / 40.0) ** 2)
            dx += -max(0.0, p) * 14.0 * w_eyes
            w_lips = math.exp(-((x - 260.0) / 45.0) ** 2 - ((y - 295.0) / 36.0) ** 2)
            dx += (x - 260.0) * 0.25 * max(0.0, p) * w_lips
            w_puff = math.exp(-((x - 345.0) / 62.0) ** 2 - ((y - 285.0) / 52.0) ** 2)
            sf = 1.0 / (1.0 + 0.36 * puff * w_puff)
            dx += (x - 315.0) * (sf - 1.0) - puff * 26.0 * w_puff
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if puff > 0.25:
            draw_comic_speed_lines(od, 365 + puff * 28, 285, [-18, 0, 18], 12, 34, color=(235, 250, 255, int(215 * puff)), width=3)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 3. SLANG-STEUPS (Yellow -_- Emoji: Heavy Blink + Side-Eye Cut + Sweat Drop!)
    # -------------------------------------------------------------------------
    if rig == "steups_sideeye_emoji":
        cut = comic_pop_curve(t, 0.16, 0.32, 0.72)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 275.0, 1.0 - 0.05 * cut)
            # Eyes cut sharply sideways & brow dips in pure unimpressed attitude
            w_eyes = math.exp(-((x - 256.0) / 130.0) ** 2 - ((y - 235.0) / 48.0) ** 2)
            dx += -cut * 20.0 * w_eyes
            dy += abs(cut) * 6.0 * w_eyes
            # Flat mouth squints/twitches slightly
            w_mouth = math.exp(-((x - 256.0) / 85.0) ** 2 - ((y - 318.0) / 28.0) ** 2)
            dy += cut * 5.0 * w_mouth
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if cut > 0.2:
            drop_y = 148 + cut * 28
            draw_comic_droplet(od, 366, drop_y, scale=1.05, alpha=int(235 * min(1.0, cut * 1.4)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 4. AH EH ABLE: Rapid Wrist-Pivot Fanning + Comic Breeze Arcs + Sweat Drop
    # -------------------------------------------------------------------------
    if rig == "fan_and_sweat":
        fan_angle = 0.36 * math.sin(ang * 2.0)
        pant = 0.5 + 0.5 * math.sin(ang * 2.0)
        drip = (t * 2.0) % 1.0

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 320.0, 1.0 - 0.04 * pant)
            w_fan = math.exp(-((x - 288.0) / 110.0) ** 2 - ((y - 318.0) / 82.0) ** 2)
            if w_fan > 0.01:
                theta = fan_angle * w_fan
                rx, ry = x - 305.0, y - 365.0
                dx += rx * (math.cos(theta) - 1.0) - ry * math.sin(theta)
                dy += rx * math.sin(theta) + ry * (math.cos(theta) - 1.0)
            w_drop = math.exp(-((x - 342.0) / 40.0) ** 2 - ((y - 165.0) / 50.0) ** 2)
            dy += -(drip * 24.0) * w_drop
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if abs(fan_angle) > 0.15:
            draw_comic_speed_lines(od, 225, 310, [-155, -175], 70, 96, color=(255, 255, 255, 190), width=3)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 5. SAVANNAH COCONUT: Anticipation Wind-Up -> Machete Chop -> Cap Pops + Glossy Splash!
    # -------------------------------------------------------------------------
    if rig == "coconut_chop":
        if t < 0.22:
            chop = -ease_in_out_cubic(t / 0.22)
            pop = 0.0
            squash = 1.0 + 0.05 * (-chop)
        elif t < 0.35:
            u = (t - 0.22) / 0.13
            chop = -1.0 + 2.0 * u
            pop = max(0.0, (u - 0.5) * 1.1)
            squash = 1.0 - 0.10 * max(0.0, u - 0.4)
        elif t < 0.78:
            u = (t - 0.35) / 0.43
            chop = 1.0 - ease_in_out_cubic(u)
            pop = math.sin(u * math.pi) * 1.15
            squash = 1.0 + 0.06 * math.sin(u * math.pi)
        else:
            chop = 0.0
            pop = 0.0
            squash = 1.0

        shx, shy = impact_shake(t, 0.31, amp=8.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 380.0, squash)
            dx += shx
            dy += shy
            w_cap = math.exp(-((x - 165.0) / 88.0) ** 2 - ((y - 125.0) / 72.0) ** 2)
            dx += pop * 22.0 * w_cap
            dy += pop * 36.0 * w_cap
            w_blade = math.exp(-((x - 310.0) / 130.0) ** 2 - ((y - 185.0) / 92.0) ** 2) * (1.0 - w_cap * 0.8)
            dy += -chop * 28.0 * w_blade
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if 0.28 < t < 0.50:
            p_hit = 1.0 - abs(t - 0.36) / 0.14
            draw_comic_starburst(od, 240, 215, 36 * p_hit, 16 * p_hit, 8, alpha=int(240 * p_hit))
        if pop > 0.18:
            for i in range(5):
                a = -math.pi * 0.85 + i * 0.38
                dist = 32 + pop * 72
                sx = 248 + math.cos(a) * dist
                sy = 235 + math.sin(a) * dist
                draw_comic_droplet(od, sx, sy, scale=0.85, alpha=int(235 * min(1.0, (1.15 - pop * 0.4))))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 6. RED FLAG / WAVE RAG: Rigid Pole + Snappy Traveling Wind Billow + Glint
    # -------------------------------------------------------------------------
    if rig == "flag_on_rigid_pole":
        def disp(x, y):
            cloth_w = max(0.0, min(1.0, (x - 150.0) / 235.0))
            wave = math.sin(ang * 2.0 - (x - 150.0) * 0.032) + 0.35 * math.sin(ang * 4.0 - (x - 150.0) * 0.05)
            dy = -wave * 22.0 * cloth_w
            dx = math.cos(ang * 2.0 - (x - 150.0) * 0.032) * 7.0 * cloth_w
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=18)
        draw_comic_twinkle(od, 128, 92, 10.0 + 4.0 * math.sin(ang * 2.0), rot=ang * 0.5, alpha=210)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 7. PINOCCHIO NOSE GROWING ("Yuh too lie!") — BOING! Elastic Overshoot + Twinkle!
    # -------------------------------------------------------------------------
    if rig == "pinocchio_nose_grow":
        grow = comic_pop_curve(t, 0.15, 0.32, 0.72)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 220.0, 260.0, 1.0 + 0.05 * grow)
            w_nose = math.exp(-((x - 335.0) / 92.0) ** 2 - ((y - 256.0) / 48.0) ** 2)
            dx += -grow * 48.0 * w_nose
            dy += math.sin(ang * 4.0) * 3.0 * max(0.0, grow) * w_nose
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if grow > 0.35:
            draw_comic_speed_lines(od, 415, 250, [-25, 0, 25], 16, 36, color=(255, 212, 59, int(225 * min(1.0, grow))), width=3)
            draw_comic_twinkle(od, 412, 200, 14.0 * min(1.1, grow), rot=ang, alpha=230)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 8. ZIPPER LIPS SLIDING SHUT ("Doh start") — Snappy Zip + Metallic *TING!*
    # -------------------------------------------------------------------------
    if rig == "zipper_lips_slide":
        zip_p = 0.5 - 0.5 * math.cos(ang)
        zx = 165.0 + zip_p * 185.0

        def disp(x, y):
            w_lip = math.exp(-((y - 260.0) / 52.0) ** 2 - ((x - 256.0) / 125.0) ** 2)
            pinch = 0.22 if x < zx else -0.14
            dy = (y - 260.0) * pinch * w_lip
            w_tab = math.exp(-((x - 325.0) / 55.0) ** 2 - ((y - 275.0) / 55.0) ** 2)
            dx = -(zip_p - 0.5) * 42.0 * w_tab
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        draw_comic_twinkle(od, zx, 262, 13.0 + 4.0 * math.sin(ang * 2.0), fill=(255, 224, 90, 255), rot=ang, alpha=240)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 9. NINJA POOF ("Ah gone"): Peace Hand Twinkles -> Shrinks & Smoke Cloud Puffs!
    # -------------------------------------------------------------------------
    if rig == "ninja_poof":
        poof = comic_pop_curve(t, 0.16, 0.34, 0.72)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Left hand pops then shrinks back into smoke
            w_hand = math.exp(-((x - 190.0) / 115.0) ** 2 - ((y - 265.0) / 135.0) ** 2)
            sf_h = 1.0 + 0.18 * max(0.0, poof) * w_hand
            dx += (x - 190.0) * (sf_h - 1.0)
            dy += (y - 265.0) * (sf_h - 1.0)
            # Right smoke cloud expands dramatically
            w_cloud = math.exp(-((x - 345.0) / 78.0) ** 2 - ((y - 235.0) / 78.0) ** 2)
            sf_c = 1.0 / (1.0 + 0.38 * max(0.0, poof) * w_cloud)
            dx += (x - 345.0) * (sf_c - 1.0) - max(0.0, poof) * 18.0 * w_cloud
            dy += (y - 235.0) * (sf_c - 1.0) + max(0.0, poof) * 10.0 * w_cloud
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if poof > 0.3:
            draw_comic_puff(od, 365 + poof * 16, 175 - poof * 16, 18 * poof, alpha=int(215 * min(1.0, poof)))
            draw_comic_twinkle(od, 165, 118, 12 * min(1.0, poof), rot=ang, alpha=230)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 10. MIND BLOWN FIREWORKS ("Mad ting") — Anticipation Squash -> KABOOM Burst!
    # -------------------------------------------------------------------------
    if rig == "mind_blown_fireworks":
        boom = comic_pop_curve(t, 0.18, 0.32, 0.70)
        shx, shy = impact_shake(t, 0.30, amp=9.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 380.0, 1.0 + 0.08 * boom)
            dx += shx
            dy += shy
            # Fireworks & stars erupting out of top (y < 210)
            w_top = math.exp(-((y - 125.0) / 78.0) ** 2)
            sf = 1.0 / (1.0 + 0.30 * max(0.0, boom) * w_top)
            dx += (x - 256.0) * (sf - 1.0)
            dy += (y - 195.0) * (sf - 1.0) + max(0.0, boom) * 22.0 * w_top
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if boom > 0.25:
            draw_comic_twinkle(od, 132, 108 - boom * 18, 15 * min(1.1, boom), fill=(255, 80, 210, 255), rot=ang, alpha=240)
            draw_comic_twinkle(od, 382, 112 - boom * 18, 15 * min(1.1, boom), fill=(0, 229, 255, 255), rot=-ang, alpha=240)
            draw_comic_twinkle(od, 256, 74 - boom * 14, 17 * min(1.1, boom), fill=(255, 220, 60, 255), rot=ang * 1.5, alpha=240)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 11. DIZZY SPIRAL EYES & PROPELLER CAP ("Doh be a dotish", "Chupidee")
    # -------------------------------------------------------------------------
    if rig == "dizzy_spiral_spin":
        wobble = math.sin(ang)
        spin_dir = math.sin(ang * 2.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 310.0, 1.0 + 0.05 * math.cos(ang * 2.0))
            dx += -wobble * 12.0
            # Local swirl twist in left and right eye regions
            for ex, ey in [(198.0, 225.0), (314.0, 225.0)]:
                r2 = (x - ex) ** 2 + (y - ey) ** 2
                w_eye = math.exp(-r2 / (44.0 ** 2))
                if w_eye > 0.02:
                    th = 0.65 * spin_dir * w_eye
                    rx, ry = x - ex, y - ey
                    dx += rx * (math.cos(th) - 1.0) - ry * math.sin(th)
                    dy += rx * math.sin(th) + ry * (math.cos(th) - 1.0)
            if "chupidee" in sid:
                w_prop = math.exp(-((x - 256.0) / 100.0) ** 2 - ((y - 98.0) / 38.0) ** 2)
                dx += -(x - 256.0) * 0.45 * (0.5 - 0.5 * math.cos(ang * 4.0)) * w_prop
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=18)
        # Orbiting comic dizzy stars around top of head
        for i in range(2):
            a_orb = ang + i * math.pi
            sx = 256 + math.cos(a_orb) * 112
            sy = 88 + math.sin(a_orb) * 18
            draw_comic_twinkle(od, sx, sy, 12.0, fill=(255, 224, 64, 255), rot=ang * 2.0, alpha=235)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 12. FORHEAD FACEPALM SMACK ("Dotishness"): Hand Lifts -> SLAMS Forehead!
    # -------------------------------------------------------------------------
    if rig == "facepalm_smack":
        if t < 0.26:
            lift = ease_in_out_cubic(t / 0.26)
            hit = 0.0
        elif t < 0.40:
            u = (t - 0.26) / 0.14
            lift = 1.0 - 1.15 * u
            hit = max(0.0, (u - 0.6) * 2.5)
        elif t < 0.78:
            u = (t - 0.40) / 0.38
            lift = -0.15 * (1.0 - u)
            hit = max(0.0, 1.0 - u * 1.8)
        else:
            lift = 0.0
            hit = 0.0

        shx, shy = impact_shake(t, 0.38, amp=10.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 340.0, 1.0 - 0.08 * hit)
            dx += shx
            dy += shy
            w_hand = math.exp(-((x - 210.0) / 95.0) ** 2 - ((y - 165.0) / 85.0) ** 2)
            dy += lift * 38.0 * w_hand
            dx += lift * 16.0 * w_hand
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if hit > 0.2:
            draw_comic_starburst(od, 220, 155, 34 * hit, 14 * hit, 8, alpha=int(230 * hit))
            draw_comic_speed_lines(od, 210, 150, [-135, -90, -45], 38, 66, color=(255, 212, 59, int(230 * hit)), width=4)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 13. BROKEN HEART TABANCA ("Tabanca"): Heart Quivers Apart + Big Teardrop Drips!
    # -------------------------------------------------------------------------
    if rig == "broken_heart_tear":
        crack = 0.5 - 0.5 * math.cos(ang * 2.0)
        drip = (t * 2.0) % 1.0

        def disp(x, y):
            side = -1.0 if x < 256.0 else 1.0
            w_half = min(1.0, abs(x - 256.0) / 60.0) * math.exp(-((y - 245.0) / 135.0) ** 2)
            dx = -side * crack * 16.0 * w_half
            dy = math.sin(ang * 4.0) * 3.0 * crack
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        draw_comic_droplet(od, 346, 330 + drip * 42, scale=1.25, alpha=int(240 * (1.0 - drip * 0.45)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 14. BROKE POCKETS MOTH / EMPTY POT ("Left on read", "Hard lucks dey")
    # -------------------------------------------------------------------------
    if rig == "broke_pockets_moth":
        shiver = math.sin(ang * 4.0)
        pull = 0.5 - 0.5 * math.cos(ang * 2.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 350.0, 1.0 - 0.04 * pull)
            side = -1.0 if x < 256.0 else 1.0
            w_pock = min(1.0, abs(x - 256.0) / 70.0) * math.exp(-((y - 315.0) / 95.0) ** 2)
            dx += -side * pull * 20.0 * w_pock + shiver * 3.0
            # Moth flutters upward on top-right
            w_moth = math.exp(-((x - 360.0) / 55.0) ** 2 - ((y - 165.0) / 55.0) ** 2)
            dy += math.sin(ang * 3.0) * 18.0 * w_moth
            dx += math.cos(ang * 2.0) * 10.0 * w_moth
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if pull > 0.35:
            draw_comic_puff(od, 155, 290 - pull * 25, 13 * pull, fill=(225, 232, 240, 255), alpha=int(180 * pull))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 15. PHONE RINGING VIBRATION ("Link me"): Authentic BRRRING-BRRRING + Pause!
    # -------------------------------------------------------------------------
    if rig == "phone_ring_vibrate":
        ring_active = (0.08 < t < 0.40) or (0.55 < t < 0.87)
        vib = math.sin(t * 2.0 * math.pi * 14.0) if ring_active else 0.0
        hop = abs(math.sin(t * 2.0 * math.pi * 7.0)) if ring_active else 0.0

        def disp(x, y):
            dx = -vib * 11.0
            dy = hop * 10.0
            w_chain = math.exp(-((x - 256.0) / 75.0) ** 2 - ((y - 256.0) / 75.0) ** 2)
            sf = 1.0 / (1.0 + 0.14 * hop * w_chain)
            dx += (x - 256.0) * (sf - 1.0)
            dy += (y - 256.0) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=14)
        if ring_active:
            draw_comic_speed_lines(od, 118, 256, [155, 180, 205], 20, 42, color=(0, 229, 255, 235), width=4)
            draw_comic_speed_lines(od, 394, 256, [-25, 0, 25], 20, 42, color=(0, 229, 255, 235), width=4)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 16. SIREN ALARM FLASH ("Real bad"): Rattling Siren + Pulsing Light Rays!
    # -------------------------------------------------------------------------
    if rig == "siren_alarm_flash":
        flash = 0.5 + 0.5 * math.sin(ang * 3.0)
        hop = abs(math.sin(ang * 3.0))

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 390.0, 1.0 + 0.08 * hop)
            dx += math.sin(ang * 6.0) * 6.0 * hop
            w_dome = math.exp(-((x - 256.0) / 85.0) ** 2 - ((y - 230.0) / 85.0) ** 2)
            sf = 1.0 / (1.0 + 0.16 * flash * w_dome)
            dx += (x - 256.0) * (sf - 1.0)
            dy += (y - 230.0) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if flash > 0.55:
            r = int(95 + (1.0 - flash) * 80)
            od.ellipse([256 - r, 210 - r, 256 + r, 210 + r], fill=(255, 65, 45, int(65 * flash)))
            draw_comic_twinkle(od, 256, 175, 16 * flash, fill=(255, 230, 120, 255), rot=ang * 2.0, alpha=230)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 17. FROZEN CHICKEN & ALARM CLOCK ("trini-mom-spoon") — EXACT COORDINATES!
    # -------------------------------------------------------------------------
    if rig == "frozen_chicken_clock":
        drip_p = (t * 2.0) % 1.0
        ring = math.sin(ang * 6.0)
        clock_hop = abs(math.sin(ang * 3.0))

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Red alarm clock is at bottom-right (385, 385)!
            w_clock = math.exp(-((x - 382.0) / 68.0) ** 2 - ((y - 382.0) / 68.0) ** 2)
            dx += ring * 13.0 * w_clock
            dy += clock_hop * 12.0 * w_clock
            # Frozen chicken block shivers slightly
            w_ice = math.exp(-((x - 230.0) / 100.0) ** 2 - ((y - 275.0) / 95.0) ** 2) * (1.0 - w_clock)
            dx += math.sin(ang * 4.0) * 3.5 * w_ice
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        # Glossy comic droplet dripping from faucet spout (262, 126 -> 192)
        draw_comic_droplet(od, 260, 128 + drip_p * 58, scale=0.95, alpha=int(245 * (1.0 - drip_p * 0.35)))
        # Comic alarm ring arcs around the bottom-right clock
        draw_comic_speed_lines(od, 382, 378, [-135, -110, -70, -45], 54, 72, color=(255, 212, 59, 230), width=3)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 18. WASA DRY SHOWERHEAD ("wasa-water-gone") — Sputtering Dust Puffs + Sad Shiver
    # -------------------------------------------------------------------------
    if rig == "wasa_dry_shower":
        cough = max(0.0, math.sin(ang * 2.0))
        look = math.sin(ang)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            w_sh = math.exp(-((x - 360.0) / 80.0) ** 2 - ((y - 105.0) / 65.0) ** 2)
            sf = 1.0 / (1.0 + 0.24 * cough * w_sh)
            dx += (x - 360.0) * (sf - 1.0)
            dy += (y - 105.0) * (sf - 1.0) - cough * 12.0 * w_sh
            w_face = math.exp(-((x - 245.0) / 95.0) ** 2 - ((y - 275.0) / 90.0) ** 2)
            dy += look * 9.0 * w_face
            dx += -look * 7.0 * w_face
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if cough > 0.3:
            draw_comic_puff(od, 335 - cough * 18, 138 + cough * 26, 14 * cough, fill=(230, 238, 245, 255), alpha=int(210 * cough))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 19. T&TEC BLACKOUT ("ttec-current-gone") — EXACT COORDINATES! Candle at (315, 330)
    # -------------------------------------------------------------------------
    if rig == "ttec_blackout_candle":
        flicker = 0.5 + 0.5 * math.sin(ang * 3.0)
        drip = (t * 2.0) % 1.0

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Candle flame is at (315, 310)!
            w_flame = math.exp(-((x - 315.0) / 34.0) ** 2 - ((y - 310.0) / 40.0) ** 2)
            dx += math.sin(ang * 4.0) * 8.0 * w_flame
            dy += flicker * 12.0 * w_flame
            # Guy on left (cx=185, cy=255) sweats & breathes heavily
            w_guy = math.exp(-((x - 185.0) / 75.0) ** 2 - ((y - 255.0) / 85.0) ** 2)
            dy += math.sin(ang * 2.0) * 5.0 * w_guy
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        r = int(26 + flicker * 16)
        od.ellipse([315 - r, 305 - r, 315 + r, 305 + r], fill=(255, 196, 40, int(65 + flicker * 55)))
        draw_comic_droplet(od, 152, 222 + drip * 22, scale=0.75, alpha=int(230 * (1.0 - drip * 0.4)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 20. CRAPAUD PUFFING PIPE & BOTH CYAN SMOKE PLUMES ("crapaud-pipe")
    # -------------------------------------------------------------------------
    if rig == "crapaud_smoke_pipe":
        puff = 0.5 - 0.5 * math.cos(ang * 2.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Toad throat sac (cx=248, cy=280) inflates
            w_throat = math.exp(-((x - 248.0) / 68.0) ** 2 - ((y - 280.0) / 52.0) ** 2)
            sf = 1.0 / (1.0 + 0.25 * puff * w_throat)
            dx += (x - 248.0) * (sf - 1.0)
            dy += (y - 280.0) * (sf - 1.0)
            # Left pipe smoke (125, 155) & Right smoke rings (375, 130) float upward
            w_sl = math.exp(-((x - 125.0) / 60.0) ** 2 - ((y - 155.0) / 65.0) ** 2)
            w_sr = math.exp(-((x - 375.0) / 75.0) ** 2 - ((y - 135.0) / 70.0) ** 2)
            dy += math.sin(ang) * 18.0 * (w_sl + w_sr)
            dx += math.cos(ang * 2.0) * 10.0 * (w_sl + w_sr)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if puff > 0.35:
            od.ellipse([118, 240, 142, 260], fill=(255, 120, 20, int(155 * puff)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 21. OPTICAL SPY / TELESCOPE / MAGNIFIER / HIGH BEAM
    # -------------------------------------------------------------------------
    if rig == "optical_spy_zoom":
        ext = comic_pop_curve(t, 0.14, 0.32, 0.72)
        scan = math.sin(ang)

        def disp(x, y):
            cx = 256.0 + scan * 30.0
            cy = 235.0 - max(0.0, ext) * 14.0
            w_lens = math.exp(-(((x - cx) / 110.0) ** 2 + ((y - cy) / 110.0) ** 2))
            sf = 1.0 / (1.0 + 0.32 * max(0.0, ext) * w_lens)
            dx = (x - cx) * (sf - 1.0) - scan * 14.0 * w_lens
            dy = (y - cy) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if ext > 0.35:
            lx = 256.0 + scan * 36.0
            ly = 230.0 - ext * 14.0
            draw_comic_twinkle(od, lx + 18, ly - 18, 13 * min(1.1, ext), fill=(160, 248, 255, 255), rot=ang, alpha=230)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 22. EAGLE WING-FLAP & CASH SWOOP ("eagle", "sou-sou")
    # -------------------------------------------------------------------------
    if rig == "eagle_wing_flap":
        flap = math.sin(ang * 2.0)
        swoop = 0.5 - 0.5 * math.cos(ang)

        def disp(x, y):
            w_wing = max(0.0, ((x - 256.0) / 195.0) ** 2) * math.exp(-((y - 175.0) / 115.0) ** 2)
            dy = -flap * 40.0 * min(1.2, w_wing) - swoop * 10.0
            w_cash = math.exp(-((x - 256.0) / 90.0) ** 2 - ((y - 360.0) / 80.0) ** 2)
            sf = 1.0 / (1.0 + 0.22 * swoop * w_cash)
            dx = (x - 256.0) * (sf - 1.0)
            dy += (y - 360.0) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if swoop > 0.45:
            draw_comic_twinkle(od, 256, 395, 14 * swoop, fill=(255, 224, 70, 255), rot=ang, alpha=235)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 23. TWO-PART CLINK / FIST BUMP / HANDSHAKE — Anticipation -> SLAM + Comic Starburst!
    # -------------------------------------------------------------------------
    if rig == "two_part_clink":
        clink = comic_pop_curve(t, 0.16, 0.30, 0.68)
        shx, shy = impact_shake(t, 0.29, amp=8.0)

        def disp(x, y):
            side = -1.0 if x < 256.0 else 1.0
            w_mid = math.exp(-((y - 256.0) / 155.0) ** 2) * min(1.0, abs(x - 256.0) / 65.0)
            dx = side * clink * 22.0 * w_mid + shx
            dy = abs(clink) * 7.0 * w_mid + shy
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if clink > 0.60:
            p = min(1.0, (clink - 0.60) / 0.40)
            draw_comic_starburst(od, 256, 228, 34 * p, 14 * p, 8, alpha=int(240 * p))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 24. HOURGLASS FLOWING SAND ("Just now")
    # -------------------------------------------------------------------------
    if rig == "hourglass_sand":
        tilt = 0.11 * math.sin(ang)

        def disp(x, y):
            rx, ry = x - 256.0, y - 256.0
            return (x + rx * (math.cos(tilt) - 1.0) - ry * math.sin(tilt),
                    y + rx * math.sin(tilt) + ry * (math.cos(tilt) - 1.0))

        frame = warp_mesh(im, disp, grid_n=14)
        for i in range(6):
            sy = int(238 + ((t * 170 + i * 18) % 102))
            draw_comic_droplet(od, 256, sy, scale=0.45, fill=(0, 229, 255, 255), alpha=230)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 25. SHIELD / UMBRELLA DEFLECT / DELULU CLOUD
    # -------------------------------------------------------------------------
    if rig == "shield_deflect":
        pulse = comic_pop_curve(t, 0.16, 0.34, 0.72)

        def disp(x, y):
            w_dome = math.exp(-((x - 256.0) / 145.0) ** 2 - ((y - 230.0) / 115.0) ** 2)
            sf = 1.0 / (1.0 + 0.18 * max(0.0, pulse) * w_dome)
            dx = (x - 256.0) * (sf - 1.0)
            dy = (y - 230.0) * (sf - 1.0) + max(0.0, pulse) * 14.0 * w_dome
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if pulse > 0.35:
            draw_comic_twinkle(od, 155, 130, 13 * min(1.0, pulse), fill=(0, 229, 255, 255), rot=ang, alpha=225)
            draw_comic_twinkle(od, 360, 145, 11 * min(1.0, pulse), fill=(255, 212, 59, 255), rot=-ang, alpha=225)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 26. HEAT-SEEKING SLIPPER MISSILE ("flying-slipper")
    # -------------------------------------------------------------------------
    if rig == "slipper_missile":
        swoop = comic_pop_curve(t, 0.15, 0.34, 0.72)

        def disp(x, y):
            w_slip = math.exp(-((x - 235.0) / 115.0) ** 2 - ((y - 205.0) / 115.0) ** 2)
            sf = 1.0 / (1.0 + 0.28 * max(0.0, swoop) * w_slip)
            dx = (x - 235.0) * (sf - 1.0) - swoop * 22.0 * w_slip
            dy = (y - 205.0) * (sf - 1.0) + swoop * 20.0 * w_slip
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if swoop > 0.25:
            draw_comic_speed_lines(od, 145, 365, [125, 135, 145], 20, 62, color=(0, 229, 255, int(220 * min(1.0, swoop))), width=4)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 27. WHEEL SWERVING OVER POTHOLE ("highway-traffic", "maxi-taxi")
    # -------------------------------------------------------------------------
    if rig == "wheel_pothole_swerve":
        bounce = abs(math.sin(ang * 2.0))

        def disp(x, y):
            w_wheel = math.exp(-((x - 340.0) / 120.0) ** 2 - ((y - 185.0) / 115.0) ** 2)
            dy = bounce * 24.0 * w_wheel
            dx = math.sin(ang * 2.0) * 14.0 * w_wheel
            w_leaf = math.exp(-((x - 205.0) / 65.0) ** 2 - ((y - 265.0) / 55.0) ** 2) * (1.0 - w_wheel)
            dx += math.sin(ang * 2.0) * 9.0 * w_leaf
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if bounce > 0.65:
            draw_comic_speed_lines(od, 135, 340, [165, 180, 195], 15, 44, color=(255, 255, 255, 200), width=3)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 28. OVERHEAD HAND / MALLET SLAMMING ("bullseye-allfours", "hang-jack", "mash-up")
    # -------------------------------------------------------------------------
    if rig == "overhead_hand_slam":
        if t < 0.28:
            lift = ease_in_out_cubic(t / 0.28)
            slam = 0.0
        elif t < 0.42:
            u = (t - 0.28) / 0.14
            lift = 1.0 - 1.35 * u
            slam = max(0.0, (u - 0.5) * 2.0)
        elif t < 0.78:
            u = (t - 0.42) / 0.36
            lift = -0.35 * (1.0 - u)
            slam = max(0.0, 1.0 - u * 1.6)
        else:
            lift = 0.0
            slam = 0.0

        shx, shy = impact_shake(t, 0.40, amp=11.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 385.0, 1.0 - 0.08 * slam)
            dx += shx
            dy += shy
            w_hand = math.exp(-((x - 285.0) / 130.0) ** 2 - ((y - 180.0) / 110.0) ** 2)
            dy += lift * 38.0 * w_hand
            if slam > 0.05:
                side = -1.0 if x < 256.0 else 1.0
                w_scatter = math.exp(-((y - 315.0) / 75.0) ** 2) * min(1.0, abs(x - 256.0) / 85.0)
                dx += -side * slam * 24.0 * w_scatter
                dy += slam * 14.0 * w_scatter
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if slam > 0.25:
            draw_comic_starburst(od, 256, 330, 40 * slam, 17 * slam, 10, alpha=int(240 * slam))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 29. BLUE DEVIL / PEPPER VEX / SOUCOUYANT — Fire Breath, Steam Puffs & Anger Vein!
    # -------------------------------------------------------------------------
    if rig == "fire_breath_and_steam":
        blast = comic_pop_curve(t, 0.16, 0.34, 0.72)
        tremble = math.sin(ang * 6.0) * max(0.0, blast)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 365.0, 1.0 + 0.07 * blast)
            dx += tremble * 5.0
            if "blue-devil" in sid:
                w_wing = math.exp(-((x - 125.0) / 75.0) ** 2 - ((y - 210.0) / 65.0) ** 2)
                dy += math.sin(ang * 2.0) * 24.0 * w_wing
                w_fire = math.exp(-((x - 360.0) / 95.0) ** 2 - ((y - 205.0) / 75.0) ** 2)
                sf = 1.0 / (1.0 + 0.36 * max(0.0, blast) * w_fire)
                dx += (x - 260.0) * (sf - 1.0)
                dy += (y - 205.0) * (sf - 1.0)
            else:
                side = -1.0 if x < 256.0 else 1.0
                w_outer = min(1.0, abs(x - 256.0) / 95.0) * math.exp(-((y - 265.0) / 115.0) ** 2)
                dx += -side * max(0.0, blast) * 24.0 * w_outer
                dy += max(0.0, blast) * 16.0 * math.exp(-((y - 135.0) / 85.0) ** 2)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if ("vex" in sid or "mad" in sid) and blast > 0.3:
            draw_comic_anger_vein(od, 318, 128, s=1.05, alpha=int(235 * min(1.0, blast)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 30. MOKO JUMBIE / CARNIVAL MAS — Joyful Jump-Up & Alternating Stilts
    # -------------------------------------------------------------------------
    if rig == "moko_stilt_walk":
        step = math.sin(ang * 2.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 410.0, 1.0 + 0.05 * abs(step))
            if y > 245.0:
                w_leg = min(1.0, (y - 245.0) / 135.0)
                side = -1.0 if x < 256.0 else 1.0
                dy += side * step * 26.0 * w_leg
                dx += step * 8.0 * w_leg
            else:
                w_arm = min(1.0, abs(x - 256.0) / 85.0)
                dy += -step * 18.0 * w_arm
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        draw_comic_twinkle(od, 125, 115, 11 + 4 * abs(step), fill=(255, 212, 59, 255), rot=ang, alpha=220)
        draw_comic_twinkle(od, 385, 120, 11 + 4 * abs(step), fill=(0, 229, 255, 255), rot=-ang, alpha=220)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 31. TASSA / STEELPAN / BOOMBOX VIBES — Snappy Beat + Floating Comic Music Notes!
    # -------------------------------------------------------------------------
    if rig == "drumstick_double_beat":
        beat = math.sin(ang * 4.0)
        groove = abs(math.sin(ang * 2.0))

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 380.0, 1.0 - 0.07 * groove)
            if y < 300.0:
                w_stick = math.exp(-((y - 175.0) / 95.0) ** 2) * min(1.0, abs(x - 256.0) / 65.0)
                side = -1.0 if x < 256.0 else 1.0
                dy += side * beat * 24.0 * w_stick
            w_head = math.exp(-((x - 256.0) / 95.0) ** 2 - ((y - 275.0) / 65.0) ** 2)
            dy += -abs(beat) * 12.0 * w_head
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        note_y = 108 - groove * 24
        draw_comic_music_note(od, 145 + math.sin(ang * 2.0) * 10, note_y, scale=0.9, fill=(0, 229, 255, 255), alpha=225)
        draw_comic_music_note(od, 365 - math.sin(ang * 2.0) * 10, note_y + 12, scale=0.9, fill=(255, 212, 59, 255), alpha=225)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 32. JET / FLIGHT / SPRINT ("freshwater-yankee", "doh-tote", "leh-we-go")
    # -------------------------------------------------------------------------
    if rig == "jet_and_toss_flight":
        fly = math.sin(ang)

        def disp(x, y):
            w_top = math.exp(-((y - 165.0) / 105.0) ** 2)
            dx = -fly * 30.0 * w_top
            dy = fly * 20.0 * w_top
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if abs(fly) > 0.3:
            draw_comic_speed_lines(od, 140, 155, [165, 180, 195], 12, 42, color=(255, 255, 255, 200), width=3)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 33. MEGAPHONE / EAR CUP / SIREN BLAST ("weyyyy", "ah-screaming", "wha-yuh-say")
    # -------------------------------------------------------------------------
    if rig == "megaphone_cone_blast":
        thump = comic_pop_curve(t, 0.14, 0.30, 0.70)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 240.0, 320.0, 1.0 + 0.06 * thump)
            w_horn = math.exp(-((x - 275.0) / 115.0) ** 2 - ((y - 235.0) / 115.0) ** 2)
            sf = 1.0 / (1.0 + 0.26 * max(0.0, thump) * w_horn)
            dx += (x - 275.0) * (sf - 1.0)
            dy += (y - 235.0) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if thump > 0.3:
            draw_comic_speed_lines(od, 345, 230, [-35, 0, 35], 35, 75, color=(255, 212, 59, int(230 * min(1.0, thump))), width=4)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 34. BELLY LAUGH / MELTING PUDDLE ("killing-me-dead", "doh-kill-meh", "a-week", "im-weak")
    # -------------------------------------------------------------------------
    if rig == "laugh_tears_and_spin":
        laugh = math.sin(ang * 3.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 350.0, 1.0 - 0.07 * abs(laugh))
            if "week" in sid or "weak" in sid:
                w_bot = math.exp(-((y - 375.0) / 85.0) ** 2)
                melt = 0.5 - 0.5 * math.cos(ang)
                dx += -(x - 256.0) * 0.22 * melt * w_bot
                dy += -melt * 22.0 * math.exp(-((y - 220.0) / 110.0) ** 2)
            else:
                w_tears = min(1.0, abs(x - 256.0) / 110.0) * math.exp(-((y - 235.0) / 85.0) ** 2)
                side = -1.0 if x < 256.0 else 1.0
                dx += -side * max(0.0, laugh) * 24.0 * w_tears
                dy += laugh * 14.0 * math.exp(-((x - 256.0) / 120.0) ** 2)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if not ("week" in sid or "weak" in sid) and laugh > 0.25:
            draw_comic_droplet(od, 118 - laugh * 18, 255 + laugh * 14, scale=0.85, alpha=220)
            draw_comic_droplet(od, 394 + laugh * 18, 255 + laugh * 14, scale=0.85, alpha=220)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 35. SUNGLASSES COOL NOD & *TING!* GLEAM ("rizz", "potcake-dog", "good-vibes-only")
    # -------------------------------------------------------------------------
    if rig == "sunglasses_cool_nod":
        drop = comic_pop_curve(t, 0.16, 0.34, 0.72)
        sh_y = 120.0 if "potcake" in sid else 208.0

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 340.0, 1.0 + 0.05 * drop)
            w_shades = math.exp(-((x - 256.0) / 115.0) ** 2 - ((y - sh_y) / 46.0) ** 2)
            dy += -max(0.0, drop) * 18.0 * w_shades
            dx += math.sin(ang) * 7.0 * w_shades
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if drop > 0.45:
            draw_comic_twinkle(od, 338, sh_y - 22, 16 * min(1.1, drop), fill=(255, 240, 120, 255), rot=ang, alpha=240)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 36. DELICIOUS TRINI FOOD STEAM & *TING!* SPARKLE
    # -------------------------------------------------------------------------
    if rig == "culinary_steam_pop":
        pop = 0.5 - 0.5 * math.cos(ang * 2.0)

        def disp(x, y):
            dx, dy = squash_stretch_offset(x, y, 256.0, 360.0, 1.0 + 0.06 * pop)
            w_steam = math.exp(-((y - 120.0) / 75.0) ** 2)
            dx += math.sin(ang * 2.0 + y * 0.08) * 10.0 * w_steam
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        draw_comic_twinkle(od, 365, 138, 12 + 4 * pop, fill=(255, 224, 90, 255), rot=ang, alpha=225)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 37. EXPRESSIVE COMIC CHARACTER / GESTURE POP (Volume-Preserving Bounce + Attitude Snap!)
    # -------------------------------------------------------------------------
    snap = comic_pop_curve(t, 0.16, 0.34, 0.72)

    def disp(x, y):
        dx, dy = squash_stretch_offset(x, y, 256.0, 370.0, 1.0 + 0.08 * snap)
        w_top = math.exp(-((y - 185.0) / 115.0) ** 2)
        dx += math.sin(ang * 2.0) * 14.0 * w_top
        return (x + dx, y + dy)

    frame = warp_mesh(im, disp, grid_n=16)
    if snap > 0.45:
        draw_comic_twinkle(od, 380, 132, 13 * min(1.1, snap), fill=(255, 224, 80, 255), rot=ang, alpha=225)
    return Image.alpha_composite(frame, overlay)


# =============================================================================
# EXPORT ANIMATED WEBP & WHATSAPP-COMPATIBLE 24-FRAME GIF
# =============================================================================
def save_animated_webp_and_gif(base_img: Image.Image, sid: str, rig: str, webp_path: str, gif_path: str):
    n_frames = 24
    duration_ms = 90  # 24 * 90ms = 2.16s (>2.0s so WhatsApp plays it as a looping animation!)
    prepped = prep_breathing_room(base_img, scale=0.91)
    rgba_frames = [render_picture_specific_frame(prepped, rig, sid, i, n_frames) for i in range(n_frames)]

    # 1. Save Transparent 512x512 Animated WebP (crisp & lighter weight)
    rgba_frames[0].save(
        webp_path,
        format="WEBP",
        save_all=True,
        append_images=rgba_frames[1:],
        duration=duration_ms,
        loop=0,
        lossless=False,
        quality=76,
        method=4,
    )

    # 2. Save WhatsApp-Compatible 512x512 24-Frame Looping GIF on Dark Studio Card (#10141E)
    gif_frames = []
    bg_color = (16, 20, 30, 255)
    for fr in rgba_frames:
        card = Image.new("RGBA", fr.size, bg_color)
        card.alpha_composite(fr)
        rgb = card.convert("RGB")
        p_frame = rgb.quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        gif_frames.append(p_frame)

    gif_frames[0].save(
        gif_path,
        format="GIF",
        save_all=True,
        append_images=gif_frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
    )


def process_one(fname: str):
    sid = fname[:-4]
    png_path = os.path.join(STICKER_DIR, fname)
    webp_out = os.path.join(OUT_DIR, f"{sid}.webp")
    gif_out = os.path.join(OUT_DIR, f"{sid}.gif")
    rig = classify_rig(sid)
    with Image.open(png_path) as im:
        base = im.convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
        save_animated_webp_and_gif(base, sid, rig, webp_out, gif_out)
    return sid, rig, os.path.getsize(webp_out) / 1024, os.path.getsize(gif_out) / 1024


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted([f for f in os.listdir(STICKER_DIR) if f.endswith(".png")])
    print(f"Building comic-artist articulated animations for {len(files)} stickers...")
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
        futures = {ex.submit(process_one, f): f for f in files}
        for fut in as_completed(futures):
            sid, rig, w_kb, g_kb = fut.result()
            done += 1
            if done % 25 == 0 or done == len(files) or "maco" in sid:
                print(f"  [{done}/{len(files)}] {sid} ({rig}) -> WebP: {w_kb:.1f}KB, GIF: {g_kb:.1f}KB")
    print(f"Completed all {len(files)} stickers in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
