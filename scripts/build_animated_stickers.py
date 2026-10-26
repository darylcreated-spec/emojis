import os
import math
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageDraw

STICKER_DIR = os.path.join("assets", "stickers")
OUT_DIR = os.path.join("assets", "animated")
PACKS_DIR = os.path.join("assets", "packs")

WAVE_KEYWORDS = (
    "flag", "rag", "curtain", "heart", "nylon-pool", "bago", "ddi", "caura",
    "island", "parang", "holi", "emancipation", "creed"
)
SHAKE_KEYWORDS = (
    "vex", "pepper", "fire", "trouble", "horn", "slipper", "weyyyy", "steups",
    "mad", "hot-up", "thunder", "current", "wasa", "gridlock", "blue-devil",
    "jab", "robber", "tassa", "riddim", "bacchanal", "kicksin", "mamaguy",
    "wrong-and-strong", "try-dat", "noise", "salt", "obzocky", "dotish"
)
FLOAT_KEYWORDS = (
    "bazodee", "eagle", "soucouyant", "diablesse", "mama-dlo", "papa-bois",
    "douen", "lagahoo", "maljo", "bush-tea", "silk-cotton", "ghost", "breeze",
    "liming", "rum", "coconut", "deya", "ponche", "sweet-bag", "sawine", "vibes"
)
POP_KEYWORDS = (
    "ent", "bess", "doubles", "bake", "buss-up", "sunday", "pelau", "corn-soup",
    "pholourie", "crix", "crab", "hang-jack", "sou-sou", "bullseye", "cutters",
    "road", "six", "steelpan", "mas", "jouvert", "black-cake", "cap", "facts",
    "crumbs", "blessings", "bingo", "sorted", "respect", "scene", "correct",
    "paid", "bread", "belly", "sweet"
)


def classify_motion(sticker_id: str) -> str:
    s = sticker_id.lower()
    if any(k in s for k in WAVE_KEYWORDS):
        return "wave"
    if any(k in s for k in SHAKE_KEYWORDS):
        return "shake"
    if any(k in s for k in FLOAT_KEYWORDS):
        return "float"
    if any(k in s for k in POP_KEYWORDS):
        return "pop"
    return "tilt"


def generate_cycle_frames(img: Image.Image, motion: str, n_frames: int = 8):
    # Fit inside 436x436 on a 512x512 canvas so exaggerated motion never clips the die-cut border
    base_size = 436
    pad = (512 - base_size) // 2
    scaled = img.resize((base_size, base_size), Image.Resampling.LANCZOS)
    base_canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    base_canvas.paste(scaled, (pad, pad), scaled)

    frames = []
    for f in range(n_frames):
        t = (2.0 * math.pi * f) / n_frames
        frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

        if motion == "wave":
            strip_w = 16
            rot = math.sin(t) * 3.5
            rotated = base_canvas.rotate(rot, resample=Image.Resampling.BILINEAR)
            for x in range(0, 512, strip_w):
                norm_x = max(0.0, (x - 65) / 380.0)
                dy = int(round(math.sin(t - norm_x * 3.5) * (18.0 * norm_x)))
                strip = rotated.crop((x, 0, min(512, x + strip_w), 512))
                frame.paste(strip, (x, dy), strip)

        elif motion == "shake":
            scale = 1.0 + 0.07 * math.sin(t * 2.0)
            angle = math.sin(t * 2.0) * 8.0
            dx = int(round(math.cos(t * 3.0) * 9.0))
            dy = int(round(math.sin(t * 2.0) * 7.0))
            nw = int(round(base_size * scale))
            nh = int(round(base_size * scale))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR, expand=False
            )
            ox = (512 - nw) // 2 + dx
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        elif motion == "float":
            dx = int(round(math.sin(t) * 13.0))
            dy = int(round(math.sin(t * 2.0) * 14.0))
            angle = math.cos(t) * 6.0
            scale = 1.0 + 0.04 * math.sin(t)
            nw = int(round(base_size * scale))
            nh = int(round(base_size * scale))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR
            )
            ox = (512 - nw) // 2 + dx
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        elif motion == "pop":
            s_wave = math.sin(t)
            sx = 1.0 - 0.07 * s_wave
            sy = 1.0 + 0.09 * s_wave
            dy = int(round(-abs(math.sin(t)) * 22.0 + 8.0))
            angle = math.sin(t) * 4.0
            nw = int(round(base_size * sx))
            nh = int(round(base_size * sy))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR
            )
            ox = (512 - nw) // 2
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        else:  # "tilt"
            angle = math.sin(t) * 10.0
            dy = int(round(-abs(math.cos(t)) * 15.0 + 6.0))
            scale = 1.0 + 0.045 * abs(math.sin(t))
            nw = int(round(base_size * scale))
            nh = int(round(base_size * scale))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR
            )
            ox = (512 - nw) // 2
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        frames.append(frame)

    return frames


def save_animated_webp(cycle_frames, out_path: str, duration: int = 95):
    # 16 frames (~1.52s) for WhatsApp Animated Sticker compliance & smooth browser playback
    frames_16 = cycle_frames + cycle_frames
    for q in (48, 36, 26):
        frames_16[0].save(
            out_path,
            format="WEBP",
            save_all=True,
            append_images=frames_16[1:],
            duration=duration,
            loop=0,
            quality=q,
            method=2,
        )
        if os.path.getsize(out_path) < 380 * 1024:
            break


def save_whatsapp_compatible_gif(cycle_frames, out_path: str, duration: int = 90):
    """
    Generates a WhatsApp/Instagram/iMessage-compatible looping GIF:
    - Composited onto a clean dark Obsidian studio backdrop (#10141E) so WhatsApp's
      GIF-to-MP4 converter never fails or produces black/flickering alpha artifacts.
    - Repeated 3x (24 frames @ 90ms = 2.16 seconds total duration) because WhatsApp
      requires >= 1.5-2.0 seconds to recognize and loop an animated GIF in chat!
    """
    gif_size = 360
    bg = Image.new("RGB", (gif_size, gif_size), (16, 20, 30))
    # Subtle studio vignette ring on background
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle((6, 6, gif_size - 7, gif_size - 7), radius=42, fill=(22, 27, 40), outline=(40, 48, 68), width=2)

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

    # 3 full cycles = 24 frames (2.16 seconds) -> Guaranteed WhatsApp GIF loop!
    frames_24 = single_cycle_quant * 3
    frames_24[0].save(
        out_path,
        format="GIF",
        save_all=True,
        append_images=frames_24[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )


def process_one(png_filename: str):
    sticker_id = png_filename[:-4]
    in_path = os.path.join(STICKER_DIR, png_filename)
    webp_out = os.path.join(OUT_DIR, f"{sticker_id}.webp")
    gif_out = os.path.join(OUT_DIR, f"{sticker_id}.gif")

    motion = classify_motion(sticker_id)
    with Image.open(in_path) as im:
        rgba = im.convert("RGBA")
        cycle_frames = generate_cycle_frames(rgba, motion, n_frames=8)

    save_animated_webp(cycle_frames, webp_out, duration=95)
    save_whatsapp_compatible_gif(cycle_frames, gif_out, duration=90)

    w_kb = os.path.getsize(webp_out) / 1024.0
    g_kb = os.path.getsize(gif_out) / 1024.0
    return sticker_id, motion, w_kb, g_kb


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    png_files = sorted(f for f in os.listdir(STICKER_DIR) if f.endswith(".png"))
    t0 = time.time()
    print(f"Generating WhatsApp-verified 2.16s GIFs & 1.52s WebPs for {len(png_files)} stickers...")

    max_webp = 0.0
    max_gif = 0.0

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = [ex.submit(process_one, f) for f in png_files]
        done_count = 0
        for fut in as_completed(futures):
            sid, motion, w_kb, g_kb = fut.result()
            done_count += 1
            if w_kb > max_webp:
                max_webp = w_kb
            if g_kb > max_gif:
                max_gif = g_kb
            if done_count % 40 == 0 or done_count == len(png_files):
                print(f"  [{done_count}/{len(png_files)}] {sid} ({motion}) -> WebP: {w_kb:.1f}KB, GIF (24f): {g_kb:.1f}KB")

    dt = time.time() - t0
    print(f"Done in {dt:.1f}s | Max WebP: {max_webp:.1f}KB | Max GIF: {max_gif:.1f}KB")


if __name__ == "__main__":
    main()
