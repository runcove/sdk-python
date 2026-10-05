"""keys.create's admin, service, member and team options and keys.list(service=True) (mirrored to the
sync client by unasync)."""

from typing import Any

import httpx
import pytest
from mockapi import Api

import cove_sdk
from cove_sdk import CoveError
from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.keys import Keys
from cove_sdk._generated.models import CreatedKey, CreateKeyRequest, KeySummary
from cove_sdk.auth import BearerAuth

CREATED = {
    "created_at": "2026-10-01T00:00:00Z",
    "id": "k1",
    "label": "ci",
    "raw_token": "cvk_x",
    "scopes": ["vms:read"],
}

SERVICE_SUMMARY = {
    "id": "k2",
    "label": "deploy",
    "scopes": ["vms:read"],
    "created_at": "2026-10-01T00:00:00Z",
    "key_prefix": "cvk_ab",
    "status": "active",
    "subject_type": "service",
    "bound_team": "eng",
}


def _t(api: Api) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
    )


WHOAMI = {"username": "admin"}


async def _create(**fields: Any) -> tuple[Api, CreatedKey]:
    api = (
        Api()
        .on("GET", "/api/whoami", (200, WHOAMI))
        .on("POST", "/api/api-keys", (201, CREATED))
    )
    created = await Keys(_t(api)).create(**fields)
    return api, created


def test_component_keys_wire_names_are_the_generated_models() -> None:
    # the names the tests below send are the regenerated CreateKeyRequest's, not this file's guess
    assert {"admin_key", "service", "member", "team"} <= set(
        CreateKeyRequest.__annotations__
    )


async def test_component_keys_create_admin_key() -> None:
    api, created = await _create(
        label="ops", scopes=["admin:fleet:read"], expires_in_secs=3600, admin_key=True
    )
    assert (api.last.method, api.last.url.path) == ("POST", "/api/api-keys")
    assert api.last_json() == {
        "label": "ops",
        "scopes": ["admin:fleet:read"],
        "expires_in_secs": 3600,
        "admin_key": True,
    }
    assert isinstance(created, CreatedKey) and created.raw_token == "cvk_x"


async def test_component_keys_create_service_key_bound_to_a_team() -> None:
    api, _ = await _create(
        label="deploy", scopes=["vms:read"], expires_in_secs=60, service="ci", team="eng"
    )
    assert api.last_json() == {
        "label": "deploy",
        "scopes": ["vms:read"],
        "expires_in_secs": 60,
        "service": "ci",
        "team": "eng",
    }


async def test_component_keys_create_service_key_bound_to_a_member() -> None:
    api, _ = await _create(
        label="deploy", expires_in_secs=60, service="ci", member="alice"
    )
    assert api.last_json() == {
        "label": "deploy",
        "expires_in_secs": 60,
        "service": "ci",
        "member": "alice",
    }


async def test_component_keys_create_team_key() -> None:
    api, _ = await _create(label="t", expires_in_secs=60, team="eng")
    assert api.last_json() == {"label": "t", "expires_in_secs": 60, "team": "eng"}


async def test_component_keys_unset_options_are_absent_not_null() -> None:
    api, _ = await _create(label="mine")
    # no scopes = the server's default set; none of the options travel as null
    assert api.last_json() == {"label": "mine"}


async def test_component_keys_create_refuses_a_misspelt_option() -> None:
    api = Api()
    with pytest.raises(TypeError, match="no field service_key"):
        await Keys(_t(api)).create(label="x", service_key="ci")
    assert api.seen == []


async def test_component_keys_list_service_keys() -> None:
    api = (
        Api()
        .on("GET", "/api/whoami", (200, WHOAMI))
        .on("GET", "/api/api-keys", (200, [SERVICE_SUMMARY]))
    )
    keys = Keys(_t(api))
    listed = await keys.list(service=True)
    assert api.last.url.params.get("service") == "true"
    assert "team" not in api.last.url.params
    assert isinstance(listed[0], KeySummary)
    assert (listed[0].subject_type, listed[0].bound_team) == ("service", "eng")
    await keys.list()
    assert dict(api.last.url.params) == {}


# -- the service options refuse a server older than service keys --------------------------------
# An older server ignores ``service`` and ``member``: it would mint a personal or team key and list
# the caller's own keys, and the reply does not say so. So the SDK reads the server's version from
# a probe of its own first, and sends nothing unless it is at least SERVICE_KEYS_MIN_API_VERSION.


def _sent(api: Api) -> list[tuple[str, str]]:
    return [(r.method, r.url.path) for r in api.seen]


def test_component_keys_service_keys_min_api_version_is_exported() -> None:
    assert cove_sdk.SERVICE_KEYS_MIN_API_VERSION == 6
    assert "SERVICE_KEYS_MIN_API_VERSION" in cove_sdk.__all__


SERVICE_CALLS: list[dict[str, Any]] = [
    {"fields": {"label": "d", "expires_in_secs": 60, "service": "ci", "team": "eng"}},
    {"fields": {"label": "d", "expires_in_secs": 60, "service": "ci", "member": "a"}},
    {"fields": {"label": "d", "expires_in_secs": 60, "member": "a"}},
    # an empty name is still a name given: the server, not the SDK, judges it
    {"fields": {"label": "d", "expires_in_secs": 60, "service": "", "team": "eng"}},
    {"fields": {"label": "d", "expires_in_secs": 60, "member": ""}},
    {"body": {"label": "d", "expires_in_secs": 60, "service": "ci", "team": "eng"}},
    {"body": CreateKeyRequest(label="d", expires_in_secs=60, service="ci", member="a")},
]


async def _call_create(keys: Keys, call: dict[str, Any]) -> CreatedKey:
    if "body" in call:
        return await keys.create(call["body"])
    return await keys.create(**call["fields"])


# Loops, not parametrize: conftest marks coroutine tests for anyio after parametrization.
async def test_component_keys_service_create_probes_then_sends_on_v6() -> None:
    for call in SERVICE_CALLS:
        api = (
            Api()
            .on("GET", "/api/whoami", (200, WHOAMI), headers={"x-cove-api-version": "6"})
            .on("POST", "/api/api-keys", (201, CREATED))
        )
        await _call_create(Keys(_t(api)), call)
        assert _sent(api) == [("GET", "/api/whoami"), ("POST", "/api/api-keys")], call


# (name, probe status, probe headers): each must refuse the service options.
OLD_SERVERS: list[tuple[str, int, dict[str, str]]] = [
    ("v5", 200, {"x-cove-api-version": "5"}),
    ("zero", 200, {"x-cove-api-version": "0"}),
    ("missing", 200, {}),
    ("unreadable", 200, {"x-cove-api-version": "six"}),
    ("probe 500", 500, {"x-cove-api-version": "6"}),
]


def _old_server(name: str, status: int, headers: dict[str, str], route: tuple[str, Any]) -> Api:
    body = WHOAMI if status < 300 else {"error": "boom"}
    return (
        Api()
        .on("GET", "/api/whoami", (status, body), headers=headers)
        .on(route[0], "/api/api-keys", route[1])
    )


# The old version also trips the transport's once-per-client skew warning; not under test here.
@pytest.mark.filterwarnings("ignore::cove_sdk.CoveApiVersionWarning")
async def test_component_keys_service_create_refused_below_v6() -> None:
    for name, status, headers in OLD_SERVERS:
        for call in SERVICE_CALLS:
            api = _old_server(name, status, headers, ("POST", (201, CREATED)))
            with pytest.raises(CoveError, match="nothing was sent"):
                await _call_create(Keys(_t(api)), call)
            assert _sent(api) == [("GET", "/api/whoami")], (name, call)


# The old version also trips the transport's once-per-client skew warning; not under test here.
@pytest.mark.filterwarnings("ignore::cove_sdk.CoveApiVersionWarning")
async def test_component_keys_service_list_refused_below_v6() -> None:
    for name, status, headers in OLD_SERVERS:
        api = _old_server(name, status, headers, ("GET", (200, [SERVICE_SUMMARY])))
        with pytest.raises(CoveError, match="nothing was sent"):
            await Keys(_t(api)).list(service=True)
        assert _sent(api) == [("GET", "/api/whoami")], name


async def test_component_keys_service_options_refused_when_the_probe_cannot_connect() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        raise httpx.ConnectError("refused", request=request)

    keys = Keys(
        AsyncCoveTransport(
            "https://h", auth=BearerAuth("cvk_t"), transport=httpx.MockTransport(handler)
        )
    )
    with pytest.raises(CoveError, match="nothing was sent"):
        await keys.create(label="d", expires_in_secs=60, service="ci", team="eng")
    with pytest.raises(CoveError, match="nothing was sent"):
        await keys.list(service=True)
    assert [r.url.path for r in seen] == ["/api/whoami", "/api/whoami"]


async def test_component_keys_service_probe_reads_its_own_response_not_an_earlier_one() -> None:
    # an earlier v6 reply leaves the transport's last-seen version at 6; the probe's own
    # header-less reply must still refuse
    api = (
        Api()
        .on("GET", "/api/api-keys", (200, []))
        .on("GET", "/api/whoami", (200, WHOAMI), headers={})
    )
    keys = Keys(_t(api))
    await keys.list()
    with pytest.raises(CoveError, match="nothing was sent"):
        await keys.list(service=True)
    assert _sent(api) == [("GET", "/api/api-keys"), ("GET", "/api/whoami")]


async def test_component_keys_service_probe_takes_the_call_timeout() -> None:
    api = (
        Api()
        .on("GET", "/api/whoami", (200, WHOAMI))
        .on("POST", "/api/api-keys", (201, CREATED))
    )
    await Keys(_t(api)).create(
        label="d", expires_in_secs=60, service="ci", team="eng", timeout=7.0
    )
    assert api.seen[0].url.path == "/api/whoami"
    assert api.seen[0].extensions["timeout"]["read"] == 7.0


async def test_component_keys_non_service_calls_send_no_probe() -> None:
    api = (
        Api()
        .on("POST", "/api/api-keys", (201, CREATED))
        .on("GET", "/api/api-keys", (200, []))
    )
    keys = Keys(_t(api))
    await keys.create(label="mine")
    await keys.create(label="ops", scopes=["admin"], expires_in_secs=60, admin_key=True)
    await keys.create(label="t", expires_in_secs=60, team="eng")
    await keys.create({"label": "n", "service": None, "member": None})
    await keys.list()
    await keys.list(team="eng")
    await keys.list(service=False)
    assert "/api/whoami" not in [r.url.path for r in api.seen]
    assert len(api.seen) == 7
