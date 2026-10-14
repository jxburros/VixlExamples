"""Re-render the art references from their editable sources with the installed Vixl.

Run from the repository root: python art/rerender.py

Heyoka: every items/*.vixl master is loaded and saved again, and its PNG, PDF, page PNGs, contact
sheet, PowerPoint, animation, thumbnail and check report are exported from it. The operation recipes,
the source artwork sheet, the collection overview and the HTML galleries are kept as they are.
Rain girl: rain-girl.png is rendered again from rain-girl-ops.json.
"""
import json
from pathlib import Path

from PIL import Image

from vixl import Project, __version__
from vixl.assurance import run_suite
from vixl.deck import contact_sheet
from vixl.timeline import export_timeline, render_at

ART = Path(__file__).resolve().parent
HEYOKA = ART / "heyoka-mirrors-paradox"
ITEMS = HEYOKA / "items"
THUMB_HEIGHT = 420


def checks(project, old_report, **where):
    design = project.check(checks=old_report["design"]["checked"]["checks"], **where)
    readability = run_suite(project, "readability", **{k: v for k, v in where.items() if k == "pages"})
    return {"design": design, "readability": readability}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + "\n")


def thumbnail(image, path):
    image = image.convert("RGB")
    width = round(image.width * THUMB_HEIGHT / image.height)
    image.resize((width, THUMB_HEIGHT), Image.LANCZOS).save(path, quality=88)


def motion_proof(project, path, frames=5, cell=180):
    duration = project.state["timeline"]["duration"]
    strip = Image.new("RGB", (frames * cell, cell), (220, 216, 208))
    for index in range(frames):
        frame = render_at(project, round(duration * index / frames)).convert("RGB")
        frame.thumbnail((cell, cell), Image.LANCZOS)
        strip.paste(frame, (index * cell, 0))
    strip.save(path)


def heyoka():
    summary = {}
    for entry in json.loads((HEYOKA / "manifest.json").read_text()):
        slug = entry["slug"]
        stem = ITEMS / slug
        project = Project.load(stem.with_suffix(".vixl"))
        project.save(stem.with_suffix(".vixl"), overwrite=True)
        pages = project.state.get("pages") or []
        project.export(stem.with_suffix(".pdf"), overwrite=True)
        if pages:
            sheet = contact_sheet(project, width=360, columns=3, labels=False)
            sheet.save(stem.with_suffix(".png"))
            passed = []
            for number, page in enumerate(pages, 1):
                page_stem = ITEMS / f"{slug}-page-{number:02d}"
                project.render(page=page["name"]).save(page_stem.with_suffix(".png"))
                old = json.loads(page_stem.with_suffix(".check.json").read_text())
                report = checks(project, old, pages=[page["name"]])
                write_json(page_stem.with_suffix(".check.json"), report)
                passed.append(report["design"]["passed"] and report["readability"]["status"])
            if "pptx" in entry["exports"]:
                project.export(stem.with_suffix(".pptx"), overwrite=True)
            thumbnail(project.render(page=pages[0]["name"]), ITEMS / f"{slug}-thumb.jpg")
            summary[slug] = passed
            continue
        image = project.render()
        image.save(stem.with_suffix(".png"))
        old = json.loads(stem.with_suffix(".check.json").read_text())
        report = checks(project, old)
        write_json(stem.with_suffix(".check.json"), report)
        summary[slug] = [report["design"]["passed"] and report["readability"]["status"]]
        thumbnail(image, ITEMS / f"{slug}-thumb.jpg")
        if entry["motion"]:
            export_timeline(project, stem.with_suffix(".webp"), fps=10, scale=0.65, overwrite=True)
            export_timeline(project, stem.with_suffix(".gif"), fps=4, scale=0.4, overwrite=True)
            motion_proof(project, ITEMS / f"{slug}-motion-proof.png")
        fillable = ITEMS / f"{slug}-fillable.pdf"
        if fillable.exists():
            project.export(fillable, fillable=True, overwrite=True)
    return summary


def rain_girl():
    operations = json.loads((ART / "rain-girl-ops.json").read_text())
    size = Image.open(ART / "rain-girl.png").size
    project = Project(*size)
    project.apply(operations)
    project.export(ART / "rain-girl.png", overwrite=True)


if __name__ == "__main__":
    print(json.dumps({"vixl": __version__, "heyoka": heyoka()}, indent=2))
    rain_girl()
