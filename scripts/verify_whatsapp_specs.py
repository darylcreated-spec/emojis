import json
import os
from PIL import Image

WORKSPACE_DIR = r"c:\Antigravity Projects\TRINI Emoj"


def main():
    contents_path = os.path.join(WORKSPACE_DIR, "assets/contents.json")
    assert os.path.exists(contents_path), "Missing assets/contents.json"

    with open(contents_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    packs = manifest.get("sticker_packs", [])
    assert len(packs) == 8, f"Expected 8 packs, found {len(packs)}"

    total_stickers = 0
    max_webp_kb = 0.0

    for pack in packs:
        tray_file = os.path.join(WORKSPACE_DIR, "assets/trays", pack["tray_image_file"])
        assert os.path.exists(tray_file), f"Missing tray icon: {tray_file}"
        tray_kb = os.path.getsize(tray_file) / 1024.0
        assert tray_kb < 50.0, f"Tray icon exceeds 50KB: {tray_kb:.1f}KB"
        with Image.open(tray_file) as timg:
            assert timg.size == (96, 96), f"Tray icon must be 96x96, got {timg.size}"

        stickers = pack.get("stickers", [])
        assert 3 <= len(stickers) <= 30, f"Pack {pack['identifier']} sticker count out of WhatsApp bounds: {len(stickers)}"

        for s in stickers:
            webp_path = os.path.join(WORKSPACE_DIR, "assets/stickers", s["image_file"])
            png_path = webp_path.replace(".webp", ".png")
            assert os.path.exists(webp_path), f"Missing WebP: {webp_path}"
            assert os.path.exists(png_path), f"Missing PNG: {png_path}"

            webp_kb = os.path.getsize(webp_path) / 1024.0
            max_webp_kb = max(max_webp_kb, webp_kb)
            assert webp_kb < 100.0, f"Sticker {s['image_file']} exceeds 100KB WhatsApp limit ({webp_kb:.1f}KB)"

            with Image.open(webp_path) as simg:
                assert simg.size == (512, 512), f"Sticker {s['image_file']} must be 512x512, got {simg.size}"

            total_stickers += 1

    # Verify PWA icons
    for icon_name in ["icon-512.png", "icon-192.png", "apple-touch-icon.png", "favicon.png", "icon-1-scotch-bonnet.png"]:
        ipath = os.path.join(WORKSPACE_DIR, "assets/icons", icon_name)
        assert os.path.exists(ipath), f"Missing PWA icon: {ipath}"

    print(
        f"VERIFICATION PASSED: {len(packs)} packs, {total_stickers} stickers (.webp & .png), "
        f"max WebP size = {max_webp_kb:.1f} KB (<100 KB WhatsApp limit), all 512x512 px, all trays 96x96 px."
    )


if __name__ == "__main__":
    main()
