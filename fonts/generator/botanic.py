"""Plant-inspired styles on the shared centre-line alphabet. Each returns [("poly", geometry)] in design units."""
import math

from shapely import affinity
from shapely.geometry import LineString, MultiPoint, Point, Polygon, box
from shapely.ops import nearest_points, unary_union

import skeleton as sk
from styles import (bbox, dist, field, is_closed, ink_distance, length, lower_map, resample, rng_for, skeleton, warp)


def unit(v):
    d = math.hypot(*v) or 1.0
    return (v[0] / d, v[1] / d)


def tangent_at(pts, i):
    a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
    return unit((b[0] - a[0], b[1] - a[1]))


def leaf(cx, cy, ang, ln, wd, steps=14):
    """A pointed leaf whose base sits on (cx, cy) and whose tip lies `ln` away along `ang` degrees."""
    top = [(ln * t / steps, wd / 2 * math.sin(math.pi * (t / steps) ** .75) ** .9) for t in range(steps + 1)]
    pts = top + [(x, -y) for x, y in reversed(top[1:-1])]
    return affinity.rotate(affinity.translate(Polygon(pts), cx, cy), ang, origin=(cx, cy))


def tendril(end, d, r0, turns, side, width):
    """A curl that leaves `end` along unit direction d and spirals inward."""
    n = (-d[1] * side, d[0] * side)
    cx, cy = end[0] + n[0] * r0, end[1] + n[1] * r0
    phi0 = math.atan2(-n[1], -n[0])
    pts = []
    for i in range(41):
        u = i / 40
        rad = r0 * (1 - .8 * u)
        a = phi0 + side * turns * 2 * math.pi * u
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return LineString(pts).buffer(width / 2, 8)


def line_geom(strokes, dots, w=1.0):
    return [LineString(resample(s, 10)) for s in strokes if len(s) > 1] + [Point(d).buffer(.01) for d in dots]


def free_ends(strokes):
    out = []
    for i, s in enumerate(strokes):
        if len(s) < 4 or is_closed(s):
            continue
        others = [o for j, o in enumerate(strokes) if j != i]
        pts = resample(s, 10)
        for end, back in ((pts[0], pts[min(3, len(pts) - 1)]), (pts[-1], pts[max(-4, -len(pts))])):
            if ink_distance(end, others) > 24:
                out.append((end, unit((end[0] - back[0], end[1] - back[1]))))
    return out


def taper_chain(pts, radii, quad=8):
    circles = [Point(p).buffer(r, quad) for p, r in zip(pts, radii)]
    return [MultiPoint([]).union(a.union(b).convex_hull) for a, b in zip(circles, circles[1:])]


# ---------------------------------------------------------------- vines and ferns


def ivy(ch, salt, width=27, leaf_len=150, leaf_w=74, curl=.8):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    parts = []
    for s in strokes:
        pts = resample(s, 12)
        parts.append(LineString(pts).buffer(width / 2, 12))
        n = 1 + int(length(pts) // 330)
        for k in range(n):
            i = int((k + r.uniform(.25, .75)) / n * (len(pts) - 1))
            t = tangent_at(pts, i)
            ang = math.degrees(math.atan2(t[1], t[0])) + r.choice([-1, 1]) * r.uniform(38, 58)
            parts.append(leaf(pts[i][0], pts[i][1], ang, leaf_len * r.uniform(.78, 1.08), leaf_w))
    for end, d in free_ends(strokes):
        if r.random() < curl:
            parts.append(tendril(end, d, r.uniform(42, 66), r.uniform(1.3, 1.8), r.choice([-1, 1]), 12))
    for d in dots:
        parts.append(Point(d).buffer(30, 16))
        parts.append(leaf(d[0], d[1], r.uniform(30, 150), 90, 44))
    return [("poly", unary_union(parts))]


def fern(ch, salt, stem=24, step=92, leaflet=92, width=40, spread=52):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    parts = []
    for s in strokes:
        pts = resample(s, 8)
        parts.append(LineString(pts).buffer(stem / 2, 10))
        total = length(pts)
        n = max(2, int(total / step))
        line = LineString(pts)
        for k in range(n + 1):
            u = k / n
            p = line.interpolate(total * u)
            i = min(len(pts) - 1, int(u * (len(pts) - 1)))
            t = tangent_at(pts, i)
            ang = math.degrees(math.atan2(t[1], t[0]))
            ln = leaflet * (1 - .45 * u) * r.uniform(.9, 1.08)
            if k < n:
                parts.append(leaf(p.x, p.y, ang + spread, ln, width))
                parts.append(leaf(p.x, p.y, ang - spread, ln, width))
            else:
                parts.append(leaf(p.x, p.y, ang, leaflet * .75, width * .9))
    for d in dots:
        for a in range(0, 360, 72):
            parts.append(leaf(d[0], d[1], a + 20, 56, 26))
    return [("poly", unary_union(parts))]


# ---------------------------------------------------------------- flowers and seeds


def flower(c, R, rot, petals=7):
    parts = [leaf(c[0], c[1], rot + k * 360 / petals, R, R * .78, 7) for k in range(petals)]
    return unary_union(parts).difference(Point(c).buffer(R * .2, 12))


def daisy(ch, salt, R=72, gap=112):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    parts = []
    for s in strokes:
        pts = resample(s, 8)
        total = length(pts)
        n = max(1, int(total / gap + .5))
        line = LineString(pts)
        for k in range(n + 1):
            p = line.interpolate(total * k / n)
            parts.append(flower((p.x, p.y), R * r.uniform(.92, 1.08), r.uniform(0, 60)))
    for d in dots:
        parts.append(flower(d, R * 1.15, r.uniform(0, 60)))
    return [("poly", unary_union(parts))]


def seeds(ch, salt, step=80, ln=104, wd=60):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    parts = []
    for s in strokes:
        pts = resample(s, 8)
        total = length(pts)
        n = max(1, int(total / step + .5))
        line = LineString(pts)
        for k in range(n + 1):
            u = k / n
            p = line.interpolate(total * u)
            i = min(len(pts) - 1, int(u * (len(pts) - 1)))
            t = tangent_at(pts, i)
            ang = math.degrees(math.atan2(t[1], t[0])) + r.uniform(-12, 12)
            half = ln / 2
            parts.append(leaf(p.x - math.cos(math.radians(ang)) * half, p.y - math.sin(math.radians(ang)) * half, ang,
                              ln * r.uniform(.9, 1.1), wd * r.uniform(.9, 1.12)))
    for d in dots:
        parts.append(leaf(d[0] - 40, d[1], 0, 80, 46))
    return [("poly", unary_union(parts))]


# ---------------------------------------------------------------- moss, cactus, twig


def body_of(strokes, dots, width):
    return unary_union([l.buffer(width / 2, 24) for l in line_geom(strokes, dots)])


def rings(geom):
    polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    out = []
    for p in polys:
        out.append(p.exterior)
        out += list(p.interiors)
    return out


def moss(ch, salt, width=92, lo=9, hi=28, step=12):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    body = body_of([resample(s, 12) for s in strokes], dots, width)
    bumps = []
    for ring in rings(body):
        n = max(8, int(ring.length / step))
        for i in range(n):
            p = ring.interpolate(ring.length * i / n)
            bumps.append(Point(p.x + r.uniform(-4, 4), p.y + r.uniform(-4, 4)).buffer(r.uniform(lo, hi), 3))
    return [("poly", unary_union([body] + bumps))]


def cactus(ch, salt, width=112, gap=70, spine=58):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    core = unary_union(line_geom([resample(s, 12) for s in strokes], dots))
    body = body_of([resample(s, 12) for s in strokes], dots, width)
    parts = [body]
    for ring in rings(body)[:1] if body.geom_type == "Polygon" else [rg for rg in rings(body) if rg.is_ccw or True][:0]:
        pass
    exteriors = [p.exterior for p in (list(body.geoms) if hasattr(body, "geoms") else [body])]
    for ring in exteriors:
        n = max(4, int(ring.length / gap))
        for i in range(n):
            q = ring.interpolate(ring.length * (i + r.uniform(-.2, .2)) / n)
            c = nearest_points(core, q)[0]
            v = unit((q.x - c.x, q.y - c.y))
            tip = (q.x + v[0] * spine * r.uniform(.8, 1.2), q.y + v[1] * spine * r.uniform(.8, 1.2))
            if body.buffer(6).contains(Point(tip)):
                continue
            perp = (-v[1], v[0])
            base = (q.x - v[0] * 12, q.y - v[1] * 12)
            parts.append(Polygon([(base[0] + perp[0] * 11, base[1] + perp[1] * 11),
                                  (base[0] - perp[0] * 11, base[1] - perp[1] * 11), tip]))
    return [("poly", unary_union(parts))]


def twig(ch, salt, r0=35, r1=11):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    f = field(r, 11, 300)
    parts = []
    for s in strokes:
        pts = resample(s, 10)
        closed = is_closed(s)
        if not closed and pts[0][1] > pts[-1][1] + 1:
            pts = pts[::-1]
        pts = [(p[0] + f(p)[0], p[1] + f(p)[1]) for p in pts]
        m = len(pts)
        if closed:
            radii = [(r0 + r1) / 2 * (1 + .25 * math.cos(4 * math.pi * i / (m - 1) + math.pi)) for i in range(m)]
        else:
            radii = [r1 + (r0 - r1) * max(0.0, 1 - i / (m - 1)) ** .8 for i in range(m)]
        parts += taper_chain(pts, radii)
        total = length(pts)
        for k in range(int(total // 250) + (0 if closed else 1)):
            i = int(r.uniform(.2, .75) * (m - 1))
            t = tangent_at(pts, i)
            side = r.choice([-1, 1])
            a = math.atan2(t[1], t[0]) + side * math.radians(r.uniform(35, 55))
            ln = r.uniform(80, 130)
            tw = [(pts[i][0] + math.cos(a + .25 * side * j / 6) * ln * j / 6,
                   pts[i][1] + math.sin(a + .25 * side * j / 6) * ln * j / 6) for j in range(7)]
            parts += taper_chain(tw, [radii[i] * .45 * (1 - j / 8) + 3 for j in range(7)])
            parts.append(leaf(tw[-1][0], tw[-1][1], math.degrees(a), 56, 28))
        tip = pts[-1]
        parts.append(leaf(tip[0], tip[1], math.degrees(math.atan2(*reversed(tangent_at(pts, m - 1)))), 60, 30))
    for d in dots:
        parts.append(Point(d).buffer(24, 12))
        parts.append(leaf(d[0], d[1], 50, 62, 30))
    return [("poly", unary_union(parts))]


# ---------------------------------------------------------------- art nouveau willow


def willow(ch, salt, rmax=32, rmin=5, curl=.55, xs=.86, slant=6):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    if ch.islower():
        strokes, dots = warp(strokes, dots, lower_map(470, 765, 260))
    sl = math.tan(math.radians(slant))
    strokes, dots = warp(strokes, dots, lambda p: (p[0] * xs + p[1] * sl, p[1]))
    parts = []
    for s in strokes:
        pts = resample(s, 9)
        m = len(pts)
        if is_closed(s):
            radii = [rmin + (rmax - rmin) * (.5 + .5 * math.cos(4 * math.pi * i / (m - 1) + math.pi)) for i in range(m)]
        else:
            radii = [rmin + (rmax - rmin) * max(0.0, math.sin(math.pi * i / (m - 1))) ** .8 for i in range(m)]
        parts += taper_chain(pts, radii)
    for end, d in free_ends(strokes):
        if r.random() < curl:
            parts.append(tendril(end, d, r.uniform(26, 40), r.uniform(1.2, 1.6), r.choice([-1, 1]), 10))
    for d in dots:
        parts.append(leaf(d[0] - 38, d[1] - 10, 20, 90, 52))
    return [("poly", unary_union(parts))]


# ---------------------------------------------------------------- garden stamp tiles


def garden(ch, salt, width=64, scale=.8, rot=3.5):
    r = rng_for(ch, salt)
    strokes, dots = skeleton(ch)
    x0, y0, x1, y1 = bbox(strokes, dots)
    ix = (x0 + x1) / 2
    kind = (ord(ch) * 3 + ord(ch) // 5) % 5
    sc = scale * (.66 if kind in (1, 2) else 1)
    s = sc if (x1 - x0) * sc < 560 else 560 / (x1 - x0)
    strokes, dots = warp([resample(t, 10) for t in strokes], dots, lambda p: ((p[0] - ix) * s, p[1] * s + (95 if kind in (1, 2) else 40)))
    ink = unary_union([l.buffer(width, 24) for l in line_geom(strokes, dots)])
    W, y0t, y1t = 880, -250, 790
    cy = (y0t + y1t) / 2
    H = y1t - y0t
    if kind == 0:  # blossom
        rx, ry = W * .29, H * .28
        petals = [Point(rx * math.cos(a * math.pi / 4), cy + ry * math.sin(a * math.pi / 4)).buffer(W * .2, 24) for a in range(8)]
        tile = unary_union(petals + [affinity.scale(Point(0, cy).buffer(1, 48), rx * 1.1, ry * 1.1)])
    elif kind in (1, 2):  # pointed leaf, leaning either way
        ls = [(W * .4 * math.sin(math.pi * t / 28) ** .85, cy - H * .5 + H * t / 28) for t in range(29)]
        tile = Polygon(ls + [(-x, y) for x, y in reversed(ls[1:-1])])
        tile = affinity.rotate(tile, 28 if kind == 1 else -28, origin=(0, cy))
    elif kind == 3:  # seed / egg
        tile = affinity.scale(Point(0, cy).buffer(1, 64), W / 2 * .96, H / 2 * .96)
    else:  # scalloped doily
        tile = unary_union([Point(math.cos(a * math.pi / 8) * W * .36, cy + math.sin(a * math.pi / 8) * H * .36).buffer(W * .13, 20)
                            for a in range(16)] + [affinity.scale(Point(0, cy).buffer(1, 48), W * .42, H * .42)])
    glyph = tile.difference(ink)
    return [("poly", affinity.rotate(glyph, r.gauss(0, rot), origin=(0, cy)))]
