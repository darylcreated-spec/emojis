"""
PeelOff E2E Test Suite — Opaque-Box Test Helpers
Shared utilities for catalog loading, binary chunk parsing, safe PIL operations,
subprocess invocation, and milestone gating.
"""

import os
import sys
import json
import re
import subprocess
import unittest
from contextlib import contextmanager
from typing import Optional, Any, Dict, List, Tuple
from PIL import Image, ImageChops, ImageStat


# Project root path
WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Global strict mode flag (set by CLI runner)
STRICT_MODE = os.environ.get("PEELOFF_STRICT_MODE", "0") == "1"


def set_strict_mode(enabled: bool):
    """Enable or disable strict release gating mode."""
    global STRICT_MODE
    STRICT_MODE = enabled
    os.environ["PEELOFF_STRICT_MODE"] = "1" if enabled else "0"


def is_strict_mode() -> bool:
    """Return whether strict gating mode is active."""
    return STRICT_MODE or os.environ.get("PEELOFF_STRICT_MODE", "0") == "1"


@contextmanager
def temporary_strict_mode(enabled: bool):
    """
    Context manager to temporarily override strict mode state,
    guaranteeing complete isolation and restoring previous state upon exit.
    """
    global STRICT_MODE
    old_global = STRICT_MODE
    old_env = os.environ.get("PEELOFF_STRICT_MODE")
    try:
        set_strict_mode(enabled)
        yield
    finally:
        STRICT_MODE = old_global
        if old_env is None:
            os.environ.pop("PEELOFF_STRICT_MODE", None)
        else:
            os.environ["PEELOFF_STRICT_MODE"] = old_env


def get_workspace_path(*subpaths: str) -> str:
    """Return absolute normalized path relative to project workspace root."""
    return os.path.normpath(os.path.join(WORKSPACE_DIR, *subpaths))


def get_python_executable() -> str:
    """Return path to active Python virtual environment or current interpreter."""
    venv_py = get_workspace_path(".venv", "Scripts", "python.exe")
    if os.path.exists(venv_py):
        return venv_py
    return sys.executable


# In-memory cache for parsed catalogs
_CACHED_PACKS: Optional[List[Dict[str, Any]]] = None
_CACHED_SLANG: Optional[List[Dict[str, Any]]] = None


def load_packs_catalog() -> List[Dict[str, Any]]:
    """
    Load the 8 cultural packs and their 100 stickers from data/packs.js.
    Uses Node.js execution with regex fallback, cached in memory.
    """
    global _CACHED_PACKS
    if _CACHED_PACKS is not None:
        return _CACHED_PACKS

    packs_path = get_workspace_path("data", "packs.js")
    if not os.path.exists(packs_path):
        raise FileNotFoundError(f"Missing packs catalog: {packs_path}")

    # Try executing with node
    try:
        cmd = [
            "node",
            "-e",
            """
            global.window = {};
            require('./data/packs.js');
            console.log(JSON.stringify(window.STICKERBOOM_PACKS));
            """
        ]
        res = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            _CACHED_PACKS = json.loads(res.stdout)
            return _CACHED_PACKS
    except Exception:
        pass

    # Regex fallback parser
    with open(packs_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract packs array
    match = re.search(r"window\.STICKERBOOM_PACKS\s*=\s*(\[[\s\S]*?\]);\s*$", content)
    if match:
        raw_json = match.group(1)
        # Convert JS object keys to JSON
        cleaned = re.sub(r"([{,]\s*)([a-zA-Z0-9_]+)\s*:", r'\1"\2":', raw_json)
        cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)
        try:
            _CACHED_PACKS = json.loads(cleaned)
            return _CACHED_PACKS
        except Exception:
            pass

    # Basic structural fallback
    pack_matches = re.findall(r'id:\s*"([^"]+)",[\s\S]*?name:\s*"([^"]+)"', content)
    packs = []
    for pid, pname in pack_matches:
        if pid.startswith("pack-"):
            packs.append({"id": pid, "name": pname, "stickers": []})
    _CACHED_PACKS = packs
    return _CACHED_PACKS


def load_slang_catalog() -> List[Dict[str, Any]]:
    """
    Load the 88 Trini slang stickers from data/trini-slang.js.
    Cached in memory.
    """
    global _CACHED_SLANG
    if _CACHED_SLANG is not None:
        return _CACHED_SLANG

    slang_path = get_workspace_path("data", "trini-slang.js")
    if not os.path.exists(slang_path):
        raise FileNotFoundError(f"Missing slang catalog: {slang_path}")

    with open(slang_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"window\.STICKERBOOM_TRINI_SLANG\s*=\s*(\[[\s\S]*?\]);\s*$", content)
    if match:
        _CACHED_SLANG = json.loads(match.group(1))
        return _CACHED_SLANG

    # Fallback via Node.js
    try:
        cmd = [
            "node",
            "-e",
            """
            global.window = {};
            require('./data/trini-slang.js');
            console.log(JSON.stringify(window.STICKERBOOM_TRINI_SLANG));
            """
        ]
        res = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            _CACHED_SLANG = json.loads(res.stdout)
            return _CACHED_SLANG
    except Exception:
        pass

    raise RuntimeError(f"Unable to parse {slang_path}")


def load_all_catalog_ids() -> List[str]:
    """Return sorted list of all 188 unique sticker IDs across packs and slang catalogs."""
    packs = load_packs_catalog()
    slang = load_slang_catalog()

    ids = set()
    for p in packs:
        for s in p.get("stickers", []):
            if "id" in s:
                ids.add(s["id"])
    for s in slang:
        if "id" in s:
            ids.add(s["id"])
    return sorted(list(ids))


def load_whatsapp_manifest() -> Dict[str, Any]:
    """Parse and return assets/contents.json."""
    manifest_path = get_workspace_path("assets", "contents.json")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# BINARY CHUNK PARSERS (OPAQUE INSPECTION WITHOUT GENERATOR COUPLING)
# =============================================================================

def parse_webp_binary(file_path: str) -> Dict[str, Any]:
    """
    Opaque binary inspection of an animated WebP file.
    Directly extracts VP8X dimensions, flags, ANIM loop count,
    and the 3-byte duration from each ANMF chunk (bypassing Pillow's None quirk).
    """
    if not os.path.exists(file_path):
        return {"error": "File does not exist", "exists": False}

    size = os.path.getsize(file_path)
    if size == 0:
        return {"error": "File is empty (0 bytes)", "exists": True, "size": 0}

    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return {"error": "Invalid RIFF/WEBP header", "valid_riff": False, "size": size}

    pos = 12
    width = None
    height = None
    has_animation = False
    has_alpha = False
    loop_count = None
    durations: List[int] = []

    while pos < len(data) - 8:
        fourcc = data[pos : pos + 4]
        chunk_size = int.from_bytes(data[pos + 4 : pos + 8], "little")
        chunk_data = data[pos + 8 : pos + 8 + chunk_size]

        if fourcc == b"VP8X" and len(chunk_data) >= 10:
            flags = chunk_data[0]
            has_animation = bool(flags & 0x02)
            has_alpha = bool(flags & 0x10)
            width = int.from_bytes(chunk_data[4:7], "little") + 1
            height = int.from_bytes(chunk_data[7:10], "little") + 1

        elif fourcc == b"ANIM" and len(chunk_data) >= 6:
            loop_count = int.from_bytes(chunk_data[4:6], "little")

        elif fourcc == b"ANMF" and len(chunk_data) >= 16:
            # Duration in ms is a 24-bit uint at offset 12 in ANMF payload
            dur = int.from_bytes(chunk_data[12:15], "little")
            durations.append(dur)

        # Chunks are padded to even number of bytes
        pos += 8 + chunk_size + (chunk_size % 2)

    return {
        "exists": True,
        "size": size,
        "valid_riff": True,
        "width": width,
        "height": height,
        "has_animation": has_animation,
        "has_alpha": has_alpha,
        "loop_count": loop_count,
        "frame_count": len(durations),
        "durations": durations,
        "total_duration_ms": sum(durations),
    }


def parse_gif_binary(file_path: str) -> Dict[str, Any]:
    """
    Opaque binary inspection of an animated GIF file.
    Extracts GIF89a header, logical screen dimensions, Netscape loop count,
    GCE frame delays (converted to ms), and color table size.
    """
    if not os.path.exists(file_path):
        return {"error": "File does not exist", "exists": False}

    size = os.path.getsize(file_path)
    if size == 0:
        return {"error": "File is empty (0 bytes)", "exists": True, "size": 0}

    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) < 13 or data[:6] not in (b"GIF89a", b"GIF87a"):
        return {"error": "Invalid GIF header", "valid_gif": False, "size": size}

    header = data[:6].decode("ascii", errors="replace")
    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")
    packed = data[10]
    has_gct = bool(packed & 0x80)
    gct_size = 3 * (2 ** ((packed & 0x07) + 1)) if has_gct else 0
    palette_colors = (2 ** ((packed & 0x07) + 1)) if has_gct else 0

    pos = 13 + gct_size
    durations: List[int] = []
    loop_count = None

    while pos < len(data):
        b = data[pos]
        if b == 0x3B:  # Trailer
            break
        elif b == 0x21:  # Extension block
            if pos + 2 > len(data):
                break
            ext_type = data[pos + 1]
            pos += 2
            if ext_type == 0xF9:  # Graphic Control Extension
                if pos < len(data):
                    block_size = data[pos]
                    if block_size >= 4 and pos + 4 <= len(data):
                        # Delay time is in hundredths of a second (centiseconds)
                        delay_cs = int.from_bytes(data[pos + 2 : pos + 4], "little")
                        durations.append(delay_cs * 10)  # ms
                    pos += block_size + 1
                    while pos < len(data) and data[pos] != 0:
                        pos += data[pos] + 1
                    pos += 1
            elif ext_type == 0xFF:  # Application Extension
                if pos < len(data):
                    block_size = data[pos]
                    app_id = data[pos + 1 : pos + 1 + block_size]
                    pos += block_size + 1
                    if b"NETSCAPE" in app_id and pos < len(data):
                        sub_size = data[pos]
                        if sub_size == 3 and pos + 4 <= len(data) and data[pos + 1] == 1:
                            loop_count = int.from_bytes(data[pos + 2 : pos + 4], "little")
                    while pos < len(data) and data[pos] != 0:
                        pos += data[pos] + 1
                    pos += 1
            else:
                while pos < len(data) and data[pos] != 0:
                    pos += data[pos] + 1
                pos += 1
        elif b == 0x2C:  # Image Descriptor
            if pos + 10 > len(data):
                break
            packed_img = data[pos + 9]
            has_lct = bool(packed_img & 0x80)
            lct_size = 3 * (2 ** ((packed_img & 0x07) + 1)) if has_lct else 0
            pos += 10 + lct_size + 1  # header + local table + LZW min code size
            while pos < len(data) and data[pos] != 0:
                pos += data[pos] + 1
            pos += 1
        else:
            pos += 1

    return {
        "exists": True,
        "size": size,
        "valid_gif": True,
        "header": header,
        "width": width,
        "height": height,
        "palette_colors": palette_colors,
        "loop_count": loop_count,
        "frame_count": len(durations),
        "durations": durations,
        "total_duration_ms": sum(durations),
    }


# =============================================================================
# PIL SAFE OPERATIONS & IMAGE QUALITY CHECKS
# =============================================================================

def safe_open_image(file_path: str) -> Tuple[Optional[Image.Image], Optional[str]]:
    """
    Safely open an image with Pillow after verifying existence and non-zero size.
    Returns in-memory (Image copy, None) on success or (None, error_str) on defect.
    Closes the underlying file descriptor to prevent ResourceWarnings.
    """
    if not os.path.exists(file_path):
        return None, f"File does not exist: {file_path}"
    size = os.path.getsize(file_path)
    if size == 0:
        return None, f"File is empty (0 bytes): {file_path}"
    try:
        with Image.open(file_path) as im:
            im.load()
            return im.copy(), None
    except Exception as exc:
        return None, f"Failed to decode image {file_path}: {exc}"


def calculate_frame_difference(img_a: Image.Image, img_b: Image.Image) -> float:
    """
    Compute the root-mean-square (RMS) pixel difference between two images.
    Returns float >= 0.0. 0.0 indicates bitwise identical frames.
    """
    a = img_a.convert("RGBA")
    b = img_b.convert("RGBA")
    diff = ImageChops.difference(a, b)
    stat = ImageStat.Stat(diff)
    rms = sum(stat.rms) / len(stat.rms)
    return rms


def check_card_background_rgb(
    gif_path: str,
    expected_rgb: Tuple[int, int, int] = (16, 20, 30),
    tolerance: int = 5
) -> Tuple[bool, Tuple[int, int, int]]:
    """
    Inspect the top-left corner (0, 0) of the first frame of a studio card GIF.
    Asserts color matches #10141E within tolerance.
    """
    im, err = safe_open_image(gif_path)
    if err or im is None:
        return False, (0, 0, 0)
    rgb_im = im.convert("RGB")
    pixel = rgb_im.getpixel((0, 0))
    match = all(abs(p - e) <= tolerance for p, e in zip(pixel, expected_rgb))
    return match, pixel


def check_webp_corner_alpha(webp_path: str, corner: Tuple[int, int] = (0, 0)) -> Tuple[bool, int]:
    """Inspect corner pixel of a transparent animated WebP to verify alpha == 0."""
    im, err = safe_open_image(webp_path)
    if err or im is None:
        return False, 255
    rgba = im.convert("RGBA")
    pixel = rgba.getpixel(corner)
    alpha = pixel[3] if len(pixel) == 4 else 255
    return alpha == 0, alpha


# =============================================================================
# SUBPROCESS EXECUTION UTILITIES
# =============================================================================

def run_command(cmd: List[str], timeout: int = 60, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """Execute a CLI command subprocess and return (returncode, stdout, stderr)."""
    work_dir = cwd or WORKSPACE_DIR
    try:
        proc = subprocess.run(
            cmd,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout}s: {' '.join(cmd)}"
    except Exception as exc:
        return -2, "", str(exc)


# =============================================================================
# PROGRESSIVE TESTABILITY GATING
# =============================================================================

def require_milestone(milestone_tag: str, condition: bool, message: str, strict: Optional[bool] = None):
    """
    Enforce progressive milestone gating.
    If condition is False:
      - In default progressive mode: raises unittest.SkipTest with milestone context.
      - In strict mode (--strict): raises AssertionError failing the release gate.
      - If strict parameter is explicitly passed, it overrides the global mode.
    """
    if not condition:
        effective_strict = is_strict_mode() if strict is None else strict
        if effective_strict:
            raise AssertionError(f"[{milestone_tag} STRICT GATE FAILED] {message}")
        else:
            raise unittest.SkipTest(f"[{milestone_tag}] {message}")
