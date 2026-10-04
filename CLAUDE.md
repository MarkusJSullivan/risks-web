# CLAUDE.md

Static GitHub Pages build of the DPIA Risk Tabletop single-player game (Pyodide runs the Python rules in the browser).

## Rules

- Never edit, commit or push inside `risks/` (git submodule). Changes needed there go into
  `docs/handoffs/NNN-<topic>.md` (see `docs/handoffs/README.md`) and are made in `risks` separately; then bump the pointer.
- Prefer workarounds here (patching fetch, rewriting output) over asking for changes in `risks`.
- Keep the SDM attribution (`game.sources`) in published pages. Code is MIT, card data CC BY 4.0.
- Layout: `bridge/` (bridge.py, boot.js), `scripts/` (build.py), `tests/`, `site/` (placeholder page), `dist/` (build output, ignored).
- Do not push, create the GitHub remote or enable Pages without the user's confirmation.
