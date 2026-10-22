"""Pull the pictures the "now the real stuff" scenes show out of this repository into work/assets/.

Needs ffmpeg and Vixl. The rain girl stages are real: the 768 operations in art/rain-girl-ops.json are replayed
in Vixl and rendered after 14 of them. Run from anywhere: python promo/vixl-is-fun/build/prepare_assets.py
"""
import glob, json, os, subprocess
from PIL import Image
from lib import HERE, REPO
from vixl import Project

E = os.path.join(REPO, "explorations")
OUTA = os.path.join(HERE, "work", "assets")
for d in ("rain", "paint", "map", "misc"):
    os.makedirs(os.path.join(OUTA, d), exist_ok=True)

def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

# rain girl: replay the recipe and keep 14 stages
ops = json.load(open(os.path.join(REPO, "art", "rain-girl-ops.json")))
p = Project(1080, 1350)
marks = sorted({4, 12, 30, 60, 100, 160, 240, 320, 400, 480, 560, 640, 700, len(ops)})
last, log = 0, []
for k, m in enumerate(marks):
    p.apply(ops[last:m]); last = m
    im = p.render().convert("RGB"); im.thumbnail((540, 675)); im.save(f"{OUTA}/rain/s{k:02d}.jpg", quality=88)
    log.append((k, m))
json.dump(log, open(f"{OUTA}/rain/marks.json", "w"))

# painting timelapse (4 fps) and the four filter variants
ffmpeg("-i", f"{E}/05-generative-painting/output/timelapse.mp4", "-vf", "fps=4,scale=800:500", "-q:v", "3", f"{OUTA}/paint/f%03d.jpg")
for n in ("variant-watercolor", "variant-oil-paint", "variant-riso-halftone", "variant-pencil-sketch"):
    Image.open(f"{E}/05-generative-painting/output/{n}.jpg").convert("RGB").resize((800, 500)).save(f"{OUTA}/misc/{n}.jpg", quality=90)

# pixel RPG map animation at its own 12 fps
ffmpeg("-i", f"{E}/04-pixel-rpg/output/map-timeline.mp4", "-vf", "fps=12", f"{OUTA}/map/f%03d.png")

# poster, proofs, infographic, cards
P = f"{E}/01-print-concert-poster/output"
Image.open(f"{P}/poster-rgb.png").convert("RGB").save(f"{OUTA}/misc/poster.jpg", quality=90)
Image.open(f"{P}/compare-rgb-vs-proof.jpg").convert("RGB").save(f"{OUTA}/misc/compare.jpg", quality=90)
Image.open(f"{P}/colorvision-sims.jpg").convert("RGB").save(f"{OUTA}/misc/cvd.jpg", quality=90)
im = Image.open(f"{E}/08-infographic/output/infographic-world.png").convert("RGB")
im.resize((640, int(im.height * 640 / im.width))).save(f"{OUTA}/misc/info.jpg", quality=90)
for ed in ("standard", "holo"):
    for path in sorted(glob.glob(f"{E}/07-trading-cards/output/set/{ed}/*.webp")):
        Image.open(path).convert("RGB").save(f"{OUTA}/misc/card-{ed}-{os.path.basename(path)[:4]}.jpg", quality=90)

# The Germ King: the sneeze (5.6 s, a little longer than the shot) and two stills for the code card
MOVIE = os.path.join(REPO, "movie", "the-germ-king.mp4")
ffmpeg("-ss", "34.6", "-t", "5.6", "-i", MOVIE, "-c:v", "libx264", "-crf", "17", "-an", f"{OUTA}/misc/germ-clip.mp4")
ffmpeg("-ss", "12", "-i", MOVIE, "-frames:v", "1", f"{OUTA}/misc/germ-still1.png")
ffmpeg("-ss", "6", "-i", MOVIE, "-frames:v", "1", f"{OUTA}/misc/germ-still2.png")
print("assets ready in", OUTA)
