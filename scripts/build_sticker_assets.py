import json
import os
import re
from collections import deque
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WORKSPACE_DIR = r"c:\Antigravity Projects\TRINI Emoj"
ARTIFACT_DIR = r"C:\Users\daryl\.gemini\antigravity\brain\71a5a202-c739-4fc9-8006-dab96ac694aa"

SHEETS = {
    "emoji_3d": os.path.join(ARTIFACT_DIR, "trini_emoji_style_3d_1792267569208.jpg"),
    "illustrated_1": os.path.join(ARTIFACT_DIR, "trini_sticker_style_illustrated_1792267569074.jpg"),
    "folklore_3d": os.path.join(ARTIFACT_DIR, "trini_pack_folklore_festivals_3d_1792268112352.jpg"),
    "social_slang": os.path.join(ARTIFACT_DIR, "trini_pack_social_slang_illustrated_1792268111885.jpg"),
}


def ensure_dirs():
    for sub in ["assets/icons", "assets/stickers", "assets/trays"]:
        os.makedirs(os.path.join(WORKSPACE_DIR, sub), exist_ok=True)


def keep_central_connected_component(rgba):
    """Removes any disconnected floating background doodles (like green WhatsApp icons) around a sticker."""
    w, h = rgba.size
    pixels = rgba.load()
    visited = bytearray(w * h)
    best_comp = []
    cx_target, cy_target = w // 2, h // 2
    best_score = -1e9

    for y in range(h):
        for x in range(w):
            idx = y * w + x
            if visited[idx] or pixels[x, y][3] == 0:
                continue
            comp = []
            q = deque([(x, y)])
            visited[idx] = 1
            min_dist_sq = 1e12
            while q:
                px, py = q.popleft()
                comp.append((px, py))
                d2 = (px - cx_target) ** 2 + (py - cy_target) ** 2
                if d2 < min_dist_sq:
                    min_dist_sq = d2
                for nx, ny in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                    if 0 <= nx < w and 0 <= ny < h:
                        nidx = ny * w + nx
                        if not visited[nidx] and pixels[nx, ny][3] > 0:
                            visited[nidx] = 1
                            q.append((nx, ny))
            # Favor large component near the center
            score = len(comp) - min_dist_sq * 0.5
            if score > best_score:
                best_score = score
                best_comp = comp

    if not best_comp:
        return rgba

    keep_mask = bytearray(w * h)
    for px, py in best_comp:
        keep_mask[py * w + px] = 1

    for y in range(h):
        for x in range(w):
            if not keep_mask[y * w + x]:
                r, g, b, _ = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
    return rgba


def remove_background_flood(tile_img, tolerance=42, crop_bottom_label=False):
    """Removes background and disconnected WhatsApp doodle artifacts from a cropped sticker tile."""
    rgba = tile_img.convert("RGBA")
    w, h = rgba.size
    if crop_bottom_label:
        h_keep = int(h * 0.85)
        rgba = rgba.crop((0, 0, w, h_keep))
        w, h = rgba.size

    if max(w, h) > 480:
        scale = 480.0 / max(w, h)
        rgba = rgba.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
        w, h = rgba.size

    pixels = rgba.load()
    corners = [
        pixels[0, 0][:3],
        pixels[w - 1, 0][:3],
        pixels[0, h - 1][:3],
        pixels[w - 1, h - 1][:3],
        pixels[w // 2, 0][:3],
    ]
    thresh = int(tolerance * 2.5)

    visited = bytearray(w * h)
    queue = deque()

    for x in range(w):
        queue.append((x, 0))
        queue.append((x, h - 1))
        visited[x] = 1
        visited[(h - 1) * w + x] = 1
    for y in range(h):
        queue.append((0, y))
        queue.append((w - 1, y))
        visited[y * w] = 1
        visited[y * w + (w - 1)] = 1

    while queue:
        cx, cy = queue.popleft()
        r, g, b, a = pixels[cx, cy]
        is_bg = False
        for sr, sg, sb in corners:
            if abs(r - sr) + abs(g - sg) + abs(b - sb) < thresh:
                is_bg = True
                break
        # Also treat faint mint-green WhatsApp doodle lines on light backgrounds as background
        if not is_bg and g > 200 and r > 170 and b > 180 and (g - r) >= 10:
            is_bg = True

        if is_bg:
            pixels[cx, cy] = (r, g, b, 0)
            if cx + 1 < w and not visited[cy * w + cx + 1]:
                visited[cy * w + cx + 1] = 1
                queue.append((cx + 1, cy))
            if cx - 1 >= 0 and not visited[cy * w + cx - 1]:
                visited[cy * w + cx - 1] = 1
                queue.append((cx - 1, cy))
            if cy + 1 < h and not visited[(cy + 1) * w + cx]:
                visited[(cy + 1) * w + cx] = 1
                queue.append((cx, cy + 1))
            if cy - 1 >= 0 and not visited[(cy - 1) * w + cx]:
                visited[(cy - 1) * w + cx] = 1
                queue.append((cx, cy - 1))

    rgba = keep_central_connected_component(rgba)
    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    return rgba


def fit_to_512_canvas(content_rgba, add_label=None, accent_hex="#DA1A35"):
    """Places RGBA artwork onto a 512x512 transparent canvas with 16px safe margin."""
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    max_w = 468
    max_h = 415 if add_label else 468

    cw, ch = content_rgba.size
    scale = min(max_w / max(1, cw), max_h / max(1, ch))
    new_w = max(1, int(cw * scale))
    new_h = max(1, int(ch * scale))
    resized = content_rgba.resize((new_w, new_h), Image.Resampling.LANCZOS)

    alpha = resized.split()[3]
    shadow = Image.new("RGBA", (new_w + 16, new_h + 16), (0, 0, 0, 0))
    shadow_alpha = alpha.point(lambda p: int(p * 0.32))
    shadow.paste((18, 19, 22, 255), (8, 10), shadow_alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))

    paste_x = (512 - new_w) // 2
    paste_y = (430 - new_h) // 2 if add_label else (512 - new_h) // 2

    canvas.alpha_composite(shadow, (max(0, paste_x - 8), max(0, paste_y - 6)))
    canvas.alpha_composite(resized, (paste_x, paste_y))

    if add_label:
        draw_sticker_pill_label(canvas, add_label, accent_hex)

    return canvas


def get_font(size, bold=True):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\impact.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def get_emoji_font(size):
    for path in [r"C:\Windows\Fonts\seguiemj.ttf", r"C:\Windows\Fonts\arialbd.ttf"]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def hex_to_rgba(hex_str, alpha=255):
    h = hex_str.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def draw_sticker_pill_label(canvas, text, accent_hex="#DA1A35"):
    draw = ImageDraw.Draw(canvas)
    font = get_font(36 if len(text) <= 14 else 29, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    pad_x, pad_y = 26, 12
    pw = min(480, tw + pad_x * 2 + 16)
    ph = th + pad_y * 2 + 10
    px = (512 - pw) // 2
    py = 492 - ph

    # Die-cut white outer border
    draw.rounded_rectangle(
        (px - 6, py - 6, px + pw + 6, py + ph + 6),
        radius=28,
        fill=(255, 255, 255, 255),
    )
    # Obsidian dark pill with accent border
    draw.rounded_rectangle(
        (px, py, px + pw, py + ph),
        radius=23,
        fill=(18, 19, 22, 255),
        outline=hex_to_rgba(accent_hex),
        width=4,
    )
    draw.text(
        (512 // 2, py + ph // 2 - 2),
        text,
        font=font,
        fill=(255, 255, 255, 255),
        anchor="mm",
    )


def extract_sheet_tile(sheet_key, row, col, name, style, accent):
    sheet_path = SHEETS[sheet_key]
    img = Image.open(sheet_path).convert("RGBA")
    w, h = img.size

    is_dark_3d = sheet_key in ("emoji_3d", "folklore_3d")
    if is_dark_3d:
        mx = int(w * 0.055)
        my_top = int(h * 0.07)
        my_bot = int(h * 0.07)
        gw = w - 2 * mx
        gh = h - my_top - my_bot
        cw = gw / 3.0
        rh = gh / 2.0
        x0 = int(mx + col * cw + cw * 0.04)
        x1 = int(mx + (col + 1) * cw - cw * 0.04)
        y0 = int(my_top + row * rh + rh * 0.02)
        y1 = int(my_top + (row + 1) * rh - rh * 0.03)
        tile = img.crop((x0, y0, x1, y1))
        cleaned = remove_background_flood(tile, tolerance=30, crop_bottom_label=True)
        return fit_to_512_canvas(cleaned, add_label=name, accent_hex=accent)
    else:
        cw = w / 3.0
        rh = h / 2.0
        x0 = int(col * cw + cw * 0.02)
        x1 = int((col + 1) * cw - cw * 0.02)
        y0 = int(row * rh + rh * 0.02)
        y1 = int((row + 1) * rh - rh * 0.02)
        tile = img.crop((x0, y0, x1, y1))
        cleaned = remove_background_flood(tile, tolerance=36, crop_bottom_label=False)
        return fit_to_512_canvas(cleaned, add_label=None, accent_hex=accent)


def render_custom_sticker(sticker):
    """Renders a clean 512x512 transparent die-cut emoji/sticker badge WITHOUT any flag ribbon or description clutter."""
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    accent = hex_to_rgba(sticker.get("accent", "#DA1A35"))
    is_3d = sticker.get("style") == "3d"
    name = sticker["name"]
    raw_emojis = [e for e in sticker.get("emojis", ["🔥"]) if e != "🇹🇹"]
    if not raw_emojis:
        raw_emojis = ["🔥"]

    cx, cy = 256, 224
    r_outer = 188

    # Soft shadow
    shadow = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse((cx - r_outer, cy - r_outer + 10, cx + r_outer, cy + r_outer + 10), fill=(18, 19, 22, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.alpha_composite(shadow)

    # Die-cut white sticker border
    draw.ellipse(
        (cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer),
        fill=(255, 255, 255, 255),
    )

    # Inner circular medallion (clean, zero flag ribbon)
    r_inner = r_outer - 16
    if is_3d:
        draw.ellipse(
            (cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner),
            fill=(24, 26, 32, 255),
            outline=accent,
            width=8,
        )
        gloss = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(gloss)
        gdraw.ellipse(
            (cx - int(r_inner * 0.58), cy - int(r_inner * 0.80), cx + int(r_inner * 0.58), cy - int(r_inner * 0.25)),
            fill=(255, 255, 255, 22),
        )
        canvas.alpha_composite(gloss)
        draw = ImageDraw.Draw(canvas)
    else:
        draw.ellipse(
            (cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner),
            fill=(250, 247, 242, 255),
            outline=accent,
            width=10,
        )

    # Render large expressive central emoji trio (zero flags, zero extra description banner)
    emoji_font_main = get_emoji_font(120)
    emoji_font_side = get_emoji_font(72)

    main_em = raw_emojis[0]
    left_em = raw_emojis[1] if len(raw_emojis) > 1 else ""
    right_em = raw_emojis[2] if len(raw_emojis) > 2 else ""

    try:
        if left_em:
            draw.text((cx - 94, cy - 4), left_em, font=emoji_font_side, anchor="mm", embedded_color=True)
        if right_em:
            draw.text((cx + 94, cy - 4), right_em, font=emoji_font_side, anchor="mm", embedded_color=True)
        draw.text((cx, cy - 12), main_em, font=emoji_font_main, anchor="mm", embedded_color=True)
    except Exception:
        draw.text((cx, cy - 12), main_em, font=emoji_font_main, fill=accent, anchor="mm")

    # Main bold die-cut slang phrase pill at bottom
    draw_sticker_pill_label(canvas, name, sticker.get("accent", "#DA1A35"))
    return canvas


def save_whatsapp_webp(rgba_512, out_webp_path):
    """Saves a 512x512 RGBA image as a <100KB WebP file."""
    for quality in (84, 72, 60):
        rgba_512.save(out_webp_path, "WEBP", quality=quality, method=2)
        if os.path.getsize(out_webp_path) < 98 * 1024:
            break


def parse_packs_from_js():
    js_path = os.path.join(WORKSPACE_DIR, "data/packs.js")
    with open(js_path, "r", encoding="utf-8") as f:
        text = f.read()

    start = text.index("window.STICKERBOOM_PACKS = [") + len("window.STICKERBOOM_PACKS = ")
    arr_str = text[start:].strip().rstrip(";")
    json_str = re.sub(r'(?<=[{,\n])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', arr_str)
    return json.loads(json_str)


def main():
    ensure_dirs()

    packs = parse_packs_from_js()
    contents_manifest = {
        "android_play_store_link": "",
        "ios_app_store_link": "",
        "sticker_packs": [],
    }

    total_count = 0
    for pack in packs:
        pack_id = pack["id"]
        pack_stickers_meta = []
        first_sticker_img = None

        for sticker in pack["stickers"]:
            sid = sticker["id"]
            if "sheetSource" in sticker and sid != "wha-appen":
                src = sticker["sheetSource"]
                rgba_512 = extract_sheet_tile(
                    src["sheet"],
                    src["row"],
                    src["col"],
                    sticker["name"],
                    sticker["style"],
                    sticker.get("accent", "#DA1A35"),
                )
            else:
                rgba_512 = render_custom_sticker(sticker)

            if first_sticker_img is None:
                first_sticker_img = rgba_512

            webp_path = os.path.join(WORKSPACE_DIR, "assets/stickers", f"{sid}.webp")
            png_path = os.path.join(WORKSPACE_DIR, "assets/stickers", f"{sid}.png")

            save_whatsapp_webp(rgba_512, webp_path)
            rgba_512.save(png_path, "PNG", compress_level=3)

            clean_emojis = [e for e in sticker.get("emojis", ["🔥"]) if e != "🇹🇹"] or ["🔥"]
            pack_stickers_meta.append(
                {
                    "image_file": f"{sid}.webp",
                    "emojis": clean_emojis[:3],
                }
            )
            total_count += 1

        tray_path = os.path.join(WORKSPACE_DIR, pack["trayIcon"])
        tray_img = first_sticker_img.resize((96, 96), Image.Resampling.LANCZOS)
        tray_img.save(tray_path, "PNG", compress_level=4)

        contents_manifest["sticker_packs"].append(
            {
                "identifier": pack_id,
                "name": f"StickerBoom: {pack['name']}"[:30],
                "publisher": "StickerBoom",
                "tray_image_file": os.path.basename(tray_path),
                "publisher_email": "daryl.created@gmail.com",
                "publisher_website": "https://stickerboom.vercel.app",
                "privacy_policy_website": "https://stickerboom.vercel.app",
                "license_agreement_website": "https://stickerboom.vercel.app",
                "image_data_version": "2",
                "avoid_cache": False,
                "animated_sticker_pack": False,
                "stickers": pack_stickers_meta,
            }
        )

    manifest_path = os.path.join(WORKSPACE_DIR, "assets/contents.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(contents_manifest, f, indent=2, ensure_ascii=False)

    print(f"Successfully rebuilt {total_count} flag-free stickers (.webp & .png) and 8 tray icons!")


if __name__ == "__main__":
    main()
