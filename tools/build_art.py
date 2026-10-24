"""Compile the checked-in imagegen sources into legacy DDS game textures.

Requires Pillow >= 11.3. No network or image generation is performed by this tool.
"""
from pathlib import Path
import struct

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art" / "source"
OUTPUT = ROOT / "gfx" / "interface" / "vvv"


def save_dds(image, path, pixel_format):
    image.save(path, pixel_format=pixel_format)
    # DDS_HEADER.dwPitchOrLinearSize is the top-level surface byte count for
    # compressed textures. Normalize it rather than relying on Pillow's pitch.
    # https://learn.microsoft.com/windows/win32/direct3ddds/dds-header
    data = bytearray(path.read_bytes())
    block_size = 8 if pixel_format == "DXT1" else 16
    size = ((image.width + 3) // 4) * ((image.height + 3) // 4) * block_size
    struct.pack_into("<I", data, 20, size)
    path.write_bytes(data)


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    field = Image.open(SOURCE / "plains.png").convert("RGB")
    field = field.resize((1536, 768), Image.Resampling.LANCZOS)
    save_dds(field, OUTPUT / "plains.dds", "DXT1")
    atlas = Image.open(SOURCE / "formations.png").convert("RGBA")
    # Equal-sized production cells align every blank number plaque at (128, 80).
    # The source intentionally has no baked-in counts or text.
    for row, team in enumerate(("red", "blue")):
        for col, troop in enumerate(("archers", "levies", "light_infantry")):
            center = (268, 768, 1265)[col]
            top = (48, 528)[row]
            cell = atlas.crop((center - 256, top, center + 256, top + 448))
            cell = cell.resize((256, 224), Image.Resampling.LANCZOS)
            save_dds(cell, OUTPUT / f"{team}_{troop}.dds", "DXT5")
    print("Built plains.dds (DXT1) and six alpha-enabled formation textures (DXT5).")


if __name__ == "__main__":
    build()
