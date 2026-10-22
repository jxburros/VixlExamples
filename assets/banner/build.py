"""The banner at the top of the repository README, made with Vixl from this repository's own outputs.

Run from the repo root:

    python assets/banner/build.py

Writes assets/banner/banner.vixl (the editable master) and banner.png. Every tile is a cropped `frame` clipped to
a rounded base, so swapping one picture is a one-line change to its path in TILES. The builder refuses to
overwrite an existing master unless you pass --overwrite.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
os.environ.setdefault("VIXL_NO_UPDATE", "1")
os.chdir(ROOT)  # image paths resolve against the workspace (the repo root)

from vixl import Project  # noqa: E402
from vixl.typefaces import install_font  # noqa: E402

W, H = 1600, 700
DEEP, PANEL, BLUE, SKY, WHITE, MUTED = "#1A1F2B", "#2F3647", "#3575EE", "#6A9AFF", "#FFFFFF", "#AEB7CA"
HEAD, BODY, MONO = "inter-tight-800", "inter-400", "jetbrains-mono-500"

GAP = 10
X0, Y0 = 600, 30  # the tile area is 1000 x 640, to the right of the text column
# (column width, [(tile height, picture)])
COLUMNS = [
    (220, [(380, "explorations/01-print-concert-poster/output/poster-rgb.png"),
           (250, "explorations/04-pixel-rpg/output/map@3x.png")]),
    (300, [(200, "explorations/05-generative-painting/output/painting.jpg"),
           (200, "explorations/02-brand-identity/output/board/brand-board.png"),
           (220, "promo/assets/germ-king.png")]),
    (220, [(330, "art/rain-girl.png"),
           (300, "explorations/07-trading-cards/output/set/holo/0004.webp")]),
    (230, [(330, "art/heyoka-mirrors-paradox/items/07-heyoka-study-01.png"),
           (300, "explorations/10-character-film/output/film-shot2.png")]),
]


def tiles():
    ops, n, x = [], 0, X0
    for width, column in COLUMNS:
        y = Y0
        for height, path in column:
            n += 1
            name = f"tile-{n:02d}"
            ops += [
                {"type": "shape", "shape": "rounded-rectangle", "name": f"{name}-base", "x": x, "y": y,
                 "width": width, "height": height, "radius": 14, "fill": PANEL},
                {"type": "frame", "name": name, "path": path, "x": x, "y": y, "width": width, "height": height,
                 "fit": "fill", "downsample": "placed@2x"},
                {"type": "clip", "target": name, "base": f"{name}-base"},
            ]
            y += height + GAP
        x += width + GAP
    return ops


def build(out):
    p = Project(W, H, DEEP)
    p._workspace = str(ROOT)
    install_font(p, "Inter Tight", 800, role="heading")
    install_font(p, "Inter", 400, role="body")
    install_font(p, "JetBrains Mono", 500)
    ops = [
        {"type": "gradient", "name": "glow", "direction": "radial", "width": 1100, "height": 1100, "x": -380,
         "y": -300, "stops": [{"offset": 0, "color": f"{BLUE}55"}, {"offset": 0.6, "color": f"{BLUE}10"},
                              {"offset": 1, "color": f"{BLUE}00"}]},
        {"type": "text", "name": "eyebrow", "text": "VIXLEXAMPLES", "font": MONO, "size": 22, "color": SKY,
         "x": 60, "y": 150},
        {"type": "text", "name": "headline-1", "text": "Made with Vixl.", "font": HEAD, "size": 66,
         "color": WHITE, "x": 56, "y": 205},
        {"type": "text", "name": "headline-2", "text": "All of it.", "font": HEAD, "size": 66,
         "color": SKY, "x": 56, "y": 272},
        {"type": "rich-text", "name": "sub", "spans": [{"text": "Posters, films, a pixel RPG, a 3,700-stroke "
                                                       "painting, a card set from a spreadsheet. Every piece "
                                                       "ships with its layered, editable master."}],
         "font": BODY, "size": 26, "color": MUTED, "line_height": 1.35, "x": 60, "y": 400, "width": 480},
        {"type": "text", "name": "footer", "text": "github.com/jxburros/Vixl", "font": MONO, "size": 20,
         "color": MUTED, "x": 60, "y": 610},
    ] + tiles()
    p.apply(ops, detail="brief")
    p.save(out / "banner.vixl", overwrite=True)
    p.render().save(out / "banner.png")


if __name__ == "__main__":
    if (HERE / "banner.vixl").exists() and "--overwrite" not in sys.argv:
        sys.exit("banner.vixl exists; pass --overwrite to rebuild it")
    build(HERE)
