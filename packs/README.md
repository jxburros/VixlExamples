# Content packs

Content packs are data that Vixl downloads when it needs them, so the engine package stays small. A pack
holds no code that Vixl runs.

| Pack | What it is | Used by |
| --- | --- | --- |
| [`emojis/`](emojis/README.md) | VIXL Line emoji artwork: about 4,000 Unicode emojis adapted from OpenMoji and 100 VIXL originals, as SVG with editable `.vixl` masters | Text that contains emojis, `vixl emoji`, emoji pack exports |

Vixl pins each pack to a commit of this repository and checks its SHA-256 before using it. Changing a
pack here does not change what Vixl downloads until Vixl's pin is updated.
