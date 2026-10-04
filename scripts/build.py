"""Build the static site into dist/: page, bridge and a minimal slice of the risks package."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "risks" / "src" / "dpia_tabletop"
DIST = ROOT / "dist"

# Whitelist: only what the browser needs to load cards. No server, sim, tuning, CLI or renderer.
PY_FILES = ("__init__.py", "cards.py", "engine.py")


def build(dist: Path = DIST) -> Path:
    if not PKG.is_dir():
        raise SystemExit("risks submodule is empty: run `git submodule update --init`")
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True)

    with zipfile.ZipFile(dist / "dpia_tabletop.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in PY_FILES:
            z.write(PKG / name, f"dpia_tabletop/{name}")
        for f in sorted((PKG / "data").rglob("*.json")):
            z.write(f, f"dpia_tabletop/data/{f.relative_to(PKG / 'data').as_posix()}")

    shutil.copy(ROOT / "site" / "index.html", dist / "index.html")
    shutil.copy(ROOT / "bridge" / "bridge.py", dist / "bridge.py")
    shutil.copy(ROOT / "bridge" / "boot.js", dist / "boot.js")
    for lic in ("LICENSE", "LICENSE-CONTENT"):
        shutil.copy(ROOT / lic, dist / lic)
    (dist / ".nojekyll").touch()
    return dist


if __name__ == "__main__":
    print(f"built {build()}")
