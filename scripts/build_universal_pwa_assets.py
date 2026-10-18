"""
Builds Universal, Flag-Free, WhatsApp-Free PWA Icons & Obsidian Vinyl Peel Splash Assets
for StickerBoom.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(ROOT, "assets", "icons")
BRAIN_DIR = r"C:\Users\daryl\.gemini\antigravity\brain\71a5a202-c739-4fc9-8006-dab96ac694aa"

os.makedirs(ICONS_DIR, exist_ok=True)

MASTER_ICON_PATH = os.path.join(BRAIN_DIR, "stickerboom_icon_master_bleed_1792360727689.jpg")
UNIVERSAL_GRID_PATH = os.path.join(BRAIN_DIR, "stickerboom_universal_icons_1792360545827.jpg")
SPLASH_SHEET_PATH = os.path.join(BRAIN_DIR, "stickerboom_universal_splashes_1792360542110.jpg")


def build_master_pwa_icons():
    img = Image.open(MASTER_ICON_PATH).convert("RGBA")
    # Save standard PWA sizes
    sizes = {
        "icon-512.png": (512, 512),
        "icon-192.png": (192, 192),
        "apple-touch-icon.png": (180, 180),
        "favicon.png": (64, 64),
        "icon-1-vinyl-peel.png": (512, 512),
        # Also overwrite legacy default filename if cached anywhere
        "icon-1-scotch-bonnet.png": (512, 512),
    }
    for filename, dim in sizes.items():
        resized = img.resize(dim, Image.Resampling.LANCZOS)
        out_path = os.path.join(ICONS_DIR, filename)
        resized.save(out_path, format="PNG", optimize=True)
        print(f"Saved {filename} ({dim[0]}x{dim[1]})")


def extract_universal_icon_options():
    grid = Image.open(UNIVERSAL_GRID_PATH).convert("RGBA")
    w, h = grid.size
    # The 2x2 grid has 4 squircle icons; crop each squircle cleanly
    # Boxes normalized (left, top, right, bottom)
    boxes = {
        "icon-2-emoji-pop.png": (int(w * 0.573), int(h * 0.095), int(w * 0.902), int(h * 0.424)),
        "icon-3-comic-burst.png": (int(w * 0.098), int(h * 0.553), int(w * 0.427), int(h * 0.882)),
        "icon-4-sticker-stack.png": (int(w * 0.573), int(h * 0.553), int(w * 0.902), int(h * 0.882)),
    }
    for filename, box in boxes.items():
        crop = grid.crop(box).resize((512, 512), Image.Resampling.LANCZOS)
        out_path = os.path.join(ICONS_DIR, filename)
        crop.save(out_path, format="PNG", optimize=True)
        print(f"Saved option {filename} (512x512)")


def build_splash_assets():
    splash_sheet = Image.open(SPLASH_SHEET_PATH).convert("RGBA")
    sw, sh = splash_sheet.size
    # Splash A is the leftmost phone screen; its centerpiece circular "StickerBoom" peeling vinyl sticker
    # is centered horizontally in phone 1 around x=[0.078..0.238], y=[0.315..0.605]
    cx1 = int(sw * 0.076)
    cx2 = int(sw * 0.238)
    box_w = cx2 - cx1
    cy_center = int(sh * 0.465)
    cy1 = cy_center - box_w // 2
    cy2 = cy1 + box_w

    emblem_crop = splash_sheet.crop((cx1, cy1, cx2, cy2)).resize((560, 560), Image.Resampling.LANCZOS)

    # Create clean circular mask around the obsidian background so it blends seamlessly on #121316
    obsidian = (18, 19, 22, 255)
    emblem_canvas = Image.new("RGBA", (560, 560), obsidian)
    mask = Image.new("L", (560, 560), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((12, 12, 548, 548), fill=255)
    emblem_canvas.paste(emblem_crop, (0, 0), mask)

    emblem_out = os.path.join(ICONS_DIR, "splash-emblem.png")
    emblem_canvas.save(emblem_out, format="PNG", optimize=True)
    print("Saved splash-emblem.png (560x560)")

    # Also build a full iOS portrait startup splash screen (1170x2532) on #121316 obsidian
    splash_full = Image.new("RGB", (1170, 2532), (18, 19, 22))
    emblem_large = emblem_canvas.resize((680, 680), Image.Resampling.LANCZOS)
    splash_full.paste(emblem_large.convert("RGB"), ((1170 - 680) // 2, (2532 - 680) // 2 - 40))
    splash_full_path = os.path.join(ICONS_DIR, "apple-splash-portrait.png")
    splash_full.save(splash_full_path, format="PNG", optimize=True)
    print("Saved apple-splash-portrait.png (1170x2532)")


if __name__ == "__main__":
    build_master_pwa_icons()
    extract_universal_icon_options()
    build_splash_assets()
