"""Turn a logo on a flat light background into small, transparent web assets.

Usage: python tools/make_logo_assets.py "<source image>" <out_dir>
Writes (all transparent, palette-compressed):
  applyhit-icon.png       96px wide  - on-page logo (shown at up to 44px, so 2x for sharp screens)
  apple-touch-icon.png    180x180    - iOS home-screen icon
  favicon-32.png / favicon-64.png    - browser tab icons

The source logo lives outside the project: ~/Downloads/Actual Logo.jpeg
Needs Pillow (pip install pillow).
"""
import sys
from pathlib import Path
from PIL import Image

LOW, HIGH = 12, 60  # distance from background: <=LOW fully clear, >=HIGH fully opaque


def remove_background(img):
    img = img.convert("RGB")
    w, h = img.size
    corners = [img.getpixel(p) for p in [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    out = Image.new("RGBA", img.size)
    src, dst = img.load(), out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            d = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            a = 0.0 if d <= LOW else 1.0 if d >= HIGH else (d - LOW) / (HIGH - LOW)
            if a == 0:
                dst[x, y] = (0, 0, 0, 0)
                continue
            # Un-blend the background so edges don't keep a light halo
            px = [min(255, max(0, round((c - k * (1 - a)) / a))) for c, k in zip((r, g, b), bg)]
            dst[x, y] = (*px, round(a * 255))
    return out


def save_small(img, path):
    # 256-colour palette with alpha keeps logos crisp at a fraction of the size
    img.quantize(colors=256, method=Image.Quantize.FASTOCTREE).save(path, optimize=True)


def square(logo, pad=1.08):
    side = round(max(logo.size) * pad)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2), logo)
    return sq


def main(src, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    logo = remove_background(Image.open(src))
    logo = logo.crop(logo.getbbox())

    w = 96
    save_small(logo.resize((w, round(logo.height * w / logo.width)), Image.LANCZOS), out_dir / "applyhit-icon.png")

    # iOS draws touch icons on black, so give it a white tile
    touch = Image.new("RGBA", (180, 180), (255, 255, 255, 255))
    inner = square(logo, 1.25).resize((180, 180), Image.LANCZOS)
    touch.paste(inner, (0, 0), inner)
    save_small(touch, out_dir / "apple-touch-icon.png")

    sq = square(logo)
    for size in (32, 64):
        save_small(sq.resize((size, size), Image.LANCZOS), out_dir / f"favicon-{size}.png")

    for p in sorted(out_dir.iterdir()):
        print(f"{p.name:24} {p.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
