"""Colour-specific primitives the unasync mirror maps by name (async_sleep -> sync_sleep),
the per-call timeout both colours' transports read, and the monotonic clock the
async layer may not import ``time`` for."""

import contextvars
import time
from collections.abc import Callable
from typing import Any, TypeVar

import anyio
import anyio.to_thread

T = TypeVar("T")

# Set by the transport's call() for one call; read by its request hook into request.extensions["timeout"].
CALL_TIMEOUT: contextvars.ContextVar[Any] = contextvars.ContextVar("cove_sdk_call_timeout", default=None)


async def async_sleep(seconds: float) -> None:
    await anyio.sleep(seconds)


def sync_sleep(seconds: float) -> None:
    time.sleep(seconds)


async def async_read_chunk(file: Any, size: int) -> Any:
    """``file.read(size)`` in a worker thread, so a blocking read never stalls the event loop."""
    return await anyio.to_thread.run_sync(file.read, size)


def sync_read_chunk(file: Any, size: int) -> Any:
    return file.read(size)


async def async_run_blocking(fn: Callable[..., T], *args: Any) -> T:
    """``fn(*args)`` in a worker thread, so blocking work (a git subprocess, reading a tree)
    never stalls the event loop."""
    return await anyio.to_thread.run_sync(fn, *args)


def sync_run_blocking(fn: Callable[..., T], *args: Any) -> T:
    return fn(*args)


def monotonic() -> float:
    """Seconds on a monotonic clock, for deadlines (``time`` is off-limits under ``_async/``)."""
    return time.monotonic()
