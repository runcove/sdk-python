"""A routed httpx.MockTransport for resource round-trips (colour-neutral: it serves both clients).

``api.on("GET", "/api/vms/x", json={...})`` answers that method and raw path (query excluded);
a route given several responses serves them in turn and then repeats the last. Every request is
kept in ``api.seen``; a request with no route fails the test with a 599 the transport raises as a
``ServerError`` naming the route, so a wrong URL never passes silently.
"""

from __future__ import annotations

import json as jsonlib
from typing import Any

import httpx

from cove_sdk._meta import API_VERSION

HEADERS = {"x-cove-api-version": str(API_VERSION)}


class Api:
    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], list[httpx.Response]] = {}
        self.seen: list[httpx.Request] = []

    def on(
        self,
        method: str,
        path: str,
        *responses: tuple[int, Any] | int | None,
        headers: dict[str, str] | None = None,
    ) -> Api:
        """Route ``method path`` to ``responses``: ``(status, json)``, a bare status (empty body),
        or ``None`` (``204``). No responses means one ``204``. ``headers`` replaces the default
        ``x-cove-api-version`` header (``{}`` sends none)."""
        hdrs = HEADERS if headers is None else headers
        built = []
        for r in responses or (None,):
            if r is None:
                built.append(httpx.Response(204, headers=hdrs))
            elif isinstance(r, int):
                built.append(httpx.Response(r, headers=hdrs))
            else:
                built.append(httpx.Response(r[0], json=r[1], headers=hdrs))
        self.routes[(method, path)] = built
        return self

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.seen.append(request)
        key = (request.method, request.url.raw_path.decode().split("?", 1)[0])
        queue = self.routes.get(key)
        if not queue:
            return httpx.Response(
                599, json={"error": f"no route for {key}"}, headers=HEADERS
            )
        response = queue.pop(0) if len(queue) > 1 else queue[0]
        # A fresh copy each time: an httpx.Response is consumed once read.
        return httpx.Response(
            response.status_code, content=response.content, headers=response.headers
        )

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handler)

    @property
    def last(self) -> httpx.Request:
        assert self.seen, "no request was sent"
        return self.seen[-1]

    def last_json(self) -> Any:
        return jsonlib.loads(self.last.content) if self.last.content else None

    def query(self) -> dict[str, str]:
        return dict(self.last.url.params)


# Minimal bodies the generated parsers accept (the fields sdk/openapi.yaml requires).
VM = {
    "auto_pause_policy": {"type": "auto_pause", "idle_timeout_secs": 600},
    "created_at": "2026-10-01T00:00:00Z",
    "disk_size_gb": 10,
    "image": "fedora-43",
    "mac_address": "02:00:00:00:00:01",
    "memory_mb": 2048,
    "name": "v",
    "state": "running",
    "updated_at": "2026-10-01T00:00:00Z",
    "vcpus": 2,
    "vm_id": "0199a000-0000-7000-8000-000000000000",
}
UUID1 = "0199a000-0000-7000-8000-000000000001"
UUID2 = "0199a000-0000-7000-8000-000000000002"
