"""Aperçus des projets : captures brutes (previews-src/raw) → site/img/<projet>.webp

    python tools/make-previews.py

Tout passe en niveaux de gris, au même format 16:10 (1600 × 1000), fond transparent :
c'est la page qui pose le fond, clair ou sombre selon le thème. Les écrans de téléphone
sont posés trois par trois ; les widgets sont recadrés sur leur contenu.
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "previews-src" / "raw"
OUT = ROOT / "site" / "img"
W, H = 1600, 1000


def gray(im: Image.Image) -> Image.Image:
    """Niveaux de gris, contraste légèrement relevé, transparence conservée."""
    im = im.convert("RGBA")
    alpha = im.getchannel("A")
    g = ImageOps.autocontrast(im.convert("L"), cutoff=0.5)
    out = Image.merge("LA", (g, alpha))
    return out


def canvas() -> Image.Image:
    return Image.new("LA", (W, H), (0, 0))


def fit(im: Image.Image, max_w: int, max_h: int) -> Image.Image:
    im = im.copy()
    im.thumbnail((max_w, max_h), Image.LANCZOS)
    return im


def scale_to_height(im: Image.Image, h: int) -> Image.Image:
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def framed(im: Image.Image, border: int = 2) -> Image.Image:
    """Fin cadre gris autour d'un écran (sinon un écran clair se perd sur un fond clair)."""
    out = Image.new("LA", (im.width + 2 * border, im.height + 2 * border), (128, 255))
    out.paste(im, (border, border))
    return out


def phones(names: list, crop_top: int = 0) -> Image.Image:
    shots = [Image.open(RAW / n) for n in names]
    if crop_top:
        shots = [s.crop((0, crop_top, s.width, s.height)) for s in shots]
    h = 880
    screens = [framed(gray(scale_to_height(s, h - 4))) for s in shots]
    gap = 56
    total = sum(s.width for s in screens) + gap * (len(screens) - 1)
    c = canvas()
    x = (W - total) // 2
    for s in screens:
        c.paste(s, (x, (H - s.height) // 2))
        x += s.width + gap
    return c


def content_box(im: Image.Image, margin: int = 60):
    """Rectangle du contenu sur un fond uni (couleur du coin)."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((5, 5)))
    diff = ImageOps.grayscale(ImageChops.difference(rgb, bg)).point(lambda v: 255 if v > 12 else 0)
    l, t, r, b = diff.getbbox() or (0, 0, im.width, im.height)
    return max(0, l - margin), max(0, t - margin), min(im.width, r + margin), min(im.height, b + margin)


def widget(name: str) -> Image.Image:
    im = Image.open(RAW / name)
    im = im.crop(content_box(im))
    c = canvas()
    s = framed(gray(fit(im, W - 200, H - 120)))
    c.paste(s, ((W - s.width) // 2, (H - s.height) // 2))
    return c


def full(name: str) -> Image.Image:
    im = Image.open(RAW / name).convert("RGB")
    return gray(ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, 0.0)))


def row(names: list, h: int) -> Image.Image:
    shots = [framed(gray(scale_to_height(Image.open(RAW / n), h))) for n in names]
    gap = 40
    total = sum(s.width for s in shots) + gap * (len(shots) - 1)
    if total > W - 80:
        k = (W - 80) / total
        shots = [s.resize((round(s.width * k), round(s.height * k)), Image.LANCZOS) for s in shots]
        total = sum(s.width for s in shots) + gap * (len(shots) - 1)
    c = canvas()
    x = (W - total) // 2
    for s in shots:
        c.paste(s, (x, (H - s.height) // 2), s)  # la transparence du rendu 3D sert de masque
        x += s.width + gap
    return c


def window(name: str, zoom: float = 2.0) -> Image.Image:
    im = Image.open(RAW / name)
    im = im.resize((round(im.width * zoom), round(im.height * zoom)), Image.LANCZOS)
    c = canvas()
    s = framed(gray(fit(im, W - 160, H - 120)))
    c.paste(s, ((W - s.width) // 2, (H - s.height) // 2))
    return c


PREVIEWS = {
    # Recto : tools/capture-steps.mjs avec les listes de démonstration de tools/recto-capture/.
    "recto": lambda: phones(["recto-s1.png", "recto-s2.png", "recto-s3.png"]),
    "rivano": lambda: phones(["rivano-1.png", "rivano-s1.png", "rivano-s2.png"]),
    "pdf-to-markdown": lambda: window("pdf-to-markdown.png"),
    "nova-strike": lambda: full("nova-strike.png"),
    "bookedo": lambda: phones(["bookedo-1.png", "bookedo-2.png", "bookedo-3.png"]),
    "crypto-widget": lambda: widget("crypto-widget.png"),
    # Captures du dépôt faites dans Chrome : on retire la barre du navigateur (88 px).
    "neodex": lambda: phones(["neodex-home.png", "neodex-info1.png", "neodex-random1.png"], crop_top=88),
    # Captures du dépôt avec un modèle chargé (la première montre l'écran vide).
    "3d-viewer": lambda: row(["3dview-widget2.png", "3dview-widget3.png"], 560),
    "countdown-widget": lambda: widget("countdown-widget.png"),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, make in PREVIEWS.items():
        im = make().convert("RGBA")
        path = OUT / f"{name}.webp"
        im.save(path, "WEBP", quality=82, method=6)
        print(f"{path.name:24} {round(path.stat().st_size / 1024)} Ko")


if __name__ == "__main__":
    main()
