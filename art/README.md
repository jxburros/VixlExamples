# Art references

- [Heyoka: Mirrors & Paradox](heyoka-mirrors-paradox/) — 18 psychedelic editorial projects with editable Vixl masters, illustrated documents, a slide deck, animation, and a fillable journal.
- [Rain girl](rain-girl.png) — artwork and its [operation recipe](rain-girl-ops.json).

`python art/rerender.py` re-renders both from their sources with the installed Vixl (the Heyoka masters, and the Rain girl recipe).
Since Vixl 0.24 the `watercolor` look pools pigment in a darker rim inside every edge of a layer, which turned the
full-width street into a dark block, so the Rain girl recipe now leaves `ground` out of its watercolor look.
