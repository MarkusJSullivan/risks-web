import json
import sys
import zipfile

import pytest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent / "scripts"))
import build as site_build  # noqa: E402


@pytest.fixture(scope="module")
def dist(tmp_path_factory):
    return site_build.build(tmp_path_factory.mktemp("dist"))


def test_zip_is_minimal(dist):
    names = zipfile.ZipFile(dist / "dpia_tabletop.zip").namelist()
    py = {n for n in names if n.endswith(".py")}
    assert py == {f"dpia_tabletop/{n}" for n in site_build.PY_FILES}
    assert any(n.endswith("v0.8/game.json") for n in names)


def test_bridge_overview_runs_from_built_package(dist, tmp_path, monkeypatch):
    zipfile.ZipFile(dist / "dpia_tabletop.zip").extractall(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.syspath_prepend(str(dist))
    import bridge

    o = json.loads(bridge.cards_overview("en"))
    assert len(o["cards"]) > 50
    assert all(c["name"] for c in o["cards"])
    assert o["sources"]["attribution"]  # SDM attribution must stay published
