"""Build web-ready images from the design originals in /design.

Run once after changing a source image:  python tools/optimise_images.py
Requires Pillow >= 11.3 (built-in AVIF support). Outputs are committed, so
nothing here runs at deploy time.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "v3" / "assets"
OUT = ROOT / "assets" / "img"

NAVY = (26, 46, 74)       # #1A2E4A
GOLD = (201, 151, 43)     # #C9972B
WHITE = (255, 255, 255)


def tint(img, rgb):
    """Recolour a single-colour transparent mark, keeping its alpha."""
    alpha = img.convert("RGBA").getchannel("A")
    solid = Image.new("RGBA", img.size, rgb + (255,))
    solid.putalpha(alpha)
    return solid


def save_modern(img, stem, avif_q=55, webp_q=80):
    img.save(OUT / f"{stem}.avif", quality=avif_q, speed=4)
    img.save(OUT / f"{stem}.webp", quality=webp_q, method=6)


def hero_mark():
    # Framing is kept untouched: the hero reveal's clip geometry is based on it.
    src = Image.open(SRC / "logo-mark-3d-transparent.png").convert("RGBA")
    for w in (640, 960, 1380):
        h = round(src.height * w / src.width)
        save_modern(src.resize((w, h), Image.LANCZOS), f"hero-mark-{w}")


def flat_marks():
    src = Image.open(SRC / "logo-mark-blue-transparent.png").convert("RGBA")
    h = 96  # 2x for a 48px-tall header mark
    w = round(src.width * h / src.height)
    for name, rgb in (("mark-navy", NAVY), ("mark-white", WHITE)):
        tint(src, rgb).resize((w, h), Image.LANCZOS).save(OUT / f"{name}.webp", lossless=True, method=6)


def icons():
    # The spiral alone reads at favicon sizes; the full mark does not.
    src = Image.open(SRC / "logo-mark-blue-transparent.png").convert("RGBA")
    spiral = tint(src.crop((333, 0, src.width, src.height)), GOLD)
    spiral = spiral.crop(spiral.getchannel("A").getbbox())

    def tile(size, pad=0.18, radius=0.22):
        # Thin strokes vanish at favicon sizes, so thicken them before scaling down.
        grow = 7 if size <= 48 else 3
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), round(size * radius), fill=255)
        bg = Image.new("RGBA", (size, size), NAVY + (255,))
        canvas.paste(bg, mask=mask)
        inner = round(size * (1 - 2 * pad))
        s = Image.new("RGBA", spiral.size, GOLD + (255,))
        s.putalpha(spiral.getchannel("A").filter(ImageFilter.MaxFilter(grow)))
        s.thumbnail((inner, inner), Image.LANCZOS)
        canvas.alpha_composite(s, ((size - s.width) // 2, (size - s.height) // 2))
        return canvas

    tile(32).save(OUT / "favicon-32.png", optimize=True)
    tile(180, radius=0).convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)
    tile(192).save(OUT / "icon-192.png", optimize=True)
    tile(512).save(OUT / "icon-512.png", optimize=True)
    tile(48).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hero_mark()
    flat_marks()
    icons()
    for p in sorted(OUT.iterdir()):
        print(f"{p.stat().st_size / 1024:7.1f} KB  {p.name}")
