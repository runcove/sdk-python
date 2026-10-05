"""secrets (bound scopes), keys, webhooks and meta round-trips (mirrored to the sync client by unasync)."""

from typing import Any

import pytest
from mockapi import UUID1, UUID2, Api

from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.keys import Keys
from cove_sdk._async.resources.meta import Meta
from cove_sdk._async.resources.secrets import (
    ProjectSecrets,
    Secrets,
    TeamSecrets,
    UserSecrets,
    VmSecrets,
)
from cove_sdk._async.resources.webhooks import Webhooks
from cove_sdk._generated.models import (
    BuildInfo,
    CliStatusResponse,
    CreatedKey,
    HealthResponse,
    ImportResponse,
    KeySummary,
    ProfileSummary,
    ReplayWebhookDeliveryResponse,
    RotateSummary,
    RotateWebhookSecretResponse,
    ScopedImportResult,
    SecretEntryDto,
    SshKey,
    VmCountResult,
    WebhookDelivery,
    WebhookDeliveryPage,
    WebhookSubscription,
    WhoamiResponse,
)
from cove_sdk._generated.models import (
    TestDeliveryResult as DeliveryTestResult,  # a Test* name pytest would try to collect
)
from cove_sdk._operations import wrapped_operations
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError


def _t(api: Api) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
    )


SECRET_BODY = {"value_b64": "aGk=", "exposure": "env"}
KEY = {
    "created_at": "2026-10-01T00:00:00Z",
    "id": "k1",
    "label": "ci",
    "raw_token": "cvk_x",
    "scopes": ["vms:read"],
}
HOOK = {
    "consec_fail_count": 0,
    "created_at": "2026-10-01T00:00:00Z",
    "events": ["vm.created"],
    "id": UUID1,
    "owner_username": "u",
    "scope": {"scope": "server"},
    "url": "https://hook",
}


def _delivery(did: str) -> dict[str, Any]:
    return {
        "attempt": 1,
        "ce_id": UUID1,
        "ce_time": "2026-10-01T00:00:00Z",
        "created_at": "2026-10-01T00:00:00Z",
        "delivery_id": did,
        "event_kind": "vm.created",
        "retry_at": 0,
        "state": "delivered",
        "subscription_id": UUID1,
    }


# -- secrets -------------------------------------------------------------------------------------


async def test_component_secrets_vm_scope() -> None:
    api = (
        Api()
        .on("GET", "/api/vms/v/secrets", (200, [{"name": "A"}]))
        .on("POST", "/api/vms/v/secrets/A", None)
        .on("DELETE", "/api/vms/v/secrets/A", (200, {"vm_count": 1}))
        .on("POST", "/api/vms/v/secrets/A/rotate", (200, {"vm_count": 1}))
        .on("POST", "/api/vms/v/secrets/import", (200, {"imported": 2}))
    )
    scope = Secrets(_t(api)).vm("v")
    assert isinstance(scope, VmSecrets)
    listed = await scope.list()
    assert isinstance(listed[0], SecretEntryDto) and listed[0].name == "A"
    assert await scope.set("A", **SECRET_BODY) is None
    assert (api.last.method, api.last_json()) == ("POST", SECRET_BODY)
    unset = await scope.unset("A")
    assert api.last.method == "DELETE" and isinstance(unset, RotateSummary)
    rotated = await scope.rotate("A", value_b64="aGk=")
    assert api.last_json() == {"value_b64": "aGk="} and isinstance(
        rotated, RotateSummary
    )
    entries = [{"name": "A", "value": "hi"}]
    imported = await scope.import_(entries=entries)
    assert api.last_json() == {"entries": entries}
    assert isinstance(imported, ImportResponse) and imported.imported == 2


SCOPED = [
    ("user", "alice", "/api/users/alice"),
    ("team", "core", "/api/teams/core"),
    ("project", "p1", "/api/projects/p1"),
]


async def test_component_secrets_scoped_subjects() -> None:
    for kind, subject, base in SCOPED:
        await _scoped_round_trip(kind, subject, base)


async def _scoped_round_trip(kind: str, subject: str, base: str) -> None:
    api = (
        Api()
        .on("GET", f"{base}/secrets", (200, [{"name": "A"}]))
        .on("POST", f"{base}/secrets/A", (200, {"vm_count": 3}))
        .on("DELETE", f"{base}/secrets/A", (200, {"vm_count": 3}))
        .on("POST", f"{base}/secrets/A/rotate", (200, {"vm_count": 3}))
        .on("POST", f"{base}/secrets/import", (200, {"imported": 1, "vm_count": 3}))
    )
    scope = getattr(Secrets(_t(api)), kind)(subject)
    assert [s.name for s in await scope.list()] == ["A"]
    set_result = await scope.set("A", value_b64="aGk=")
    assert isinstance(set_result, VmCountResult) and set_result.vm_count == 3
    assert (api.last.method, api.last.url.path) == ("POST", f"{base}/secrets/A")
    assert isinstance(await scope.unset("A"), RotateSummary)
    assert api.last.method == "DELETE"
    assert isinstance(await scope.rotate("A", {"value_b64": "aGk="}), RotateSummary)
    assert api.last.url.path == f"{base}/secrets/A/rotate"
    imported = await scope.import_({"entries": []})
    assert isinstance(imported, ScopedImportResult) and imported.vm_count == 3
    assert [r.url.path for r in api.seen] == [
        f"{base}/secrets",
        f"{base}/secrets/A",
        f"{base}/secrets/A",
        f"{base}/secrets/A/rotate",
        f"{base}/secrets/import",
    ]


async def test_component_secrets_refuse_dot_segments_before_sending() -> None:
    api = Api()
    secrets = Secrets(_t(api))
    for bind in (secrets.vm, secrets.user, secrets.team, secrets.project):
        with pytest.raises(CoveError, match="path segment"):
            bind("..")
    with pytest.raises(CoveError, match="path segment"):
        await secrets.user("alice").set(".", value_b64="aGk=")
    assert api.seen == []


def test_component_secrets_scopes_are_reachable_by_the_coverage_walker() -> None:
    assert Secrets.__cove_scopes__ == (
        VmSecrets,
        UserSecrets,
        TeamSecrets,
        ProjectSecrets,
    )
    ops = wrapped_operations(Secrets)
    assert len(ops) == 20
    assert {"deleteVmSecret", "unsetUserSecret", "importProjectSecrets"} <= ops


# -- keys ----------------------------------------------------------------------------------------


async def test_component_keys_round_trips() -> None:
    summary = {**KEY, "key_prefix": "cvk_ab", "status": "active"}
    del summary["raw_token"]
    api = (
        Api()
        .on("GET", "/api/api-keys", (200, [summary]))
        .on("POST", "/api/api-keys", (201, KEY))
        .on("DELETE", "/api/api-keys/k1", None)
        .on("POST", "/api/api-keys/k1/rotate", (200, KEY))
    )
    keys = Keys(_t(api))
    listed = await keys.list(team="core")
    assert api.query() == {"team": "core"} and isinstance(listed[0], KeySummary)
    created = await keys.create(label="ci", scopes=["vms:read"], expires_in_secs=60)
    assert api.last_json() == {
        "label": "ci",
        "scopes": ["vms:read"],
        "expires_in_secs": 60,
    }
    assert isinstance(created, CreatedKey) and created.raw_token == "cvk_x"
    assert await keys.revoke("k1") is None
    assert (api.last.method, api.last.url.path) == ("DELETE", "/api/api-keys/k1")
    rotated = await keys.rotate("k1")
    assert api.last.method == "POST" and isinstance(rotated, CreatedKey)


# -- webhooks ------------------------------------------------------------------------------------


async def test_component_webhooks_subscription_round_trips() -> None:
    base = f"/api/webhooks/{UUID1}"
    api = (
        Api()
        .on("GET", "/api/webhooks", (200, [HOOK]))
        .on("POST", "/api/webhooks", (201, HOOK))
        .on("GET", base, (200, HOOK))
        .on("PUT", base, (200, {**HOOK, "url": "https://new"}))
        .on("DELETE", base, None)
        .on(
            "POST",
            f"{base}/rotate",
            (200, {"rotated_at": "2026-10-01T00:00:00Z", "secret": "whsec_n"}),
        )
        .on(
            "POST",
            f"{base}/test",
            (200, {"delivery_id": UUID2, "sig_header": "v1,x", "state": "delivered"}),
        )
        .on("POST", f"{base}/disable", (200, HOOK))
        .on("POST", f"{base}/enable", (200, HOOK))
    )
    hooks = Webhooks(_t(api))
    listed = await hooks.list(scope="server")
    assert api.query() == {"scope": "server"} and isinstance(
        listed[0], WebhookSubscription
    )
    made = await hooks.create(events=["vm.created"], scope="server", url="https://hook")
    assert api.last_json() == {
        "events": ["vm.created"],
        "scope": "server",
        "url": "https://hook",
    }
    assert str(made.id) == UUID1
    assert str((await hooks.get(UUID1)).id) == UUID1
    updated = await hooks.update(UUID1, url="https://new")
    assert (api.last.method, api.last_json(), updated.url) == (
        "PUT",
        {"url": "https://new"},
        "https://new",
    )
    assert await hooks.delete(UUID1) is None
    assert api.last.method == "DELETE"
    rotated = await hooks.rotate_secret(UUID1)
    assert (
        isinstance(rotated, RotateWebhookSecretResponse) and rotated.secret == "whsec_n"
    )
    tested = await hooks.test(UUID1)
    assert isinstance(tested, DeliveryTestResult) and tested.state == "delivered"
    assert isinstance(await hooks.disable(UUID1), WebhookSubscription)
    assert api.last.url.path == f"{base}/disable"
    assert isinstance(await hooks.enable(UUID1), WebhookSubscription)
    assert api.last.url.path == f"{base}/enable"
    with pytest.raises(CoveError, match="path segment"):
        await hooks.get("..")


async def test_component_webhooks_deliveries() -> None:
    base = f"/api/webhooks/{UUID1}/deliveries"
    api = (
        Api()
        .on(
            "GET",
            base,
            (200, {"deliveries": [_delivery(UUID1)], "next_cursor": "c1"}),
            (200, {"deliveries": [_delivery(UUID2)], "next_cursor": None}),
            (200, {"deliveries": [], "next_cursor": None}),
        )
        .on("GET", f"{base}/{UUID2}", (200, _delivery(UUID2)))
        .on("POST", f"{base}/{UUID2}/replay", (202, {"new_delivery_id": UUID1}))
    )
    hooks = Webhooks(_t(api))
    got = [
        str(d.delivery_id) async for d in hooks.iter_deliveries(UUID1, state="failed")
    ]
    assert got == [UUID1, UUID2]
    assert [dict(r.url.params) for r in api.seen] == [
        {"state": "failed"},
        {"state": "failed", "cursor": "c1"},
    ]
    page = await hooks.list_deliveries(UUID1, limit=5)
    assert api.query() == {"limit": "5"} and isinstance(page, WebhookDeliveryPage)
    one = await hooks.get_delivery(UUID1, UUID2)
    assert isinstance(one, WebhookDelivery) and str(one.delivery_id) == UUID2
    replay = await hooks.replay_delivery(UUID1, UUID2)
    assert api.last.method == "POST" and isinstance(
        replay, ReplayWebhookDeliveryResponse
    )
    assert str(replay.new_delivery_id) == UUID1


# -- meta ----------------------------------------------------------------------------------------


async def test_component_meta_round_trips() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/health",
            (
                200,
                {
                    "pool_available": 1,
                    "status": "ok",
                    "uptime_secs": 5,
                    "vms_running": 2,
                },
            ),
        )
        .on(
            "GET",
            "/api/version",
            (200, {"built_at": "t", "commit": "c", "name": "cove", "version": "1.0.0"}),
        )
        .on("GET", "/api/whoami", (200, {"username": "alice"}))
        .on(
            "GET",
            "/api/me",
            (
                200,
                {
                    "active_cli_ticket_count": 0,
                    "key_count": 1,
                    "keys_managed": False,
                    "ldap_linked": False,
                    "roles": ["user"],
                    "username": "alice",
                },
            ),
        )
        .on(
            "GET",
            "/api/me/keys",
            (200, [{"abbreviated": "ssh-ed25519 AAA…", "id": "s1", "label": "laptop"}]),
        )
        .on("GET", "/api/me/cli-status", (200, {"has_cli_ticket": True}))
    )
    meta = Meta(_t(api))
    health = await meta.health()
    assert isinstance(health, HealthResponse) and health.status == "ok"
    version = await meta.version()
    assert isinstance(version, BuildInfo) and version.version == "1.0.0"
    who = await meta.whoami()
    assert isinstance(who, WhoamiResponse) and who.username == "alice"
    me = await meta.me()
    assert isinstance(me, ProfileSummary) and me.roles == ["user"]
    keys = await meta.me_keys()
    assert isinstance(keys[0], SshKey) and keys[0].label == "laptop"
    status = await meta.cli_status()
    assert isinstance(status, CliStatusResponse) and status.has_cli_ticket
    assert [r.url.path for r in api.seen] == [
        "/api/health",
        "/api/version",
        "/api/whoami",
        "/api/me",
        "/api/me/keys",
        "/api/me/cli-status",
    ]
