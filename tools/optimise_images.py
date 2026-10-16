"""Build web-ready images from the design originals in /design.

Run once after changing a source image:  python tools/optimise_images.py
Requires Pillow >= 11 with WebP support. Outputs are committed, so
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


def hero_mark():
    # Framing is kept untouched: the hero reveal's clip geometry is based on it.
    # WebP only: lossy AVIF adds faint alpha noise across the transparent area,
    # which shows as a dark box on the navy hero. WebP keeps it clean.
    src = Image.open(SRC / "logo-mark-3d-transparent.png").convert("RGBA")
    for w in (640, 720, 960, 1380):
        h = round(src.height * w / src.width)
        img = src.resize((w, h), Image.LANCZOS)
        img.putalpha(img.getchannel("A").point(lambda v: 0 if v < 16 else v))
        img.save(OUT / f"hero-mark-{w}.webp", quality=80, method=6, alpha_quality=100)


def small_3d_mark():
    # Header/footer logo (replaces the earlier flat line-drawing marks): the metal 3D mark, cropped to the wires (no empty
    # margin) and sized 2x for a 32px-tall display. Lossy WebP with clean alpha,
    # as for the hero.
    src = Image.open(SRC / "logo-mark-3d-transparent.png").convert("RGBA")
    src = src.crop(src.getchannel("A").getbbox())
    h = 64
    w = round(src.width * h / src.height)
    img = src.resize((w, h), Image.LANCZOS)
    img.putalpha(img.getchannel("A").point(lambda v: 0 if v < 16 else v))
    img.save(OUT / "mark-3d.webp", quality=88, method=6, alpha_quality=100)
    print(f"mark-3d.webp is {w}x{h} (display at {w // 2}x{h // 2})")


def story_poster():
    # Still of the hero's first 3D frame (rendered by tools/story-poster.mjs).
    # Shown until three.js loads, and kept when WebGL 2 is unavailable.
    src_path = ROOT / "tools" / ".out" / "story-poster.png"
    if not src_path.exists():
        print("story-poster: no render found, skipped (run: npm run poster:3d)")
        return
    img = Image.open(src_path).convert("RGBA").resize((760, 760), Image.LANCZOS)
    img.putalpha(img.getchannel("A").point(lambda v: 0 if v < 16 else v))
    img.save(OUT / "story-poster.webp", quality=76, method=6, alpha_quality=100)


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
    small_3d_mark()
    story_poster()
    icons()
    for p in sorted(OUT.iterdir()):
        print(f"{p.stat().st_size / 1024:7.1f} KB  {p.name}")
