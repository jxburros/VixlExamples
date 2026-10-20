# VixlExamples

A showcase of what [Vixl](https://github.com/jxburros/Vixl) can do: long creative projects, films, the
marketing pack, the evaluation results and kits that measure Vixl against other tools, and the content
packs Vixl downloads on demand. The engine, its documentation and the agent skill live in the
[Vixl repository](https://github.com/jxburros/Vixl); this one holds the media, so the engine repository
stays small.

| Folder | What it is |
| --- | --- |
| [`explorations/`](explorations/README.md) | Ten complex projects (print poster, brand identity, kinetic launch, pixel RPG, generative painting, photo lab, trading cards, infographic, campaign, character film) plus logo alternatives, each with a `build.py` |
| [`art/`](art/README.md) | Art references: *Heyoka: Mirrors & Paradox* (18 editorial projects) and *Rain girl* with its operation recipe |
| [`marketing/`](marketing/README.md) | The Vixl marketing pack: social graphics, carousel, deck, print, forms, motion teaser and app animations |
| [`promo/`](promo/README.md) | *Vixl in 60 seconds*, *It does that*, and the promo template [variety pack](promo/variety/README.md) |
| [`movie/`](movie/README.md) | *The Germ King*, a short animated film |
| [`eval-results/`](eval-results) | Published agent evaluations, tool comparisons, the 0.26 gallery and the blind re-judging |
| [`evals/tool-comparison/`](evals/tool-comparison/README.md) | The hand-run tool comparison kit: briefs, fixtures, runs and the re-judging packages |
| [`evals/live-runs/`](evals/live-runs) | Recorded live agent runs that the Vixl agent-eval baseline budgets are based on |
| [`qa-reports/`](qa-reports) | Release QA reports |
| [`packs/`](packs/README.md) | Content packs Vixl downloads when needed, such as the [emoji artwork](packs/emojis/README.md) |
| [`showcases/`](showcases/README.md) | Small demonstrations moved out of Vixl's `examples/`: the lyric video and the cut-paper scene |
| [`fonts/`](fonts/README.md) | 23 installable fonts (OTF and TTF) drawn with Vixl's font maker: a [display set](fonts/display/README.md) and a [botanical set](fonts/botanical/README.md), with the generator scripts |

## Running the builds

Install Vixl (see its [getting started](https://github.com/jxburros/Vixl/blob/main/docs/getting-started.md)),
then run each build from the root of this repository, for example `python explorations/04-pixel-rpg/build.py`
or `python marketing/build.py`.

A few builds use files from the Vixl repository (the brand kit in `assets/brand` and the scripts in
`examples/`): the marketing pack, the promo films and the logo comparison. Clone Vixl beside this
repository (`../Vixl`), or point `VIXL_REPO` at a Vixl checkout:

```bash
git clone https://github.com/jxburros/Vixl ../Vixl
VIXL_REPO=../Vixl python promo/build/make_video.py
```

## Adding to this repository

New showcases, experiments, generated media, evaluation results and large content packs go here rather
than into Vixl. Vixl links to them. Keep only what Vixl's tests, docs or packaging need in the Vixl
repository (its `docs/assets`, `assets/` and `examples/`).
