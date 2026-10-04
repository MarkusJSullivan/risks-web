# The Data Protection Risk Game (web)

Static website for the game, served by GitHub Pages straight from this repo:
https://markusjsullivan.github.io/risks-web/

The game itself lives in [dpia-tabletop](https://github.com/MarkusJSullivan/dpia-tabletop). This repo only holds its
published build.

## What is on the site

| File | What it is |
|---|---|
| `index.html` | Start page: play online or play on paper. |
| `play.html` | The single-player game (Symbol card style, no picture files). The Python rules run in the browser via [Pyodide](https://pyodide.org); there is no server. |
| `boot.js`, `bridge.py`, `dpia_tabletop.zip` | Load Pyodide, answer the page's `/api` calls from the Python rules (`bridge.py`), rules and card data (no server code). |
| `paper.html`, `paper/` | The paper version: rulebook, player aid, facilitator sheet, card PDFs, risk matrix. Copied from `docs/paper` of dpia-tabletop. |

Everything is generated from a local clone of dpia-tabletop (`risks/`, not part of this repo) by `scripts/rebuild.py`,
which updates the clone, builds the pages and runs the tests. `scripts/`, `tests/` and `risks/` are local only (see
`.gitignore`). Do not edit the generated files by hand: change the build or the source and rebuild.

## Licence

Card text: CC BY 4.0 (`LICENSE-CONTENT`). Code: MIT (`LICENSE`). Loosely based on the German Standard Data Protection
Model (SDM) and NIST SP 800-53 Rev. 5; the attribution is on every page.
