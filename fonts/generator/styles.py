"""Ways to turn the shared centre lines into glyph outlines. Each style returns a list of items:
("stroke", pts, width, cap)  an open path Vixl strokes itself
("poly", shapely geometry)   a filled outline (holes allowed)
Units are font design units (1000 per em, y up)."""
import math
import random
import zlib

import numpy as np
from shapely import affinity
from shapely.geometry import LineString, MultiPoint, Point, Polygon, box
from shapely.ops import unary_union

import skeleton as sk


def rng_for(ch, salt):
    return random.Random(zlib.crc32(f"{salt}:{ch}".encode()))


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def length(pts):
    return sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def resample(pts, step):
    if len(pts) < 2:
        return list(pts)
    total = length(pts)
    n = max(2, int(total / step) + 1)
    line = LineString(pts)
    return [tuple(line.interpolate(total * i / (n - 1)).coords[0]) for i in range(n)]


def is_closed(pts):
    return len(pts) > 20 and dist(pts[0], pts[-1]) < 3


def skeleton(ch):
    g = sk.G[ch]
    return [list(s) for s in g["strokes"]], list(g["dots"])


def warp(strokes, dots, f):
    return [[f(p) for p in s] for s in strokes], [f(p) for p in dots]


def bbox(strokes, dots):
    xs = [p[0] for s in strokes for p in s] + [p[0] for p in dots]
    ys = [p[1] for s in strokes for p in s] + [p[1] for p in dots]
    return min(xs), min(ys), max(xs), max(ys)


def field(rng, amp, wl):
    p = [rng.uniform(0, 6.283) for _ in range(4)]
    k = 6.283 / wl

    def f(pt):
        x, y = pt
        return (amp * math.sin(k * (x * .9 + y * .4) + p[0]) + amp * .5 * math.sin(k * 1.7 * (y - x * .3) + p[1]),
                amp * math.sin(k * (y * .8 - x * .5) + p[2]) + amp * .5 * math.sin(k * 1.9 * (x + y * .2) + p[3]))
    return f


def lower_map(xh, asc, desc):
    """Vertical map for lowercase: new x-height, ascender/cap line and descender depth."""
    def f(p):
        x, y = p
        if y < 0:
            return (x, y * desc / 200.0)
        if y <= 500:
            return (x, y * xh / 500.0)
        return (x, xh + (y - 500) * (asc - xh) / 230.0)
    return f


def ink_distance(pt, others):
    return min((LineString(o).distance(Point(pt)) for o in others), default=1e9)


def stroke_items(strokes, dots, width, cap="round", dot_r=None):
    items = [("stroke", s, width, cap) for s in strokes if len(s) > 1]
    for d in dots:
        items.append(("poly", Point(d).buffer(dot_r or width * .55, 24)))
    return items


# ---------------------------------------------------------------- handwriting


def hand(ch, salt, width, jit, slant, rot, narrow=1.0, step=22, lift=0.0, bounce=14, xh_scale=1.0, overshoot=1.0):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    if ch.islower() and xh_scale != 1.0:
        strokes, dots = warp(strokes, dots, lower_map(500 * xh_scale, 730 + 20 * (xh_scale - 1) * 5, 200))
    x0, y0, x1, y1 = bbox(strokes, dots)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    theta = math.radians(r.gauss(0, rot))
    sx = r.uniform(.93, 1.07) * narrow
    dy = r.gauss(0, bounce) + lift
    f = field(r, jit, 300)
    ct, st = math.cos(theta), math.sin(theta)

    def place(p, t=0.0, spiral=(cx, cy, 0)):
        x, y = p
        scx, scy, amt = spiral
        if amt:
            k = 1 + amt * (t - .5)
            x, y = scx + (x - scx) * k, scy + (y - scy) * k
        x, y = (x - cx) * sx, y - cy
        x, y = x * ct - y * st, x * st + y * ct
        x, y = x + cx, y + cy
        wx, wy = f((x, y))
        x, y = x + wx, y + wy + dy
        return (x + (y - cy) * slant, y)

    out_s = []
    for s in strokes:
        pts = resample(s, step)
        if is_closed(s):
            sx0, sy0, sx1, sy1 = bbox([s], [])
            c = ((sx0 + sx1) / 2, (sy0 + sy1) / 2)
            n = len(pts)
            pts = pts + pts[1:int(n * .13 * overshoot) + 1]
            m = len(pts)
            pts = [place(p, i / (m - 1), (c[0], c[1], .09)) for i, p in enumerate(pts)]
        else:
            if length(pts) > 60 and overshoot:
                ext = r.uniform(4, 16) * overshoot
                a, b = pts[0], pts[1]
                d = dist(a, b) or 1
                pts.insert(0, (a[0] + (a[0] - b[0]) / d * ext, a[1] + (a[1] - b[1]) / d * ext))
                a, b = pts[-1], pts[-2]
                d = dist(a, b) or 1
                pts.append((a[0] + (a[0] - b[0]) / d * ext, a[1] + (a[1] - b[1]) / d * ext))
            pts = [place(p) for p in pts]
        out_s.append(pts)
    out_d = [place(d) for d in dots]
    return stroke_items(out_s, out_d, width, dot_r=width * .62)


# ---------------------------------------------------------------- broad nib


def nib(ch, salt, width, angle, slant, xscale, hair, lower=None, round_off=4, jit=0.0, wob=0.0, serif=0):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    if ch.islower() and lower:
        strokes, dots = warp(strokes, dots, lower_map(*lower))
    f = field(r, jit, 340) if jit else None
    sl = math.tan(math.radians(slant))

    def move(p):
        x, y = p
        x *= xscale
        if f:
            dx, dy = f((x, y))
            x, y = x + dx, y + dy
        return (x + y * sl, y)

    strokes, dots = warp(strokes, dots, move)
    if serif:
        extra = []
        for i, t in enumerate(strokes):
            if len(t) < 4 or is_closed(t):
                continue
            others = [o for j, o in enumerate(strokes) if j != i]
            for end, nxt in ((t[0], t[min(6, len(t) - 1)]), (t[-1], t[max(-7, -len(t))])):
                d = (nxt[0] - end[0], nxt[1] - end[1])
                span = math.hypot(*d) or 1
                if abs(d[1]) / span > .88 and ink_distance(end, others) > 25:
                    extra.append([(end[0] - serif, end[1]), (end[0] + serif, end[1])])
        strokes = strokes + extra
    nv = (math.cos(math.radians(angle)) * width / 2, math.sin(math.radians(angle)) * width / 2)
    pieces = []
    for s in strokes:
        pts = resample(s, 14)
        for a, b in zip(pts, pts[1:]):
            pieces.append(MultiPoint([(a[0] + nv[0], a[1] + nv[1]), (a[0] - nv[0], a[1] - nv[1]),
                                      (b[0] + nv[0], b[1] + nv[1]), (b[0] - nv[0], b[1] - nv[1])]).convex_hull)
    for d in dots:
        perp = (math.cos(math.radians(angle + 90)) * 20, math.sin(math.radians(angle + 90)) * 20)
        a, b = (d[0] - perp[0], d[1] - perp[1]), (d[0] + perp[0], d[1] + perp[1])
        pieces.append(MultiPoint([(a[0] + nv[0], a[1] + nv[1]), (a[0] - nv[0], a[1] - nv[1]),
                                  (b[0] + nv[0], b[1] + nv[1]), (b[0] - nv[0], b[1] - nv[1])]).convex_hull)
    geom = unary_union([p.buffer(hair / 2, 8) for p in pieces if not p.is_empty])
    if round_off:
        geom = geom.buffer(round_off, 8).buffer(-round_off, 8)
    return [("poly", geom)]


# ---------------------------------------------------------------- pearl line (elegant all caps)


def pearl(ch, salt, width=15, ball=26):
    base = ch.upper() if ch.isalpha() else ch
    small = ch.isalpha() and ch.islower()
    strokes, dots = skeleton(base)
    if small:
        strokes, dots = warp(strokes, dots, lambda p: (p[0] * .8, p[1] * .8))
    items = stroke_items(strokes, dots, width, dot_r=ball)
    for i, s in enumerate(strokes):
        if len(s) < 2 or is_closed(s):
            continue
        others = [o for j, o in enumerate(strokes) if j != i]
        for end in (s[0], s[-1]):
            if ink_distance(end, others) > 20:
                items.append(("poly", Point(end).buffer(ball * (.8 if small else 1), 24)))
    return items


# ---------------------------------------------------------------- bubbles, neon, noodles


def bubble(ch, salt, width=140, bounce=22, rot=4):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    x0, y0, x1, y1 = bbox(strokes, dots)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    th = math.radians(r.gauss(0, rot))
    dy = r.gauss(0, bounce)
    ct, st = math.cos(th), math.sin(th)

    def mv(p):
        x, y = p[0] - cx, p[1] - cy
        return (x * ct - y * st + cx, x * st + y * ct + cy + dy)

    if ch in "ij":
        dots = [(d[0], d[1] + 45) for d in dots]
    strokes, dots = warp([resample(s, 14) for s in strokes], dots, mv)
    return stroke_items(strokes, dots, width, dot_r=width * .6)


def neon(ch, salt, outer=64, inner=20):
    strokes, dots = skeleton(ch)
    lines = [LineString(resample(s, 8)) for s in strokes if len(s) > 1]
    lines += [Point(d).buffer(.01) for d in dots]
    shell = unary_union([l.buffer(outer, 24) for l in lines])
    core = unary_union([l.buffer(inner, 24) for l in lines])
    return [("poly", shell.difference(core))]


def noodle(ch, salt, base=34, swing=.5, amp=34, wl=300):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    f = field(r, amp, wl)
    phase = r.uniform(0, 6.283)
    pieces = []
    for s in strokes:
        pts = resample(s, 10)
        pts = [(p[0] + f(p)[0], p[1] + f(p)[1]) for p in pts]
        total = length(pts) or 1
        acc = 0
        circles = []
        for i, p in enumerate(pts):
            if i:
                acc += dist(p, pts[i - 1])
            rad = base * (1 + swing * math.sin(acc / 80 + phase))
            circles.append(Point(p).buffer(rad, 12))
        for a, b in zip(circles, circles[1:]):
            pieces.append(unary_union([a, b]).convex_hull)
    for d in dots:
        pieces.append(Point(d[0] + f(d)[0], d[1] + f(d)[1]).buffer(base * 1.5, 16))
    return [("poly", unary_union(pieces))]


# ---------------------------------------------------------------- ransom tiles


TILE_W, TILE_BOTTOM, TILE_TOP = 860, -250, 790


def tiles(ch, salt, width=70, scale=.82, rot=4):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    x0, y0, x1, y1 = bbox(strokes, dots)
    ix = (x0 + x1) / 2
    s = scale if (x1 - x0) * scale < 700 else 700 / (x1 - x0)
    strokes, dots = warp([resample(t, 10) for t in strokes], dots, lambda p: ((p[0] - ix) * s, p[1] * s + 40))
    lines = [LineString(t) for t in strokes if len(t) > 1] + [Point(d).buffer(.01) for d in dots]
    ink = unary_union([l.buffer(width, 24) for l in lines])
    kind = (ord(ch) * 7 + 3) % 6
    W, y0t, y1t = TILE_W, TILE_BOTTOM, TILE_TOP
    cy = (y0t + y1t) / 2
    if kind in (0, 1):
        tile = box(-W / 2, y0t, W / 2, y1t).buffer(-90).buffer(90, 16)
    elif kind == 2:
        tile = affinity.scale(Point(0, cy).buffer(1, 48), W / 2, (y1t - y0t) / 2)
    elif kind == 3:
        h = (y1t - y0t) / 2
        tile = Polygon([(-W / 2 + 160, cy + h), (W / 2 - 160, cy + h), (W / 2, cy + h - 160), (W / 2, cy - h + 160),
                        (W / 2 - 160, cy - h), (-W / 2 + 160, cy - h), (-W / 2, cy - h + 160), (-W / 2, cy + h - 160)])
    elif kind == 4:
        tile = box(-W / 2, y0t, W / 2, y1t)
        for sx in (-1, 1):
            for sy in (y0t, y1t):
                tile = tile.difference(Point(sx * W / 2, sy).buffer(95, 24))
    else:
        h = (y1t - y0t) / 2
        tile = Polygon([(-W / 2, cy - h + 60), (0, cy - h), (W / 2, cy - h + 60), (W / 2, cy + h - 60), (0, cy + h),
                        (-W / 2, cy + h - 60)]).buffer(30, 8)
    glyph = tile.difference(ink)
    glyph = affinity.rotate(glyph, r.gauss(0, rot), origin=(0, cy))
    return [("poly", glyph)]


# ---------------------------------------------------------------- pixels and LEDs

PIX_Y = [(-200, -200), (0, 0), (250, 200), (350, 300), (500, 400), (700, 600), (740, 640)]


PIX_ROWS = {
    "a": [".###.", "....#", ".####", "#...#", ".####"],
    "e": [".###.", "#...#", "#####", "#....", ".####"],
    "s": [".####", "#....", ".###.", "....#", "####."],
    "w": ["#...#", "#...#", "#.#.#", "##.##", "#...#"],
    "x": ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".####"],
    "&": [".##..", "#..#.", "#..#.", ".##..", "#.#.#", "#..#.", ".##.#"],
    "%": ["##...#", "##..#.", "...#..", "..#...", ".#..##", "#...##"],
}


def pixel_cells(ch, c=100, thr=.28, stroke=88):
    if ch in PIX_ROWS:
        rows = PIX_ROWS[ch]
        return [(i, len(rows) - 1 - r) for r, line in enumerate(rows) for i, v in enumerate(line) if v == "#"]
    strokes, dots = skeleton(ch)
    dots = [(x, 700 if y > 600 else y) for x, y in dots]
    ys = [k[0] for k in PIX_Y]
    ds = [k[1] for k in PIX_Y]
    strokes, dots = warp(strokes, dots, lambda p: (p[0], float(np.interp(p[1], ys, ds))))
    x0, y0, x1, y1 = bbox(strokes, dots)
    wid = max(c, round((x1 - x0) / c) * c)
    sx = wid / max(1.0, (x1 - x0))
    strokes, dots = warp(strokes, dots, lambda p: ((p[0] - x0) * sx, p[1]))
    lines = [LineString(resample(s, 8)) for s in strokes if len(s) > 1] + [Point(d) for d in dots]
    ink = unary_union([l.buffer(stroke / 2, 16) for l in lines])
    minx, miny, maxx, maxy = ink.bounds
    cells = []
    for i in range(int(math.floor(minx / c)) - 1, int(math.ceil(maxx / c)) + 2):
        for j in range(int(math.floor(miny / c)) - 1, int(math.ceil(maxy / c)) + 2):
            cell = box(i * c - c / 2, j * c - c / 2, i * c + c / 2, j * c + c / 2)
            if ink.intersection(cell).area / cell.area >= thr:
                cells.append((i, j))
    return cells


def pixels(ch, salt, c=100, gap=0, thr=.28, stroke=88, round_dots=0):
    cells = pixel_cells(ch, c, thr, stroke)
    if round_dots:
        return [("poly", unary_union([Point(i * c, j * c).buffer(c * round_dots, 16) for i, j in cells]))]
    h = c / 2 - gap / 2
    return [("poly", unary_union([box(i * c - h, j * c - h, i * c + h, j * c + h) for i, j in cells]))]


# ---------------------------------------------------------------- angular rune cut, drips


def runecut(ch, salt, width=46, tol=70, jit=10):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    pieces = []
    for t in strokes:
        pts = list(LineString(resample(t, 10)).simplify(tol).coords)
        if is_closed(t):
            pts = [(x + r.uniform(-jit, jit), y + r.uniform(-jit, jit)) for x, y in pts[:-1]]
            pts.append(pts[0])
        else:
            pts = [(x + r.uniform(-jit, jit), y + r.uniform(-jit, jit)) for x, y in pts]
        pieces.append(LineString(pts).buffer(width / 2, cap_style="flat", join_style="mitre", mitre_limit=4))
    for d in dots:
        q = width * .75
        pieces.append(Polygon([(d[0], d[1] + q), (d[0] + q, d[1]), (d[0], d[1] - q), (d[0] - q, d[1])]))
    return [("poly", unary_union(pieces))]


def drippy(ch, salt, width=100):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    lines = [LineString(resample(t, 12)) for t in strokes if len(t) > 1] + [Point(d).buffer(.01) for d in dots]
    body = unary_union([l.buffer(width / 2, 24) for l in lines])
    minx, miny, maxx, maxy = body.bounds
    parts = [body]
    count = 1 + int((maxx - minx) // 430)
    for x in sorted(r.uniform(minx + width * .45, maxx - width * .45) for _ in range(count)):
        hit = LineString([(x, miny - 50), (x, maxy + 50)]).intersection(body)
        if hit.is_empty:
            continue
        y = hit.bounds[1]
        run = r.uniform(90, 300)
        rad = r.uniform(19, 27)
        parts.append(LineString([(x, y + 30), (x, y - run)]).buffer(rad, 12))
        parts.append(Point(x, y - run).buffer(rad * 1.75, 16))
    return [("poly", unary_union(parts))]
