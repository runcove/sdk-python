"""checkpoints, policies, host, tags and audit round-trips (mirrored to the sync client by unasync)."""

from typing import Any

import pytest
from mockapi import UUID1, Api

from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.audit import Audit
from cove_sdk._async.resources.checkpoints import Checkpoints
from cove_sdk._async.resources.host import Host
from cove_sdk._async.resources.policies import Policies
from cove_sdk._async.resources.tags import Tags
from cove_sdk._generated.models import (
    AdmissionStatus,
    AuditEntry,
    AuditPage,
    CapacityReport,
    Checkpoint,
    CheckpointPage,
    HostTelemetrySeries,
    IdleState,
    ImagesResponse,
    ReservationRef,
    SystemStatus,
    TagEntry,
    TagSummary,
    TtlPolicyView,
)
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError


def _t(api: Api) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
    )


def _cp(cid: str) -> dict[str, Any]:
    return {
        "created_at": "2026-10-01T00:00:00Z",
        "id": cid,
        "owner_username": "u",
        "state": "available",
        "vm_id": "id",
    }


CAPACITY = {
    "active_vms": 1,
    "cpu": {
        "cpu_ratio": 1.0,
        "headroom_vcpus": 4,
        "host_cores": 8,
        "reservation_vcpus": 0,
    },
    "disk": {
        "fs_available_bytes": 1,
        "fs_total_bytes": 2,
        "fs_used_bytes": 1,
        "soft_limit_pct": 90,
    },
    "max_vms": 10,
    "ram": {
        "headroom_mb": 1,
        "host_total_mb": 2,
        "mem_available_mb": 3,
        "pending_resize_mb": 0,
        "psi_mem_avg10_pct": 0.0,
        "ratio": 1.0,
        "reservation_mb": 0,
        "reserved_mb": 0,
        "swap_total_mb": 0,
        "swap_used_mb": 0,
    },
    "reservations": [],
}
RESERVATION = {
    "disk_bytes": 1,
    "flow_id": "f1",
    "id": UUID1,
    "kind": "create",
    "memory_mb": 512,
    "ttl_expires_ms": 1,
    "vcpus": 1,
}


# -- checkpoints ---------------------------------------------------------------------------------


async def test_component_checkpoints_round_trips() -> None:
    api = (
        Api()
        .on("POST", "/api/vms/v/checkpoints", (200, _cp("c1")))
        .on(
            "GET",
            "/api/vms/v/checkpoints",
            (200, {"checkpoints": [_cp("c1")], "next_cursor": None}),
        )
        .on("GET", "/api/checkpoints/c1", (200, _cp("c1")))
        .on("DELETE", "/api/checkpoints/c1", None)
        .on("POST", "/api/vms/v/hibernate", (200, _cp("c2")))
    )
    cps = Checkpoints(_t(api))
    made = await cps.create("v", description="before upgrade")
    assert api.last_json() == {"description": "before upgrade"}
    assert isinstance(made, Checkpoint) and made.id == "c1"
    await cps.create("v")
    assert api.last_json() == {}
    page = await cps.list_for_vm("v", limit=5)
    assert api.query() == {"limit": "5"}
    assert isinstance(page, CheckpointPage) and page.checkpoints[0].id == "c1"
    got = await cps.get("c1")
    assert (api.last.method, api.last.url.path, got.id) == (
        "GET",
        "/api/checkpoints/c1",
        "c1",
    )
    assert await cps.delete("c1") is None
    assert api.last.method == "DELETE"
    hib = await cps.hibernate("v")
    assert (api.last.method, hib.id) == ("POST", "c2")
    with pytest.raises(CoveError):
        await cps.get("..")


async def test_component_checkpoints_list_all_and_iterators() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/checkpoints",
            (200, {"checkpoints": [_cp("a")], "next_cursor": "c1"}),
            (200, {"checkpoints": [_cp("b")], "next_cursor": None}),
            (200, {"checkpoints": [_cp("z")], "next_cursor": None}),
        )
        .on(
            "GET",
            "/api/vms/v/checkpoints",
            (200, {"checkpoints": [_cp("x")], "next_cursor": "k"}),
            (200, {"checkpoints": [_cp("y")], "next_cursor": None}),
        )
    )
    cps = Checkpoints(_t(api))
    assert [c.id async for c in cps.iter_all(limit=1)] == ["a", "b"]
    assert [dict(r.url.params) for r in api.seen] == [
        {"limit": "1"},
        {"limit": "1", "cursor": "c1"},
    ]
    page = await cps.list_all(cursor="q")
    assert api.query() == {"cursor": "q"} and page.checkpoints[0].id == "z"
    assert [c.id async for c in cps.iter_for_vm("v", cursor="k0")] == ["x", "y"]
    assert [dict(r.url.params) for r in api.seen[-2:]] == [
        {"cursor": "k0"},
        {"cursor": "k"},
    ]


# -- policies ------------------------------------------------------------------------------------


async def test_component_policies_round_trips() -> None:
    api = (
        Api()
        .on("POST", "/api/vms/v/auto-pause", None)
        .on("GET", "/api/vms/v/idle-state", (200, {"kind": {"type": "active"}}))
        .on("POST", "/api/vms/v/expiry", None)
        .on("GET", "/api/vms/v/expiry", (200, {"policy": {"max_lifetime_secs": 3600}}))
    )
    pol = Policies(_t(api))
    assert (
        await pol.set_auto_pause("v", {"type": "auto_pause", "idle_timeout_secs": 600})
        is None
    )
    assert api.last_json() == {
        "policy": {"type": "auto_pause", "idle_timeout_secs": 600}
    }
    idle = await pol.get_idle_state("v")
    assert isinstance(idle, IdleState)
    assert await pol.set_expiry("v", {"max_lifetime_secs": 3600}) is None
    assert (api.last.method, api.last_json()) == (
        "POST",
        {"policy": {"max_lifetime_secs": 3600}},
    )
    view = await pol.get_expiry("v")
    assert isinstance(view, TtlPolicyView) and view.policy.max_lifetime_secs == 3600


# -- host ----------------------------------------------------------------------------------------


async def test_component_host_round_trips() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/system/status",
            (
                200,
                {
                    "ch_processes": 1,
                    "memory_total_mb": 2,
                    "memory_used_mb": 1,
                    "paused": 0,
                    "pool": [],
                    "running": 1,
                    "stopped": 0,
                    "tap_devices": 1,
                },
            ),
        )
        .on("GET", "/api/host/capacity-check", (200, {"capacity": CAPACITY}))
        .on("GET", "/api/host/capacity", (200, CAPACITY))
        .on("POST", "/api/host/reservations", (200, RESERVATION))
        .on("DELETE", f"/api/host/reservations/{UUID1}", None)
        .on("GET", "/api/host/telemetry", (200, {}))
        .on("GET", "/api/images", (200, {"images": [], "oci_cache": []}))
    )
    host = Host(_t(api))
    status = await host.system_status()
    assert isinstance(status, SystemStatus) and status.ch_processes == 1
    assert isinstance(await host.capacity_check(), AdmissionStatus)
    cap = await host.capacity()
    assert isinstance(cap, CapacityReport) and cap.max_vms == 10
    action = {"type": "create", "disk_bytes": 1, "memory_min_mb": 512, "vcpus_min": 1}
    ref = await host.reserve(action=action, flow_id="f1")
    assert api.last_json() == {"action": action, "flow_id": "f1"}
    assert isinstance(ref, ReservationRef) and ref.flow_id == "f1"
    assert await host.release_reservation(UUID1) is None
    assert (api.last.method, api.last.url.path) == (
        "DELETE",
        f"/api/host/reservations/{UUID1}",
    )
    tel = await host.telemetry(from_=1767225600, limit=3)
    assert api.query() == {"from": "1767225600", "limit": "3"}
    assert isinstance(tel, HostTelemetrySeries)
    assert isinstance(await host.images(), ImagesResponse)


# -- tags ----------------------------------------------------------------------------------------


async def test_component_tags_delete_says_whether_the_key_existed() -> None:
    # API version 7: a tag delete answers whether the key was set.
    api = Api().on("DELETE", "/api/vms/v/tags/typo", (200, {"existed": False}))
    out = await Tags(_t(api)).delete("v", "typo")
    assert out is not None and out.existed is False


async def test_component_tags_round_trips() -> None:
    entry = {
        "key": "env",
        "set_at": "2026-10-01T00:00:00Z",
        "set_by": "u",
        "value": "prod",
    }
    api = (
        Api()
        .on("GET", "/api/vms/v/tags", (200, [entry]))
        .on("PUT", "/api/vms/v/tags/env", None)
        .on("DELETE", "/api/vms/v/tags/env", None)
        .on(
            "GET",
            "/api/tags",
            (
                200,
                [
                    {
                        "distinct_values": 1,
                        "key": "env",
                        "sample_vms": ["v"],
                        "vm_count": 1,
                    }
                ],
            ),
        )
        .on("PUT", "/api/vms/v/team", None)
        .on("DELETE", "/api/vms/v/team", None)
    )
    tags = Tags(_t(api))
    listed = await tags.list_for_vm("v")
    assert isinstance(listed[0], TagEntry) and listed[0].value == "prod"
    assert await tags.set("v", "env", "prod") is None
    assert (api.last.method, api.last_json()) == ("PUT", {"value": "prod"})
    assert await tags.delete("v", "env") is None
    assert (api.last.method, api.last.url.path) == ("DELETE", "/api/vms/v/tags/env")
    summary = await tags.list_all()
    assert isinstance(summary[0], TagSummary) and summary[0].vm_count == 1
    assert await tags.set_team("v", "core") is None
    assert (api.last.method, api.last_json()) == ("PUT", {"team": "core"})
    assert await tags.unset_team("v") is None
    assert (api.last.method, api.last.url.path) == ("DELETE", "/api/vms/v/team")
    with pytest.raises(CoveError):
        await tags.set("v", "..", "x")
    assert len(api.seen) == 6


# -- audit ---------------------------------------------------------------------------------------


async def test_component_audit_list_and_iter() -> None:
    def entry(i: int) -> dict[str, Any]:
        return {
            "actor_kind": "user",
            "at": "2026-10-01T00:00:00Z",
            "event_kind": "vm.created",
            "event_payload": {},
            "id": i,
        }

    api = Api().on(
        "GET",
        "/api/audit",
        (200, {"entries": [entry(1)], "next_cursor": "c1"}),
        (200, {"entries": [entry(2)], "next_cursor": None}),
        (200, {"entries": [entry(3)], "next_cursor": None}),
    )
    audit = Audit(_t(api))
    got = [e async for e in audit.iter(vm="v", kind="vm.created")]
    assert [e.id for e in got] == [1, 2] and isinstance(got[0], AuditEntry)
    assert [dict(r.url.params) for r in api.seen] == [
        {"vm": "v", "kind": "vm.created"},
        {"vm": "v", "kind": "vm.created", "cursor": "c1"},
    ]
    page = await audit.list(
        user="u", key_id="k", source_ip="1.2.3.4", since="s", until="t", limit=1
    )
    assert api.query() == {
        "user": "u",
        "key_id": "k",
        "source_ip": "1.2.3.4",
        "since": "s",
        "until": "t",
        "limit": "1",
    }
    assert isinstance(page, AuditPage) and page.entries[0].id == 3
