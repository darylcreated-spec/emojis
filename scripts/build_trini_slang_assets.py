"""
Builds all 88 Wordless Literal 3D Trini Slang Stickers (512x512 Transparent PNG & <100KB WebP),
Category & Master .ZIP Archives, and data/trini-slang.js for StickerBoom.
"""
from collections import deque
import json
import os
import zipfile
from PIL import Image, ImageFilter

WORKSPACE_DIR = r"c:\Antigravity Projects\TRINI Emoj"
ARTIFACT_DIR = r"C:\Users\daryl\.gemini\antigravity\brain\fa0e441c-33b8-49cd-852d-43128a862fab"

SHEETS = {
    "lit1": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_1_png_1792957119707.jpg"), 3, 3),
    "lit2": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_2_1792957129747.jpg"), 3, 3),
    "lit3": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_3_1792957538117.jpg"), 3, 3),
    "lit4": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_4_1792957544916.jpg"), 3, 3),
    "lit5": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_5_1792957542373.jpg"), 3, 3),
    "lit6": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_6_1792957551644.jpg"), 3, 3),
    "lit7": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_7_1792957566180.jpg"), 3, 3),
    "lit8": (os.path.join(ARTIFACT_DIR, "trini_slang_literal_icons_8_png_1792957543273.jpg"), 3, 4),
    "scene1": (os.path.join(ARTIFACT_DIR, "trini_slang_wordless_pictorial_1_1792956333083.jpg"), 3, 3),
    "scene2": (os.path.join(ARTIFACT_DIR, "trini_slang_wordless_pictorial_2_1792956423145.jpg"), 3, 3),
}

ITEMS_88 = [
    (1, "wha-yuh-say", "Wha yuh say?", "someone visually speaking but the listener hears nothing", "Greetings & Links", ("scene1", 0, 0), "Hand cupped to ear with muted soundwaves"),
    (2, "wha-go-on", "Wha go on?", "how are you doing", "Greetings & Links", ("lit2", 2, 1), "Two hands meeting in a fist bump"),
    (3, "doh-study-dat", "Doh study dat", "something bad is happening but i have a solution", "Co-Signs & Facts", ("scene1", 0, 1), "Chill character with golden umbrella deflecting storm"),
    (4, "leh-we-go", "Leh we go .", "follow me", "Greetings & Links", ("lit3", 0, 0), "Single winged running sneaker"),
    (5, "ah-coming", "Ah coming", "i will be there but i am running late", "Greetings & Links", ("scene1", 0, 2), "Sprinting late with clock and coffee"),
    (6, "ah-reach", "Ah reach", "i have arrived", "Greetings & Links", ("lit3", 0, 1), "Red 3D GPS location pin on golden target"),
    (7, "ah-gone", "Ah gone", "i am leaving", "Greetings & Links", ("lit3", 0, 2), "Peace sign hand with puff of smoke"),
    (8, "ent", "Ent?", "look for affirmation from a friend", "Co-Signs & Facts", ("lit4", 1, 0), "Hand over golden heart / affirmation"),
    (9, "right-dey", "Right dey —", "someone is close", "Greetings & Links", ("lit3", 1, 0), "Hand pointing straight down at glowing spot"),
    (10, "just-now", "Just now", "wait a couple of seconds", "Greetings & Links", ("lit3", 1, 1), "Golden 3D hourglass with turquoise sand"),
    (11, "small-ting", "Small ting", "no problem", "Co-Signs & Facts", ("lit2", 2, 0), "Hand making tiny-pinch gesture with sparkle"),
    (12, "no-scene", "No scene.", "yes", "Co-Signs & Facts", ("lit3", 1, 2), "Emerald-green 3D checkmark badge"),
    (13, "all-ah-dat", "All ah dat.", "plenty stuff to do", "Co-Signs & Facts", ("lit3", 2, 0), "Towering stack of colourful parcels and boxes"),
    (14, "yuh-good", "Yuh good?", "is every thing ok", "Greetings & Links", ("lit3", 2, 1), "Warm thumbs-up hand beside a golden heart"),
    (15, "how-yuh-mean", "How yuh mean?", "explain yourself", "Disbelief & Comedy", ("lit3", 2, 2), "Tilted 3D question mark with raised eyebrow"),
    (16, "doh-start", "Doh start", "keep quiet", "Attitude & Shade", ("lit4", 0, 0), "3D lips zipped shut with a golden zipper"),
    (17, "watch-nah", "Watch nah", "take notice", "Disbelief & Comedy", ("lit4", 0, 1), "Wide 3D cartoon side-eyes with sparkle"),
    (18, "hear-nah", "Hear nah", "stop talking and listen to me", "Disbelief & Comedy", ("lit4", 0, 2), "Hand cupping an attentive ear with soundwaves"),
    (19, "for-true", "For true?", "i am not lying", "Co-Signs & Facts", ("lit4", 1, 0), "Open palm raised over a glowing golden heart"),
    (20, "real-talk", "Real talk", "facts", "Co-Signs & Facts", ("lit2", 1, 2), "Golden studio microphone drop"),
    (21, "bet", "Bet.", "ok", "Co-Signs & Facts", ("lit4", 1, 1), "Two hands locked in a firm handshake"),
    (22, "yuh-mad", "Yuh mad?", "are you angry", "Attitude & Shade", ("lit4", 1, 2), "Red 3D thermometer bursting with fire"),
    (23, "yuh-jokin", "Yuh jokin'", "what you are saying is unreal", "Disbelief & Comedy", ("lit4", 2, 0), "Colourful 3D jester hat with golden bells"),
    (24, "doh-play", "Doh play", "make sense", "Disbelief & Comedy", ("lit4", 2, 1), "Yellow 3D caution warning triangle"),
    (25, "lemme-see", "Lemme see", "take something away from someone and examine it", "Disbelief & Comedy", ("lit2", 1, 1), "Golden magnifying glass with turquoise lens"),
    (26, "nah-man", "Nah man!", "you are not speaking the truth", "Disbelief & Comedy", ("lit4", 2, 2), "Arms crossed in a bold X over a red X"),
    (27, "boy-please", "Boy, please!", "immediately stop your action", "Disbelief & Comedy", ("lit5", 0, 0), "Raised talk-to-the-hand stop palm with sparkles"),
    (28, "steups", "Steups", "disapproval", "Attitude & Shade", ("lit8", 2, 1), "Unimpressed disapproval expression"),
    (29, "tanty", "Tanty!", "mother sister", "People & Drama", ("lit5", 0, 1), "Smiling Trini Aunty with red hibiscus & gold hoops"),
    (30, "gyal", "Gyal!", "girl", "People & Drama", ("lit5", 0, 2), "Crowned Caribbean woman with star earrings"),
    (31, "boi", "Boi!", "boy", "People & Drama", ("lit5", 1, 0), "Expressive young Caribbean man with fade"),
    (32, "yuh-too-lie", "Yuh too lie!", "not telling the truth", "Disbelief & Comedy", ("lit5", 1, 1), "3D face with a long wooden Pinocchio nose"),
    (33, "doh-kill-meh", "Doh kill meh", "an unrealistic story", "Disbelief & Comedy", ("lit5", 1, 2), "Laughing 3D face crying rivers of tears"),
    (34, "ah-done", "Ah done", "stop talking", "Attitude & Shade", ("lit5", 2, 0), "Two hands dusting each other off"),
    (35, "is-a-jokes", "Is a jokes", "unfactual information", "Disbelief & Comedy", ("lit5", 2, 1), "Colourful Carnival jester comedy mask"),
    (36, "mad-ting", "Mad ting", "unreal news", "Disbelief & Comedy", ("lit5", 2, 2), "Mind-blown head erupting with neon fireworks"),
    (37, "wicked", "Wicked!", "evil person", "People & Drama", ("lit6", 0, 0), "Purple 3D smiling devil face with golden horns"),
    (38, "high-beam", "high beam", "a woman having an orgasm / peak excitement", "People & Drama", ("lit1", 1, 0), "Two blazing car high-beam headlights"),
    (39, "a-week", "a week", "a funny situation", "Disbelief & Comedy", ("lit6", 0, 1), "Yellow laughing face melting into a puddle"),
    (40, "too-much", "Too much", "over sharing", "Attitude & Shade", ("lit6", 0, 2), "Two hands clamping firmly over both ears"),
    (41, "dohh-bother", "Dohh bother", "nevermind", "Attitude & Shade", ("lit6", 1, 0), "Hand doing a dismissive wave-off"),
    (42, "mash-up", "Mash up", "destroy something", "Vibes, Belly & Money", ("lit1", 1, 2), "Wooden mallet smashing a rock into shards"),
    (43, "real-bad", "Real bad", "real problems", "Vibes, Belly & Money", ("lit6", 1, 1), "Flashing red 3D emergency siren light"),
    (44, "ah-screaming", "Ah screaming!", "enjoying a moment", "Disbelief & Comedy", ("lit6", 1, 2), "Colourful megaphone blasting party confetti"),
    (45, "doh-watch-me", "Doh watch me", "pay no attention to me", "Attitude & Shade", ("lit6", 2, 0), "Dark sunglasses with hand blocking view"),
    (46, "mind-yuh-business", "Mind yuh business", "pay attention to yourself and not others", "Attitude & Shade", ("scene2", 2, 2), "Sipping coconut water inside a golden bubble"),
    (47, "stay-in-yuh-lane", "Stay in yuh lane", "dont speak about stuff you dont know about", "Attitude & Shade", ("scene2", 0, 1), "Driving strictly inside painted neon road lanes"),
    (48, "yuh-too-bold", "Yuh too bold", "making a point without the relevant information", "Attitude & Shade", ("lit6", 2, 1), "Hand holding up a crimson penalty Red Card"),
    (49, "yuh-real-brave", "Yuh real brave", "have no fear", "People & Drama", ("lit6", 2, 2), "Majestic golden-maned 3D lion wearing a medal"),
    (50, "badmind", "Badmind", "not happy for someone who won", "Attitude & Shade", ("scene1", 1, 1), "Jealous green side-eye next to trophy winner"),
    (51, "vex", "Vex", "angry", "Attitude & Shade", ("lit2", 0, 2), "Fiery red angry Scotch Bonnet pepper blowing steam"),
    (52, "dont-hot-up-yuh-head", "dont Hot up yuh head", "no problem", "Co-Signs & Facts", ("lit2", 1, 0), "Glowing turquoise melting 3D ice cube"),
    (53, "take-a-set", "Take a set", "listen", "Attitude & Shade", ("lit1", 2, 0), "Striped folding veranda beach chair"),
    (54, "doh-get-on-so", "Doh get on so", "behave", "Attitude & Shade", ("lit7", 0, 0), "Hand wagging index finger sternly"),
    (55, "yuh-feeling-yuhself", "Yuh feeling yuhself", "having problems / acting grand", "People & Drama", ("lit7", 0, 1), "Hand holding ornate golden mirror with sparkles"),
    (56, "big-up-yuhself", "Big up yuhself", "take a bow", "Co-Signs & Facts", ("lit7", 0, 2), "Jewel-encrusted golden royal crown"),
    (57, "respect", "Respect", "Salute & honor", "Co-Signs & Facts", ("lit7", 1, 0), "Two-finger forehead salute with golden star"),
    (58, "liming", "Liming", "lets go out", "Greetings & Links", ("lit7", 1, 1), "Two frosty tropical drinks clinking by a palm leaf"),
    (59, "doh-be-a-dotish", "Doh be a dotish", "stupid person", "Attitude & Shade", ("lit7", 1, 2), "Dizzy cartoon face with spiral eyes and stars"),
    (60, "dotishness", "Dotishness", "doing stupid things", "Attitude & Shade", ("lit7", 2, 0), "Expressive character doing a forehead facepalm"),
    (61, "fass", "Fass", "studying other people", "People & Drama", ("lit7", 2, 1), "Brass-and-gold extending spyglass telescope"),
    (62, "maco", "Maco", "looking closely at other people", "People & Drama", ("scene2", 0, 0), "Peeking through curtains with binoculars"),
    (63, "tabanca", "Tabanca", "broken relation with someone that did not workout", "People & Drama", ("lit2", 0, 1), "Glossy 3D broken heart with a blue tear drop"),
    (64, "horn", "Horn", "being unfaithful", "People & Drama", ("lit1", 2, 2), "Pair of glossy golden-red bull horns"),
    (65, "wha-yuh-on", "Wha yuh on?", "doing something stupid", "Attitude & Shade", ("lit7", 2, 2), "Squinting face with raised eyebrow & flashlight"),
    (66, "yuh-outside", "Yuh outside?", "meet up to hang out with a group", "Greetings & Links", ("lit8", 0, 0), "Neon streetlamp glowing beside an open party door"),
    (67, "link-me", "Link me", "i want in", "Greetings & Links", ("lit8", 0, 1), "Vibrating smartphone with golden chain link"),
    (68, "link-up", "Link up", "meeting up with a group of friends", "Greetings & Links", ("lit1", 2, 1), "Two interlocking golden 3D chain links"),
    (69, "vibes", "Vibes", "enjoying the same thing", "Vibes, Belly & Money", ("lit8", 0, 2), "Vibrant 3D boombox with neon music notes"),
    (70, "good-vibes-only", "Good vibes only", "no hate or shade", "Vibes, Belly & Money", ("lit8", 0, 3), "Smiling golden sun wearing cool sunglasses"),
    (71, "the-vibe-different", "The vibe different", "not feeling the same thing as other people", "Vibes, Belly & Money", ("lit8", 1, 0), "Thermometer gauge needle in the icy blue zone"),
    (72, "no-cap", "No cap", "no joking", "Co-Signs & Facts", ("lit1", 0, 2), "Blue baseball cap with red prohibition slash"),
    (73, "cap", "Cap", "joking", "Disbelief & Comedy", ("lit1", 0, 1), "Single vibrant electric-blue baseball cap"),
    (74, "lowkey", "Lowkey", "making a move without anyone seeing you", "Vibes, Belly & Money", ("scene2", 0, 2), "Sneaky hoodie character tip-toeing past spotlight"),
    (75, "highkey", "Highkey", "letting everyone notice you", "Vibes, Belly & Money", ("lit8", 1, 1), "Two golden stage spotlights crossing beams"),
    (76, "im-weak", "I'm weak", "laughing real hard its so overwhelming", "Disbelief & Comedy", ("scene2", 1, 0), "Laughing so hard melting into a rainbow puddle"),
    (77, "im-dead", "I'm dead", "soon to be in problems", "Vibes, Belly & Money", ("lit8", 1, 2), "Expressive 3D cartoon skull with lightning spark"),
    (78, "ate", "Ate", "belly full", "Vibes, Belly & Money", ("lit8", 1, 3), "Happy 3D character rubbing a full round belly"),
    (79, "ate-and-left-no-crumbs", "Ate and left no crumbs", "belly full and the plate is empty", "Vibes, Belly & Money", ("lit1", 1, 1), "Sparkling-clean white plate with golden fork & knife"),
    (80, "its-not-giving", "It's not giving", "take no prisoners", "Vibes, Belly & Money", ("lit8", 2, 0), "Bold 3D hand giving a giant thumbs-down"),
    (81, "be-so-for-real", "Be so for real", "not on the same page as someone", "Vibes, Belly & Money", ("lit8", 2, 1), "Flat deadpan unimpressed 3D face"),
    (82, "delulu", "Delulu", "Living in a fantasy world", "Vibes, Belly & Money", ("scene2", 2, 1), "Floating on pink clouds with heart glasses & unicorns"),
    (83, "rizz", "Rizz", "throwing shade / charm someone's way", "Vibes, Belly & Money", ("lit8", 2, 2), "Smooth winking 3D face lowering sunglasses"),
    (84, "red-flag", "Red flag", "a person with real problems", "Vibes, Belly & Money", ("lit1", 0, 0), "Single vibrant crimson flag waving on a golden pole"),
    (85, "soft-launch", "Soft launch", "pre party", "Greetings & Links", ("lit8", 2, 3), "Two crystal champagne flutes clinking by velvet curtain"),
    (86, "hard-lucks-dey", "Hard lucks Dey", "all finished before you can get one", "Vibes, Belly & Money", ("lit2", 2, 2), "Single open, completely empty black iron pot"),
    (87, "left-on-read", "Left on read", "pocket empty", "Vibes, Belly & Money", ("scene1", 2, 1), "Turning both pants pockets inside-out with moth & cobweb"),
    (88, "the-eagle-has-landed", "the eagle has landed", "getting paid", "Vibes, Belly & Money", ("lit2", 0, 0), "Eagle swooping down clutching a stack of cash"),
]


def remove_white_bg_flood(tile_img):
    """Flood-fills the pure white outer background from borders while preserving die-cut sticker art."""
    rgba = tile_img.convert("RGBA")
    w, h = rgba.size
    pixels = rgba.load()

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
        # Pure white / near-white background outside the die-cut shadow
        if r >= 246 and g >= 246 and b >= 246:
            pixels[cx, cy] = (r, g, b, 0)
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < w and 0 <= ny < h:
                    nidx = ny * w + nx
                    if not visited[nidx]:
                        visited[nidx] = 1
                        queue.append((nx, ny))

    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    return rgba


def fit_to_512_wordless(content_rgba):
    """Centers the die-cut 3D icon onto a 512x512 transparent canvas with a 16px safe margin (ZERO TEXT)."""
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    max_dim = 472
    cw, ch = content_rgba.size
    scale = min(max_dim / max(1, cw), max_dim / max(1, ch))
    new_w = max(1, int(cw * scale))
    new_h = max(1, int(ch * scale))
    resized = content_rgba.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Soft drop shadow so white die-cut borders pop on light and dark chat backgrounds
    alpha = resized.split()[3]
    shadow = Image.new("RGBA", (new_w + 16, new_h + 16), (0, 0, 0, 0))
    shadow_alpha = alpha.point(lambda p: int(p * 0.25))
    shadow.paste((18, 19, 22, 255), (8, 10), shadow_alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))

    paste_x = (512 - new_w) // 2
    paste_y = (512 - new_h) // 2
    canvas.alpha_composite(shadow, (max(0, paste_x - 8), max(0, paste_y - 8)))
    canvas.alpha_composite(resized, (paste_x, paste_y))
    return canvas


def save_whatsapp_webp(rgba_512, out_webp_path):
    for quality in (84, 72, 60, 50):
        rgba_512.save(out_webp_path, "WEBP", quality=quality, method=4)
        if os.path.getsize(out_webp_path) < 98 * 1024:
            break


def main():
    os.makedirs(os.path.join(WORKSPACE_DIR, "assets/stickers"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_DIR, "assets/packs"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_DIR, "data"), exist_ok=True)

    loaded_sheets = {}
    for k, (p, rows, cols) in SHEETS.items():
        loaded_sheets[k] = (Image.open(p).convert("RGBA"), rows, cols)

    slang_catalog = []
    all_zip_files = []

    for num, sid, raw, meaning, cat, (sh_key, r, c), visual in ITEMS_88:
        file_id = f"slang-{sid}"
        img, rows, cols = loaded_sheets[sh_key]
        w, h = img.size
        cw = w / cols
        rh = h / rows
        pad_x = cw * 0.015
        pad_y = rh * 0.015
        tile = img.crop((int(c * cw + pad_x), int(r * rh + pad_y), int((c + 1) * cw - pad_x), int((r + 1) * rh - pad_y)))

        cleaned = remove_white_bg_flood(tile)
        rgba_512 = fit_to_512_wordless(cleaned)

        png_rel = f"assets/stickers/{file_id}.png"
        webp_rel = f"assets/stickers/{file_id}.webp"
        png_path = os.path.join(WORKSPACE_DIR, png_rel)
        webp_path = os.path.join(WORKSPACE_DIR, webp_rel)

        rgba_512.save(png_path, "PNG", compress_level=4)
        save_whatsapp_webp(rgba_512, webp_path)

        all_zip_files.append((png_path, f"png/{file_id}.png"))
        all_zip_files.append((webp_path, f"webp/{file_id}.webp"))

        slang_catalog.append({
            "num": num,
            "id": file_id,
            "slug": sid,
            "name": raw,
            "meaning": meaning,
            "category": cat,
            "visual": visual,
            "style": "3d",
            "pngUrl": png_rel,
            "webpUrl": webp_rel,
        })

    # Write master Trini Slang .ZIP archive
    zip_path = os.path.join(WORKSPACE_DIR, "assets/packs/trini-slang-all-88.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for disk_path, arc_name in all_zip_files:
            zf.write(disk_path, arcname=arc_name)
        zf.writestr("trini-slang-manifest.json", json.dumps(slang_catalog, indent=2, ensure_ascii=False))

    # Write data/trini-slang.js
    js_path = os.path.join(WORKSPACE_DIR, "data/trini-slang.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// StickerBoom — Universal Trini Slang 88-Item Literal 3D Pictorial Catalog\n")
        f.write("// 100% Wordless 3D Visual Icons (512x512 PNG & <100KB WebP)\n\n")
        f.write("window.STICKERBOOM_TRINI_SLANG = ")
        f.write(json.dumps(slang_catalog, indent=2, ensure_ascii=False))
        f.write(";\n")

    print(f"Successfully generated {len(slang_catalog)} 512x512 PNG & WebP Trini Slang stickers, trini-slang-all-88.zip, and data/trini-slang.js!")


if __name__ == "__main__":
    main()
