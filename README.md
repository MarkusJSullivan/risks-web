# risks-web

Publishes the single-player DPIA Risk Tabletop game on GitHub Pages. The game (`risks/`, a git submodule of
[dpia-tabletop](https://github.com/MarkusJSullivan/dpia-tabletop)) is server-authoritative, so this repo runs its
existing Python rules in the browser with Pyodide and serves a static build.

## Phases

1. **Set up the repo (done):** empty layout, `risks` pulled in as a submodule, no code.
2. **Make it work:** Pyodide proof of concept, `bridge/bridge.py` (the three `/api` routes), `bridge/boot.js`
   (fetch patch), `scripts/build.py` (one page per style into `dist/`), tests, and a Pages workflow.

## Key rule

risks-web never touches `risks`: no edits, commits or pushes inside the submodule. If `risks` needs a change, write a
handoff plan in `docs/handoffs/` and make the change in `risks` separately, then bump the pointer here. Prefer
workarounds in this repo over asking for changes.

## Clone

    git clone --recurse-submodules <url-of-risks-web>
    # already cloned without it:
    git submodule update --init

## Bumping the submodule pointer

    git -C risks fetch
    git -C risks checkout <commit>
    git add risks
    git commit -m "Bump risks to <commit>"

## Licence

Code: MIT (`LICENSE`). Card data: CC BY 4.0 (`LICENSE-CONTENT`). The SDM attribution (`game.sources` in the risks
data) must be kept wherever the cards are published.
