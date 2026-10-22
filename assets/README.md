# Assets

Small shared files that the builds in this repository need. Nothing here is generated at run time.

| Path | What it is | Used by |
| --- | --- | --- |
| [`banner/`](banner/) | The README banner: a Vixl document (`banner.vixl`) built from this repository's own outputs, with its `build.py` | The root README |
| `brand/ripple/` | The Vixl logo kit's editable masters (`Editable-Vixl/`) and outlined SVGs (`SVG/`), plus its `START-HERE.md` | [`marketing/`](../marketing/README.md), [`promo/`](../promo/README.md) |
| `brand/digital-shift/PNG/` | The retired previous logo, for comparison | [`explorations/logo-alternatives/`](../explorations/logo-alternatives/README.md) |
| `vixl-docs/` | Five pictures from Vixl's documentation (chart, slides, filled form, workflow, emoji sheet) shown in the 60-second film and the marketing pack | `promo/build/scenes.py`, `marketing/build.py` |

## These are copies

The brand kit and the five documentation pictures belong to [Vixl](https://github.com/jxburros/Vixl); they were
copied from its 0.30.3 source so that every build here needs only `python -m pip install vixl-engine`, not a Vixl
checkout. They don't change when Vixl's artwork does. To refresh them, copy `assets/brand/ripple/` and the same
pictures from `docs/assets/generated/` in a Vixl checkout, then rebuild the pieces that use them.

The Vixl logo and brand artwork follow Vixl's [licence](https://github.com/jxburros/Vixl/blob/main/LICENSE) and
brand notes.
