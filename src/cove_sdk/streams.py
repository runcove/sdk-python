"""The events the SDK's streams yield: streamed exec, the console tail and the event streams.

Colour-neutral: ``client.vms.exec(...)`` yields the ``Exec*`` events on both clients, and the event
streams (``client.events.lifecycle()``, ``all_vms()``, ``vm(name)``) yield :class:`LifecycleEvent`
or :class:`VmEvent`, plus :class:`StreamLagged` when the server dropped events for this
connection. Match on the class (``isinstance`` or ``match``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ExecStdout:
    """A chunk of the command's stdout, exactly as sent (newlines included; concatenate verbatim)."""

    data: str


@dataclass(frozen=True, slots=True)
class ExecStderr:
    """A chunk of the command's stderr, exactly as sent."""

    data: str


@dataclass(frozen=True, slots=True)
class ExecExit:
    """Terminal: the command exited with ``code``.

    ``timed_out`` is true when the guest killed the command at its ``timeout_secs`` deadline
    (``code`` is then 124); it is false for a command that exited on its own, even with 124, and
    from a server too old to report it.
    """

    code: int
    timed_out: bool = False


@dataclass(frozen=True, slots=True)
class ExecError:
    """Terminal: the exec failed (the guest agent or the host reported ``error``)."""

    error: str


@dataclass(frozen=True, slots=True)
class ExecPaused:
    """Terminal: the VM left the running state mid-exec, so the server cut the stream."""

    reason: str
    new_state: str


ExecEvent = ExecStdout | ExecStderr | ExecExit | ExecError | ExecPaused
"""What an exec stream yields; it ends after exactly one ``ExecExit``/``ExecError``/``ExecPaused``."""


@dataclass(frozen=True, slots=True)
class ExecResult:
    """``vms.exec_collect``'s result: all of stdout and stderr, the exit code, and whether the
    command was killed at its deadline (``exit_code`` is then 124)."""

    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False


@dataclass(frozen=True, slots=True)
class LifecycleEvent:
    """A typed lifecycle event (``events.lifecycle()``): ``data`` is the frame's decoded JSON."""

    id: str | None
    data: Any


@dataclass(frozen=True, slots=True)
class VmEvent:
    """A VM event stream frame (``events.all_vms()``, ``events.vm(name)``).

    ``kind`` is the SSE event name (``connected``, ``vm-update``, ``state``, ``progress``,
    ``error``, ...) and ``data`` its decoded JSON. Not the same as ``cove_sdk.types.VmEvent``,
    an entry of the paginated VM event log.
    """

    kind: str
    data: Any


@dataclass(frozen=True, slots=True)
class StreamLagged:
    """The server dropped ``skipped`` events because this connection fell behind.

    They are not replayed: re-read the state you need (list or get the VMs).
    """

    skipped: int


__all__ = [
    "ExecError",
    "ExecEvent",
    "ExecExit",
    "ExecPaused",
    "ExecResult",
    "ExecStderr",
    "ExecStdout",
    "LifecycleEvent",
    "StreamLagged",
    "VmEvent",
]
