"""Build every font with Vixl: draw glyph layers, font-design / font-glyph / font-build, export, then a specimen."""
import json
import sys
from pathlib import Path

from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry.polygon import orient

import skeleton as sk
import styles as st
from vixl import Project
from vixl.fonts import import_font

OUT = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "out")
OUT.mkdir(parents=True, exist_ok=True)

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = UPPER.lower()
DIGITS = "0123456789"
PUNCT = ".,!?:;-'\"()/&@+=*#$%"
CHARS = UPPER + LOWER + DIGITS + PUNCT

KERN = {"AV": -50, "AW": -40, "AY": -50, "AT": -50, "VA": -50, "WA": -40, "YA": -50, "TA": -50, "LT": -70, "LV": -60,
        "LY": -60, "LW": -40, "PA": -60, "FA": -50, "To": -60, "Ta": -60, "Te": -60, "Tr": -30, "Ty": -50, "Tu": -30,
        "Yo": -50, "Ve": -30, "Vo": -30, "Wa": -30, "Wo": -30, "r.": -40, "r,": -40, "y.": -50, "y,": -50, "ov": -10,
        "vo": -10, "fo": -25, "fe": -25, "fa": -25, "fl": -15, "fi": -15, "ff": -20, "we": -15, "wo": -15, "ye": -20, "yo": -20}


def items_bounds(items):
    xs0, ys0, xs1, ys1 = [], [], [], []
    for it in items:
        if it[0] == "stroke":
            b = LineString(it[1]).buffer(it[2] / 2).bounds
        else:
            b = it[1].bounds
        xs0.append(b[0]); ys0.append(b[1]); xs1.append(b[2]); ys1.append(b[3])
    return min(xs0), min(ys0), max(xs1), max(ys1)


def ring_d(coords, fx, fy):
    pts = list(coords)[:-1]
    return "M" + " L".join(f"{fx(x):.1f} {fy(y):.1f}" for x, y in pts) + " Z"


def geom_d(geom, fx, fy, tol):
    if geom.is_empty:
        return ""
    polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    out = []
    for poly in polys:
        if not isinstance(poly, Polygon) or poly.is_empty:
            continue
        poly = orient(poly.simplify(tol, preserve_topology=True), 1.0)
        out.append(ring_d(poly.exterior.coords, fx, fy))
        out += [ring_d(r.coords, fx, fy) for r in poly.interiors]
    return " ".join(out)


def build(spec):
    slug, family = spec["slug"], spec["family"]
    EM = spec.get("em", 250)
    k = EM / 1000.0
    sbm = spec.get("sb", {"round": 45, "straight": 70, "diag": 25, "mark": 55})
    track = spec.get("track", 0)
    asc, desc = spec.get("ascent", 800), spec.get("descent", 250)

    glyphs = {}
    for ch in CHARS:
        items = spec["style"](ch, slug)
        x0, y0, x1, y1 = items_bounds(items)
        cls = sk.classes(ch.upper() if spec.get("caps_only") and ch.isalpha() else ch)
        sb = sbm[cls] if isinstance(sbm, dict) else sbm
        glyphs[ch] = dict(items=items, x0=x0, x1=x1, sb=sb, adv=(x1 - x0) + 2 * sb + track)

    pad = 24
    cellw = int(max(g["adv"] for g in glyphs.values()) * k + 2 * pad)
    cellh = int((asc + desc) * k + 2 * pad)
    cols = 10
    rows = (len(CHARS) + cols - 1) // cols
    W, Hh = cols * cellw, rows * cellh
    p = Project(W, Hh, background="#ffffff")

    kern = {pair: round(v * k * spec.get("kern", 1.0), 1) for pair, v in KERN.items() if spec.get("kern", 1.0)}
    ops = [{"type": "font-design", "family": family, "style": "Regular", "em": EM, "ascent": asc * k, "descent": desc * k,
            "x_height": spec.get("x_height", 500) * k, "cap_height": spec.get("cap_height", 700) * k,
            "space": spec.get("space", 280) * k, "weight": spec.get("weight", 400),
            "italic_angle": spec.get("italic_angle", 0), "designer": "Vixl", "version": "1.000",
            "description": spec["blurb"], "kerning": kern,
            "license": "Created with Vixl; free to use."}]
    for n, ch in enumerate(CHARS):
        g = glyphs[ch]
        cx, cy = (n % cols) * cellw, (n // cols) * cellh
        base = cy + pad + asc * k
        left = cx + pad  # origin x; the ink sits one side bearing in
        fx = lambda x, g=g, left=left: left + (x - g["x0"] + g["sb"]) * k
        fy = lambda y, base=base: base - y * k
        names = []
        for i, it in enumerate(g["items"]):
            name = f"{slug}-{ord(ch):04x}-{i}"
            if it[0] == "stroke":
                d = "M" + " L".join(f"{fx(x):.1f} {fy(y):.1f}" for x, y in it[1])
                ops.append({"type": "shape", "shape": "path", "name": name, "path": d, "fill": "none",
                            "stroke": "#000000", "stroke_width": round(it[2] * k, 2), "line_cap": it[3],
                            "line_join": "round"})
            else:
                d = geom_d(it[1], fx, fy, spec.get('tol', .5))
                if not d:
                    continue
                ops.append({"type": "shape", "shape": "path", "name": name, "path": d, "fill": "#000000"})
            names.append(name)
        ops.append({"type": "font-glyph", "char": ch, "targets": names, "origin": [left, base],
                    "advance": round(g["adv"] * k, 2)})
    ops.append({"type": "font-build", "name": slug})
    res = p.apply(ops)
    for w in res.get("warnings", []) or []:
        print("   warn:", w)
    sheet = OUT / f"{slug}-glyphs.png"
    p.render().convert("RGB").save(sheet)
    path = OUT / f"{family.replace(' ', '')}.otf"
    if path.exists():
        path.unlink()
    rep = {}
    p.export(str(path), report=rep)
    ttf = path.with_suffix(".ttf")
    if ttf.exists():
        ttf.unlink()
    p.export(str(ttf))
    p.save(str(OUT / f"{slug}.vixl"), overwrite=True)
    print(f"{family}: {rep.get('glyphs')} glyphs, {rep.get('bytes')} bytes", rep.get("warnings") or "")
    return path


def specimen(spec, path):
    slug, family = spec["slug"], spec["family"]
    bg, ink, accent = spec["colors"]
    p = Project(1600, 1000, background=bg)
    import_font(p, str(path), slug)
    big = spec.get("title_size", 190)
    ops = []

    def text(t, x, y, size, color=ink, **kw):
        ops.append({"type": "text", "text": t, "x": x, "baseline_y": y, "size": size, "color": color, "font": slug,
                    "name": f"t{len(ops)}", **kw})

    text(spec.get("title", family), 80, 70 + big * .82, big, accent)
    ops.append({"type": "shape", "shape": "rectangle", "name": "rule", "x": 80, "y": 70 + big + 30, "width": 1440,
                "height": 3, "fill": ink, "opacity": .35})
    y = 70 + big + 110
    for line in spec.get("lines", ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ", "abcdefghijklm", "nopqrstuvwxyz", "0123456789 .,!?&@#$%"]):
        text(line, 80, y, spec.get("size", 84), ink)
        y += spec.get("lead", 108)
    text(spec.get("pangram", "Sphinx of black quartz, judge my vow!"), 80, 1000 - 70, spec.get("psize", 70), accent)
    p.apply(ops)
    out = OUT / f"{slug}-specimen.png"
    p.render().convert("RGB").save(out)
    p.save(str(OUT / f"{slug}-specimen.vixl"), overwrite=True)
    return out


if __name__ == "__main__":
    import importlib, os
    SPECS = importlib.import_module(os.environ.get('FONTSET', 'fontspecs')).SPECS
    only = [a for a in sys.argv[1:] if not a.startswith("-") and a != str(OUT)] if len(sys.argv) > 2 else []
    for spec in SPECS:
        if only and spec["slug"] not in only:
            continue
        pth = build(spec)
        specimen(spec, pth)
