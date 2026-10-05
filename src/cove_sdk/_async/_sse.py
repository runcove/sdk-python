"""Server-Sent Events: a bounded line splitter and the event parser (a port of the TypeScript ``sse.ts``).

The splitter reads raw byte chunks (``response.aiter_bytes()``), never httpx's ``aiter_lines()``:
that one's ``LineDecoder`` buffers a newline-free stream in full before yielding, so the memory a
cap exists to bound would already be spent. Here a line longer than the cap raises as soon as the
buffered remainder passes it, i.e. having held at most the cap plus one chunk.

Grammar, as ``sse.ts``: ``event:`` / ``data:`` / ``id:`` fields, blank-line dispatch, ``:``
comments ignored, one leading space stripped from a value, multi-line ``data`` joined with ``\\n``,
default event ``message``; lines end in ``\\n``, ``\\r\\n`` or ``\\r``. A final event the stream
did not terminate with a blank line is still dispatched, as ``sse.ts`` does. ``id`` is per event
(Cove sends one on every lifecycle frame and none elsewhere); it is never sent back, since the
server does not honour ``Last-Event-ID``.

Each generator closes its source when it is closed, so closing the outermost one releases the
whole chain.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, AsyncIterator
from dataclasses import dataclass

from ..errors import CoveError

MAX_SSE_BYTES = 16 * 2**20
"""The cap on one line and on one event's data: the TypeScript SDK's value."""


@dataclass(frozen=True, slots=True)
class ServerSentEvent:
    event: str
    data: str
    id: str | None = None


def _mib(cap: int) -> str:
    return f"{cap // 2**20} MiB" if cap % 2**20 == 0 else f"{cap} bytes"


class _LineSplitter:
    """Splits bytes on ``\\n``, ``\\r\\n`` and ``\\r``, refusing a line longer than ``cap`` bytes."""

    __slots__ = ("_buf", "_cap", "_skip_lf")

    def __init__(self, cap: int) -> None:
        self._buf = bytearray()
        self._cap = cap
        # A chunk that ended in "\r" may be followed by the "\n" of the same CRLF.
        self._skip_lf = False

    def _check(self, length: int) -> None:
        if length > self._cap:
            raise CoveError(f"SSE line exceeded {_mib(self._cap)}")

    def feed(self, chunk: bytes) -> list[bytes]:
        if not chunk:
            return []  # carries nothing: a pending CRLF stays pending
        if self._skip_lf:
            # Only this chunk's first byte can complete the CRLF, whatever the rest holds.
            self._skip_lf = False
            if chunk[:1] == b"\n":
                chunk = chunk[1:]
                if not chunk:
                    return []
        buf = self._buf
        pos = len(buf)  # the remainder held before this chunk has no line end in it
        buf += chunk
        lines: list[bytes] = []
        start = 0
        lf = buf.find(b"\n", pos)
        cr = buf.find(b"\r", pos)
        while lf != -1 or cr != -1:
            end = lf if cr == -1 or (lf != -1 and lf < cr) else cr
            self._check(end - start)
            lines.append(bytes(buf[start:end]))
            start = end + 1
            if end == cr:
                if cr + 1 == len(buf):
                    self._skip_lf = (
                        True  # the "\n" of this CRLF may open the next chunk
                    )
                elif lf == cr + 1:
                    start += 1
            # Each search runs again only once passed, so many short lines stay linear.
            if lf != -1 and lf < start:
                lf = buf.find(b"\n", start)
            if cr != -1 and cr < start:
                cr = buf.find(b"\r", start)
        del buf[:start]
        self._check(len(buf))
        return lines

    def finish(self) -> bytes | None:
        rest = bytes(self._buf)
        self._buf.clear()
        return rest or None


async def iter_lines(
    chunks: AsyncIterator[bytes], cap: int = MAX_SSE_BYTES
) -> AsyncGenerator[str, None]:
    """Decode ``chunks`` into lines (UTF-8, undecodable bytes replaced), each at most ``cap`` bytes."""
    splitter = _LineSplitter(cap)
    try:
        async for chunk in chunks:
            for line in splitter.feed(chunk):
                yield line.decode("utf-8", "replace")
        rest = splitter.finish()
        if rest is not None:
            yield rest.decode("utf-8", "replace")
    finally:
        close = getattr(chunks, "aclose", None)
        if close is not None:
            await close()


async def parse_sse(
    lines: AsyncIterator[str], cap: int = MAX_SSE_BYTES
) -> AsyncGenerator[ServerSentEvent, None]:
    """Parse SSE ``lines`` into events; one event's data may hold at most ``cap`` characters."""
    event: str | None = None
    data: list[str] = []
    size = 0
    event_id: str | None = None
    seen = False

    try:
        async for line in lines:
            if line == "":
                if seen:
                    yield ServerSentEvent(event or "message", "\n".join(data), event_id)
                event, data, size, event_id, seen = None, [], 0, None, False
                continue
            if line.startswith(":"):
                continue
            field, sep, value = line.partition(":")
            if sep and value.startswith(" "):
                value = value[1:]
            seen = True
            if field == "event":
                event = value
            elif field == "data":
                size += len(value) + (1 if data else 0)
                if size > cap:
                    raise CoveError(f"SSE event exceeded {_mib(cap)}")
                data.append(value)
            elif field == "id" and "\0" not in value:
                event_id = value
        if seen:
            yield ServerSentEvent(event or "message", "\n".join(data), event_id)
    finally:
        close = getattr(lines, "aclose", None)
        if close is not None:
            await close()


__all__ = ["MAX_SSE_BYTES", "ServerSentEvent", "iter_lines", "parse_sse"]
