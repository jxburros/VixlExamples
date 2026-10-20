"""One Vixl poster with every botanical font set in itself."""
import sys
from pathlib import Path
from PIL import ImageFont
from vixl import Project
from vixl.fonts import import_font
from fontspecs_botanical import SPECS

root = Path(sys.argv[1])
order = ["ivy-tendril", "willow-wisp", "fern-frond", "bare-branch", "daisy-chain", "garden-stamp", "moss-rug", "seed-pod", "cactus-spine"]
kind = {"ivy-tendril": "climbing", "willow-wisp": "art nouveau", "fern-frond": "woodland", "bare-branch": "winter",
        "daisy-chain": "meadow", "garden-stamp": "stamps", "moss-rug": "forest floor", "seed-pod": "seed tray", "cactus-spine": "desert"}
by = {s["slug"]: s for s in SPECS}
CW, CH = 900, 330
rows = (len(order) + 1) // 2
p = Project(2 * CW, rows * CH + 150, background="#111111")
ops = []
for slug in order:
    import_font(p, str(root / "fonts" / (by[slug]["family"].replace(" ", "") + ".otf")), slug)
for i, slug in enumerate(order):
    s = by[slug]
    bg, ink, accent = s["colors"]
    col, row = i % 2, i // 2
    x, y = col * CW, row * CH
    w = ImageFont.truetype(str(root / "fonts" / (s["family"].replace(" ", "") + ".ttf")), 100).getlength(s["family"])
    size = min(150, 100 * 740 / w)
    ops.append({"type": "shape", "shape": "rectangle", "name": f"bg-{slug}", "x": x, "y": y, "width": CW, "height": CH, "fill": bg})
    ops.append({"type": "text", "name": f"name-{slug}", "text": s["family"], "font": slug, "size": round(size), "color": accent if slug != "seed-pod" else ink,
                "x": x + 70, "baseline_y": y + 195})
    ops.append({"type": "text", "name": f"kind-{slug}", "text": kind[slug].upper(), "size": 18, "color": ink, "opacity": .65,
                "tracking": 4, "x": x + 70, "y": y + CH - 52})
if len(order) % 2:  # fill the last half-row
    x, y = CW, (rows - 1) * CH
    ops.append({"type": "shape", "shape": "rectangle", "name": "bg-fill", "x": x, "y": y, "width": CW, "height": CH, "fill": "#1f3324"})
    ops.append({"type": "text", "name": "fill-text", "text": "9 botanical fonts", "size": 54, "color": "#cfe8b8", "x": x + 70, "y": y + 120})
ops.append({"type": "text", "name": "footer", "text": "BOTANICAL FONTS DRAWN WITH VIXL  ·  EVERY GLYPH IS ORDINARY LAYERS  ·  OTF + TTF",
            "size": 26, "color": "#f2f2f2", "tracking": 5, "x": "center", "y": rows * CH + 55})
res = p.apply(ops)
out = root / "poster.png"
p.render().convert("RGB").save(out)
p.save(str(root / "vixl-sources" / "poster.vixl"), overwrite=True)
print(out)
