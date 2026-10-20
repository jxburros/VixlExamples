# Fonts drawn with Vixl

Complete, installable fonts (OTF and TTF, 84 glyphs each: A-Z, a-z, 0-9 and 20 punctuation marks) made with Vixl's
[font maker](https://github.com/jxburros/Vixl/blob/main/docs/guides/text/custom-fonts.md). Every glyph is ordinary
Vixl layers (stroked paths and filled outlines); `font-design`, `font-glyph` and `font-build` turn them into a font and
`export` writes the files. Each font has a `.vixl` document, so the glyphs stay editable.

| Set | Fonts | Poster |
| --- | --- | --- |
| [`display/`](display) | 14 fonts: elegant (Gilded Italic, Pearl Line, Velvet Didone), handwritten (Scribble Hand, Ballpoint Note), weird (Noodle Wobble, Ransom Tiles, Drippy Goo, Rune Cut), stylized (Neon Tube, Puffy Bubble, Pixel Pop, LED Matrix, Chisel Marker) | [`display/poster.png`](display/poster.png) |
| [`botanical/`](botanical) | 9 plant fonts: Ivy Tendril, Willow Wisp, Fern Frond, Bare Branch, Daisy Chain, Garden Stamp, Moss Rug, Seed Pod, Cactus Spine | [`botanical/poster.png`](botanical/poster.png) |

Each set folder holds `fonts/` (the OTF and TTF files), `specimens/` (a rendered specimen per font, set in the font
itself), `glyph-sheets/` (the proof sheet of drawn glyphs), `vixl-sources/` (the editable documents, one per font plus
the poster) and `poster.png`.

The font files carry the licence note "Created with Vixl; free to use." in their name table. Characters outside the
84 drawn glyphs (accents, dashes) are not in the fonts.

## How they are made

One centre-line alphabet (`generator/skeleton.py`) is styled in many ways: `styles.py` (marker and ballpoint hands,
broad-nib calligraphy, hairline pearls, bubbles, neon, noodles, tiles, pixels, runes, drips) and `botanic.py`
(vines, ferns, daisies, moss, cactus spines, twigs, willow, seeds, garden stamps). `build.py` draws each glyph into a
Vixl document, builds and exports the font, then renders a specimen. Geometry uses `shapely`, which Vixl already
depends on.

```bash
pip install vixl-engine            # or a checkout of Vixl: pip install -e ../Vixl

# display set (all fonts, or name some slugs such as pixel-pop neon-tube)
python fonts/generator/build.py OUT_DIR
# botanical set
FONTSET=fontspecs_botanical python fonts/generator/build.py OUT_DIR ivy-tendril fern-frond

# posters (read the fonts/ and vixl-sources/ of a set folder, write poster.png)
python fonts/generator/poster_display.py fonts/display
python fonts/generator/poster_botanical.py fonts/botanical
```

A full set takes a few minutes; builds of different fonts can run in parallel. Output goes flat into `OUT_DIR`
(`Family.otf`, `Family.ttf`, `slug-glyphs.png`, `slug-specimen.png`, `slug.vixl`). The glyph spacing is automatic with
a small kerning table, so a few pairs are loose; tune `sb`, `track` and the kerning in the font specs.
