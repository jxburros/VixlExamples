"""A looping construction-paper unicorn that gallops and jumps a fence.

Run from the root of this repository with Vixl installed:

    python showcases/paper-unicorn/build.py [OUTPUT_DIR]

Writes the .vixl master, a preview PNG, a looping GIF and an MP4. The unicorn stays in place while
four paper strips (far hills, near hills with trees, the path and the front grass) scroll past at
different speeds. Every strip moves a whole number of its own repeats per loop, so the loop has no
seam, and the fence on the path comes round exactly once.
"""
import math
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from vixl.project import Project
from vixl.timeline import export_timeline, render_at

W, H = 960, 540
LOOP = 3000                     # ms
STRIDE = 500                    # one gallop stride, ms (6 strides per loop)
JUMP = (1000, 2000)             # the jump replaces strides 3 and 4
STEP = 1000 / 24                # key spacing; cut-paper holds them at 12 fps
GROUND_TILE = 1200              # the path moves one tile per loop, so the fence passes once

CREAM, CREAM_SHADE, CREAM_LIGHT = '#fbf4e8', '#e6d6c3', '#ffffff'
HOOF, HOOF_FAR = '#b49ad8', '#8f78bb'
RAINBOW = ['#f2789f', '#f79d5c', '#f7d35e', '#7cc8a4', '#6fb1e0', '#a585d6']

ops = []
pieces = []                     # paper pieces big enough to show the paper texture


def add(*items):
    for op in items:
        if op['type'] in ('shape', 'pen') and op.get('fill') and 'name' in op:
            if 'points' in op:
                xs, ys = zip(*op['points'])
                area = (max(xs) - min(xs)) * (max(ys) - min(ys))
            else:
                area = op['width'] * op['height']
            if area >= 900:
                pieces.append(op['name'])
    ops.extend(items)


def paper_tile(path, size=256, seed=7):
    """A seamless construction-paper tile: soft mottling, short fibres and flecks on a transparent ground,
    so one tile textures every colour of paper."""
    rng = np.random.default_rng(seed)

    def soft_noise(sigma):  # filtered in the frequency domain, so it wraps at the tile edges
        f = np.fft.fftfreq(size)
        g = np.exp(-(f[:, None] ** 2 + f[None, :] ** 2) * (2 * np.pi * sigma) ** 2 / 2)
        out = np.real(np.fft.ifft2(np.fft.fft2(rng.normal(size=(size, size))) * g))
        return out / np.abs(out).max()

    mottle = 0.6 * soft_noise(10) + 0.4 * soft_noise(3) + 0.12 * rng.normal(size=(size, size))
    marks = Image.new('RGBA', (size * 3, size * 3))
    draw = ImageDraw.Draw(marks)
    shifts = [(ox, oy) for ox in (0, size, 2 * size) for oy in (0, size, 2 * size)]
    for _ in range(260):
        x, y = rng.uniform(0, size, 2)
        a, length, bend = rng.uniform(0, math.pi), rng.uniform(6, 22), rng.normal(0, 0.25)
        pts = [(x + length * t * math.cos(a + bend * t), y + length * t * math.sin(a + bend * t)) for t in np.linspace(0, 1, 6)]
        color = (255, 255, 255, int(rng.uniform(40, 110))) if rng.random() < .7 else (60, 40, 30, int(rng.uniform(25, 60)))
        for ox, oy in shifts:
            draw.line([(px + ox, py + oy) for px, py in pts], fill=color, width=1)
    for _ in range(90):
        (x, y), r = rng.uniform(0, size, 2), rng.uniform(.5, 1.4)
        color = (50, 35, 25, int(rng.uniform(40, 90))) if rng.random() < .6 else (255, 255, 255, 120)
        for ox, oy in shifts:
            draw.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=color)
    tile = Image.new('RGBA', (size, size))
    for color, alpha in (((0, 0, 0), np.clip(-mottle, 0, None)), ((255, 255, 255), np.clip(mottle, 0, None))):
        layer = np.zeros((size, size, 4), np.uint8)
        layer[..., :3], layer[..., 3] = color, (alpha * (0.35 if color[0] == 0 else 0.6) * 255).astype(np.uint8)
        tile.alpha_composite(Image.fromarray(layer, 'RGBA'))
    tile.alpha_composite(marks.crop((size, size, 2 * size, 2 * size)))
    tile.save(path)


def blob(name, points, fill, corners=None, tension=1):
    op = {'type': 'pen', 'name': name, 'points': [[round(x, 1), round(y, 1)] for x, y in points],
          'closed': True, 'fill': fill, 'tension': tension}
    if corners:
        op['corners'] = corners
    add(op)
    return name


def leaf(name, base, tip, width, fill, bend=0.0):
    """A tapered paper lock from base to tip, bowed sideways by bend (fraction of its length)."""
    (bx, by), (tx, ty) = base, tip
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    pts = []
    for s, side in ((0.0, 1), (0.35, 1), (0.7, 1), (1.0, 0), (0.7, -1), (0.35, -1)):
        half = width / 2 * (1 - s) ** 0.8 * side
        bow = bend * length * math.sin(math.pi * s)
        pts.append((bx + dx * s + nx * (half + bow), by + dy * s + ny * (half + bow)))
    return blob(name, pts, fill, corners=[3])


def keys(fn, start=0, end=LOOP):
    times, t = [], start
    while t < end - 1e-6:
        times.append(t)
        t += STEP
    times.append(end)
    return [{'time': round(t, 2), 'value': round(fn(t), 3)} for t in times]


def track(target, prop, fn, **kw):
    add({'type': 'keyframes', 'target': target, 'property': prop, 'keys': keys(fn, **kw)})


def scroll(target, distance):
    add({'type': 'keyframes', 'target': target, 'property': 'translate-x',
         'keys': [{'time': 0, 'value': 0}, {'time': LOOP, 'value': -distance}]})


def wave(t, phase=0.0, period=STRIDE):
    return math.sin(2 * math.pi * (t / period + phase))


def smooth(a, b, u):
    u = max(0.0, min(1.0, u))
    return a + (b - a) * u * u * (3 - 2 * u)


def posed(t, gallop, poses):
    """gallop(t) outside the jump; inside it, ease through poses [(u, value)] that start and end on the gallop."""
    if not JUMP[0] < t < JUMP[1]:
        return gallop(t)
    u = (t - JUMP[0]) / (JUMP[1] - JUMP[0])
    pts = [(0.0, gallop(JUMP[0]))] + poses + [(1.0, gallop(JUMP[1]))]
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        if u0 <= u <= u1:
            return smooth(v0, v1, (u - u0) / (u1 - u0))
    return gallop(t)


def jump_u(t):
    return (t - JUMP[0]) / (JUMP[1] - JUMP[0]) if JUMP[0] < t < JUMP[1] else None


def lift(t):
    """Height of the leap, 0–1, over the airborne part of the jump."""
    u = jump_u(t)
    if u is None or not 0.12 < u < 0.88:
        return 0.0
    v = (u - 0.12) / 0.76
    return 4 * v * (1 - v)


# ---------------------------------------------------------------- scenery
def sky():
    add({'type': 'shape', 'name': 'sky', 'shape': 'rectangle', 'width': W, 'height': H, 'x': 0, 'y': 0, 'fill': '#93cbe6'})
    # Rainbow: stacked paper arcs, the innermost cut from sky paper.
    for i, color in enumerate(RAINBOW):
        outer, inner = 270 - i * 15, 270 - i * 15 - 17   # each band overlaps the next a little
        arc = lambda r: [(250 + r * math.cos(a), 400 - r * math.sin(a)) for a in np.linspace(0, math.pi, 40)]
        band = arc(outer) + arc(inner)[::-1]
        blob(f'rainbow-{i}', band, color, corners=[0, 39, 40, 79], tension=0.5)
    add({'type': 'group', 'name': 'rainbow', 'targets': [f'rainbow-{i}' for i in range(len(RAINBOW))]})
    # Sun with twelve rays: turning 30° per loop is seamless.
    rays = []
    for i in range(12):
        a = math.radians(i * 30)
        cx, cy = 830, 92
        p = lambda r, da: (cx + r * math.cos(a + da), cy + r * math.sin(a + da))
        rays.append(blob(f'ray-{i}', [p(56, -0.13), p(84, 0), p(56, 0.13)], '#ffc94d' if i % 2 else '#ffb547', corners=[0, 1, 2], tension=0))
    add({'type': 'group', 'name': 'sun-rays', 'targets': rays},
        {'type': 'pivot', 'target': 'sun-rays', 'value': [830, 92], 'units': 'canvas'},
        {'type': 'shape', 'name': 'sun-disc', 'shape': 'ellipse', 'width': 108, 'height': 108, 'x': 776, 'y': 38, 'fill': '#ffd45c'},
        {'type': 'shape', 'name': 'sun-face', 'shape': 'ellipse', 'width': 70, 'height': 70, 'x': 787, 'y': 49, 'fill': '#ffe48f'},
        {'type': 'group', 'name': 'sun', 'targets': ['sun-rays', 'sun-disc', 'sun-face']})
    add({'type': 'keyframes', 'target': 'sun-rays', 'property': 'rotation',
         'keys': [{'time': 0, 'value': 0}, {'time': LOOP, 'value': 30}]})
    clouds = []
    for i, (x, y, w) in enumerate([(70, 60, 150), (330, 110, 110), (560, 40, 170)]):
        clouds.append(f'cloud-{i}-group')
        add({'type': 'shape', 'name': f'cloud-{i}', 'shape': 'cloud', 'width': w, 'height': w * 0.55, 'x': x, 'y': y, 'fill': '#fdfbf6'},
            {'type': 'group', 'name': f'cloud-{i}-group', 'targets': [f'cloud-{i}']})
    add({'type': 'motion', 'recipe': 'hover', 'targets': clouds, 'amount': 5, 'period': LOOP, 'duration': LOOP, 'stagger': 700})


def hills(name, color, period, base, heights, distance, extra=None):
    """A strip of rolling hills that repeats every `period` px and scrolls `distance` per loop."""
    pts, x = [], -60.0
    span = W + distance + 120
    n = len(heights)
    while x <= span:
        k = (x / period) % 1.0
        h = sum(a * math.cos(2 * math.pi * (k * f + ph)) for f, a, ph in heights)
        pts.append((x, base - h))
        x += 16
    pts += [(span, H + 20), (-60, H + 20)]
    blob(f'{name}-paper', pts, color, corners=[len(pts) - 2, len(pts) - 1])
    members = [f'{name}-paper'] + (extra(span) if extra else [])
    add({'type': 'group', 'name': name, 'targets': members})
    scroll(name, distance)


def trees(span):
    names = []
    for k in range(int(span // 480) + 2):
        for j, (dx, h, color) in enumerate([(70, 70, '#3f8f5a'), (300, 52, '#4f9d4a'), (390, 84, '#367c4e')]):
            x = k * 480 + dx
            if x > span:
                continue
            n = f'tree-{k}-{j}'
            add({'type': 'shape', 'name': f'{n}-trunk', 'shape': 'rounded-rectangle', 'width': 12, 'height': h * 0.7,
                 'x': x - 6, 'y': 392 - h * 0.7, 'fill': '#8a5a3b', 'radius': 4},
                {'type': 'shape', 'name': f'{n}-crown', 'shape': 'ellipse', 'width': h * 0.95, 'height': h,
                 'x': x - h * 0.475, 'y': 392 - h * 1.45, 'fill': color},
                {'type': 'shape', 'name': f'{n}-shine', 'shape': 'ellipse', 'width': h * 0.38, 'height': h * 0.42,
                 'x': x - h * 0.3, 'y': 392 - h * 1.36, 'fill': '#6fbf63'})
            names += [f'{n}-trunk', f'{n}-crown', f'{n}-shine']
    return names


def path_strip():
    """The dirt path, the grass in front of it and the fence: one 1200 px tile, scrolled once per loop."""
    span = W + GROUND_TILE + 100
    add({'type': 'shape', 'name': 'path-paper', 'shape': 'rectangle', 'width': span + 60, 'height': 70, 'x': -60, 'y': 420, 'fill': '#e3c08c'})
    names = ['path-paper']
    for k in range(3):
        o = k * GROUND_TILE - 60
        # pebbles
        for j, (dx, dy, s) in enumerate([(90, 448, 14), (260, 432, 9), (540, 452, 12), (780, 436, 10), (980, 450, 13), (1130, 434, 8)]):
            n = f'pebble-{k}-{j}'
            add({'type': 'shape', 'name': n, 'shape': 'ellipse', 'width': s * 1.5, 'height': s, 'x': o + dx, 'y': dy, 'fill': '#c9a26d'})
            names.append(n)
        # the fence the unicorn jumps: centred under it at mid-jump
        fx = o + 470 + GROUND_TILE / 2 + 60 - 55
        for j, px in enumerate((0, 92)):
            n = f'fence-{k}-post-{j}'
            add({'type': 'pen', 'name': n, 'points': [[fx + px, 462], [fx + px, 392], [fx + px + 9, 382], [fx + px + 18, 392], [fx + px + 18, 462]],
                 'closed': True, 'smooth': False, 'fill': '#b97c4b'})
            names.append(n)
        for j, ry in enumerate((400, 428)):
            n = f'fence-{k}-rail-{j}'
            add({'type': 'shape', 'name': n, 'shape': 'rounded-rectangle', 'width': 136, 'height': 14,
                 'x': fx - 13, 'y': ry, 'fill': '#d39a62' if j == 0 else '#c98d57', 'radius': 3, 'rotation': -3 if j else 2})
            names.append(n)
    # front grass with flowers
    pts, x = [], -60.0
    while x <= span:
        k = (x / 120) % 1.0
        pts.append((x, 478 - 6 * math.sin(2 * math.pi * k) - 3 * math.sin(4 * math.pi * k + 1)))
        x += 15
    pts += [(span, H + 20), (-60, H + 20)]
    blob('grass-paper', pts, '#5fa556', corners=[len(pts) - 2, len(pts) - 1])
    names.append('grass-paper')
    petals = ['#ffffff', '#f7a8c4', '#ffd45c', '#b9a3e3']
    for k in range(3):
        o = k * GROUND_TILE - 60
        for j, (dx, dy, s) in enumerate([(40, 500, 26), (210, 518, 20), (370, 496, 24), (520, 522, 18), (690, 504, 26),
                                         (850, 520, 20), (1000, 498, 22), (1120, 516, 18)]):
            n = f'flower-{k}-{j}'
            add({'type': 'shape', 'name': n, 'shape': 'flower', 'width': s, 'height': s, 'x': o + dx, 'y': dy, 'fill': petals[j % 4]},
                {'type': 'shape', 'name': f'{n}-eye', 'shape': 'ellipse', 'width': s * 0.36, 'height': s * 0.36,
                 'x': o + dx + s * 0.32, 'y': dy + s * 0.32, 'fill': '#f2a33a'})
            names += [n, f'{n}-eye']
        for j, dx in enumerate((130, 450, 760, 1060)):
            n = f'tuft-{k}-{j}'
            bx = o + dx
            blob(n, [(bx, 492), (bx + 6, 470), (bx + 11, 486), (bx + 18, 464), (bx + 22, 486), (bx + 30, 474), (bx + 32, 494)],
                 '#4c9147', corners=[1, 3, 5], tension=0.3)
            names.append(n)
    add({'type': 'group', 'name': 'ground', 'targets': names})
    scroll('ground', GROUND_TILE)


# ---------------------------------------------------------------- unicorn
FRONT, HIND = 'front', 'hind'
LEGS = {  # name: (hip x, hip y, kind, near?, gallop phase)
    'leg-hind-far': (428, 318, HIND, False, 0.00),
    'leg-front-far': (528, 318, FRONT, False, 0.42),
    'leg-hind-near': (406, 322, HIND, True, 0.10),
    'leg-front-near': (552, 322, FRONT, True, 0.54),
}


def leg(name, hx, hy, kind, near):
    fill = CREAM if near else CREAM_SHADE
    hoof = HOOF if near else HOOF_FAR
    add({'type': 'shape', 'name': f'{name}-thigh', 'shape': 'rounded-rectangle', 'width': 44 if kind == HIND else 30, 'height': 84,
         'x': hx - (22 if kind == HIND else 15), 'y': hy - 26, 'fill': fill, 'radius': [20, 20, 12, 12] if kind == HIND else 14},
        {'type': 'shape', 'name': f'{name}-shin', 'shape': 'rounded-rectangle', 'width': 17, 'height': 62,
         'x': hx - 8.5, 'y': hy + 50, 'fill': fill, 'radius': 8},
        {'type': 'shape', 'name': f'{name}-sock', 'shape': 'rounded-rectangle', 'width': 19, 'height': 12,
         'x': hx - 9.5, 'y': hy + 98, 'fill': '#f6d9e3' if near else '#dcc0cc', 'radius': 5},
        {'type': 'shape', 'name': f'{name}-hoof', 'shape': 'rounded-rectangle', 'width': 25, 'height': 16,
         'x': hx - 12.5, 'y': hy + 108, 'fill': hoof, 'radius': [4, 4, 7, 7]},
        {'type': 'group', 'name': f'{name}-lower', 'targets': [f'{name}-shin', f'{name}-sock', f'{name}-hoof']},
        {'type': 'pivot', 'target': f'{name}-lower', 'value': [hx, hy + 56], 'units': 'canvas'},
        {'type': 'group', 'name': name, 'targets': [f'{name}-thigh', f'{name}-lower']},
        {'type': 'pivot', 'target': name, 'value': [hx, hy - 6], 'units': 'canvas'})


def leg_motion(name, kind, near, phase):
    front = kind == FRONT
    spread = 0 if near else 5
    upper_base, upper_amp = (2, 30) if front else (-6, 26)
    lower_base, lower_amp = (0, 72) if front else (10, 55)

    def upper(t):
        return upper_base + upper_amp * wave(t, phase)

    def lower(t):  # the joint folds while the leg swings forward
        return lower_base + lower_amp * max(0.0, -math.cos(2 * math.pi * (t / STRIDE + phase))) ** 1.3

    if front:
        up_poses = [(0.14, -38 + spread), (0.5, -58 + spread), (0.78, -32 + spread), (0.9, -14)]
        low_poses = [(0.14, 95), (0.5, 120), (0.78, 12), (0.9, 4)]
    else:
        up_poses = [(0.12, 38 + spread), (0.3, 10), (0.5, -34 + spread), (0.8, -30 + spread), (0.92, -12)]
        low_poses = [(0.12, 4), (0.3, 60), (0.5, 92), (0.8, 78), (0.92, 30)]
    track(name, 'rotation', lambda t: posed(t, upper, up_poses))
    track(f'{name}-lower', 'rotation', lambda t: posed(t, lower, low_poses))


def unicorn():
    add({'type': 'shape', 'name': 'unicorn-shadow', 'shape': 'ellipse', 'width': 230, 'height': 22, 'x': 365, 'y': 444, 'fill': '#c79f68'},
        {'type': 'pivot', 'target': 'unicorn-shadow', 'value': 'center'})
    track('unicorn-shadow', 'scale', lambda t: 1 - 0.45 * lift(t))
    track('unicorn-shadow', 'opacity', lambda t: 0.9 - 0.5 * lift(t))

    for name in ('leg-hind-far', 'leg-front-far'):
        leg(name, *LEGS[name][:4])

    # tail: rainbow locks from the rump
    tail = []
    for i, color in enumerate(RAINBOW[:5]):
        tail.append(leaf(f'tail-{i}', (382, 272 + i * 5), (276 + i * 10, 292 + i * 22), 30 - i * 2, color, bend=-0.18 + i * 0.03))
    add({'type': 'group', 'name': 'tail', 'targets': tail},
        {'type': 'pivot', 'target': 'tail', 'value': [386, 280], 'units': 'canvas'})

    blob('body', [(372, 292), (388, 262), (440, 248), (500, 247), (553, 254), (584, 282), (580, 322), (552, 344),
                  (470, 350), (408, 346), (375, 322)], CREAM)
    blob('body-belly', [(420, 332), (470, 340), (540, 334), (556, 340), (520, 351), (470, 352), (420, 346)], CREAM_SHADE)

    # mane locks behind the neck, then neck, ear, horn, head
    mane = []
    spine = [(612, 146), (596, 172), (575, 204), (552, 236), (528, 262)]
    for i, (bx, by) in enumerate(spine):
        n = leaf(f'mane-{i}', (bx + 10, by + 2), (bx - 46 - i * 3, by + 40 + i * 3), 34, RAINBOW[i % 5], bend=0.2)
        add({'type': 'group', 'name': f'{n}-lock', 'targets': [n]},
            {'type': 'pivot', 'target': f'{n}-lock', 'value': [bx + 10, by + 2], 'units': 'canvas'})
        mane.append(f'{n}-lock')
    blob('neck', [(520, 266), (548, 222), (582, 178), (608, 150), (636, 162), (628, 205), (600, 262), (578, 300), (540, 300)], CREAM)
    blob('neck-shade', [(600, 264), (622, 214), (628, 205), (614, 250), (590, 296), (578, 300)], CREAM_SHADE)
    blob('ear', [(610, 156), (614, 116), (634, 150)], CREAM, corners=[1])
    blob('ear-in', [(616, 150), (617, 128), (628, 148)], '#f5b3c8', corners=[1])
    blob('horn', [(627, 146), (668, 86), (648, 154)], '#f4c552', corners=[0, 1, 2], tension=0)
    blob('horn-light', [(633, 144), (664, 94), (642, 146)], '#ffe08a', corners=[0, 1, 2], tension=0)
    for j, (x0, y0, x1, y1) in enumerate([(631, 134, 648, 140), (641, 119, 655, 125), (651, 104, 661, 109)]):
        add({'type': 'pen', 'name': f'horn-band-{j}', 'points': [[x0, y0], [x1, y1]], 'stroke': '#d6962f', 'stroke_width': 3.5, 'line_cap': 'round'})
    blob('head', [(604, 162), (624, 144), (664, 142), (700, 166), (722, 198), (716, 220), (692, 226), (660, 214), (630, 204), (606, 188)], CREAM)
    blob('head-shine', [(626, 156), (650, 150), (672, 156), (650, 162)], CREAM_LIGHT)
    add({'type': 'shape', 'name': 'muzzle', 'shape': 'ellipse', 'width': 40, 'height': 32, 'x': 686, 'y': 192, 'fill': '#f8d3dc'},
        {'type': 'shape', 'name': 'nostril', 'shape': 'ellipse', 'width': 7, 'height': 5, 'x': 707, 'y': 200, 'fill': '#b0738a', 'rotation': 20},
        {'type': 'shape', 'name': 'cheek', 'shape': 'ellipse', 'width': 22, 'height': 13, 'x': 650, 'y': 186, 'fill': '#f7a9bf'},
        {'type': 'pen', 'name': 'eye', 'points': [[642, 172], [651, 177], [662, 172]], 'stroke': '#3b2a4a', 'stroke_width': 4, 'line_cap': 'round'},
        {'type': 'pen', 'name': 'lash', 'points': [[643, 172], [638, 167]], 'stroke': '#3b2a4a', 'stroke_width': 3, 'line_cap': 'round'},
        {'type': 'pen', 'name': 'smile', 'points': [[694, 214], [703, 217], [710, 213]], 'stroke': '#b0738a', 'stroke_width': 2.5, 'line_cap': 'round'})
    forelock = leaf('forelock', (626, 150), (650, 178), 22, RAINBOW[0], bend=-0.25)
    add({'type': 'group', 'name': 'forelock-lock', 'targets': [forelock]},
        {'type': 'pivot', 'target': 'forelock-lock', 'value': [626, 150], 'units': 'canvas'})
    forelock = 'forelock-lock'
    head_parts = ['neck', 'neck-shade'] + mane + ['ear', 'ear-in', 'horn', 'horn-light', 'horn-band-0', 'horn-band-1', 'horn-band-2',
                         'head', 'head-shine', 'muzzle', 'nostril', 'cheek', 'eye', 'lash', 'smile', forelock]
    add({'type': 'group', 'name': 'head-neck', 'targets': head_parts},
        {'type': 'pivot', 'target': 'head-neck', 'value': [548, 288], 'units': 'canvas'})

    for name in ('leg-hind-near', 'leg-front-near'):
        leg(name, *LEGS[name][:4])

    rig = ['leg-hind-far', 'leg-front-far', 'tail', 'body', 'body-belly', 'head-neck',
           'leg-hind-near', 'leg-front-near']
    add({'type': 'group', 'name': 'unicorn', 'targets': rig},
        {'type': 'pivot', 'target': 'unicorn', 'value': [480, 300], 'units': 'canvas'})

    # whole-body motion: a stride bob and rock, then the leap
    bob = lambda t: 7 * math.cos(2 * math.pi * t / STRIDE)

    def body_y(t):
        u = jump_u(t)
        if u is None:
            return bob(t)
        crouch = 12 * math.sin(math.pi * u / 0.12) if u < 0.12 else 0
        land = 12 * math.sin(math.pi * (u - 0.88) / 0.12) if u > 0.88 else 0
        return bob(t) + crouch + land - 90 * lift(t)

    track('unicorn', 'translate-y', body_y)
    track('unicorn', 'rotation', lambda t: posed(t, lambda s: 2.5 * wave(s, 0.25), [(0.16, -11), (0.5, 0), (0.82, 9), (0.93, 3)]))
    track('head-neck', 'rotation', lambda t: posed(t, lambda s: 4 * wave(s, 0.1), [(0.15, -7), (0.5, -2), (0.85, 6)]))
    track('tail', 'rotation', lambda t: 7 * wave(t, -0.15) + 22 * lift(t))
    for i, n in enumerate(mane):
        track(n, 'rotation', lambda t, i=i: 6 * wave(t, -0.12 * i) - 8 * lift(t))
    track(forelock, 'rotation', lambda t: 5 * wave(t, -0.2))
    for name, (_, _, kind, near, phase) in LEGS.items():
        leg_motion(name, kind, near, phase)

    # paper sparkles that pop out behind the hooves during the leap
    for i, (x, y, s, c) in enumerate([(318, 380, 44, '#ffd45c'), (270, 326, 32, '#f7a8c4'), (352, 304, 34, '#ffffff'), (236, 392, 28, '#b9a3e3')]):
        n = f'sparkle-{i}'
        add({'type': 'shape', 'name': f'{n}-star', 'shape': 'sparkle', 'width': s, 'height': s, 'x': x, 'y': y, 'fill': c},
            {'type': 'group', 'name': n, 'targets': [f'{n}-star']},
            {'type': 'pivot', 'target': n, 'value': 'center'})
        t0 = JUMP[0] + 150 + i * 90

        def pop(t, t0=t0):
            u = (t - t0) / 600
            return math.sin(math.pi * u) if 0 < u < 1 else 0.0
        track(n, 'scale', lambda t, pop=pop: 0.05 + 1.1 * pop(t))
        track(n, 'opacity', lambda t, pop=pop: min(1.0, 2.5 * pop(t)))
        track(n, 'rotation', lambda t, pop=pop: 90 * pop(t))


def texture_strength(name):
    fill = next(op['fill'] for op in ops if op.get('name') == name and 'fill' in op)
    light = sum(int(fill[i:i + 2], 16) for i in (1, 3, 5)) / 765
    return round(0.5 - 0.3 * light, 2)  # pale paper shows its fibres with less


def build():
    project = Project(W, H, '#93cbe6')
    with tempfile.TemporaryDirectory() as tmp:
        paper_tile(Path(tmp) / 'paper.png')
        project.apply([{'type': 'add', 'path': str(Path(tmp) / 'paper.png'), 'name': 'paper-tile'},
                       {'type': 'pattern-define', 'target': 'paper-tile', 'name': 'construction-paper'},
                       {'type': 'remove', 'target': 'paper-tile'}])
    sky()
    hills('far-hills', '#a6d49b', 320, 352, [(1, 18, 0.0), (2, 9, 0.3)], 640)
    hills('near-hills', '#78b866', 480, 398, [(1, 16, 0.2), (3, 6, 0.0)], 960, extra=trees)
    path_strip()
    unicorn()
    add({'type': 'layer-depth', 'target': 'far-hills', 'depth': 3},
        {'type': 'layer-depth', 'target': 'near-hills', 'depth': 2})
    paper = ['sky', 'rainbow', 'sun', 'cloud-0-group', 'cloud-1-group', 'cloud-2-group', 'far-hills', 'near-hills', 'ground', 'unicorn'] + [f'sparkle-{i}' for i in range(4)]
    add({'type': 'cut-paper', 'target': 'sky', 'grain': .015, 'roughness': .2, 'thickness': 1, 'fps': 12, 'jitter': 0, 'seed': 3},
        {'type': 'cut-paper', 'targets': paper[1:], 'children': True, 'grain': .02, 'roughness': .45, 'thickness': 3, 'fps': 12, 'jitter': .3, 'seed': 11},
        *[{'type': 'pattern-fill', 'target': n, 'pattern': 'construction-paper', 'name': f'{n}-paper', 'seed': i,
           'opacity': texture_strength(n), 'tile_variation': .25} for i, n in enumerate(pieces)],
        *[{'type': 'effect', 'target': n, 'name': 'vignette', 'strength': .1, 'radius': .9} for n in pieces if n != 'sky' and not n.startswith('rainbow')],
        {'type': 'lighting', 'ambient': .95, 'lights': [{'x': 830, 'y': 90, 'radius': 520, 'color': '#fff1cf', 'intensity': .16}], 'vignette': .2},
        {'type': 'timeline-set', 'duration': LOOP, 'fps': 12, 'loop': 0})
    project.apply(ops)
    return project


def main(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    project = build()
    project.save(output / 'paper-unicorn.vixl', overwrite=True)
    render_at(project, 1500).save(output / 'paper-unicorn.png')
    export_timeline(project, output / 'paper-unicorn.gif', scale=0.6, overwrite=True)
    export_timeline(project, output / 'paper-unicorn.mp4', fps=24, overwrite=True)
    from vixl.checks import check_design
    print(check_design(project, checks=['motion'])['outcome']['review_reasons'])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('output', nargs='?', default=str(Path(__file__).parent))
    main(parser.parse_args().output)
