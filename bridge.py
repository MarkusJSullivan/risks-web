"""Runs inside Pyodide (and natively in tests): answers the game page's /api calls without a server.

Same routes, JSON and status codes as dpia_tabletop.server; sessions live in memory until the page is reloaded.
"""
from __future__ import annotations

import json
import secrets

from dpia_tabletop.cards import CardSet
from dpia_tabletop.game import Game
from dpia_tabletop.server import GameError

_game = Game(CardSet.load())
_sessions: dict[str, dict] = {}


def handle(path: str, body: str) -> list:
    """[status, json text] for a request path such as /api/new or /api/<token>/action."""
    status, payload = _route(path, body)
    return [status, json.dumps(payload, ensure_ascii=False)]


def _route(path: str, raw: str) -> tuple[int, dict]:
    try:
        body = json.loads(raw or "{}")
    except ValueError:
        return 400, {"error": "invalid JSON"}
    if not isinstance(body, dict):
        return 400, {"error": "expected a JSON object"}
    parts = [p for p in path.split("?")[0].split("/") if p]
    try:
        if parts == ["api", "new"]:
            seed = body.get("seed")
            if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
                return 400, {"error": "seed must be an integer"}
            state = _game.new_game(seed, body.get("handSize"), body.get("mode"))
            token = secrets.token_urlsafe(24)
            _sessions[token] = state
            return 200, {"session": token, "view": _game.view(state)}
        if parts == ["api", "clientlog"]:
            return 200, {"ok": True}
        if len(parts) == 3 and parts[0] == "api" and parts[2] in ("view", "action"):
            state = _sessions.get(parts[1])
            if state is None:
                return 404, {"error": "unknown or expired session"}
            if parts[2] == "view":
                return 200, {"view": _game.view(state)}
            new_state, events = _game.apply(state, body)
            _sessions[parts[1]] = new_state
            return 200, {"view": _game.view(new_state), "events": events}
    except GameError as exc:
        return (400 if parts == ["api", "new"] else 409), {"error": str(exc)}
    return 404, {"error": "not found"}
