"""client.admin round-trips (mirrored to the sync client by unasync)."""

from typing import Any

import httpx
import pytest
from mockapi import HEADERS, Api

from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.admin import Admin
from cove_sdk._generated.models import (
    AdminBulkVmResponse,
    AdminCheckpointSummary,
    AdminCheckpointSummaryPage,
    AdminDrainResponse,
    AdminForceCreateResponse,
    AdminHostStateResponse,
    AdminQuotaDefaultsResponse,
    AdminQuotaOverrideResponse,
    AdminRetimeoutResponse,
    AdminTeamQuotaOverrideResponse,
    AdminUserSummary,
    AdminVmSummary,
    AdminVmSummaryPage,
    ProjectMember,
    RevokeSessionsResponse,
    UpdateAgentsResponse,
)
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError, NotFoundError, PermissionDeniedError


def _t(api: Api) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
    )


def _vm(name: str) -> dict[str, Any]:
    return {
        "created_at": "2026-10-01T00:00:00Z",
        "image": "fedora-43",
        "state": "running",
        "updated_at": "2026-10-01T00:00:00Z",
        "vm_id": f"id-{name}",
        "vm_name": name,
    }


def _cp(cid: str) -> dict[str, Any]:
    return {
        "checkpoint_id": cid,
        "created_at": "2026-10-01T00:00:00Z",
        "owner_username": "u",
        "state": "available",
    }


USER = {
    "created_at": "2026-10-01T00:00:00Z",
    "last_seen_at": "2026-10-01T00:00:00Z",
    "usage": {
        "disk_gb": {"current": 10, "max": 100},
        "ram_mb": {"current": 2048, "max": 8192},
        "vcpus": {"current": 2, "max": 8},
        "vm_count": {"current": 1, "max": 5},
    },
    "username": "alice",
}
BULK = {
    "attempted": 2,
    "dry_run": True,
    "failed": 0,
    "scope": {"type": "user", "username": "alice"},
    "succeeded": 2,
    "targets": [],
}


# -- fleet and host ------------------------------------------------------------------------------


async def test_component_admin_fleet_and_host_round_trips() -> None:
    api = (
        Api()
        .on(
            "POST",
            "/api/admin/auto-pause/retimeout",
            (
                200,
                {
                    "by_current_value": {"600": 3, "1800": 1},
                    "changed": [],
                    "dry_run": True,
                    "skipped_custom": [],
                    "target_secs": 900,
                    "total_auto_pause": 4,
                },
            ),
        )
        .on(
            "POST",
            "/api/admin/drain",
            (
                200,
                {
                    "attempted": 3,
                    "budget_secs": 30,
                    "failed": 0,
                    "succeeded": 3,
                    "targets": [],
                    "timed_out": 0,
                },
            ),
        )
        .on(
            "GET",
            "/api/admin/host-state",
            (
                200,
                {
                    "audit_emit_failed_total": 0,
                    "broadcast_lag": [],
                    "orphaned_checkpoint_bytes": 0,
                    "orphaned_checkpoint_count": 2,
                    "snapshot_images": [],
                    "ttl_pending_count": 0,
                },
            ),
        )
        .on("POST", "/api/admin/vms/delete-bulk", (200, BULK))
        .on("POST", "/api/admin/vms/stop-bulk", (200, {**BULK, "dry_run": False}))
    )
    admin = Admin(_t(api))
    re = await admin.update_auto_pause_timeouts(
        from_secs=600, to_secs=900, dry_run=True
    )
    assert api.last_json() == {"from_secs": 600, "to_secs": 900, "dry_run": True}
    assert isinstance(re, AdminRetimeoutResponse) and re.target_secs == 900
    assert re.by_current_value.to_dict() == {"600": 3, "1800": 1}

    drained = await admin.drain_host(budget_secs=30)
    assert (api.last.method, api.query()) == ("POST", {"budget_secs": "30"})
    assert isinstance(drained, AdminDrainResponse) and drained.succeeded == 3
    await admin.drain_host()
    assert api.query() == {}

    state = await admin.host_state()
    assert isinstance(state, AdminHostStateResponse)
    assert state.orphaned_checkpoint_count == 2

    deleted = await admin.bulk_delete_vms(
        scope={"type": "user", "username": "alice"}, dry_run=True
    )
    assert api.last.url.path == "/api/admin/vms/delete-bulk"
    assert api.last_json() == {
        "scope": {"type": "user", "username": "alice"},
        "dry_run": True,
    }
    assert isinstance(deleted, AdminBulkVmResponse) and deleted.attempted == 2
    stopped = await admin.bulk_stop_vms(scope={"type": "all"}, include_pool=True)
    assert api.last.url.path == "/api/admin/vms/stop-bulk"
    assert api.last_json() == {"scope": {"type": "all"}, "include_pool": True}
    assert stopped.dry_run is False


async def test_component_admin_drain_403_is_permission_denied() -> None:
    api = Api().on(
        "POST",
        "/api/admin/drain",
        (
            403,
            {"code": "scope_denied", "message": "no", "required": "admin:fleet:write"},
        ),
    )
    with pytest.raises(PermissionDeniedError):
        await Admin(_t(api)).drain_host()


async def test_component_admin_update_vm_agents_sends_the_exact_bytes() -> None:
    binary = b"\x7fELF\x02\x01\x01\x00" + bytes(range(256)) + b"{not json}"
    api = Api().on(
        "POST",
        "/api/admin/update-agents",
        (200, {"failed": 0, "results": [], "updated": 4}),
    )
    out = await Admin(_t(api)).update_vm_agents(binary)
    sent = api.last
    assert sent.method == "POST"
    assert sent.content == binary
    assert sent.headers["content-type"] == "application/octet-stream"
    assert isinstance(out, UpdateAgentsResponse) and out.updated == 4


# -- projects, quotas, users ---------------------------------------------------------------------


async def test_component_admin_project_members_round_trips() -> None:
    member = {
        "added_at": "2026-10-01T00:00:00Z",
        "added_by": "root",
        "project_id": "p1",
        "username": "alice",
    }
    api = (
        Api()
        .on("GET", "/api/admin/projects/p1/members", (200, [member]))
        .on("POST", "/api/admin/projects/p1/members", None)
        .on("DELETE", "/api/admin/projects/p1/members/alice", None)
    )
    admin = Admin(_t(api))
    members = await admin.list_project_members("p1")
    assert isinstance(members[0], ProjectMember) and members[0].username == "alice"
    assert await admin.add_project_member("p1", "alice") is None
    assert api.last_json() == {"project_id": "p1", "username": "alice"}
    assert await admin.remove_project_member("p1", "alice") is None
    assert api.last.method == "DELETE"
    with pytest.raises(CoveError):
        await admin.remove_project_member("p1", "..")
    with pytest.raises(CoveError):
        await admin.add_project_member(".", "alice")
    assert len(api.seen) == 3  # the refused calls sent nothing


async def test_component_admin_quota_round_trips() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/admin/quota-defaults",
            (
                200,
                {
                    "disk_gb_max": 100,
                    "ram_mb_max": 8192,
                    "vcpus_max": 8,
                    "vm_count_max": 5,
                },
            ),
        )
        .on(
            "GET",
            "/api/admin/quotas/alice",
            (200, {"username": "alice", "vcpus_max": 16}),
        )
        .on("PUT", "/api/admin/quotas/alice", None)
        .on("DELETE", "/api/admin/quotas/alice", None)
        .on(
            "POST",
            "/api/admin/quotas/alice/force-create",
            (
                200,
                {
                    "bypass_id": "b1",
                    "granted_at": "2026-10-01T00:00:00Z",
                    "granted_by": "root",
                    "username": "alice",
                },
            ),
        )
        .on(
            "GET",
            "/api/admin/team-quotas/t1",
            (200, {"team_id": "t1", "ram_mb_max": 4096}),
        )
        .on("PUT", "/api/admin/team-quotas/t1", None)
        .on("DELETE", "/api/admin/team-quotas/t1", None)
    )
    admin = Admin(_t(api))
    defaults = await admin.quota_defaults()
    assert isinstance(defaults, AdminQuotaDefaultsResponse) and defaults.vcpus_max == 8
    uq = await admin.get_user_quota("alice")
    assert isinstance(uq, AdminQuotaOverrideResponse) and uq.vcpus_max == 16
    assert await admin.set_user_quota("alice", vcpus_max=16, ram_mb_max=None) is None
    assert (api.last.method, api.last_json()) == (
        "PUT",
        {"vcpus_max": 16, "ram_mb_max": None},
    )
    assert await admin.delete_user_quota("alice") is None
    assert (api.last.method, api.last.url.path) == ("DELETE", "/api/admin/quotas/alice")
    bypass = await admin.grant_quota_bypass("alice")
    assert isinstance(bypass, AdminForceCreateResponse) and bypass.bypass_id == "b1"
    tq = await admin.get_team_quota("t1")
    assert isinstance(tq, AdminTeamQuotaOverrideResponse) and tq.ram_mb_max == 4096
    assert await admin.set_team_quota("t1", {"vm_count_max": 3}) is None
    assert (api.last.method, api.last_json()) == ("PUT", {"vm_count_max": 3})
    assert await admin.delete_team_quota("t1") is None
    assert (api.last.method, api.last.url.path) == (
        "DELETE",
        "/api/admin/team-quotas/t1",
    )
    with pytest.raises(TypeError):
        await admin.set_user_quota("alice", cpus=1)  # a misspelt field never travels
    with pytest.raises(CoveError):
        await admin.get_team_quota("..")


async def test_component_admin_users_round_trips() -> None:
    api = (
        Api()
        .on("GET", "/api/admin/users", (200, [USER]))
        .on("GET", "/api/admin/users/alice", (200, USER))
        .on("POST", "/api/admin/users/alice/revoke-sessions", (200, {"revoked": 2}))
    )
    api.routes[("GET", "/api/admin/users/bob")] = [
        httpx.Response(404, text="no such user", headers=HEADERS)
    ]
    admin = Admin(_t(api))
    users = await admin.list_users()
    assert isinstance(users[0], AdminUserSummary) and users[0].usage.vcpus.current == 2
    got = await admin.get_user("alice")
    assert got.username == "alice"
    revoked = await admin.revoke_user_sessions("alice")
    assert isinstance(revoked, RevokeSessionsResponse) and revoked.revoked == 2
    assert api.last.method == "POST"
    with pytest.raises(NotFoundError) as caught:
        await admin.get_user("bob")  # the contract's text/plain 404
    assert "no such user" in str(caught.value)


# -- every VM and checkpoint ---------------------------------------------------------------------


async def test_component_admin_vms_list_and_iter() -> None:
    api = Api().on(
        "GET",
        "/api/admin/vms",
        (200, {"vms": [_vm("a"), _vm("b")], "next_cursor": "c1"}),
        (200, {"vms": [_vm("c")], "next_cursor": None}),
        (200, {"vms": [_vm("z")], "next_cursor": None}),
    )
    admin = Admin(_t(api))
    names = [vm.vm_name async for vm in admin.iter_vms(user="alice", limit=2)]
    assert names == ["a", "b", "c"]
    assert [dict(r.url.params) for r in api.seen] == [
        {"user": "alice", "limit": "2"},
        {"user": "alice", "limit": "2", "cursor": "c1"},
    ]
    page = await admin.list_vms()
    assert api.query() == {}
    assert isinstance(page, AdminVmSummaryPage)
    assert isinstance(page.vms[0], AdminVmSummary) and page.vms[0].vm_name == "z"


async def test_component_admin_checkpoints_list_iter_and_delete() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/admin/checkpoints",
            (200, {"checkpoints": [_cp("a")], "next_cursor": "c1"}),
            (200, {"checkpoints": [_cp("b")], "next_cursor": None}),
            (200, {"checkpoints": [_cp("z")], "next_cursor": None}),
        )
        .on("DELETE", "/api/admin/checkpoints/a", None)
    )
    admin = Admin(_t(api))
    ids = [cp.checkpoint_id async for cp in admin.iter_checkpoints(orphaned=True)]
    assert ids == ["a", "b"]
    assert [dict(r.url.params) for r in api.seen] == [
        {"orphaned": "true"},
        {"orphaned": "true", "cursor": "c1"},
    ]
    page = await admin.list_checkpoints(user="bob", limit=1)
    assert api.query() == {"user": "bob", "limit": "1"}
    assert isinstance(page, AdminCheckpointSummaryPage)
    assert isinstance(page.checkpoints[0], AdminCheckpointSummary)
    assert await admin.delete_checkpoint("a") is None
    assert (api.last.method, api.last.url.path) == (
        "DELETE",
        "/api/admin/checkpoints/a",
    )
    with pytest.raises(CoveError):
        await admin.delete_checkpoint("..")
