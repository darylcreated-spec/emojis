import os
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageDraw

STICKER_DIR = os.path.join("assets", "stickers")
OUT_DIR = os.path.join("assets", "animated")


def warp_mesh(img: Image.Image, disp_fn, grid_n: int = 16) -> Image.Image:
    """
    Fast C-level Pillow MESH warp using a vertex displacement function disp_fn(x, y) -> (src_x, src_y).
    Allows independent anatomical parts of a single sticker to move, zoom, pivot, or wave seamlessly.
    """
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
            mesh.append(
                (
                    (x0, y0, x1, y1),
                    (nw[0], nw[1], sw[0], sw[1], se[0], se[1], ne[0], ne[1]),
                )
            )
    return img.transform((w, h), Image.Transform.MESH, mesh, Image.Resampling.BICUBIC)


def classify_rig(sid: str) -> str:
    s = sid.lower()
    # 1. MACO: Window blind rolls up, curtains part, guy leans out & scans with binoculars
    if "maco" in s:
        return "maco_window_binoculars"
    # 2. FASS / TELESCOPE / MAGNIFYING GLASS / FLASHLIGHT
    if any(k in s for k in ("fass", "lemme-see", "wha-yuh-on", "high-beam", "watch-nah", "how-yuh-mean")):
        return "optical_spy_zoom"
    # 3. STEUPS: Eyes side-eye, lips pucker, 3D air-puff shoots out from mouth
    if "steups" in s:
        return "steups_puff"
    # 4. AH EH ABLE: Hand fan pivots back & forth rapidly around wrist while sweat drop drips
    if "ah-eh-able" in s:
        return "fan_and_sweat"
    # 5. SAVANNAH COCONUT: Machete chops down & green coconut cap pops off with water splash
    if "savannah-coconut" in s:
        return "coconut_chop"
    # 6. RED FLAG / WAVE RAG: Pole stays 100% rigid while flag cloth ripples in wind
    if any(k in s for k in ("red-flag", "flag", "rag")):
        return "flag_on_rigid_pole"
    # 7. PINOCCHIO NOSE GROWING ("Yuh too lie!")
    if "yuh-too-lie" in s:
        return "pinocchio_nose_grow"
    # 8. ZIPPER LIPS ("Doh start")
    if "doh-start" in s:
        return "zipper_lips_slide"
    # 9. EAGLE WING-FLAP & SWOOP / SOU-SOU CASH
    if any(k in s for k in ("eagle", "sou-sou")):
        return "eagle_wing_flap"
    # 10. TWO-PART CLINK / FIST BUMP / HANDSHAKE / CLAPPING HANDS
    if any(k in s for k in ("liming", "soft-launch", "wha-go-on", "bet", "link-up", "ah-done", "too-much")):
        return "two_part_clink"
    # 11. HOURGLASS FLOWING SAND ("Just now")
    if "just-now" in s:
        return "hourglass_sand"
    # 12. UMBRELLA / SHIELD DEFLECTING RAIN OR MALJO SPARKS
    if any(k in s for k in ("doh-study-dat", "no-maljo", "mind-yuh-business")):
        return "shield_deflect"
    # 13. HEAT-SEEKING SLIPPER TRAJECTORY
    if "flying-slipper" in s:
        return "slipper_missile"
    # 14. FROZEN CHICKEN DRIPPING TAP & RINGING ALARM CLOCK
    if "trini-mom-spoon" in s:
        return "frozen_chicken_clock"
    # 15. WASA DRY SHOWERHEAD COUGHING DUST & SOAP SUDS
    if "wasa-water-gone" in s:
        return "wasa_dry_shower"
    # 16. T&TEC BLACKOUT ("Blacks!"): Fan stops, lights dim, candle flickers
    if "ttec-current-gone" in s:
        return "ttec_blackout_candle"
    # 17. CRAPAUD PUFFING PIPE & RISING CYAN SMOKE RINGS
    if "crapaud-pipe" in s:
        return "crapaud_smoke_pipe"
    # 18. SPINNING TIRE SWERVING OVER BANANA-TREE POTHOLE / MAXI TAXI
    if any(k in s for k in ("highway-traffic", "maxi-taxi", "stay-in-yuh-lane")):
        return "wheel_pothole_swerve"
    # 19. OVERHEAD HAND / MALLET SLAMMING DOMINO / CARD / ROCK / MIC
    if any(k in s for k in ("bullseye-allfours", "hang-jack", "mash-up", "real-talk", "ah-reach", "right-dey")):
        return "overhead_hand_slam"
    # 20. BLUE DEVIL / PEPPER / THERMOMETER ERUPTING FIRE & STEAM
    if any(k in s for k in ("blue-devil", "soucouyant", "vex", "yuh-mad", "mad-ting", "wicked", "horn", "badmind")):
        return "fire_breath_and_steam"
    # 21. MOKO JUMBIE ALTERNATING STILT-WALKING LEGS & WAVING ARMS
    if "moko-jumbie" in s or "carnival-mas" in s:
        return "moko_stilt_walk"
    # 22. TASSA DRUM / STEELPAN ALTERNATING STICK BEATS
    if any(k in s for k in ("tassa-chutney", "steelpan-3d", "parang-season")):
        return "drumstick_double_beat"
    # 23. FOREIGN JET AIRPLANE TAKING OFF OVER PASSPORT / DOH TOTE BAG TOSS / SPRINTING
    if any(k in s for k in ("freshwater-yankee", "doh-tote", "leh-we-go", "ah-coming", "ah-gone", "lowkey")):
        return "jet_and_toss_flight"
    # 24. MEGAPHONE / BOOMBOX / SIREN / EAR CUPPING SONIC BLAST
    if any(k in s for k in ("weyyyy", "ah-screaming", "wha-yuh-say", "hear-nah", "vibes", "real-bad", "link-me", "yuh-outside", "highkey")):
        return "megaphone_cone_blast"
    # 25. BELLY LAUGH SQUIRTING TEARS / MELTING PUDDLE / PROPELLER CAP SPIN
    if any(k in s for k in ("killing-me-dead", "doh-kill-meh", "a-week", "im-weak", "im-dead", "just-picong", "chupidee", "doh-be-a-dotish", "is-a-jokes", "yuh-jokin", "dotishness")):
        return "laugh_tears_and_spin"
    # 26. SUNGLASSES DROP & WINK ("Rizz", "Doh watch me", "Pothound", "Good vibes")
    if any(k in s for k in ("rizz", "doh-watch-me", "potcake-dog", "good-vibes-only", "stress-free-liming", "take-a-set", "dont-hot-up-yuh-head", "the-vibe-different")):
        return "sunglasses_cool_nod"
    # 27. DELICIOUS TRINI FOOD STEAMING & GLAZE SHIMMER
    if any(k in s for k in ("trini-chow", "crix-and-cheese", "buss-up-shut", "sunday-lunch", "corn-soup", "doubles-3d", "slight-pepper", "bake-and-shark", "crab-and-dumpling", "deya-parsad", "ate", "rel-bess", "small-ting")):
        return "culinary_steam_pop"
    # 28. FINGER WAG / HAND GESTURE / CROWN / EMPTY POCKETS
    return "articulated_gesture"


def render_picture_specific_frame(im: Image.Image, rig: str, sid: str, f: int, n_frames: int = 24) -> Image.Image:
    W, H = im.size
    t = f / n_frames
    ang = 2.0 * math.pi * t
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # -------------------------------------------------------------------------
    # 1. MACO: Venetian window blind rolls up, guy leans forward & scans with binoculars
    # -------------------------------------------------------------------------
    if rig == "maco_window_binoculars":
        if t < 0.25:
            open_p = 0.5 - 0.5 * math.cos(math.pi * (t / 0.25))
            bino_zoom = 0.0
            scan = 0.0
        elif t < 0.78:
            open_p = 1.0
            sub_t = (t - 0.25) / 0.53
            bino_zoom = math.sin(sub_t * math.pi)
            scan = math.sin(sub_t * 2 * math.pi)
        else:
            close_t = (t - 0.78) / 0.22
            open_p = 0.5 + 0.5 * math.cos(math.pi * close_t)
            bino_zoom = 0.0
            scan = 0.0

        bino_cx = 295.0 + scan * 18.0
        bino_cy = 202.0

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Curtains gently part outward inside the frame (keeping outer border crisp)
            wy_c = math.exp(-((y - 265.0) / 140.0) ** 4)
            wx_l = math.exp(-((x - 140.0) / 48.0) ** 2) * wy_c
            wx_r = math.exp(-((x - 372.0) / 48.0) ** 2) * wy_c
            dx += -(1.0 - open_p) * 24.0 * wx_l + (1.0 - open_p) * 24.0 * wx_r

            # Binoculars + eyes pop forward & scan left/right through the open window
            if bino_zoom > 0.01:
                dist2 = ((x - bino_cx) / 115.0) ** 2 + ((y - bino_cy) / 82.0) ** 2
                w_b = math.exp(-dist2 * 1.35)
                sf = 1.0 / (1.0 + 0.38 * bino_zoom * w_b)
                dx += (x - bino_cx) * (sf - 1.0) - scan * 25.0 * w_b
                dy += (y - bino_cy) * (sf - 1.0) + bino_zoom * 8.0 * w_b

            # Coffee steam rising
            w_st = math.exp(-((x - 260.0) / 25.0) ** 2 - ((y - 335.0) / 30.0) ** 2)
            dx += math.sin(ang * 2 + y * 0.12) * 6.0 * w_st
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=18)

        # Draw 3D Wooden Venetian Window Blinds rolling up/down inside the window frame
        blind_bottom_y = int(90 + (1.0 - open_p) * 320)
        if blind_bottom_y > 96:
            slat_h = 18
            for sy in range(90, blind_bottom_y, slat_h):
                y2 = min(sy + slat_h - 2, blind_bottom_y)
                od.rounded_rectangle([148, sy, 366, y2], radius=3, fill=(214, 158, 92, 248), outline=(120, 74, 30, 255), width=2)
                od.line([(152, sy + 3), (362, sy + 3)], fill=(248, 208, 148, 220), width=2)
            od.rounded_rectangle([144, blind_bottom_y - 6, 370, blind_bottom_y + 4], radius=4, fill=(168, 108, 48, 255), outline=(90, 50, 18, 255), width=2)
            od.line([(256, 90), (256, blind_bottom_y + 22)], fill=(245, 235, 210, 230), width=2)
            od.ellipse([251, blind_bottom_y + 20, 261, blind_bottom_y + 32], fill=(255, 184, 0, 255), outline=(90, 50, 18, 255), width=2)

        if bino_zoom > 0.2:
            gx = int(358 + scan * 24)
            gy = int(196 - bino_zoom * 4)
            r = int(14 + bino_zoom * 10)
            od.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(0, 229, 255, int(115 * bino_zoom)))
            od.ellipse([gx - r // 2, gy - r // 2, gx + r // 2, gy + r // 2], fill=(255, 255, 255, int(230 * bino_zoom)))

        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 2. OPTICAL SPY / TELESCOPE EXTEND / MAGNIFYING LENS SWEEP
    # -------------------------------------------------------------------------
    if rig == "optical_spy_zoom":
        ext = 0.5 - 0.5 * math.cos(ang)  # 0 -> 1 -> 0
        scan = math.sin(ang)

        def disp(x, y):
            # Focal lens / spyglass tip region zooms & pans across the image
            cx = 256.0 + scan * 42.0
            cy = 230.0 - ext * 18.0
            w_lens = math.exp(-(((x - cx) / 110.0) ** 2 + ((y - cy) / 110.0) ** 2))
            sf = 1.0 / (1.0 + 0.42 * ext * w_lens)
            dx = (x - cx) * (sf - 1.0) - scan * 18.0 * w_lens
            dy = (y - cy) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if ext > 0.25:
            lx = int(256 + scan * 42)
            ly = int(230 - ext * 18)
            od.ellipse([lx - 26, ly - 26, lx + 26, ly + 26], outline=(0, 229, 255, int(190 * ext)), width=3)
            od.ellipse([lx + 6, ly - 18, lx + 18, ly - 6], fill=(255, 255, 255, int(220 * ext)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 3. STEUPS: Side-eye roll + lips pucker + 3D air-puff shooting out of mouth
    # -------------------------------------------------------------------------
    if rig == "steups_puff":
        suck_p = max(0.0, math.sin(ang))
        puff_p = max(0.0, math.sin(ang - 0.6))

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Eyes (y: 170..255) cut sideways to the right & roll upward
            w_eyes = math.exp(-((x - 250.0) / 110.0) ** 2 - ((y - 215.0) / 42.0) ** 2)
            dx += -suck_p * 18.0 * w_eyes
            dy += suck_p * 8.0 * w_eyes
            # Lips (cx=260, cy=295) pinch inward then twitch
            w_lips = math.exp(-((x - 260.0) / 48.0) ** 2 - ((y - 295.0) / 38.0) ** 2)
            dx += (x - 260.0) * 0.28 * suck_p * w_lips
            # Air puff on the right (cx=340, cy=288) expands & shoots outward!
            w_puff = math.exp(-((x - 340.0) / 65.0) ** 2 - ((y - 288.0) / 55.0) ** 2)
            sf = 1.0 / (1.0 + 0.45 * puff_p * w_puff)
            dx += (x - 310.0) * (sf - 1.0) - puff_p * 28.0 * w_puff
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if puff_p > 0.15:
            px = int(355 + puff_p * 42)
            py = int(288 - puff_p * 8)
            r = int(12 + puff_p * 16)
            al = int(210 * (1.0 - puff_p * 0.6))
            od.arc([px - r, py - r, px + r, py + r], start=-55, end=55, fill=(0, 229, 255, al), width=4)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 4. AH EH ABLE: Hand fan pivots back & forth around wrist + sweat drop drips
    # -------------------------------------------------------------------------
    if rig == "fan_and_sweat":
        fan_angle = 0.34 * math.sin(ang * 2.0)  # 2 fast fan sweeps per loop
        drip = (t * 2.0) % 1.0

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Hand fan region (x: 160..400, y: 230..410) rotates around wrist pivot (305, 365)
            w_fan = math.exp(-((x - 285.0) / 115.0) ** 2 - ((y - 315.0) / 85.0) ** 2)
            if w_fan > 0.01:
                theta = fan_angle * w_fan
                rx = x - 305.0
                ry = y - 365.0
                dx += rx * (math.cos(theta) - 1.0) - ry * math.sin(theta)
                dy += rx * math.sin(theta) + ry * (math.cos(theta) - 1.0)
            # Sweat drop on top-right temple (cx=345, cy=165) slides down
            w_drop = math.exp(-((x - 345.0) / 42.0) ** 2 - ((y - 165.0) / 52.0) ** 2)
            dy += -(drip * 28.0) * w_drop
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        return frame

    # -------------------------------------------------------------------------
    # 5. SAVANNAH COCONUT: Machete chops down & coconut cap pops off with water splash
    # -------------------------------------------------------------------------
    if rig == "coconut_chop":
        # t=0..0.28: Machete raises up; t=0.28..0.45: Machete chops down; t=0.45..0.85: Cap flies up & water splashes!
        if t < 0.28:
            chop = -(t / 0.28)
            pop = 0.0
        elif t < 0.45:
            chop = -1.0 + 2.0 * ((t - 0.28) / 0.17)
            pop = max(0.0, (t - 0.34) / 0.11) * 0.5
        elif t < 0.82:
            chop = 1.0 - ((t - 0.45) / 0.37)
            pop = math.sin(((t - 0.34) / 0.52) * math.pi)
        else:
            chop = 0.0
            pop = 0.0

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Top coconut cap (x: 50..265, y: 30..215) pops upward & left when chopped
            w_cap = math.exp(-((x - 165.0) / 92.0) ** 2 - ((y - 125.0) / 75.0) ** 2)
            dx += pop * 22.0 * w_cap
            dy += pop * 36.0 * w_cap
            # Machete blade (diagonal from (120,300) to (460,80)) swings down
            w_blade = math.exp(-((x - 310.0) / 135.0) ** 2 - ((y - 185.0) / 95.0) ** 2) * (1.0 - w_cap * 0.8)
            dy += -chop * 26.0 * w_blade
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if pop > 0.2:
            for i in range(6):
                a = -math.pi * 0.85 + i * 0.32
                dist = 35 + pop * 75
                sx = int(256 + math.cos(a) * dist)
                sy = int(245 + math.sin(a) * dist)
                od.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(0, 229, 255, int(230 * (1.0 - pop * 0.5))))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 6. RED FLAG / WAVE RAG: Pole stays 100% rigid while cloth billows in wind
    # -------------------------------------------------------------------------
    if rig == "flag_on_rigid_pole":
        def disp(x, y):
            # Pole on left (x < 155) has zero displacement; cloth (x >= 155) ripples progressively
            cloth_w = max(0.0, min(1.0, (x - 145.0) / 240.0))
            wave = math.sin(ang * 2.0 - (x - 145.0) * 0.032)
            dy = -wave * 28.0 * cloth_w
            dx = math.cos(ang * 2.0 - (x - 145.0) * 0.032) * 8.0 * cloth_w
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=18)

    # -------------------------------------------------------------------------
    # 7. PINOCCHIO NOSE GROWING ("Yuh too lie!")
    # -------------------------------------------------------------------------
    if rig == "pinocchio_nose_grow":
        grow = 0.5 - 0.5 * math.cos(ang)  # 0 -> 1 -> 0

        def disp(x, y):
            # Nose region extending to the right/center-right (x > 235, y: 200..310) stretches outward!
            w_nose = math.exp(-((x - 335.0) / 95.0) ** 2 - ((y - 256.0) / 48.0) ** 2)
            dx = -grow * 54.0 * w_nose
            return (x + dx, y)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 8. ZIPPER LIPS SLIDING SHUT ("Doh start")
    # -------------------------------------------------------------------------
    if rig == "zipper_lips_slide":
        zip_p = 0.5 - 0.5 * math.cos(ang)  # zipper pull moves left -> right -> left
        zx = 165.0 + zip_p * 185.0

        def disp(x, y):
            # Lips pinch vertically behind the zipper pull (x < zx) and open slightly ahead of it
            w_lip = math.exp(-((y - 260.0) / 55.0) ** 2 - ((x - 256.0) / 130.0) ** 2)
            pinch = 0.22 if x < zx else -0.15
            dy = (y - 260.0) * pinch * w_lip
            # Zipper tab near zx moves horizontally
            w_tab = math.exp(-((x - 310.0) / 55.0) ** 2 - ((y - 265.0) / 55.0) ** 2)
            dx = -(zip_p - 0.5) * 48.0 * w_tab
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        # Metallic sparkle on the moving zipper pull
        od.ellipse([int(zx) - 10, 250, int(zx) + 10, 270], fill=(255, 184, 0, 220))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 9. EAGLE WING-FLAP & SWOOP ("The eagle has landed" / "Sou-sou")
    # -------------------------------------------------------------------------
    if rig == "eagle_wing_flap":
        flap = math.sin(ang * 2.0)  # 2 powerful wingbeats per loop
        swoop = math.sin(ang)

        def disp(x, y):
            # Left wing (x < 205, y < 290) and Right wing (x > 305, y < 290) flap up & down!
            wing_dist = abs(x - 256.0) / 220.0
            w_wing = max(0.0, (x - 256.0) ** 2 / (210.0 ** 2)) * math.exp(-((y - 175.0) / 110.0) ** 2)
            dy = -flap * 44.0 * min(1.2, w_wing) - swoop * 12.0
            # Center talons & cash bundle (x: 180..330, y > 260) zoom forward
            w_cash = math.exp(-((x - 256.0) / 85.0) ** 2 - ((y - 350.0) / 80.0) ** 2)
            sf = 1.0 / (1.0 + 0.22 * max(0.0, swoop) * w_cash)
            dx = (x - 256.0) * (sf - 1.0)
            dy += (y - 350.0) * (sf - 1.0)
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 10. TWO-PART CLINK / FIST BUMP / HANDSHAKE ("Liming", "Wha go on", "Bet", "Link up")
    # -------------------------------------------------------------------------
    if rig == "two_part_clink":
        # Pull apart (-1) then clink together (+1) in the center!
        clink = math.sin(ang * 2.0)

        def disp(x, y):
            # Left half (x < 256) and right half (x >= 256) move toward/away from center x=256
            side = -1.0 if x < 256.0 else 1.0
            w_mid = math.exp(-((y - 256.0) / 160.0) ** 2) * min(1.0, abs(x - 256.0) / 70.0)
            dx = side * clink * 24.0 * w_mid
            dy = abs(clink) * 8.0 * w_mid
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if clink > 0.65:
            # Clink starburst at center contact point
            p = (clink - 0.65) / 0.35
            for i in range(8):
                a = i * (math.pi / 4.0)
                r1, r2 = int(12 + p * 14), int(26 + p * 32)
                od.line(
                    [(256 + int(math.cos(a) * r1), 220 + int(math.sin(a) * r1)),
                     (256 + int(math.cos(a) * r2), 220 + int(math.sin(a) * r2))],
                    fill=(255, 184, 0, int(240 * (1.0 - p * 0.5))),
                    width=4,
                )
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 11. HOURGLASS FLOWING SAND ("Just now")
    # -------------------------------------------------------------------------
    if rig == "hourglass_sand":
        tilt = 0.12 * math.sin(ang)

        def disp(x, y):
            rx, ry = x - 256.0, y - 256.0
            dx = rx * (math.cos(tilt) - 1.0) - ry * math.sin(tilt)
            dy = rx * math.sin(tilt) + ry * (math.cos(tilt) - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=14)
        # Draw flowing turquoise sand stream through the center neck (x=256, y: 235..345)
        for i in range(7):
            sy = int(238 + ((t * 180 + i * 16) % 105))
            od.ellipse([252, sy - 4, 260, sy + 4], fill=(0, 229, 255, 235))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 12. UMBRELLA / SHIELD DEFLECTING RAIN OR MALJO SPARKS
    # -------------------------------------------------------------------------
    if rig == "shield_deflect":
        pulse = max(0.0, math.sin(ang * 2.0))

        def disp(x, y):
            # Umbrella canopy / shield dome bounces upward & outward to deflect
            w_dome = math.exp(-((x - 256.0) / 145.0) ** 2 - ((y - 220.0) / 115.0) ** 2)
            sf = 1.0 / (1.0 + 0.18 * pulse * w_dome)
            dx = (x - 256.0) * (sf - 1.0)
            dy = (y - 220.0) * (sf - 1.0) + pulse * 14.0 * w_dome
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if pulse > 0.2:
            r = int(145 + pulse * 45)
            od.arc([256 - r, 230 - r, 256 + r, 230 + r], start=200, end=340, fill=(0, 229, 255, int(210 * (1.0 - pulse * 0.5))), width=5)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 13. HEAT-SEEKING SLIPPER TRAJECTORY ("flying-slipper")
    # -------------------------------------------------------------------------
    if rig == "slipper_missile":
        flight = math.sin(ang)

        def disp(x, y):
            # Target rings (background) rotate one way while the 3D slipper zooms forward along its diagonal!
            w_slip = math.exp(-((x - 225.0) / 115.0) ** 2 - ((y - 190.0) / 115.0) ** 2)
            sf = 1.0 / (1.0 + 0.32 * max(0.0, flight) * w_slip)
            dx = (x - 225.0) * (sf - 1.0) - flight * 24.0 * w_slip
            dy = (y - 190.0) * (sf - 1.0) + flight * 22.0 * w_slip
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if flight > 0.1:
            # Target lock-on reticle pulse
            r = int(85 + (1.0 - flight) * 35)
            od.ellipse([235 - r, 180 - r, 235 + r, 180 + r], outline=(255, 42, 95, int(210 * flight)), width=4)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 14. FROZEN CHICKEN DRIPPING TAP & RINGING ALARM CLOCK ("trini-mom-spoon")
    # -------------------------------------------------------------------------
    if rig == "frozen_chicken_clock":
        drip_p = (t * 2.0) % 1.0
        ring = math.sin(ang * 6.0)  # Fast alarm bell vibration!

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Red alarm clock at bottom-right (cx=302, cy=262) shakes violently
            w_clock = math.exp(-((x - 302.0) / 68.0) ** 2 - ((y - 262.0) / 68.0) ** 2)
            dx += ring * 14.0 * w_clock
            dy += math.cos(ang * 6.0) * 8.0 * w_clock
            # Frozen chicken cube (cx=205, cy=225) shivers slightly
            w_ice = math.exp(-((x - 205.0) / 95.0) ** 2 - ((y - 225.0) / 85.0) ** 2) * (1.0 - w_clock)
            dx += math.sin(ang * 3.0) * 4.0 * w_ice
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        # Animated water drop falling from faucet spout (x=262, y: 112 -> 168)
        drop_y = int(112 + drip_p * 54)
        od.ellipse([256, drop_y - 7, 268, drop_y + 7], fill=(0, 229, 255, int(240 * (1.0 - drip_p * 0.4))))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 15. WASA DRY SHOWERHEAD COUGHING DUST & SOAP SUDS ("wasa-water-gone")
    # -------------------------------------------------------------------------
    if rig == "wasa_dry_shower":
        cough = max(0.0, math.sin(ang * 2.0))
        look = math.sin(ang)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Showerhead & dust puffs at top-right (cx=365, cy=95) sputter & expand downward
            w_sh = math.exp(-((x - 365.0) / 85.0) ** 2 - ((y - 95.0) / 65.0) ** 2)
            sf = 1.0 / (1.0 + 0.28 * cough * w_sh)
            dx += (x - 365.0) * (sf - 1.0)
            dy += (y - 95.0) * (sf - 1.0) - cough * 14.0 * w_sh
            # Soap suds & eyes (cx=255, cy=225) shift upward toward the dry showerhead
            w_face = math.exp(-((x - 255.0) / 95.0) ** 2 - ((y - 235.0) / 75.0) ** 2)
            dy += look * 10.0 * w_face
            dx += -look * 8.0 * w_face
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 16. T&TEC BLACKOUT ("ttec-current-gone"): Fan stops, candle flickers warmly
    # -------------------------------------------------------------------------
    if rig == "ttec_blackout_candle":
        flicker = 0.5 + 0.5 * math.sin(ang * 3.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Candle flame (cx=214, cy=295) dances & stretches upward
            w_flame = math.exp(-((x - 214.0) / 32.0) ** 2 - ((y - 295.0) / 38.0) ** 2)
            dx += math.sin(ang * 4.0) * 8.0 * w_flame
            dy += flicker * 12.0 * w_flame
            # Sweat drops on face (cx=125, cy=230) slide down
            w_sweat = math.exp(-((x - 125.0) / 65.0) ** 2 - ((y - 230.0) / 55.0) ** 2)
            dy += -((t * 2.0) % 1.0) * 14.0 * w_sweat
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        # Warm pulsing candlelight glow halo around the candle (214, 295)
        r = int(28 + flicker * 18)
        od.ellipse([214 - r, 295 - r, 214 + r, 295 + r], fill=(255, 184, 0, int(65 + flicker * 55)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 17. CRAPAUD PUFFING PIPE & RISING CYAN SMOKE RINGS ("crapaud-pipe")
    # -------------------------------------------------------------------------
    if rig == "crapaud_smoke_pipe":
        puff = 0.5 - 0.5 * math.cos(ang * 2.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Toad throat sac (cx=250, cy=280) inflates & deflates
            w_throat = math.exp(-((x - 250.0) / 68.0) ** 2 - ((y - 280.0) / 52.0) ** 2)
            sf = 1.0 / (1.0 + 0.24 * puff * w_throat)
            dx += (x - 250.0) * (sf - 1.0)
            dy += (y - 280.0) * (sf - 1.0)
            # Cyan smoke rings (top-right x > 265, y < 235) rise & expand!
            w_smoke = math.exp(-((x - 355.0) / 95.0) ** 2 - ((y - 135.0) / 85.0) ** 2)
            dy += math.sin(ang) * 22.0 * w_smoke
            dx += math.cos(ang * 2.0) * 12.0 * w_smoke
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        # Glowing ember inside the wooden pipe bowl (138, 255) when puffing
        if puff > 0.3:
            od.ellipse([126, 242, 152, 264], fill=(255, 110, 0, int(180 * puff)))
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 18. WHEEL SWERVING OVER BANANA-TREE POTHOLE ("highway-traffic", "maxi-taxi")
    # -------------------------------------------------------------------------
    if rig == "wheel_pothole_swerve":
        bounce = math.sin(ang * 2.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Upper/right wheel or vehicle (x > 220, y < 310) bounces & swerves while pothole stays grounded
            w_wheel = math.exp(-((x - 355.0) / 120.0) ** 2 - ((y - 170.0) / 115.0) ** 2)
            dy += bounce * 24.0 * w_wheel
            dx += math.cos(ang) * 18.0 * w_wheel
            # Banana leaves in pothole (cx=205, cy=265) wave gently
            w_leaf = math.exp(-((x - 205.0) / 65.0) ** 2 - ((y - 265.0) / 55.0) ** 2) * (1.0 - w_wheel)
            dx += math.sin(ang * 2.0) * 10.0 * w_leaf
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 19. OVERHEAD HAND / MALLET SLAMMING DOMINO / CARD / ROCK ("bullseye-allfours", "hang-jack", "mash-up")
    # -------------------------------------------------------------------------
    if rig == "overhead_hand_slam":
        # t=0..0.32: Hand raises high up; t=0.32..0.48: SLAMS down onto table; t=0.48..0.85: Shockwave scatters pieces!
        if t < 0.32:
            lift = t / 0.32
            slam = 0.0
        elif t < 0.50:
            p = (t - 0.32) / 0.18
            lift = 1.0 - 1.5 * p
            slam = p
        else:
            p = (t - 0.50) / 0.50
            lift = -0.5 * (1.0 - p)
            slam = max(0.0, 1.0 - p * 1.4)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Upper slamming hand/mallet/pin (y < 310) lifts up then slams down!
            w_hand = math.exp(-((x - 295.0) / 135.0) ** 2 - ((y - 185.0) / 115.0) ** 2)
            dy += lift * 38.0 * w_hand
            # Scattered dominoes/shards on left & right (y: 230..400) fly outward on slam!
            if slam > 0.05:
                side = -1.0 if x < 256.0 else 1.0
                w_scatter = math.exp(-((y - 315.0) / 75.0) ** 2) * min(1.0, abs(x - 256.0) / 85.0)
                dx += -side * slam * 26.0 * w_scatter
                dy += slam * 16.0 * w_scatter
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if slam > 0.25:
            r = int(45 + (1.0 - slam) * 145)
            od.ellipse([256 - r, 345 - r // 2, 256 + r, 345 + r // 2], outline=(255, 184, 0, int(220 * slam)), width=5)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 20. BLUE DEVIL / PEPPER / THERMOMETER ERUPTING FIRE & STEAM
    # -------------------------------------------------------------------------
    if rig == "fire_breath_and_steam":
        blast = 0.5 - 0.5 * math.cos(ang * 2.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            if "blue-devil" in sid:
                # Left wing flaps while fire plume on right (x > 250, y: 120..300) shoots out!
                w_wing = math.exp(-((x - 125.0) / 75.0) ** 2 - ((y - 210.0) / 65.0) ** 2)
                dy += math.sin(ang * 2.0) * 26.0 * w_wing
                w_fire = math.exp(-((x - 360.0) / 95.0) ** 2 - ((y - 205.0) / 75.0) ** 2)
                sf = 1.0 / (1.0 + 0.42 * blast * w_fire)
                dx += (x - 260.0) * (sf - 1.0)
                dy += (y - 205.0) * (sf - 1.0)
            else:
                # Steam puffs / flames on outer left & right or top erupt outward while center trembles!
                side = -1.0 if x < 256.0 else 1.0
                w_outer = min(1.0, abs(x - 256.0) / 95.0) * math.exp(-((y - 260.0) / 120.0) ** 2)
                dx += -side * blast * 28.0 * w_outer
                dy += blast * 18.0 * math.exp(-((y - 135.0) / 85.0) ** 2)
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 21. MOKO JUMBIE ALTERNATING STILT-WALKING LEGS & WAVING ARMS
    # -------------------------------------------------------------------------
    if rig == "moko_stilt_walk":
        step = math.sin(ang * 2.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Left stilt (x < 256, y > 260) and Right stilt (x >= 256, y > 260) step up and down alternately!
            if y > 240.0:
                w_leg = min(1.0, (y - 240.0) / 140.0)
                side = -1.0 if x < 256.0 else 1.0
                dy += side * step * 28.0 * w_leg
                dx += step * 8.0 * w_leg
            else:
                # Upper arms & feathers wave in celebratory rhythm
                w_arm = min(1.0, abs(x - 256.0) / 90.0)
                dy += -step * 18.0 * w_arm
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 22. TASSA DRUM / STEELPAN ALTERNATING STICK BEATS
    # -------------------------------------------------------------------------
    if rig == "drumstick_double_beat":
        beat = math.sin(ang * 4.0)  # 4 fast alternating stick strikes per loop!

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Left stick (x < 256, y < 290) and right stick (x >= 256, y < 290) strike alternately
            if y < 300.0:
                w_stick = math.exp(-((y - 175.0) / 95.0) ** 2) * min(1.0, abs(x - 256.0) / 65.0)
                side = -1.0 if x < 256.0 else 1.0
                dy += side * beat * 28.0 * w_stick
            # Drumhead / pan belly (cx=256, cy=275) bounces on every strike
            w_head = math.exp(-((x - 256.0) / 95.0) ** 2 - ((y - 275.0) / 65.0) ** 2)
            dy += -abs(beat) * 12.0 * w_head
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 23. FOREIGN JET TAKING OFF OVER PASSPORT / DOH TOTE BAG TOSS / SPRINTING
    # -------------------------------------------------------------------------
    if rig == "jet_and_toss_flight":
        fly = math.sin(ang)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            # Upper flying jet / tossed object / winged shoe (y < 275) flies across while base stays grounded
            w_top = math.exp(-((y - 165.0) / 105.0) ** 2)
            dx += -fly * 34.0 * w_top
            dy += fly * 22.0 * w_top
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 24. MEGAPHONE / BOOMBOX / EAR CUPPING SONIC BLAST
    # -------------------------------------------------------------------------
    if rig == "megaphone_cone_blast":
        thump = max(0.0, math.sin(ang * 2.0))

        def disp(x, y):
            # Horn / speaker cone expands rapidly on each bass beat while outer waves shoot outward
            w_horn = math.exp(-((x - 275.0) / 115.0) ** 2 - ((y - 235.0) / 115.0) ** 2)
            sf = 1.0 / (1.0 + 0.30 * thump * w_horn)
            dx = (x - 275.0) * (sf - 1.0)
            dy = (y - 235.0) * (sf - 1.0)
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if thump > 0.2:
            r = int(95 + (1.0 - thump) * 120)
            od.arc([275 - r, 235 - r, 275 + r, 235 + r], start=-45, end=45, fill=(0, 229, 255, int(220 * thump)), width=5)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 25. BELLY LAUGH SQUIRTING TEARS / MELTING PUDDLE / PROPELLER CAP SPIN
    # -------------------------------------------------------------------------
    if rig == "laugh_tears_and_spin":
        laugh = math.sin(ang * 3.0)

        def disp(x, y):
            dx, dy = 0.0, 0.0
            if "week" in sid or "weak" in sid:
                # Upper head sinks down while bottom puddle spreads wide!
                w_bot = math.exp(-((y - 375.0) / 85.0) ** 2)
                melt = 0.5 - 0.5 * math.cos(ang)
                dx += -(x - 256.0) * 0.24 * melt * w_bot
                dy += -melt * 24.0 * math.exp(-((y - 220.0) / 110.0) ** 2)
            else:
                # Head rocks in rapid belly laugh while left/right tear splashes squirt outward!
                w_tears = min(1.0, abs(x - 256.0) / 110.0) * math.exp(-((y - 235.0) / 85.0) ** 2)
                side = -1.0 if x < 256.0 else 1.0
                dx += -side * max(0.0, laugh) * 26.0 * w_tears
                dy += laugh * 16.0 * math.exp(-((x - 256.0) / 120.0) ** 2)
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 26. SUNGLASSES DROP & WINK ("Rizz", "Doh watch me", "Pothound", "Good vibes")
    # -------------------------------------------------------------------------
    if rig == "sunglasses_cool_nod":
        drop = 0.5 - 0.5 * math.cos(ang)

        def disp(x, y):
            # Sunglasses band (y: 165..245) dips down on the bridge of the nose then snaps up!
            w_shades = math.exp(-((x - 256.0) / 115.0) ** 2 - ((y - 205.0) / 42.0) ** 2)
            dy = -drop * 22.0 * w_shades
            dx = math.sin(ang) * 8.0 * w_shades
            return (x + dx, y + dy)

        frame = warp_mesh(im, disp, grid_n=16)
        if drop > 0.6:
            # Specular lens gleam sweeping across the sunglasses
            gx = int(200 + drop * 110)
            od.line([(gx - 12, 185), (gx + 12, 215)], fill=(255, 255, 255, 220), width=5)
        return Image.alpha_composite(frame, overlay)

    # -------------------------------------------------------------------------
    # 27. DELICIOUS TRINI FOOD STEAMING & GLAZE SHIMMER
    # -------------------------------------------------------------------------
    if rig == "culinary_steam_pop":
        pop = 0.5 - 0.5 * math.cos(ang)

        def disp(x, y):
            # Top steam & garnish (y < 210) waves & rises while center dish pulses forward appetizingly
            w_steam = math.exp(-((y - 120.0) / 75.0) ** 2)
            dx = math.sin(ang * 2.0 + y * 0.08) * 12.0 * w_steam
            w_food = math.exp(-((x - 256.0) / 125.0) ** 2 - ((y - 275.0) / 95.0) ** 2)
            sf = 1.0 / (1.0 + 0.16 * pop * w_food)
            dx += (x - 256.0) * (sf - 1.0)
            dy = (y - 275.0) * (sf - 1.0) + pop * 10.0 * w_food
            return (x + dx, y + dy)

        return warp_mesh(im, disp, grid_n=16)

    # -------------------------------------------------------------------------
    # 28. ARTICULATED FINGER WAG / HAND GESTURE / CROWN / POCKETS
    # -------------------------------------------------------------------------
    wag = math.sin(ang * 2.0)

    def disp(x, y):
        # Upper hand/finger/crown tip (y < 270) pivots back and forth while wrist/base stays anchored
        w_tip = math.exp(-((y - 175.0) / 105.0) ** 2)
        dx = wag * 24.0 * w_tip
        dy = -abs(wag) * 12.0 * w_tip
        return (x + dx, y + dy)

    return warp_mesh(im, disp, grid_n=16)


def save_animated_webp_and_gif(base_img: Image.Image, sid: str, rig: str, webp_path: str, gif_path: str):
    n_frames = 24
    duration_ms = 90  # 24 * 90ms = 2.16s (>2.0s so WhatsApp plays it as a looping animation!)
    rgba_frames = [render_picture_specific_frame(base_img, rig, sid, i, n_frames) for i in range(n_frames)]

    # 1. Save Transparent 512x512 Animated WebP
    rgba_frames[0].save(
        webp_path,
        format="WEBP",
        save_all=True,
        append_images=rgba_frames[1:],
        duration=duration_ms,
        loop=0,
        lossless=False,
        quality=80,
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
    print(f"Building picture-specific articulated animations for {len(files)} stickers...")
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
