"""One Vixl poster with every font set in itself."""
import sys
from pathlib import Path
from PIL import ImageFont
from vixl import Project
from vixl.fonts import import_font
from fontspecs import SPECS

root = Path(sys.argv[1])
order = ["gilded-italic", "pearl-line", "velvet-didone", "scribble-hand", "ballpoint-note", "noodle-wobble",
         "ransom-tiles", "drippy-goo", "rune-cut", "neon-tube", "puffy-bubble", "pixel-pop", "led-matrix", "chisel-marker"]
kind = {"gilded-italic": "elegant", "pearl-line": "elegant", "velvet-didone": "elegant", "scribble-hand": "handwritten",
        "ballpoint-note": "handwritten", "noodle-wobble": "weird", "ransom-tiles": "weird", "drippy-goo": "weird",
        "rune-cut": "weird", "neon-tube": "stylized", "puffy-bubble": "stylized", "pixel-pop": "stylized",
        "led-matrix": "stylized", "chisel-marker": "stylized"}
by = {s["slug"]: s for s in SPECS}
CW, CH, M = 900, 330, 0
p = Project(2 * CW, 7 * CH + 150, background="#111111")
ops = []
for slug in order:
    path = next((root / "fonts").glob(by[slug]["family"].replace(" ", "") + ".otf"))
    import_font(p, str(path), slug)
for i, slug in enumerate(order):
    s = by[slug]
    bg, ink, accent = s["colors"]
    col, row = i % 2, i // 2
    x, y = col * CW, row * CH
    ttf = root / "fonts" / (s["family"].replace(" ", "") + ".ttf")
    title = s["family"]
    w = ImageFont.truetype(str(ttf), 100).getlength(title)
    size = min(150, 100 * 740 / w)
    ops.append({"type": "shape", "shape": "rectangle", "name": f"bg-{slug}", "x": x, "y": y, "width": CW, "height": CH, "fill": bg})
    ops.append({"type": "text", "name": f"name-{slug}", "text": title, "font": slug, "size": round(size), "color": accent if slug not in ("ransom-tiles",) else accent,
                "x": x + 70, "baseline_y": y + 195})
    ops.append({"type": "text", "name": f"kind-{slug}", "text": kind[slug].upper(), "size": 18, "color": ink, "opacity": .6,
                "tracking": 4, "x": x + 70, "y": y + CH - 52})
ops.append({"type": "text", "name": "footer", "text": "14 FONTS DRAWN WITH VIXL  ·  EVERY GLYPH IS ORDINARY LAYERS  ·  OTF + TTF",
            "size": 26, "color": "#f2f2f2", "tracking": 5, "x": "center", "y": 7 * CH + 55})
res = p.apply(ops)
for w in res.get("warnings", []) or []:
    print("warn", w)
out = root / "poster.png"
p.render().convert("RGB").save(out)
p.save(str(root / "vixl-sources" / "poster.vixl"), overwrite=True)
print(out)
