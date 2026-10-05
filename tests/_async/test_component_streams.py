"""ExecStream and EventStream over a MockTransport (mirrored to the sync layer by unasync).

Each response body is a byte stream that records being closed, so leaving a ``with`` block is
seen to release the response rather than assumed to.
"""

import json
from collections.abc import AsyncIterator, Callable
from typing import Any

import httpx
import pytest
from mockapi import HEADERS

from cove_sdk._async._sse import ServerSentEvent
from cove_sdk._async._streams import EventStream, ExecStream
from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveConnectionError, CoveError, PermissionDeniedError
from cove_sdk.streams import (
    ExecError,
    ExecExit,
    ExecPaused,
    ExecStderr,
    ExecStdout,
    StreamLagged,
)

SSE = {**HEADERS, "content-type": "text/event-stream"}


class Body(httpx.AsyncByteStream):
    """A response body that yields ``parts`` (an exception instance is raised) and records closes."""

    def __init__(self, parts: list[bytes | Exception]) -> None:
        self.parts = parts
        self.closed = 0

    async def __aiter__(self) -> AsyncIterator[bytes]:
        for part in self.parts:
            if isinstance(part, Exception):
                raise part
            yield part

    async def aclose(self) -> None:
        self.closed += 1


def _transport(
    handler: Callable[[httpx.Request], httpx.Response],
) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=httpx.MockTransport(handler)
    )


def _serve(*bodies: Body) -> tuple[list[httpx.Request], AsyncCoveTransport]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, headers=SSE, stream=bodies[len(seen) - 1])

    return seen, _transport(handler)


def _exec(t: AsyncCoveTransport) -> ExecStream:
    return ExecStream(t, "/api/vms/v/exec", body={"command": ["ls"]})


EXEC_FRAMES = (
    b"event: stdout\ndata: a\ndata: \n\n"  # "a\n": a trailing newline arrives as an empty data line
    b": keep-alive\n\n"
    b"event: progress\ndata: whatever\n\n"  # unknown kind: skipped
    b"event: stderr\ndata:  b \n\n"
    b'event: exit\ndata: {"code":3}\n\n'
    b"event: stdout\ndata: after the end\n\n"
)


async def test_component_exec_yields_typed_events_and_ends_at_exit() -> None:
    body = Body([EXEC_FRAMES])
    seen, t = _serve(body)
    async with _exec(t) as stream:
        events = [e async for e in stream]
    assert events == [ExecStdout("a\n"), ExecStderr(" b "), ExecExit(3)]
    assert seen[0].method == "POST" and seen[0].url.path == "/api/vms/v/exec"
    assert seen[0].headers["accept"] == "text/event-stream"
    assert json.loads(seen[0].content) == {"command": ["ls"]}
    assert body.closed == 1


async def test_component_exec_error_and_paused_are_terminal() -> None:
    _, t = _serve(
        Body(
            [
                b'event: error\ndata: {"error":"agent gone"}\n\nevent: stdout\ndata: x\n\n'
            ]
        ),
        Body([b'event: paused\ndata: {"reason":"r","new_state":"pausing"}\n\n']),
    )
    async with _exec(t) as stream:
        assert [e async for e in stream] == [ExecError("agent gone")]
    async with _exec(t) as stream:
        assert [e async for e in stream] == [ExecPaused("r", "pausing")]


async def test_component_exec_malformed_terminal_payload_raises() -> None:
    for frame in (
        b"event: exit\ndata: {trunc\n\n",
        b'event: exit\ndata: {"code":"0"}\n\n',
    ):
        _, t = _serve(Body([frame]))
        with pytest.raises(CoveError, match="exit"):
            async with _exec(t) as stream:
                async for _ in stream:
                    pass


async def test_component_exec_break_closes_the_response() -> None:
    body = Body([b"event: stdout\ndata: 1\n\n", b"event: stdout\ndata: 2\n\n"])
    _, t = _serve(body)
    async with _exec(t) as stream:
        async for _ in stream:
            break
        assert body.closed == 0  # positive control: still open inside the block
    assert body.closed == 1


async def test_component_exec_exception_in_block_closes_the_response() -> None:
    body = Body([b"event: stdout\ndata: 1\n\n"])
    _, t = _serve(body)
    with pytest.raises(KeyError):
        async with _exec(t) as stream:
            async for _ in stream:
                raise KeyError("boom")
    assert body.closed == 1


async def test_component_exec_unentered_iteration_is_refused() -> None:
    seen, t = _serve(Body([EXEC_FRAMES]), Body([EXEC_FRAMES]))
    stream = _exec(t)
    with pytest.raises(CoveError, match="use the stream in a with block"):
        async for _ in stream:
            pass
    assert seen == []  # nothing was sent
    async with stream:
        pass
    with pytest.raises(CoveError, match="use the stream in a with block"):
        async for _ in stream:
            pass


async def test_component_exec_transport_failure_mid_stream_is_a_cove_error() -> None:
    body = Body([b"event: stdout\ndata: 1\n\n", httpx.ReadError("reset")])
    _, t = _serve(body)
    got: list[Any] = []
    with pytest.raises(CoveConnectionError):
        async with _exec(t) as stream:
            async for e in stream:
                got.append(e)
    assert got == [ExecStdout("1")] and body.closed == 1


async def test_component_exec_non_2xx_raises_on_entry() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403, headers=HEADERS, json={"code": "scope_denied", "message": "no"}
        )

    with pytest.raises(PermissionDeniedError):
        async with _exec(_transport(handler)):
            pass


def _named(sse: ServerSentEvent) -> str | None:
    return None if sse.event == "skip" else f"{sse.event}:{sse.data}"


class Clock:
    """A fake monotonic clock that only the fake sleep advances."""

    def __init__(self) -> None:
        self.now = 100.0
        self.slept: list[float] = []

    def __call__(self) -> float:
        return self.now

    async def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


def _clocked(
    clock: Clock, *bodies: Body
) -> tuple[list[float], list[httpx.Request], AsyncCoveTransport]:
    at: list[float] = []
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        at.append(clock.now)
        if len(seen) > len(bodies):
            return httpx.Response(
                403, headers=HEADERS, json={"code": "scope_denied", "message": "no"}
            )
        return httpx.Response(200, headers=SSE, stream=bodies[len(seen) - 1])

    return at, seen, _transport(handler)


def _events(
    t: AsyncCoveTransport, clock: Clock, *, reconnect: bool = True
) -> EventStream[str]:
    return EventStream(
        t,
        "/api/vms/events",
        decode=_named,
        reconnect=reconnect,
        _sleep=clock.sleep,
        _clock=clock,
    )


async def test_component_event_stream_reconnects_after_a_clean_end() -> None:
    clock = Clock()
    first = Body([b"event: skip\ndata: x\n\n"])
    second = Body([b"event: a\ndata: 1\n\n"])
    at, seen, t = _clocked(clock, first, second)
    async with _events(t, clock) as stream:
        async for evt in stream:
            assert evt == "a:1"
            break
    assert len(seen) == 2 and [r.url.path for r in seen] == ["/api/vms/events"] * 2
    assert seen[1].headers["accept"] == "text/event-stream"
    assert "last-event-id" not in seen[1].headers  # the server does not honour it
    assert at[1] - at[0] >= 1.0 and clock.slept == [1.0]
    assert first.closed == 1 and second.closed == 1


async def test_component_event_stream_waits_only_what_is_left_of_the_second() -> None:
    clock = Clock()

    class SlowBody(Body):
        async def __aiter__(self) -> AsyncIterator[bytes]:
            clock.now += 0.75  # this connection lived 0.75 s
            for part in self.parts:
                assert isinstance(part, bytes)
                yield part

    at, seen, t = _clocked(clock, SlowBody([b""]), Body([b"event: a\ndata: 1\n\n"]))
    async with _events(t, clock) as stream:
        async for _ in stream:
            break
    assert clock.slept == [pytest.approx(0.25)] and at[1] - at[0] >= 1.0


async def test_component_event_stream_without_reconnect_makes_one_request() -> None:
    clock = Clock()
    at, seen, t = _clocked(clock, Body([b"event: a\ndata: 1\n\n"]), Body([b""]))
    async with _events(t, clock, reconnect=False) as stream:
        assert [e async for e in stream] == ["a:1"]
    assert len(seen) == 1 and clock.slept == []


async def test_component_event_stream_non_2xx_on_reconnect_raises_and_stops() -> None:
    clock = Clock()
    first = Body([b"event: a\ndata: 1\n\n"])
    at, seen, t = _clocked(clock, first)  # the second request answers 403
    got: list[Any] = []
    with pytest.raises(PermissionDeniedError):
        async with _events(t, clock) as stream:
            async for evt in stream:
                got.append(evt)
    assert got == ["a:1"] and len(seen) == 2 and first.closed == 1


async def test_component_event_stream_lagged_frame_is_typed() -> None:
    clock = Clock()
    at, seen, t = _clocked(
        clock, Body([b'event: lagged\ndata: {"skipped":7}\n\nevent: a\ndata: 2\n\n'])
    )
    async with _events(t, clock, reconnect=False) as stream:
        assert [e async for e in stream] == [StreamLagged(7), "a:2"]


async def test_component_event_stream_unentered_iteration_is_refused() -> None:
    clock = Clock()
    at, seen, t = _clocked(clock, Body([b""]))
    with pytest.raises(CoveError, match="use the stream in a with block"):
        async for _ in _events(t, clock):
            pass
    assert seen == []


async def test_component_event_stream_break_closes_the_response() -> None:
    clock = Clock()
    body = Body([b"event: a\ndata: 1\n\n", b"event: a\ndata: 2\n\n"])
    at, seen, t = _clocked(clock, body)
    async with _events(t, clock) as stream:
        async for _ in stream:
            break
    assert body.closed == 1 and len(seen) == 1


async def test_component_event_stream_iterating_again_after_its_end_says_closed() -> (
    None
):
    clock = Clock()
    at, seen, t = _clocked(clock, Body([b"event: a\ndata: 1\n\n"]))
    async with _events(t, clock, reconnect=False) as stream:
        assert [e async for e in stream] == ["a:1"]
        with pytest.raises(CoveError, match="stream has ended"):
            async for _ in stream:
                pass
    with pytest.raises(CoveError, match="use the stream in a with block"):
        async for _ in stream:
            pass
    assert len(seen) == 1
