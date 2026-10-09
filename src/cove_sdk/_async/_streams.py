"""Context-managed SSE streams: streamed exec, and the event streams with their reconnect loop.

Both are used as ``async with ... as stream: async for event in stream`` (sync: ``with`` /
``for``). Leaving the block -- an early ``break``, an exception, or the end of the stream --
closes the response, which is what stops the server holding an SSE task and a broadcast receiver
for a stream nobody reads. Iterating a stream outside its block raises :class:`CoveError`: a bare
generator would be closed only when the garbage collector got to it.

The request is sent on entering the block, so a non-2xx (raised by the transport's response hook
as its :class:`~cove_sdk.errors.CoveAPIError`) surfaces there. A transport failure mid-stream
raises :class:`~cove_sdk.errors.CoveConnectionError` (``CoveTimeoutError`` for an idle timeout).
Cancellation is never caught.
"""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator, AsyncIterator, Callable, Mapping
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, Generic, Protocol, Self, TypeVar

import httpx

from .._colour import async_sleep, monotonic
from ..errors import CoveConnectionError, CoveError, CoveTimeoutError, _parse_api_version
from ..streams import (
    ExecError,
    ExecEvent,
    ExecExit,
    ExecPaused,
    ExecStderr,
    ExecStdout,
    LifecycleEvent,
    StreamLagged,
    VmEvent,
)
from ._sse import ServerSentEvent, iter_lines, parse_sse
from ._transport import CLIENT_DEFAULT, AsyncCoveTransport, TimeoutArg, api_path

T = TypeVar("T")

RECONNECT_INTERVAL = 1.0
"""An event stream reconnects at most once per this many seconds."""

_NOT_ENTERED = "use the stream in a with block"


class _Sleep(Protocol):
    async def __call__(self, seconds: float, /) -> None: ...


def _json(kind: str, data: str) -> Any:
    try:
        return json.loads(data)
    except ValueError:
        shown = data if len(data) <= 200 else data[:200] + "..."
        raise CoveError(f"malformed `{kind}` event: {shown}") from None


def _field(kind: str, payload: Any, name: str, typ: type) -> Any:
    value = payload.get(name) if isinstance(payload, dict) else None
    # bool is an int subclass, and never a valid exit code.
    if not isinstance(value, typ) or isinstance(value, bool):
        raise CoveError(f"malformed `{kind}` event: no {typ.__name__} `{name}`")
    return value


def _exec_event(sse: ServerSentEvent) -> ExecEvent | None:
    kind = sse.event
    if kind == "stdout":
        return ExecStdout(sse.data)
    if kind == "stderr":
        return ExecStderr(sse.data)
    if kind == "exit":
        payload = _json(kind, sse.data)
        code = _field(kind, payload, "code", int)
        # A server older than `timed_out` leaves it out.
        return ExecExit(code, payload.get("timed_out") is True)
    if kind == "error":
        return ExecError(_field(kind, _json(kind, sse.data), "error", str))
    if kind == "paused":
        payload = _json(kind, sse.data)
        return ExecPaused(
            _field(kind, payload, "reason", str),
            _field(kind, payload, "new_state", str),
        )
    # An informational kind this SDK does not know: skipped, as in TypeScript.
    return None


def decode_console(sse: ServerSentEvent) -> str | None:
    """The console stream's one event type, ``console``: a raw console line."""
    return sse.data if sse.event == "console" else None


def decode_lifecycle(sse: ServerSentEvent) -> LifecycleEvent | None:
    """``lifecycle`` frames; the opening ``connected`` frame and unknown kinds are skipped."""
    if sse.event != "lifecycle":
        return None
    return LifecycleEvent(sse.id, _json(sse.event, sse.data))


def decode_vm_event(sse: ServerSentEvent) -> VmEvent:
    """Every frame of a VM event stream, by name (``connected``, ``vm-update``, ``state``, ...)."""
    return VmEvent(sse.event, _json(sse.event, sse.data))


def vm_stream_ended(event: VmEvent) -> bool:
    """Whether the server ends ``events.vm(name)``'s stream after ``event``: a ``state`` of
    ``deleted``, or an ``error`` (a failed create). The name is free again, and a later VM under
    it is a different VM, so the stream does not reconnect."""
    if event.kind == "error":
        return True
    data = event.data
    return (
        event.kind == "state"
        and isinstance(data, dict)
        and data.get("state") == "deleted"
    )


class _Stream:
    """One SSE response at a time, opened and closed explicitly."""

    def __init__(
        self,
        transport: AsyncCoveTransport,
        method: str,
        path: str,
        *,
        params: Mapping[str, object] | None,
        body: object,
        timeout: TimeoutArg,
    ) -> None:
        self._t = transport
        self._method = method
        self._path = path
        self._params = params
        self._body = body
        self._timeout = timeout
        self._cm: AbstractAsyncContextManager[httpx.Response] | None = None
        self._response: httpx.Response | None = None
        self._entered = False
        self._inside = False  # between entering and leaving the with block
        self._events: AsyncGenerator[Any, None] | None = None

    async def _open(self) -> httpx.Response:
        cm = self._t.stream(
            self._method,
            self._path,
            params=self._params,
            json=self._body,
            timeout=self._timeout,
        )
        response = await cm.__aenter__()
        self._cm, self._response = cm, response
        return response

    async def _close_response(self) -> None:
        cm, self._cm, self._response = self._cm, None, None
        if cm is not None:
            await cm.__aexit__(None, None, None)

    async def _frames(
        self, response: httpx.Response
    ) -> AsyncGenerator[ServerSentEvent, None]:
        events = parse_sse(iter_lines(response.aiter_bytes()))
        try:
            async for sse in events:
                yield sse
        except httpx.TimeoutException as exc:
            raise CoveTimeoutError(f"stream timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise CoveConnectionError(f"stream failed: {exc}") from exc
        finally:
            await events.aclose()

    async def __aenter__(self) -> Self:
        if self._entered:
            raise CoveError("a stream can be entered once")
        await self._open()
        self._entered = self._inside = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._inside = False
        events, self._events = self._events, None
        try:
            if events is not None:
                await events.aclose()
        finally:
            await self._close_response()

    def _check_entered(self) -> None:
        if not self._inside:
            raise CoveError(_NOT_ENTERED)
        if self._response is None:
            # Inside the block, but the stream ended without reconnecting.
            raise CoveError("the stream has ended; open a new one to read more")


class ExecStream(_Stream):
    """``vms.exec``'s stream: ``ExecStdout``/``ExecStderr`` chunks, then exactly one terminal
    ``ExecExit``/``ExecError``/``ExecPaused``, after which iteration stops."""

    def __init__(
        self,
        transport: AsyncCoveTransport,
        path: str,
        *,
        body: Mapping[str, object],
        timeout: TimeoutArg = None,
        min_api_version: int | None = None,
    ) -> None:
        super().__init__(
            transport, "POST", path, params=None, body=dict(body), timeout=timeout
        )
        self._min_api_version = min_api_version

    async def _open(self) -> httpx.Response:
        if self._min_api_version is not None:
            await self._require_api_version(self._min_api_version)
        return await super()._open()

    async def _require_api_version(self, minimum: int) -> None:
        """Refuse an exec with stdin unless the server says it speaks ``minimum`` or later: an
        older server ignores stdin and would run the command on empty input. ``/api/whoami`` is in
        the contract and served on every listener, and every successful reply carries
        ``x-cove-api-version``; read it from this reply, not the transport's last-seen version. A
        missing, zero or unreadable version, or a read that fails, is refused too."""
        try:
            response = await self._t.request(
                "GET",
                api_path("/api/whoami"),
                timeout=CLIENT_DEFAULT if self._timeout is None else self._timeout,
            )
        except (CoveTimeoutError, CoveConnectionError):
            raise
        except CoveError as exc:
            raise CoveError(
                f"could not read the server's API version ({exc}), so cannot confirm it supports "
                f"exec stdin (API {minimum} or later); nothing was sent"
            ) from exc
        version = _parse_api_version(response.headers.get("x-cove-api-version"))
        if not version or version < minimum:
            raise CoveError(
                f"this server (API {'unknown' if version is None else version}) does not support "
                f"exec stdin; upgrade the server to API {minimum} or later. An older server would "
                "run the command without its input; nothing was sent"
            )

    def __aiter__(self) -> AsyncIterator[ExecEvent]:
        self._check_entered()
        if self._events is None:
            self._events = self._iterate()
        return self._events

    async def _iterate(self) -> AsyncGenerator[ExecEvent, None]:
        assert self._response is not None
        frames = self._frames(self._response)
        try:
            async for sse in frames:
                event = _exec_event(sse)
                if event is None:
                    continue
                yield event
                if isinstance(event, (ExecExit, ExecError, ExecPaused)):
                    return
        finally:
            await frames.aclose()


class EventStream(Generic[T]):
    """An SSE event stream, decoded by ``decode`` (``None`` skips a frame); ``lagged`` frames
    become :class:`~cove_sdk.streams.StreamLagged`.

    With ``reconnect`` (the default for the event streams) a clean end of stream -- the server
    closes every event stream after 300 s -- opens a new one, at most once per second. The SDK
    sends no ``Last-Event-ID`` (the server does not honour one), so a reconnect starts from "now"
    and events between the close and the reconnect are lost. A non-2xx on a reconnect raises.

    ``terminal`` names an item after which the server ends the stream for good: the stream is
    closed and iteration stops there, without reconnecting.
    """

    def __init__(
        self,
        transport: AsyncCoveTransport,
        path: str,
        *,
        decode: Callable[[ServerSentEvent], T | None],
        params: Mapping[str, object] | None = None,
        reconnect: bool = True,
        timeout: TimeoutArg = None,
        terminal: Callable[[T], bool] | None = None,
        _sleep: _Sleep = async_sleep,
        _clock: Callable[[], float] = monotonic,
    ) -> None:
        self._stream = _Stream(
            transport, "GET", path, params=params, body=None, timeout=timeout
        )
        self._decode = decode
        self._reconnect = reconnect
        self._terminal = terminal
        self._sleep = _sleep
        self._clock = _clock
        self._connected_at = 0.0

    async def __aenter__(self) -> Self:
        await self._stream.__aenter__()
        self._connected_at = self._clock()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self._stream.__aexit__(exc_type, exc, tb)

    def __aiter__(self) -> AsyncIterator[T | StreamLagged]:
        s = self._stream
        s._check_entered()
        if s._events is None:
            s._events = self._iterate()
        events: AsyncIterator[T | StreamLagged] = s._events
        return events

    async def _iterate(self) -> AsyncGenerator[T | StreamLagged, None]:
        s = self._stream
        ended = False
        while True:
            assert s._response is not None
            frames = s._frames(s._response)
            try:
                async for sse in frames:
                    if sse.event == "lagged":
                        payload = _json(sse.event, sse.data)
                        yield StreamLagged(_field(sse.event, payload, "skipped", int))
                        continue
                    item = self._decode(sse)
                    if item is None:
                        continue
                    yield item
                    if self._terminal is not None and self._terminal(item):
                        ended = True
                        break
            finally:
                await frames.aclose()
            await s._close_response()
            if ended or not self._reconnect:
                return
            wait = self._connected_at + RECONNECT_INTERVAL - self._clock()
            if wait > 0:
                await self._sleep(wait)
            await s._open()
            self._connected_at = self._clock()


__all__ = [
    "RECONNECT_INTERVAL",
    "EventStream",
    "ExecStream",
    "decode_console",
    "decode_lifecycle",
    "decode_vm_event",
    "vm_stream_ended",
]
