"""client.events: the lifecycle and VM event streams over a MockTransport (mirrored by unasync)."""

import httpx
import pytest
from mockapi import HEADERS

from cove_sdk._async import _streams
from cove_sdk._async._streams import EventStream
from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.events import Events
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError
from cove_sdk.streams import LifecycleEvent, StreamLagged, VmEvent

SSE = {**HEADERS, "content-type": "text/event-stream"}


def _events(*bodies: bytes) -> tuple[list[httpx.Request], Events]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if len(seen) > len(bodies):
            raise AssertionError(f"unexpected request {len(seen)}: {request.url}")
        return httpx.Response(200, headers=SSE, content=bodies[len(seen) - 1])

    t = AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=httpx.MockTransport(handler)
    )
    return seen, Events(t)


def _sse_request(req: httpx.Request, path: str) -> None:
    assert (req.method, req.url.raw_path.decode()) == ("GET", path)
    assert req.headers["accept"] == "text/event-stream"
    assert "last-event-id" not in req.headers


async def test_component_events_lifecycle_yields_typed_events() -> None:
    seen, events = _events(
        b"event: connected\ndata: {}\n\n"
        b'event: lifecycle\nid: 7\ndata: {"kind":"vm_created","vm_name":"v"}\n\n'
        b'event: lagged\ndata: {"skipped":2}\n\n'
    )
    async with events.lifecycle(reconnect=False) as stream:
        got = [e async for e in stream]
    assert got == [
        LifecycleEvent("7", {"kind": "vm_created", "vm_name": "v"}),
        StreamLagged(2),
    ]
    _sse_request(seen[0], "/api/lifecycle-events")


async def test_component_events_all_vms_yields_every_frame_by_name() -> None:
    seen, events = _events(
        b'event: connected\ndata: {"vm_count":1}\n\n'
        b'event: vm-update\ndata: {"vm_name":"v","state":"stopped","event_type":"vm-update"}\n\n'
    )
    async with events.all_vms(reconnect=False) as stream:
        got = [e async for e in stream]
    assert got == [
        VmEvent("connected", {"vm_count": 1}),
        VmEvent(
            "vm-update",
            {"vm_name": "v", "state": "stopped", "event_type": "vm-update"},
        ),
    ]
    _sse_request(seen[0], "/api/vms/events")


async def test_component_events_vm_streams_one_vm() -> None:
    seen, events = _events(
        b'event: state\ndata: {"state":"creating","timestamp":"t"}\n\n'
    )
    async with events.vm("my vm", reconnect=False) as stream:
        got = [e async for e in stream]
    assert got == [VmEvent("state", {"state": "creating", "timestamp": "t"})]
    _sse_request(seen[0], "/api/vms/my%20vm/events")


async def test_component_events_vm_guards_the_name_before_sending() -> None:
    seen, events = _events(b"")
    with pytest.raises(CoveError, match="Invalid path segment"):
        events.vm("..")
    assert seen == []


async def test_component_events_reconnect_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # No real one-second wait in a unit run: the interval is the module's to read at reconnect.
    monkeypatch.setattr(_streams, "RECONNECT_INTERVAL", 0.0)
    for name, path in (
        ("lifecycle", "/api/lifecycle-events"),
        ("all_vms", "/api/vms/events"),
        ("vm", "/api/vms/v/events"),
    ):
        seen, events = _events(
            b"event: connected\ndata: {}\n\n",
            b"event: lifecycle\nid: 1\ndata: {}\n\nevent: state\ndata: {}\n\n",
        )
        opener = getattr(events, name)
        stream = opener("v") if name == "vm" else opener()
        assert isinstance(stream, EventStream)
        async with stream:
            async for evt in stream:
                if isinstance(evt, LifecycleEvent) or (
                    isinstance(evt, VmEvent) and evt.kind == "state"
                ):
                    break
        assert [r.url.path for r in seen] == [path, path], name


def test_component_events_methods_declare_their_operations() -> None:
    assert Events.lifecycle.__cove_operation__ == "streamLifecycleEvents"  # type: ignore[attr-defined]
    assert Events.all_vms.__cove_operation__ == "streamAllVmEvents"  # type: ignore[attr-defined]
    assert Events.vm.__cove_operation__ == "streamVmEvents"  # type: ignore[attr-defined]


async def _vm_until(events: Events, cap: int) -> list[object]:
    # A cap, not a drain: a stream that reconnects past its end would otherwise read on until
    # the fake server refuses the extra request.
    got: list[object] = []
    async with events.vm("v") as stream:
        async for evt in stream:
            got.append(evt)
            if len(got) == cap:
                break
    return got


async def test_component_events_vm_ends_after_deleted_without_reconnecting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_streams, "RECONNECT_INTERVAL", 0.0)
    # The second body is what a reconnect would meet while the row is still being removed.
    seen, events = _events(
        b'event: state\ndata: {"state":"running","timestamp":"t1"}\n\n'
        b'event: state\ndata: {"state":"deleted","timestamp":"t2"}\n\n'
        # Past the terminal frame in the same body: a real server never sends it, a proxy might.
        b'event: state\ndata: {"state":"running","timestamp":"t-late"}\n\n',
        b'event: state\ndata: {"state":"deleting","timestamp":"t3"}\n\n',
    )
    got = await _vm_until(events, 3)
    assert got == [
        VmEvent("state", {"state": "running", "timestamp": "t1"}),
        VmEvent("state", {"state": "deleted", "timestamp": "t2"}),
    ]
    assert len(seen) == 1


async def test_component_events_vm_ends_after_a_failed_create_without_raising(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_streams, "RECONNECT_INTERVAL", 0.0)
    seen, events = _events(
        b'event: state\ndata: {"state":"creating","timestamp":"t1"}\n\n'
        b'event: error\ndata: {"stage":"boot","message":"no"}\n\n'
        b'event: state\ndata: {"state":"creating","timestamp":"t-late"}\n\n',
        b'event: state\ndata: {"state":"creating","timestamp":"t2"}\n\n',
    )
    got = await _vm_until(events, 3)
    assert got == [
        VmEvent("state", {"state": "creating", "timestamp": "t1"}),
        VmEvent("error", {"stage": "boot", "message": "no"}),
    ]
    assert len(seen) == 1


async def test_component_events_vm_reconnects_after_a_non_terminal_close(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_streams, "RECONNECT_INTERVAL", 0.0)
    seen, events = _events(
        b'event: state\ndata: {"state":"running","timestamp":"t1"}\n\n'
        b'event: progress\ndata: {"stage":"s","message":"m"}\n\n',
        b'event: state\ndata: {"state":"deleting","timestamp":"t2"}\n\n',
    )
    got = await _vm_until(events, 3)
    assert got[-1] == VmEvent("state", {"state": "deleting", "timestamp": "t2"})
    assert len(seen) == 2


async def test_component_events_all_vms_is_not_ended_by_a_deletion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The fleet stream outlives any one VM: only `vm(name)` has terminal frames.
    monkeypatch.setattr(_streams, "RECONNECT_INTERVAL", 0.0)
    seen, events = _events(
        b'event: vm-deleted\ndata: {"vm_name":"v","state":"deleted"}\n\n'
        b'event: error\ndata: {"stage":"s","message":"m"}\n\n',
        b'event: connected\ndata: {"vm_count":0}\n\n',
    )
    got: list[object] = []
    async with events.all_vms() as stream:
        async for evt in stream:
            got.append(evt)
            if len(got) == 3:
                break
    assert got[-1] == VmEvent("connected", {"vm_count": 0})
    assert len(seen) == 2
