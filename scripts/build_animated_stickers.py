import os
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageEnhance

STICKER_DIR = os.path.join("assets", "stickers")
OUT_DIR = os.path.join("assets", "animated")


def classify_action(sid: str) -> str:
    s = sid.lower()
    # 1. Flag / Cloth waving in wind
    if any(k in s for k in ("flag", "rag", "curtain")):
        return "flag_wind"
    # 2. Boiling rage / Pepper / Fire / Hot up / Mystical Folklore
    if any(k in s for k in (
        "vex", "pepper", "fire", "hot-up", "mad", "blue-devil", "jab",
        "soucouyant", "horn", "bacchanal", "obzocky", "wrong-and-strong",
        "diablesse", "lagahoo", "midnight-robber"
    )):
        return "boiling_rage"
    # 3. Ice / Cool down / Chill water / Take a set
    if any(k in s for k in (
        "cool", "easy", "chill", "nylon-pool", "coconut", "ddi", "caura", "bago",
        "liming", "river-lime", "take-a-set", "no-scene", "small-ting", "mama-dlo",
        "papa-bois", "silk-cotton"
    )):
        return "ice_chill"
    # 4. Eagle swoop / Money rain / Payday
    if any(k in s for k in (
        "eagle", "sou-sou", "bread", "rich", "paid", "gold", "million", "worth"
    )):
        return "money_swoop"
    # 5. Maco / Peeping / Zoom-in side-eye / Questioning
    if any(k in s for k in (
        "maco", "watch-nah", "see-trouble", "look-trouble", "hear-nah", "fuh-real",
        "owah", "jokin", "serious", "sus", "side-eye", "wha-go-on", "wha-appen",
        "freshwater", "yuh-too-fas", "mauvais-langue", "fass", "high-beam",
        "lemme-see", "how-yuh-mean", "be-so-for-real", "wha-yuh-on", "wha-yuh-say",
        "lowkey", "douen"
    )):
        return "maco_zoom"
    # 6. Heavy Slam / Impact Shockwave (Hang Jack, Facts, Slipper, Six, Bullseye, Ent)
    if any(k in s for k in (
        "hang-jack", "bullseye", "cricket-six", "slipper", "spoon", "facts",
        "bingo", "period", "done-talk", "say-less", "bet", "correct", "sorted",
        "lock-in", "clutch", "heavy", "ent", "for-true", "real-talk", "highkey",
        "all-ah-dat", "real-bad", "wicked"
    )):
        return "impact_slam"
    # 7. Bazodee / Dizzy Spiral / Drunk / Foolish
    if any(k in s for k in (
        "bazodee", "chupidee", "dotish", "clown", "rum", "ponche", "one-for-de-road",
        "drunk", "confuse", "lost", "delulu"
    )):
        return "bazodee_spin"
    # 8. Belly Laugh / Wheezing / Tears of Joy
    if any(k in s for k in (
        "killing-me-dead", "ah-eh-able", "kicksin", "picong", "dead", "kicks",
        "jokes", "laugh", "funny", "comedy", "wheeze", "too-much", "doh-make-joke",
        "ah-screaming", "doh-kill-meh", "im-weak", "a-week"
    )):
        return "belly_laugh"
    # 9. Delicious Hot Food / Rising Aroma & Sparkles
    if any(k in s for k in (
        "doubles", "bake", "buss-up", "sunday-lunch", "pelau", "corn-soup",
        "pholourie", "crix", "crab", "black-cake", "parsad", "sweet-bag",
        "sawine", "cutters", "bush-tea", "ate", "crumbs", "bess", "sweet", "belly", "sauce"
    )):
        return "food_aroma"
    # 10. Soca / Bass Thump / Soundwaves / Carnival Mas
    if any(k in s for k in (
        "steelpan", "tassa", "riddim", "parang", "chowtal", "weyyyy", "carnival-mas",
        "jouvert", "vibes", "loud", "outside", "party", "fete", "noise", "energy",
        "dame-lorraine", "moko-jumbie", "pierrot-grenade", "phagwa-holi",
        "emancipation-pride", "every-creed-and-race", "the-vibe-different"
    )):
        return "bass_thump"
    # 11. Tabanca / Heartbreak / Rain / Exhausted Slump
    if any(k in s for k in (
        "tabanca", "coma", "mash-up", "soft", "salt", "wasa", "current",
        "tired", "stress", "cry", "sad", "hurt", "broke", "pressure", "hard-lucks"
    )):
        return "tabanca_rain"
    # 12. Speed Dash / Peel Off / Ghost / On the way
    if any(k in s for k in (
        "maxi", "goat-race", "ghost", "speed", "move", "run", "pass", "dip", "fly",
        "fast", "highway-traffic", "ah-coming", "ah-gone", "ah-reach", "just-now",
        "leh-we-go", "right-dey"
    )):
        return "speed_dash"
    # 13. Stop / No Cap / Reject Head-Shake
    if any(k in s for k in (
        "cyah-take-dat", "maljo", "cap", "lie", "nah", "cut-it-out", "lane",
        "try-dat", "mouth", "steups", "stop", "fake", "beg", "extra", "bold", "brave",
        "doh-tote", "ah-done", "badmind", "boy-please", "doh-get-on-so", "doh-play",
        "doh-start", "doh-study-dat", "doh-watch-me", "dohh-bother", "its-not-giving",
        "left-on-read", "mind-yuh-business"
    )):
        return "reject_shake"
    # 14. Crown Shine / Confident Nod / Greetings, Charm & Respect
    return "crown_shine"


def draw_star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, color):
    if r <= 1:
        return
    pts = []
    for i in range(8):
        ang = i * math.pi / 4.0
        rad = r if i % 2 == 0 else r * 0.35
        pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
    draw.polygon(pts, fill=color)


def generate_action_frames(img: Image.Image, action: str, n_frames: int = 8):
    base_size = 420
    pad = (512 - base_size) // 2
    scaled = img.resize((base_size, base_size), Image.Resampling.LANCZOS)
    base_canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    base_canvas.paste(scaled, (pad, pad), scaled)

    frames = []
    for f in range(n_frames):
        t = (2.0 * math.pi * f) / n_frames
        frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        fx = ImageDraw.Draw(frame)

        if action == "flag_wind":
            # Left pole stays anchored; cloth ripples with 3D wave + wind streaks
            strip_w = 12
            for x in range(0, 512, strip_w):
                # Anchor left 30% (pole), ripple right 70% (flag cloth)
                norm_x = max(0.0, (x - 135) / 310.0)
                wave = math.sin(t * 2.0 - norm_x * 4.2)
                dy = int(round(wave * (26.0 * (norm_x ** 1.15))))
                strip = base_canvas.crop((x, 0, min(512, x + strip_w), 512))
                if norm_x > 0.05:
                    # Dynamic cloth shading on wave crests/troughs
                    shade = 1.0 + 0.18 * math.cos(t * 2.0 - norm_x * 4.2)
                    rgb = ImageEnhance.Brightness(strip.convert("RGB")).enhance(shade)
                    strip = Image.merge("RGBA", (*rgb.split(), strip.getchannel("A")))
                frame.paste(strip, (x, dy), strip)
            # Animated wind-streak lines
            for i in range(3):
                wx = int((f * 64 + i * 160) % 420) + 40
                wy = 120 + i * 115 + int(math.sin(t + i) * 14)
                fx.arc((wx, wy, wx + 85, wy + 28), start=190, end=350, fill=(255, 255, 255, 190), width=4)

        elif action == "boiling_rage":
            # Top half swells with fiery heat, high-frequency tremor, rising steam/flames
            pulse = 0.5 + 0.5 * math.sin(t * 2.0)
            jx = int(round(math.cos(t * 4.0) * 11.0)) if f % 2 == 0 else -int(round(math.cos(t * 4.0) * 11.0))
            jy = int(round(-pulse * 14.0))
            sw = int(round(base_size * (1.0 + 0.09 * pulse)))
            sh = int(round(base_size * (1.0 + 0.11 * pulse)))
            s_img = scaled.resize((sw, sh), Image.Resampling.BILINEAR)
            # Boost red/warmth on peak anger frames
            rgb = ImageEnhance.Color(s_img.convert("RGB")).enhance(1.0 + 0.35 * pulse)
            s_img = Image.merge("RGBA", (*rgb.split(), s_img.getchannel("A")))
            # Glowing crimson heat aura behind character
            aura_r = int(190 + 35 * pulse)
            fx.ellipse((256 - aura_r, 256 - aura_r, 256 + aura_r, 256 + aura_r), fill=(255, 42, 42, int(55 * pulse)))
            frame.paste(s_img, ((512 - sw) // 2 + jx, (512 - sh) // 2 + jy), s_img)
            # Rising steam puffs & flame sparks
            for i in range(4):
                prog = ((f / n_frames) + i * 0.25) % 1.0
                sx = 130 + i * 82 + int(math.sin(prog * 6.0 + i) * 18)
                sy = int(150 - prog * 125)
                rad = int((1.0 - prog) * 22 + 6)
                alpha = int((1.0 - prog) * 235)
                fx.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=(255, int(180 - prog * 120), 40, alpha))

        elif action == "ice_chill":
            # Smooth icy float + falling snow/frost crystals & cyan aura
            dy = int(round(math.sin(t) * 14.0))
            fx.ellipse((76, 76 + dy, 436, 436 + dy), fill=(0, 229, 255, 38))
            frame.paste(scaled, (pad, pad + dy), scaled)
            for i in range(5):
                prog = ((f / n_frames) + i * 0.2) % 1.0
                cx = 85 + i * 85 + int(math.cos(prog * 5.0 + i) * 15)
                cy = int(50 + prog * 400)
                draw_star(fx, cx, cy, 14 * (1.0 - abs(prog - 0.5)), (165, 243, 252, 230))

        elif action == "money_swoop":
            # Wing-spread horizontal swoop + raining gold coins
            wing_sx = 1.0 + 0.14 * math.sin(t)
            wing_sy = 1.0 - 0.06 * math.sin(t)
            dy = int(round(math.cos(t) * 22.0))
            sw = int(round(base_size * wing_sx))
            sh = int(round(base_size * wing_sy))
            s_img = scaled.resize((sw, sh), Image.Resampling.BILINEAR)
            frame.paste(s_img, ((512 - sw) // 2, (512 - sh) // 2 + dy), s_img)
            # Raining 3D gold coins
            for i in range(5):
                prog = ((f / n_frames) + i * 0.2) % 1.0
                cx = 75 + i * 90 + int(math.sin(t + i) * 12)
                cy = int(40 + prog * 430)
                cw = max(4, int(18 * abs(math.cos(t + i))))
                fx.ellipse((cx - cw, cy - 18, cx + cw, cy + 18), fill=(255, 200, 0, 240), outline=(255, 245, 150, 255), width=2)

        elif action == "maco_zoom":
            # Dramatic lean-in & zoom-in peek + scanning radar arcs
            # Creeps in close and holds wide-eyed, then ducks back
            zoom_curve = max(0.0, math.sin(t)) ** 0.6
            scale = 0.90 + 0.24 * zoom_curve
            dx = int(round((1.0 - zoom_curve) * -28.0))
            angle = (1.0 - zoom_curve) * -9.0
            sw = int(round(base_size * scale))
            s_img = scaled.resize((sw, sw), Image.Resampling.BILINEAR).rotate(angle, resample=Image.Resampling.BILINEAR)
            frame.paste(s_img, ((512 - sw) // 2 + dx, (512 - sw) // 2), s_img)
            if zoom_curve > 0.45:
                # Alert "!" / scan lines popping on peak zoom
                r_ring = int(180 + zoom_curve * 55)
                fx.arc((256 - r_ring, 256 - r_ring, 256 + r_ring, 256 + r_ring), start=310, end=45, fill=(0, 229, 255, 230), width=6)
                fx.arc((256 - r_ring, 256 - r_ring, 256 + r_ring, 256 + r_ring), start=135, end=225, fill=(255, 184, 0, 230), width=6)

        elif action == "impact_slam":
            # Winds up high (frames 0-2), SLAMS down on frame 3 with squash & shockwave, rebounds
            slam_profile = [
                (0.92, 0.92, -45, 8.0),   # wind up
                (0.88, 0.96, -70, 14.0),  # peak wind up
                (0.95, 1.12, -10, -4.0),  # fast drop
                (1.22, 0.78, 38, 0.0),    # SLAM IMPACT!
                (1.10, 0.88, 24, 2.0),    # shockwave hold
                (0.96, 1.05, -8, -2.0),   # rebound
                (1.02, 0.98, 4, 0.0),     # settle
                (1.00, 1.00, 0, 0.0),     # base
            ]
            sx, sy, dy, ang = slam_profile[f % len(slam_profile)]
            sw = int(round(base_size * sx))
            sh = int(round(base_size * sy))
            s_img = scaled.resize((sw, sh), Image.Resampling.BILINEAR).rotate(ang, resample=Image.Resampling.BILINEAR)
            # Draw ground shockwave on impact frames (3, 4, 5)
            if f in (3, 4, 5):
                prog = (f - 2) / 3.0
                rx = int(120 + prog * 120)
                ry = int(28 + prog * 26)
                alpha = int((1.0 - prog * 0.7) * 240)
                fx.ellipse((256 - rx, 430 - ry, 256 + rx, 430 + ry), outline=(255, 184, 0, alpha), width=6)
                draw_star(fx, 85, 380 - int(prog * 40), 22 * (1.1 - prog), (255, 42, 95, alpha))
                draw_star(fx, 425, 380 - int(prog * 40), 22 * (1.1 - prog), (0, 229, 255, alpha))
            frame.paste(s_img, ((512 - sw) // 2, (512 - sh) // 2 + dy), s_img)

        elif action == "bazodee_spin":
            # Horizontal shear/wobble + orbiting dizzy stars above head
            strip_h = 16
            for y in range(0, 512, strip_h):
                norm_y = (512 - y) / 512.0
                dx = int(round(math.sin(t + norm_y * 3.0) * (24.0 * norm_y)))
                strip = base_canvas.crop((0, y, 512, min(512, y + strip_h)))
                frame.paste(strip, (dx, y), strip)
            # Orbiting dizzy stars Halo at top
            for i in range(4):
                ang = t + i * (math.pi / 2.0)
                ox = 256 + int(math.cos(ang) * 145)
                oy = 92 + int(math.sin(ang) * 32)
                draw_star(fx, ox, oy, 18, (255, 208, 0, 245))

        elif action == "belly_laugh":
            # Rapid 2x-per-loop accordion belly laugh bounce + flying tear drops
            laugh_wave = math.sin(t * 2.0)
            sx = 1.0 + 0.11 * laugh_wave
            sy = 1.0 - 0.11 * laugh_wave
            dy = int(round(-abs(laugh_wave) * 22.0))
            ang = math.sin(t) * 9.0
            sw = int(round(base_size * sx))
            sh = int(round(base_size * sy))
            s_img = scaled.resize((sw, sh), Image.Resampling.BILINEAR).rotate(ang, resample=Image.Resampling.BILINEAR)
            frame.paste(s_img, ((512 - sw) // 2, (512 - sh) // 2 + dy), s_img)
            # Flying laugh teardrops splashing left and right
            prog = (f % 4) / 4.0
            tx_off = int(prog * 75)
            ty_off = int((prog ** 2) * 55 - prog * 25)
            alpha = int((1.0 - prog) * 240)
            fx.ellipse((85 - tx_off, 190 + ty_off, 112 - tx_off, 212 + ty_off), fill=(0, 229, 255, alpha))
            fx.ellipse((400 + tx_off, 190 + ty_off, 427 + tx_off, 212 + ty_off), fill=(0, 229, 255, alpha))

        elif action == "food_aroma":
            # Appetizing warm pulse + wavy rising hot steam ribbons + golden sparkles
            scale = 1.0 + 0.05 * math.sin(t)
            sw = int(round(base_size * scale))
            s_img = scaled.resize((sw, sw), Image.Resampling.BILINEAR)
            frame.paste(s_img, ((512 - sw) // 2, (512 - sw) // 2 + 12), s_img)
            # 3 wavy rising aroma steam lines
            for i in range(3):
                bx = 165 + i * 90
                pts = []
                for step in range(8):
                    py = 175 - step * 18 - int(((f / n_frames) * 28) % 28)
                    px = bx + int(math.sin(t + step * 0.8 + i) * 14)
                    pts.append((px, py))
                fx.line(pts, fill=(255, 248, 225, 185), width=6)
            # Twinkling golden stars
            draw_star(fx, 95, 140, 18 * abs(math.sin(t)), (255, 200, 0, 240))
            draw_star(fx, 418, 125, 18 * abs(math.cos(t)), (255, 200, 0, 240))

        elif action == "bass_thump":
            # 120-BPM double subwoofer thump + expanding neon soundwave rings
            beat = abs(math.sin(t * 2.0)) ** 2.2
            scale = 0.94 + 0.16 * beat
            sw = int(round(base_size * scale))
            s_img = scaled.resize((sw, sw), Image.Resampling.BILINEAR)
            # Soundwave rings expanding outward
            for ring_i in range(2):
                r_prog = ((f / n_frames) + ring_i * 0.5) % 1.0
                rad = int(150 + r_prog * 100)
                alpha = int((1.0 - r_prog) * 210)
                col = (255, 42, 95, alpha) if ring_i == 0 else (0, 229, 255, alpha)
                fx.ellipse((256 - rad, 256 - rad, 256 + rad, 256 + rad), outline=col, width=5)
            frame.paste(s_img, ((512 - sw) // 2, (512 - sw) // 2), s_img)

        elif action == "tabanca_rain":
            # Heavy drooping sigh slump (anchored at bottom, squashes down) + falling rain streaks
            droop = 0.5 + 0.5 * math.sin(t)
            sh = int(round(base_size * (1.0 - 0.10 * droop)))
            sw = int(round(base_size * (1.0 + 0.05 * droop)))
            s_img = scaled.resize((sw, sh), Image.Resampling.BILINEAR)
            frame.paste(s_img, ((512 - sw) // 2, 512 - pad - sh), s_img)
            # Falling rain streaks
            for i in range(6):
                rx = 75 + i * 72
                ry = int(((f * 58 + i * 85) % 420) + 30)
                fx.line([(rx, ry), (rx - 6, ry + 34)], fill=(56, 189, 248, 205), width=4)

        elif action == "speed_dash":
            # Forward aerodynamic tilt + speed dash across frame + neon speed streaks
            dash = math.sin(t)
            dx = int(round(dash * 36.0))
            s_img = scaled.rotate(-10.0 * abs(dash), resample=Image.Resampling.BILINEAR)
            # Neon speed lines behind
            for i in range(4):
                ly = 135 + i * 80
                lx = 35 + ((f * 55 + i * 70) % 140)
                fx.line([(lx, ly), (lx + 95, ly)], fill=(0, 229, 255, 220), width=6)
            frame.paste(s_img, (pad + dx, pad), s_img)

        elif action == "reject_shake":
            # Sharp horizontal "NO!" head-shake snap left-right-left + crimson warning pulse
            dx = int(round(math.sin(t * 2.0) * 28.0))
            ang = math.sin(t * 2.0) * 11.0
            s_img = scaled.rotate(ang, resample=Image.Resampling.BILINEAR)
            frame.paste(s_img, (pad + dx, pad), s_img)
            if f % 2 == 0:
                fx.arc((44, 44, 468, 468), start=0, end=360, fill=(255, 42, 95, 190), width=6)

        else:  # "crown_shine"
            # Confident slow head-nod dip + diagonal golden metallic sheen sweep + sparkles
            nod_y = int(round(math.sin(t) * 16.0))
            frame.paste(scaled, (pad, pad + nod_y), scaled)
            # Diagonal light-sweep across the sticker's alpha mask
            alpha_mask = frame.getchannel("A")
            sheen = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(sheen)
            sx = int(-150 + (f / n_frames) * 820)
            s_draw.polygon([(sx, 0), (sx + 95, 0), (sx - 125, 512), (sx - 220, 512)], fill=(255, 245, 190, 110))
            frame = Image.composite(Image.alpha_composite(frame, sheen), frame, alpha_mask)
            fx = ImageDraw.Draw(frame)
            draw_star(fx, 105, 110, 20 * abs(math.sin(t)), (255, 200, 0, 245))
            draw_star(fx, 410, 145, 18 * abs(math.cos(t)), (0, 229, 255, 245))

        frames.append(frame)

    return frames


def save_animated_webp(cycle_frames, out_path: str, duration: int = 105):
    cycle_frames[0].save(
        out_path,
        format="WEBP",
        save_all=True,
        append_images=cycle_frames[1:],
        duration=duration,
        loop=0,
        quality=52,
        method=0,
    )


def save_whatsapp_compatible_gif(cycle_frames, out_path: str, duration: int = 90):
    gif_size = 340
    bg = Image.new("RGB", (gif_size, gif_size), (16, 20, 30))
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle(
        (6, 6, gif_size - 7, gif_size - 7),
        radius=42,
        fill=(22, 27, 40),
        outline=(40, 48, 68),
        width=2,
    )

    single_cycle_quant = []
    pal_img = None

    for fr in cycle_frames:
        small = fr.resize((gif_size, gif_size), Image.Resampling.BILINEAR)
        comp = bg.copy()
        comp.paste(small, (0, 0), small)
        if pal_img is None:
            pal_img = comp.quantize(colors=128, method=Image.Quantize.FASTOCTREE)
        q = comp.quantize(palette=pal_img, dither=Image.Dither.NONE)
        single_cycle_quant.append(q)

    frames_24 = single_cycle_quant * 3
    frames_24[0].save(
        out_path,
        format="GIF",
        save_all=True,
        append_images=frames_24[1:],
        duration=duration,
        loop=0,
        optimize=False,
    )


def process_one(png_filename: str):
    sticker_id = png_filename[:-4]
    in_path = os.path.join(STICKER_DIR, png_filename)
    webp_out = os.path.join(OUT_DIR, f"{sticker_id}.webp")
    gif_out = os.path.join(OUT_DIR, f"{sticker_id}.gif")

    action = classify_action(sticker_id)
    with Image.open(in_path) as im:
        rgba = im.convert("RGBA")
        cycle_frames = generate_action_frames(rgba, action, n_frames=8)

    save_animated_webp(cycle_frames, webp_out, duration=95)
    save_whatsapp_compatible_gif(cycle_frames, gif_out, duration=90)

    w_kb = os.path.getsize(webp_out) / 1024.0
    g_kb = os.path.getsize(gif_out) / 1024.0
    return sticker_id, action, w_kb, g_kb


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    png_files = sorted(f for f in os.listdir(STICKER_DIR) if f.endswith(".png"))
    t0 = time.time()
    print(f"Generating 14 action-specific animations + FX for {len(png_files)} stickers...")

    counts = {}
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = [ex.submit(process_one, f) for f in png_files]
        done_count = 0
        for fut in as_completed(futures):
            sid, action, w_kb, g_kb = fut.result()
            done_count += 1
            counts[action] = counts.get(action, 0) + 1
            if done_count % 35 == 0 or done_count == len(png_files):
                print(f"  [{done_count}/{len(png_files)}] {sid} ({action}) -> WebP: {w_kb:.1f}KB, GIF: {g_kb:.1f}KB")

    dt = time.time() - t0
    print(f"Completed in {dt:.1f}s!")
    print("Action breakdown:", counts)


if __name__ == "__main__":
    main()
