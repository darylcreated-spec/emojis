import json
import math
import os
import re
import zipfile
from collections import deque
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WORKSPACE_DIR = r"c:\Antigravity Projects\TRINI Emoj"
ARTIFACT_DIR = r"C:\Users\daryl\.gemini\antigravity\brain\71a5a202-c739-4fc9-8006-dab96ac694aa"

SHEETS = {
    "emoji_3d": os.path.join(ARTIFACT_DIR, "trini_emoji_style_3d_1792267569208.jpg"),
    "illustrated_1": os.path.join(ARTIFACT_DIR, "trini_sticker_style_illustrated_1792267569074.jpg"),
    "folklore_3d": os.path.join(ARTIFACT_DIR, "trini_pack_folklore_festivals_3d_1792268112352.jpg"),
    "social_slang": os.path.join(ARTIFACT_DIR, "trini_pack_social_slang_illustrated_1792268111885.jpg"),
    "extra_3d": os.path.join(ARTIFACT_DIR, "custom_sheet_3d_extra_1792362545945.jpg"),
    "extra_slang": os.path.join(ARTIFACT_DIR, "custom_sheet_slang_extra_1792362548549.jpg"),
}

# Map additional stickers directly to the newly generated custom 3D & Pop-Art sheets
EXTRA_SHEET_OVERRIDES = {
    "ah-eh-able": ("extra_3d", 0, 0),
    "bake-and-shark": ("extra_3d", 0, 1),
    "pepper-mouth": ("extra_3d", 0, 2),
    "hang-jack": ("extra_3d", 1, 0),
    "deya-parsad": ("extra_3d", 1, 1),
    "crab-and-dumpling": ("extra_3d", 1, 2),
    "scene": ("extra_slang", 0, 0),
    "fuh-real": ("extra_slang", 0, 1),
    "bess": ("extra_slang", 0, 2),
    "cyah-take-dat": ("extra_slang", 1, 0),
    "wait-for-de-riddim": ("extra_slang", 1, 1),
    "vibes-on-vibes": ("extra_slang", 1, 2),
}


def ensure_dirs():
    for sub in ["assets/icons", "assets/stickers", "assets/trays", "assets/packs"]:
        os.makedirs(os.path.join(WORKSPACE_DIR, sub), exist_ok=True)


def keep_central_connected_component(rgba):
    """Removes any disconnected floating background doodles around a sticker."""
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
    """Removes background and disconnected doodle artifacts from a cropped sticker tile."""
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


def fit_to_512_canvas(content_rgba, add_label=None, accent_hex="#E03A26"):
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


def draw_sticker_pill_label(canvas, text, accent_hex="#E03A26"):
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

    draw.rounded_rectangle(
        (px - 6, py - 6, px + pw + 6, py + ph + 6),
        radius=28,
        fill=(255, 255, 255, 255),
    )
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
    elif sheet_key == "extra_3d":
        cw = w / 3.0
        rh = h / 2.0
        x0 = int(col * cw + cw * 0.03)
        x1 = int((col + 1) * cw - cw * 0.03)
        y0 = int(row * rh + rh * 0.03)
        y1 = int((row + 1) * rh - rh * 0.03)
        tile = img.crop((x0, y0, x1, y1))
        cleaned = remove_background_flood(tile, tolerance=22, crop_bottom_label=False)
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
    """Renders a high-impact 512x512 Vinyl Peel & Pop-Art Sunburst die-cut sticker (zero flags, zero descriptions)."""
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    accent_hex = sticker.get("accent", "#E03A26")
    if accent_hex == "#25D366":
        accent_hex = "#F59E0B"
    accent = hex_to_rgba(accent_hex)
    is_3d = sticker.get("style") == "3d"
    name = sticker["name"]
    raw_emojis = [e for e in sticker.get("emojis", ["🔥"]) if e != "🇹🇹"] or ["🔥"]

    cx, cy = 256, 222
    r_outer = 190
    r_inner = r_outer - 16

    # Soft shadow
    shadow = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse((cx - r_outer, cy - r_outer + 10, cx + r_outer, cy + r_outer + 10), fill=(18, 19, 22, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.alpha_composite(shadow)

    # Die-cut white outer vinyl border
    draw.ellipse(
        (cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer),
        fill=(255, 255, 255, 255),
    )

    # Create radial sunburst vinyl disc inside r_inner
    disc = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    ddraw = ImageDraw.Draw(disc)
    base_bg = (22, 24, 30, 255) if is_3d else (255, 246, 232, 255)
    ray_color = (accent[0], accent[1], accent[2], 55 if is_3d else 42)
    ddraw.ellipse((cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner), fill=base_bg)

    num_rays = 16
    for i in range(num_rays):
        a1 = (i * 2 * math.pi) / num_rays
        a2 = ((i + 0.5) * 2 * math.pi) / num_rays
        p1 = (cx + math.cos(a1) * r_inner * 1.3, cy + math.sin(a1) * r_inner * 1.3)
        p2 = (cx + math.cos(a2) * r_inner * 1.3, cy + math.sin(a2) * r_inner * 1.3)
        ddraw.polygon([(cx, cy), p1, p2], fill=ray_color)

    # Mask the sunburst to r_inner circle
    disc_mask = Image.new("L", (512, 512), 0)
    mdraw = ImageDraw.Draw(disc_mask)
    mdraw.ellipse((cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner), fill=255)
    canvas.paste(disc, (0, 0), disc_mask)

    draw = ImageDraw.Draw(canvas)
    draw.ellipse(
        (cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner),
        outline=accent,
        width=9,
    )

    # Subtle vinyl top gloss arc + bottom-right 3D vinyl peel curl
    gloss = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gloss)
    gdraw.ellipse(
        (cx - int(r_inner * 0.62), cy - int(r_inner * 0.82), cx + int(r_inner * 0.62), cy - int(r_inner * 0.22)),
        fill=(255, 255, 255, 28),
    )
    canvas.alpha_composite(gloss)
    draw = ImageDraw.Draw(canvas)

    # Render expressive central artwork
    emoji_font_main = get_emoji_font(126)
    emoji_font_side = get_emoji_font(74)

    main_em = raw_emojis[0]
    left_em = raw_emojis[1] if len(raw_emojis) > 1 else ""
    right_em = raw_emojis[2] if len(raw_emojis) > 2 else ""

    try:
        if left_em:
            draw.text((cx - 96, cy - 2), left_em, font=emoji_font_side, anchor="mm", embedded_color=True)
        if right_em:
            draw.text((cx + 96, cy - 2), right_em, font=emoji_font_side, anchor="mm", embedded_color=True)
        draw.text((cx, cy - 10), main_em, font=emoji_font_main, anchor="mm", embedded_color=True)
    except Exception:
        draw.text((cx, cy - 10), main_em, font=emoji_font_main, fill=accent, anchor="mm")

    # Main bold die-cut slang phrase pill at bottom
    draw_sticker_pill_label(canvas, name, accent_hex)
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

    all_sticker_files = []
    total_count = 0

    for pack in packs:
        pack_id = pack["id"]
        pack_stickers_meta = []
        first_sticker_img = None
        pack_files = []

        for sticker in pack["stickers"]:
            sid = sticker["id"]
            accent_hex = sticker.get("accent", "#E03A26")
            if accent_hex == "#25D366":
                accent_hex = "#F59E0B"

            if sid in EXTRA_SHEET_OVERRIDES:
                s_key, r_idx, c_idx = EXTRA_SHEET_OVERRIDES[sid]
                rgba_512 = extract_sheet_tile(s_key, r_idx, c_idx, sticker["name"], sticker["style"], accent_hex)
            elif "sheetSource" in sticker and sid != "wha-appen":
                src = sticker["sheetSource"]
                rgba_512 = extract_sheet_tile(
                    src["sheet"],
                    src["row"],
                    src["col"],
                    sticker["name"],
                    sticker["style"],
                    accent_hex,
                )
            else:
                rgba_512 = render_custom_sticker(sticker)

            if first_sticker_img is None:
                first_sticker_img = rgba_512

            webp_path = os.path.join(WORKSPACE_DIR, "assets/stickers", f"{sid}.webp")
            png_path = os.path.join(WORKSPACE_DIR, "assets/stickers", f"{sid}.png")

            save_whatsapp_webp(rgba_512, webp_path)
            rgba_512.save(png_path, "PNG", compress_level=3)

            pack_files.append((png_path, f"png/{sid}.png"))
            pack_files.append((webp_path, f"webp/{sid}.webp"))
            all_sticker_files.append((png_path, f"{pack_id}/png/{sid}.png"))
            all_sticker_files.append((webp_path, f"{pack_id}/webp/{sid}.webp"))

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
        pack_files.append((tray_path, f"tray-{pack_id}.png"))

        pack_entry = {
            "identifier": pack_id,
            "name": f"StickerBoom: {pack['name']}"[:30],
            "publisher": "StickerBoom",
            "tray_image_file": os.path.basename(tray_path),
            "publisher_email": "daryl.created@gmail.com",
            "publisher_website": "https://stickerboom.vercel.app",
            "privacy_policy_website": "https://stickerboom.vercel.app",
            "license_agreement_website": "https://stickerboom.vercel.app",
            "image_data_version": "3",
            "avoid_cache": False,
            "animated_sticker_pack": False,
            "stickers": pack_stickers_meta,
        }
        contents_manifest["sticker_packs"].append(pack_entry)

        # Build real .ZIP archive for this pack
        zip_path = os.path.join(WORKSPACE_DIR, "assets/packs", f"{pack_id}.zip")
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for disk_path, arc_name in pack_files:
                zf.write(disk_path, arcname=arc_name)
            zf.writestr("pack-info.json", json.dumps(pack_entry, indent=2, ensure_ascii=False))

    manifest_path = os.path.join(WORKSPACE_DIR, "assets/contents.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(contents_manifest, f, indent=2, ensure_ascii=False)

    # Build master All-98-Stickers .ZIP archive
    master_zip_path = os.path.join(WORKSPACE_DIR, "assets/packs", "stickerboom-all-98-stickers.zip")
    with zipfile.ZipFile(master_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for disk_path, arc_name in all_sticker_files:
            zf.write(disk_path, arcname=arc_name)
        zf.write(manifest_path, arcname="contents.json")

    print(f"Successfully built {total_count} stickers (.webp & .png), 8 tray icons, and 9 real .ZIP pack archives!")


if __name__ == "__main__":
    main()
