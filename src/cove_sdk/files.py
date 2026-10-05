"""Colour-neutral parts of ``client.vms.files``: what ``stat`` answers, and the wire helpers both
clients share (the ``path`` query, the ``mode`` encoding, the response headers)."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote

from .errors import CoveError

__all__ = ["VmFileStat"]


@dataclass(frozen=True, slots=True)
class VmFileStat:
    """One file in a VM: ``size`` in bytes (``Content-Length``); ``mode``, its permission bits
    as a number (``0o644`` is ``420``, as in ``FileUploaded.mode``), or ``None`` when the
    response did not carry them; and ``mtime``, its modification time from ``Last-Modified``
    (whole seconds, UTC), or ``None`` when the response did not carry one (an older server)."""

    size: int
    mode: int | None
    mtime: datetime | None = None


def file_query(path: str, mode: str | None = None) -> str:
    """The query of a file operation, encoded by hand.

    The server only percent-decodes, so a ``+`` is a literal plus and a space must be ``%20``;
    form encoding (httpx's ``params=``) would write a space as ``+``.
    """
    if not isinstance(path, str):
        raise CoveError("a file path must be a str")
    try:
        query = "?path=" + quote(path, safe="")
    except UnicodeEncodeError:
        # A lone surrogate has no UTF-8 form, so no request can name this path.
        raise CoveError("a file path must be valid Unicode (it has a lone surrogate)") from None
    if mode is not None:
        query += "&mode=" + quote(mode, safe="")
    return query


def wire_mode(mode: int | str) -> str:
    """``mode`` as the server's four octal digits, refusing anything outside ``0o777``."""
    if isinstance(mode, int) and not isinstance(mode, bool):
        if not 0 <= mode <= 0o777:
            raise CoveError(f"a file mode must be within 0o777, got {mode!r}")
        return f"{mode:04o}"
    if isinstance(mode, str) and re.fullmatch(r"0?[0-7]{1,3}", mode):
        return mode
    raise CoveError(
        f"a file mode must be octal permission bits within 0777, got {mode!r}"
    )


def stat_of(headers: Mapping[str, str], method: str) -> VmFileStat:
    """The size and mode a 200 file response's headers carry."""
    encoding = (headers.get("content-encoding") or "").strip().lower()
    if method == "GET" and encoding not in ("", "identity"):
        # A proxy may ignore Accept-Encoding: identity; httpx would then decode the body while
        # Content-Length still counts the encoded bytes.
        raise CoveError(
            f"GET file answered with Content-Encoding {encoding}, "
            "so its Content-Length does not count its bytes"
        )
    length = (headers.get("content-length") or "").strip()
    if re.fullmatch(r"[0-9]{1,19}", length) is None:
        raise CoveError(
            f"{method} file answered 200 without a readable Content-Length, "
            "so its size is unknown"
        )
    raw_mode = (headers.get("x-cove-file-mode") or "").strip()
    mode = int(raw_mode, 8) if re.fullmatch(r"[0-7]{1,4}", raw_mode) else None
    return VmFileStat(
        size=int(length), mode=mode, mtime=http_date(headers.get("last-modified"))
    )


def http_date(value: str | None) -> datetime | None:
    """An HTTP-date (``Last-Modified``) as an aware UTC ``datetime``, or ``None`` if unreadable."""
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value.strip())
    except (TypeError, ValueError, IndexError):
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


# The code a HEAD error's status implies, where the status alone is unambiguous, for a server
# that does not name it in ``X-Cove-Error-Code``. A 403 (a denied path or a missing scope) and a
# 404 (a missing VM or file) are not.
HEAD_IMPLIED_CODES: Mapping[int, str] = {
    413: "file_too_large",
    422: "file_not_regular",
    503: "unavailable",
}
