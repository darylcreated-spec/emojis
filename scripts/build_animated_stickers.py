import os
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image

STICKER_DIR = os.path.join("assets", "stickers")
OUT_DIR = os.path.join("assets", "animated")

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


def generate_frames(img: Image.Image, motion: str, n_frames: int = 10):
    # Fit inside 444x444 on a 512x512 canvas so motion never clips the die-cut border
    base_size = 444
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
            rot = math.sin(t) * 2.5
            rotated = base_canvas.rotate(rot, resample=Image.Resampling.BILINEAR)
            for x in range(0, 512, strip_w):
                norm_x = max(0.0, (x - 70) / 380.0)
                dy = int(round(math.sin(t - norm_x * 3.4) * (15.0 * norm_x)))
                strip = rotated.crop((x, 0, min(512, x + strip_w), 512))
                frame.paste(strip, (x, dy), strip)

        elif motion == "shake":
            # Rapid energetic shake + pulse
            scale = 1.0 + 0.055 * math.sin(t * 2.0)
            angle = math.sin(t * 2.0) * 6.5
            dx = int(round(math.cos(t * 3.0) * 7.0))
            dy = int(round(math.sin(t * 2.0) * 5.0))
            nw = int(round(base_size * scale))
            nh = int(round(base_size * scale))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR, expand=False
            )
            ox = (512 - nw) // 2 + dx
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        elif motion == "float":
            # Smooth figure-8 levitation + gentle 3D sway
            dx = int(round(math.sin(t) * 10.0))
            dy = int(round(math.sin(t * 2.0) * 11.0))
            angle = math.cos(t) * 4.5
            scale = 1.0 + 0.03 * math.sin(t)
            nw = int(round(base_size * scale))
            nh = int(round(base_size * scale))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR
            )
            ox = (512 - nw) // 2 + dx
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        elif motion == "pop":
            # Elastic squash-and-stretch bounce pop
            s_wave = math.sin(t)
            sx = 1.0 - 0.055 * s_wave
            sy = 1.0 + 0.075 * s_wave
            dy = int(round(-abs(math.sin(t)) * 18.0 + 6.0))
            angle = math.sin(t) * 3.0
            nw = int(round(base_size * sx))
            nh = int(round(base_size * sy))
            s_img = scaled.resize((nw, nh), Image.Resampling.BILINEAR).rotate(
                angle, resample=Image.Resampling.BILINEAR
            )
            ox = (512 - nw) // 2
            oy = (512 - nh) // 2 + dy
            frame.paste(s_img, (ox, oy), s_img)

        else:  # "tilt"
            # Playful pendulum rock + bounce
            angle = math.sin(t) * 8.0
            dy = int(round(-abs(math.cos(t)) * 12.0 + 5.0))
            scale = 1.0 + 0.035 * abs(math.sin(t))
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


def save_animated_webp(frames, out_path: str, duration: int = 105):
    for q in (52, 40, 30):
        frames[0].save(
            out_path,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            quality=q,
            method=2,
        )
        if os.path.getsize(out_path) < 260 * 1024:
            break


def save_transparent_gif(frames, out_path: str, duration: int = 105):
    gif_size = 360
    small_frames = [fr.resize((gif_size, gif_size), Image.Resampling.BILINEAR) for fr in frames]
    gif_frames = []
    rgb0 = small_frames[0].convert("RGB")
    pal_img = rgb0.quantize(colors=127, method=Image.Quantize.FASTOCTREE)
    raw_pal = pal_img.getpalette() or [0] * 768
    palette = raw_pal[: 127 * 3] + [0, 0, 0] * (256 - 127)

    for fr in small_frames:
        alpha = fr.getchannel("A")
        q = fr.convert("RGB").quantize(palette=pal_img, dither=Image.Dither.NONE)
        mask = alpha.point(lambda a: 255 if a < 128 else 0)
        q.paste(255, mask=mask)
        q.putpalette(palette)
        gif_frames.append(q)

    gif_frames[0].save(
        out_path,
        format="GIF",
        save_all=True,
        append_images=gif_frames[1:],
        duration=duration,
        loop=0,
        transparency=255,
        disposal=2,
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
        frames = generate_frames(rgba, motion, n_frames=8)

    save_animated_webp(frames, webp_out, duration=105)
    save_transparent_gif(frames, gif_out, duration=105)

    w_kb = os.path.getsize(webp_out) / 1024.0
    g_kb = os.path.getsize(gif_out) / 1024.0
    return sticker_id, motion, w_kb, g_kb


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    png_files = sorted(f for f in os.listdir(STICKER_DIR) if f.endswith(".png"))
    t0 = time.time()
    print(f"Generating animated .webp and .gif for {len(png_files)} stickers across {os.cpu_count()} cores...")

    max_webp = 0.0
    max_gif = 0.0
    counts = {}

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = [ex.submit(process_one, f) for f in png_files]
        done_count = 0
        for fut in as_completed(futures):
            sid, motion, w_kb, g_kb = fut.result()
            done_count += 1
            counts[motion] = counts.get(motion, 0) + 1
            if w_kb > max_webp:
                max_webp = w_kb
            if g_kb > max_gif:
                max_gif = g_kb
            if done_count % 30 == 0 or done_count == len(png_files):
                print(f"  [{done_count}/{len(png_files)}] Latest: {sid} ({motion}) -> WebP: {w_kb:.1f}KB, GIF: {g_kb:.1f}KB")

    dt = time.time() - t0
    print(f"Completed all {len(png_files)} stickers (372 animated files) in {dt:.1f}s!")
    print(f"Motion profile breakdown: {counts}")
    print(f"Max Animated WebP size: {max_webp:.1f} KB (WhatsApp limit < 500 KB)")
    print(f"Max Animated GIF size:  {max_gif:.1f} KB")


if __name__ == "__main__":
    main()
