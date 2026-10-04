"""Runs inside Pyodide (and natively in tests): exposes the card set as JSON for the page."""
from __future__ import annotations

import json

from dpia_tabletop.cards import CardSet


def _text(value, lang: str) -> str:
    """Pick a language from a ``{"en": ..., "de": ...}`` value; pass plain strings through."""
    if isinstance(value, dict):
        return value.get(lang) or value.get("en") or ""
    return value or ""


def cards_overview(lang: str = "en") -> str:
    cs = CardSet.load()
    game = cs.data["game"]
    sources = game["sources"]
    cards = []
    for c in cs.by_id.values():
        cards.append(
            {
                "id": c["id"],
                "kind": c.get("type", ""),
                "family": c.get("familyLabel") or c.get("family") or "",
                "name": _text(c.get("name") or c.get("title"), lang),
                "text": _text(c.get("description") or c.get("flavour"), lang),
            }
        )
    return json.dumps(
        {
            "title": _text(game["title"], lang),
            "version": cs.version,
            "scenario": _text(game["scenario"], lang),
            "sources": {"primary": sources["primary"], "url": sources["url"], "attribution": sources["attribution"]},
            "cards": cards,
        },
        ensure_ascii=False,
    )
