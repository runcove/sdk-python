"""client.vms round-trips against a routed MockTransport (mirrored to the sync client by unasync)."""

from typing import Any

import pytest
from mockapi import UUID1, VM, Api

from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.vms import Vms
from cove_sdk._colour import monotonic
from cove_sdk._generated.models import (
    CloneResponse,
    ConnectionInfo,
    CreateVmRequest,
    CreateVmResponse,
    ExecOutputDto,
    ProxyInvite,
    ProxyPortInfo,
    ProxyUrlInfo,
    ResizeResult,
    VmConsole,
    VmDetail,
    VmEvent,
    VmProcess,
    VmStats,
    VmSummary,
    VmSummaryPage,
    VmTelemetrySeries,
)
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError, CoveTimeoutError, NotFoundError


def _vms(api: Api) -> Vms:
    return Vms(
        AsyncCoveTransport(
            "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
        )
    )


def _summary(name: str) -> dict[str, Any]:
    return {"image": "fedora-43", "name": name, "state": "running"}


PORT = {"is_primary": True, "port": 8080, "public": False, "url": "https://p"}
INVITE = {
    "expires_at": "2026-10-01T00:00:00Z",
    "invite_id": "inv1",
    "port": 8080,
    "url": "https://i",
    "vm_name": "v",
}
STATS = {
    "cpu_percent": 1.5,
    "disk_available_bytes": 1,
    "disk_usage_bytes": 2,
    "load_avg": [0.1, 0.2, 0.3],
    "memory_available_bytes": 3,
    "memory_cached_bytes": 4,
    "memory_free_bytes": 5,
    "memory_total_bytes": 6,
    "net_rx_bytes": 7,
    "net_tx_bytes": 8,
}


async def test_component_vms_list_sends_only_the_given_query() -> None:
    api = Api().on(
        "GET", "/api/vms", (200, {"vms": [_summary("a")], "next_cursor": None})
    )
    page = await _vms(api).list(state="running", limit=5)
    assert api.last.method == "GET" and api.query() == {
        "state": "running",
        "limit": "5",
    }
    assert isinstance(page, VmSummaryPage) and page.vms[0].name == "a"


async def test_component_vms_iter_walks_every_page() -> None:
    api = Api().on(
        "GET",
        "/api/vms",
        (200, {"vms": [_summary("a"), _summary("b")], "next_cursor": "c1"}),
        (200, {"vms": [_summary("c")], "next_cursor": None}),
    )
    names = [vm.name async for vm in _vms(api).iter(tag="team=x")]
    assert names == ["a", "b", "c"]
    assert [dict(r.url.params) for r in api.seen] == [
        {"tag": "team=x"},
        {"tag": "team=x", "cursor": "c1"},
    ]
    vm: Any = None
    async for vm in _vms(api).iter():
        break
    assert isinstance(vm, VmSummary)


async def test_component_vms_create_posts_initial_tags_as_a_map() -> None:
    api = Api().on("POST", "/api/vms", (202, {"name": "web"}))
    created = await _vms(api).create(name="web", initial_tags={"k": "v"})
    assert api.last.method == "POST" and api.last.url.path == "/api/vms"
    assert api.last_json() == {"name": "web", "initial_tags": {"k": "v"}}
    assert isinstance(created, CreateVmResponse) and created.name == "web"
    # the generated model and a plain mapping are the same request
    await _vms(api).create(CreateVmRequest(name="web", cpus=2))
    assert api.last_json() == {"name": "web", "cpus": 2}
    await _vms(api).create({"name": "web", "image": "fedora-43"})
    assert api.last_json() == {"name": "web", "image": "fedora-43"}


async def test_component_vms_create_refuses_an_unknown_field_before_sending() -> None:
    api = Api()
    with pytest.raises(TypeError, match="initial_tag"):
        await _vms(api).create(name="web", initial_tag={"k": "v"})
    with pytest.raises(TypeError, match="not both"):
        await _vms(api).create(CreateVmRequest(name="web"), cpus=2)
    assert api.seen == []


async def test_component_vms_get_encodes_the_name_as_one_segment() -> None:
    api = Api().on("GET", "/api/vms/web%201", (200, {**VM, "name": "web 1"}))
    vm = await _vms(api).get("web 1")
    assert api.last.url.raw_path == b"/api/vms/web%201"
    assert isinstance(vm, VmDetail) and vm.name == "web 1"


async def test_component_vms_dot_segments_are_refused_before_sending() -> None:
    api = Api()
    vms = _vms(api)
    for call in (
        lambda: vms.get(".."),
        lambda: vms.delete("."),
        lambda: vms.stop(""),
        lambda: vms.remove_port("v", ".."),  # type: ignore[arg-type]
        lambda: vms.revoke_invite("v", ".."),
        lambda: vms.exec_with_secrets("..", command=["true"], selector={"kind": "all"}),
    ):
        with pytest.raises(CoveError, match="path segment"):
            await call()
    assert api.seen == []


async def test_component_vms_get_maps_404() -> None:
    api = Api().on(
        "GET", "/api/vms/x", (404, {"error": "not found", "code": "vm_not_found"})
    )
    with pytest.raises(NotFoundError):
        await _vms(api).get("x")


async def test_component_vms_lifecycle_verbs_post_and_return_none() -> None:
    api = Api()
    api.on("POST", "/api/vms/v/stop", 202)
    for verb in ("start", "pause", "resume"):
        api.on("POST", f"/api/vms/v/{verb}", 200)
    api.on("DELETE", "/api/vms/v", 202)
    vms = _vms(api)
    assert await vms.stop("v") is None
    assert await vms.start("v") is None
    assert await vms.pause("v") is None
    assert await vms.resume("v") is None
    assert await vms.delete("v") is None
    assert [(r.method, r.url.path) for r in api.seen] == [
        ("POST", "/api/vms/v/stop"),
        ("POST", "/api/vms/v/start"),
        ("POST", "/api/vms/v/pause"),
        ("POST", "/api/vms/v/resume"),
        ("DELETE", "/api/vms/v"),
    ]


async def test_component_vms_wake_resize_clone_connect() -> None:
    api = (
        Api()
        .on("POST", "/api/vms/v/wake", None)
        .on(
            "POST",
            "/api/vms/v/resize",
            (200, {"actual_cpus": 4, "actual_memory_mb": 4096, "partial": False}),
        )
        .on(
            "POST",
            "/api/vms/src/clone",
            (200, {"fingerprints": ["f"], "new_vm": {**VM, "name": "dst"}}),
        )
        .on(
            "POST",
            "/api/vms/v/connect",
            (
                200,
                {
                    "bastion_host": "b",
                    "bastion_port": 22,
                    "bastion_ssh_host_pubkey": "k",
                    "ticket_secret": "t",
                },
            ),
        )
    )
    vms = _vms(api)
    assert await vms.wake("v") is None
    assert api.last_json() == {}
    await vms.wake("v", checkpoint_id=UUID1)
    assert api.last_json() == {"checkpoint_id": UUID1}
    resized = await vms.resize("v", cpus=4, memory_mb=4096)
    assert api.last_json() == {"cpus": 4, "memory_mb": 4096}
    assert isinstance(resized, ResizeResult) and resized.actual_cpus == 4
    cloned = await vms.clone("src", new_vm_name="dst")
    assert api.last_json() == {"new_vm_name": "dst"}
    assert isinstance(cloned, CloneResponse) and cloned.new_vm.name == "dst"
    info = await vms.connect("v")
    assert api.last.method == "POST" and isinstance(info, ConnectionInfo)
    assert info.ticket_secret == "t"


async def test_component_vms_ports_and_invites() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/vms/v/url",
            (200, {"ports": [PORT], "ssh_url": "ssh://s", "vm_name": "v"}),
        )
        .on("POST", "/api/vms/v/ports", 201)
        .on("DELETE", "/api/vms/v/ports/8080", None)
        .on("PUT", "/api/vms/v/ports/8080/public", 200)
        .on("GET", "/api/vms/v/ports", (200, [PORT]))
        .on("POST", "/api/vms/v/ports/8080/invites", (201, INVITE))
        .on("GET", "/api/vms/v/invites", (200, [INVITE]))
        .on("DELETE", "/api/vms/v/invites/inv1", None)
    )
    vms = _vms(api)
    url = await vms.get_url("v")
    assert isinstance(url, ProxyUrlInfo) and url.ports[0].port == 8080
    assert await vms.add_port("v", 8080) is None
    assert api.last_json() == {"port": 8080}
    assert await vms.remove_port("v", 8080) is None
    assert api.last.method == "DELETE"
    assert await vms.set_port_public("v", 8080, True) is None
    assert (api.last.method, api.last_json()) == ("PUT", {"public": True})
    ports = await vms.list_ports("v")
    assert isinstance(ports[0], ProxyPortInfo)
    invite = await vms.create_invite("v", 8080, ttl_secs=3600)
    assert api.last_json() == {"ttl_secs": 3600}
    assert isinstance(invite, ProxyInvite) and invite.invite_id == "inv1"
    invites = await vms.list_invites("v")
    assert [i.invite_id for i in invites] == ["inv1"]
    assert await vms.revoke_invite("v", "inv1") is None
    assert api.last.url.path == "/api/vms/v/invites/inv1"


async def test_component_vms_monitoring() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/vms/v/processes",
            (200, [{"comm": "sh", "cpu_percent": 0.5, "pid": 1, "rss_bytes": 9}]),
        )
        .on("GET", "/api/vms/v/stats", (200, STATS))
        .on("GET", "/api/vms/v/console", (200, {"lines": ["boot"]}))
        .on("GET", "/api/vms/v/telemetry", (200, {"vm_id": "id"}))
    )
    vms = _vms(api)
    procs = await vms.processes("v", top=3)
    assert api.query() == {"top": "3"} and isinstance(procs[0], VmProcess)
    stats = await vms.stats("v")
    assert isinstance(stats, VmStats) and stats.net_tx_bytes == 8
    console = await vms.console("v", lines=10)
    assert api.query() == {"lines": "10"}
    assert isinstance(console, VmConsole) and console.lines == ["boot"]
    tel = await vms.telemetry("v", from_=100, to=200, step=10)
    assert api.query() == {"from": "100", "to": "200", "step": "10"}
    assert isinstance(tel, VmTelemetrySeries)
    await vms.console("v")
    assert api.query() == {}


async def test_component_vms_events_log_and_iter() -> None:
    def ev(i: int) -> dict[str, Any]:
        return {"id": i, "kind": "started", "ts": i, "vm_id": "id"}

    api = Api().on(
        "GET",
        "/api/vms/v/events-log",
        (200, {"events": [ev(1)], "next_cursor": "c1"}),
        (200, {"events": [ev(2)], "next_cursor": None}),
        (200, {"events": [ev(3)], "next_cursor": None}),
    )
    vms = _vms(api)
    events = [e async for e in vms.iter_events_log("v", limit=1)]
    assert [e.id for e in events] == [1, 2] and isinstance(events[0], VmEvent)
    assert [dict(r.url.params) for r in api.seen] == [
        {"limit": "1"},
        {"limit": "1", "cursor": "c1"},
    ]
    page = await vms.events_log("v", cursor="c7")
    assert api.query() == {"cursor": "c7"} and page.events[0].id == 3


async def test_component_vms_exec_with_secrets_posts_to_its_own_route() -> None:
    api = Api().on(
        "POST",
        "/api/vms/v/exec-with-secrets",
        (200, {"exit_code": 0, "stdout": "hi\n", "stderr": ""}),
    )
    out = await _vms(api).exec_with_secrets(
        "v", command=["true"], selector={"kind": "subset", "names": ["A"]}
    )
    assert api.last.url.path == "/api/vms/v/exec-with-secrets"
    body = api.last_json()
    assert body == {"command": ["true"], "selector": {"kind": "subset", "names": ["A"]}}
    assert "timeout_secs" not in body
    assert (
        isinstance(out, ExecOutputDto) and out.stdout == "hi\n" and out.exit_code == 0
    )


async def test_component_vms_exec_with_secrets_sends_timeout_secs_and_reads_timed_out() -> None:
    api = Api().on(
        "POST",
        "/api/vms/v/exec-with-secrets",
        (200, {"exit_code": 124, "stdout": "started\n", "stderr": "", "timed_out": True}),
    )
    out = await _vms(api).exec_with_secrets(
        "v", command=["sleep", "60"], selector={"kind": "all"}, timeout_secs=5
    )
    assert api.last_json() == {
        "command": ["sleep", "60"],
        "selector": {"kind": "all"},
        "timeout_secs": 5,
    }
    assert out.exit_code == 124 and out.timed_out is True


async def test_component_vms_wait_for_state_returns_once_the_state_is_reached() -> None:
    api = Api().on(
        "GET",
        "/api/vms/v",
        (200, {**VM, "state": "creating"}),
        (200, {**VM, "state": "creating"}),
        (200, {**VM, "state": "running"}),
    )
    vm = await _vms(api).wait_for_state("v", {"running"}, timeout=2.0, interval=0.01)
    assert isinstance(vm, VmDetail) and vm.state == "running"
    assert len(api.seen) == 3


async def test_component_vms_wait_for_state_accepts_one_state_as_a_string() -> None:
    api = Api().on("GET", "/api/vms/v", (200, {**VM, "state": "stopped"}))
    vm = await _vms(api).wait_for_state("v", "stopped", timeout=1.0, interval=0.01)
    assert vm.state == "stopped"


async def test_component_vms_wait_for_state_times_out_naming_the_last_state() -> None:
    api = Api().on("GET", "/api/vms/v", (200, {**VM, "state": "creating"}))
    started = monotonic()
    with pytest.raises(CoveTimeoutError, match="creating"):
        await _vms(api).wait_for_state("v", {"running"}, timeout=0.3, interval=0.1)
    elapsed = monotonic() - started
    assert 0.25 <= elapsed < 2.0
    assert 2 <= len(api.seen) <= 6
