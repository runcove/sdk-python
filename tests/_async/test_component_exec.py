"""vms.exec, vms.exec_collect and vms.stream_console over a MockTransport (mirrored by unasync)."""

import json
from collections.abc import Callable

import httpx
import pytest
from mockapi import HEADERS

from cove_sdk._async._streams import EventStream, ExecStream
from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.vms import Vms
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError
from cove_sdk.streams import ExecExit, ExecResult, ExecStdout

SSE = {**HEADERS, "content-type": "text/event-stream"}


def _vms(*bodies: bytes) -> tuple[list[httpx.Request], Vms]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if len(seen) > len(bodies):
            raise AssertionError(f"unexpected request {len(seen)}: {request.url}")
        return httpx.Response(200, headers=SSE, content=bodies[len(seen) - 1])

    t = AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=httpx.MockTransport(handler)
    )
    return seen, Vms(t)


OUTPUT = b'event: stdout\ndata: a\n\nevent: stdout\ndata: b\n\nevent: exit\ndata: {"code":0}\n\n'


async def test_component_exec_collect_gathers_output_and_exit_code() -> None:
    seen, vms = _vms(OUTPUT)
    assert await vms.exec_collect("v", command=["echo", "ab"]) == ExecResult(
        "ab", "", 0
    )
    req = seen[0]
    assert (req.method, req.url.path) == ("POST", "/api/vms/v/exec")
    assert req.headers["accept"] == "text/event-stream"
    assert json.loads(req.content) == {"command": ["echo", "ab"]}  # no timeout_secs


async def test_component_exec_sends_timeout_secs_and_streams() -> None:
    seen, vms = _vms(OUTPUT)
    stream = vms.exec("my vm", command=["ls"], timeout_secs=5)
    assert isinstance(stream, ExecStream) and seen == []  # nothing sent until entered
    async with stream:
        events = [e async for e in stream]
    assert events == [ExecStdout("a"), ExecStdout("b"), ExecExit(0)]
    assert seen[0].url.raw_path == b"/api/vms/my%20vm/exec"
    assert json.loads(seen[0].content) == {"command": ["ls"], "timeout_secs": 5}


async def test_component_exec_and_exec_collect_send_cwd_env_user_login() -> None:
    seen, vms = _vms(OUTPUT, OUTPUT)
    opts: dict[str, object] = {
        "cwd": "/srv/app",
        "env": {"GH_TOKEN": "t0k", "LANG": "C.UTF-8"},
        "user": "builder",
        "login": True,
    }
    async with vms.exec(
        "v",
        command=["gh", "--version"],
        timeout_secs=10,
        cwd="/srv/app",
        env={"GH_TOKEN": "t0k", "LANG": "C.UTF-8"},
        user="builder",
        login=True,
    ) as stream:
        _ = [e async for e in stream]
    assert await vms.exec_collect(
        "v",
        command=["gh", "--version"],
        cwd="/srv/app",
        env={"GH_TOKEN": "t0k", "LANG": "C.UTF-8"},
        user="builder",
        login=True,
    ) == ExecResult("ab", "", 0)
    assert json.loads(seen[0].content) == {
        "command": ["gh", "--version"],
        "timeout_secs": 10,
        **opts,
    }
    assert json.loads(seen[1].content) == {"command": ["gh", "--version"], **opts}


async def test_component_exec_login_false_is_left_out() -> None:
    seen, vms = _vms(OUTPUT)
    await vms.exec_collect("v", command=["true"], login=False)
    assert json.loads(seen[0].content) == {"command": ["true"]}


TIMED_OUT = (
    b"event: stdout\ndata: started\ndata: \n\n"
    b'event: exit\ndata: {"code":124,"timed_out":true}\n\n'
)


async def test_component_exec_reports_a_command_killed_at_its_deadline() -> None:
    _, vms = _vms(TIMED_OUT, TIMED_OUT, b'event: exit\ndata: {"code":124,"timed_out":false}\n\n')
    async with vms.exec("v", command=["sleep", "60"], timeout_secs=1) as stream:
        events = [e async for e in stream]
    assert events[-1] == ExecExit(124, timed_out=True)
    assert await vms.exec_collect("v", command=["sleep", "60"]) == ExecResult(
        "started\n", "", 124, timed_out=True
    )
    # A command that exits 124 on its own is not a timeout.
    assert await vms.exec_collect("v", command=["false"]) == ExecResult("", "", 124)


async def test_component_exec_collect_raises_on_error_and_paused() -> None:
    _, vms = _vms(b'event: error\ndata: {"error":"agent gone"}\n\n')
    with pytest.raises(CoveError, match="exec failed: agent gone"):
        await vms.exec_collect("v", command=["ls"])
    _, vms = _vms(b'event: paused\ndata: {"reason":"r","new_state":"pausing"}\n\n')
    with pytest.raises(CoveError, match="exec interrupted.*pausing"):
        await vms.exec_collect("v", command=["ls"])


async def test_component_exec_collect_raises_without_a_terminal_event() -> None:
    _, vms = _vms(b"event: stdout\ndata: a\n\n")
    with pytest.raises(CoveError, match="ended without a terminal event"):
        await vms.exec_collect("v", command=["ls"])


async def test_component_exec_guards_the_name_before_sending() -> None:
    seen, vms = _vms(OUTPUT)
    for call in (
        lambda: vms.exec("..", command=["ls"]),
        lambda: vms.stream_console("."),
    ):
        with pytest.raises(CoveError, match="Invalid path segment"):
            call()
    with pytest.raises(CoveError, match="Invalid path segment"):
        await vms.exec_collect("", command=["ls"])
    assert seen == []


async def test_component_stream_console_yields_lines_and_does_not_reconnect() -> None:
    seen, vms = _vms(
        b"event: console\ndata: booting\n\n: keep-alive\n\nevent: console\ndata: login:\n\n"
    )
    stream = vms.stream_console("v", lines=5)
    assert isinstance(stream, EventStream)
    async with stream:
        assert [line async for line in stream] == ["booting", "login:"]
    assert len(seen) == 1  # a console tail is not an event log: no reconnect by default
    req = seen[0]
    assert (req.method, req.url.path) == ("GET", "/api/vms/v/console/stream")
    assert dict(req.url.params) == {"lines": "5"}
    assert req.headers["accept"] == "text/event-stream"


async def test_component_stream_console_omits_lines_when_not_given() -> None:
    seen, vms = _vms(b"")
    async with vms.stream_console("v") as stream:
        assert [line async for line in stream] == []
    assert seen[0].url.query == b""


def test_component_exec_methods_declare_their_operations() -> None:
    ops: dict[str, Callable[..., object]] = {
        "execVm": Vms.exec,
        "streamVmConsole": Vms.stream_console,
    }
    for op_id, fn in ops.items():
        assert getattr(fn, "__cove_operation__") == op_id
