"""AsyncCoveClient's shell: lifecycle, redaction, credentials, server_api_version (mirrored to CoveClient)."""

import warnings

import httpx
import pytest

from cove_sdk import AsyncCoveClient, CoveConfigError
from cove_sdk._meta import API_VERSION

TOKEN = "cvk_" + "s" * 43
TICKET = "wg-ticket-secret"


def _mock(seen: list[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200, json={}, headers={"x-cove-api-version": str(API_VERSION)}
        )

    return httpx.MockTransport(handler)


async def test_component_client_closes_its_http_client_on_exit() -> None:
    seen: list[httpx.Request] = []
    async with AsyncCoveClient("https://h", token=TOKEN, transport=_mock(seen)) as c:
        assert not c._transport._http.is_closed
        await c._transport.request("GET", "/api/vms")
    assert c._transport._http.is_closed
    c2 = AsyncCoveClient("https://h", token=TOKEN, transport=_mock(seen))
    await c2.aclose()
    assert c2._transport._http.is_closed


async def test_component_client_sends_its_credential() -> None:
    seen: list[httpx.Request] = []
    async with AsyncCoveClient("https://h", token=TOKEN, transport=_mock(seen)) as c:
        await c._transport.request("GET", "/api/vms")
    async with AsyncCoveClient("https://h", ticket=TICKET, transport=_mock(seen)) as c:
        await c._transport.request("GET", "/api/vms")
    assert [r.headers["Authorization"] for r in seen] == [
        f"Bearer {TOKEN}",
        f"Warpgate {TICKET}",
    ]


def test_component_client_repr_redacts_credentials() -> None:
    for kw in ({"token": TOKEN}, {"ticket": TICKET}):
        c = AsyncCoveClient("https://h/", transport=_mock([]), **kw)
        r = repr(c)
        assert TOKEN not in r and TICKET not in r and str(c) == r
        assert "base_url='https://h'" in r and "auth=<redacted>" in r


def test_component_client_takes_exactly_one_credential() -> None:
    with pytest.raises(CoveConfigError):
        AsyncCoveClient("https://h", transport=_mock([]))
    with pytest.raises(CoveConfigError):
        AsyncCoveClient("https://h", token=TOKEN, ticket=TICKET, transport=_mock([]))


def test_component_client_refuses_plain_http_to_a_remote_host() -> None:
    with pytest.raises(CoveConfigError):
        AsyncCoveClient("http://example.com", token=TOKEN, transport=_mock([]))
    AsyncCoveClient(
        "http://example.com", token=TOKEN, transport=_mock([]), allow_insecure_http=True
    )


async def test_component_server_api_version_is_none_until_a_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={}, headers={"x-cove-api-version": "42"})

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        async with AsyncCoveClient(
            "https://h", token=TOKEN, transport=httpx.MockTransport(handler)
        ) as c:
            assert c.server_api_version is None
            await c._transport.request("GET", "/api/vms")
            assert c.server_api_version == 42


GROUPS = (
    "vms",
    "checkpoints",
    "policies",
    "host",
    "secrets",
    "tags",
    "audit",
    "keys",
    "webhooks",
    "meta",
    "events",
    "admin",
    "teams",
)


async def test_component_client_exposes_the_resource_groups_over_its_transport() -> (
    None
):
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        body: object = {"username": "alice"}
        if request.url.path.endswith("/secrets"):
            body = [{"name": "A"}]
        return httpx.Response(
            200, json=body, headers={"x-cove-api-version": str(API_VERSION)}
        )

    async with AsyncCoveClient(
        "https://h", token=TOKEN, transport=httpx.MockTransport(handler)
    ) as c:
        for group in GROUPS:
            assert getattr(c, group)._t is c._transport, group
        who = await c.meta.whoami()
        names = [s.name for s in await c.secrets.vm("v").list()]
    assert who.username == "alice" and names == ["A"]
    assert [r.url.path for r in seen] == ["/api/whoami", "/api/vms/v/secrets"]
    assert all(r.headers["Authorization"] == f"Bearer {TOKEN}" for r in seen)
