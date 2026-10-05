"""Errors raised by the Cove SDK.

Every error the SDK raises is a :class:`CoveError`. A non-2xx response is a :class:`CoveAPIError`
subclass chosen by status (a port of ``CoveAPIError.fromResponse`` in the TypeScript SDK); a
transport failure is a :class:`CoveConnectionError`; bad client construction is a
:class:`CoveConfigError`. The SDK defines no error code of its own: ``code`` is always the exact wire
string from the server's closed ``ErrorCode`` catalogue or a ``DenyReason`` code.
"""

from __future__ import annotations

import dataclasses
import json
import re
import types
from collections.abc import Mapping
from typing import NoReturn

from ._meta import API_VERSION

__all__ = [
    "AuthenticationError",
    "ConflictError",
    "CoveAPIError",
    "CoveApiVersionWarning",
    "CoveConfigError",
    "CoveConnectionError",
    "CoveDecodeError",
    "CoveError",
    "CoveTimeoutError",
    "DenyReason",
    "DownloadTruncatedError",
    "FileNotRegularError",
    "FilePathDeniedError",
    "FileTooLargeError",
    "NotFoundError",
    "PayloadTooLargeError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "UnavailableError",
    "UpgradeRequiredError",
    "ValidationError",
    "VmFileNotFoundError",
    "raise_for",
]


class CoveError(Exception):
    """Base class of every error the SDK raises."""


class CoveConfigError(CoveError, ValueError):
    """The client was constructed with bad arguments (credentials, base URL)."""


class CoveConnectionError(CoveError):
    """The server could not be reached, or answered with a redirect (Cove never redirects)."""


class CoveTimeoutError(CoveConnectionError):
    """An httpx timeout expired."""


class CoveDecodeError(CoveError):
    """A 2xx response whose body the SDK could not decode into the operation's model.

    ``status`` is the HTTP status; ``body`` the raw response text (as ``CoveAPIError.body``, not
    truncated; never a credential, which travels in a request header). ``__cause__`` is the
    parser's own exception.
    """

    def __init__(self, status: int, message: str, body: str) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class CoveAPIError(CoveError):
    """The server answered with a non-2xx status.

    ``code`` is the body's ``code`` (else ``error``), kept as the exact wire string;
    ``message`` its ``message`` (else ``error``, else the raw text); ``body`` the parsed JSON
    body, or the text when it is not JSON, or ``None`` when empty.
    """

    def __init__(
        self, status: int, code: str | None, message: str, body: object
    ) -> None:
        super().__init__(f"HTTP {status}{' ' + code if code else ''}: {message}")
        self.status = status
        self.code = code
        self.message = message
        self.body = body


class AuthenticationError(CoveAPIError):
    """401: missing, malformed, expired or revoked credential."""


class PermissionDeniedError(CoveAPIError):
    """403: the credential lacks the scope. Most denials arrive as 404 instead (existence non-leak)."""


class NotFoundError(CoveAPIError):
    """404. Cove answers 404 for "exists but not yours" too (existence non-leak)."""


class ConflictError(CoveAPIError):
    """409: the operation conflicts with current state.

    ``deny`` is set when the body is an admission or quota denial (a ``DenyReason`` branch);
    ``retry_after_secs`` is the body's value when present (``vm_name_taken``).
    """

    def __init__(
        self,
        status: int,
        code: str | None,
        message: str,
        body: object,
        *,
        deny: DenyReason | None = None,
        retry_after_secs: int | None = None,
    ) -> None:
        super().__init__(status, code, message, body)
        self.deny = deny
        self.retry_after_secs = retry_after_secs


class UpgradeRequiredError(CoveAPIError):
    """426 with code ``CLI_TOO_OLD``: the server refuses this SDK's API version.

    ``server_api_version`` is the server's ``x-cove-api-version``; ``min_cli_version`` the body's
    minimum cove-cli version, exposed under that honest name.
    """

    def __init__(
        self,
        status: int,
        code: str | None,
        message: str,
        body: object,
        *,
        server_api_version: int | None,
        min_cli_version: str | None,
    ) -> None:
        super().__init__(status, code, message, body)
        self.server_api_version = server_api_version
        self.min_cli_version = min_cli_version


class ValidationError(CoveAPIError):
    """The request's shape or values were rejected: a 422, or a 400 ``validation_failed``.

    The server answers 400 ``validation_failed`` for a request it cannot decode (malformed JSON, a
    field of the wrong type, an unknown enum value, a query or path value of the wrong type) and
    422 for a well-formed value it refuses. Both raise this class; ``status`` tells them apart. A
    400 with any other code stays a plain :class:`CoveAPIError`.
    """


class RateLimitError(CoveAPIError):
    """429 ``rate_limited``: this source IP spent its request budget on the bearer listener.

    The budget is per source IP (default 30 requests per second, set by the operator), so every
    caller behind one NAT or tunnel shares it. ``retry_after_secs`` is the response's
    ``Retry-After`` in seconds, or ``None`` when the header is absent or not delta-seconds. The SDK
    never retries: wait that long, then send the request again.
    """

    def __init__(
        self,
        status: int,
        code: str | None,
        message: str,
        body: object,
        *,
        retry_after_secs: int | None = None,
    ) -> None:
        super().__init__(status, code, message, body)
        self.retry_after_secs = retry_after_secs


class ServerError(CoveAPIError):
    """5xx: server-side failure (503 also means the subsystem is disabled on the host).

    ``retry_after_secs`` is the response's ``Retry-After`` in seconds when it sent one as
    delta-seconds, else ``None``.
    """

    def __init__(
        self,
        status: int,
        code: str | None,
        message: str,
        body: object,
        *,
        retry_after_secs: int | None = None,
    ) -> None:
        super().__init__(status, code, message, body)
        self.retry_after_secs = retry_after_secs


class PayloadTooLargeError(CoveAPIError):
    """413: the request or the resource is larger than the server allows."""


class FileTooLargeError(PayloadTooLargeError):
    """413 ``file_too_large``: the file is over the host's ``[files] max_bytes``, or an upload body
    is longer than its ``Content-Length``. The message states the limit."""


class FilePathDeniedError(PermissionDeniedError):
    """403 ``file_path_denied``: the path is on the host's deny-list or a pseudo filesystem.

    Not a scope problem: a key without ``files:read`` / ``files:write`` is a plain
    :class:`PermissionDeniedError` (``scope_denied``).
    """


class VmFileNotFoundError(NotFoundError):
    """404 ``file_not_found``: the file or its parent directory does not exist in the VM."""


class FileNotRegularError(ValidationError):
    """422 ``file_not_regular``: the target is not a regular file, or a path component is a
    symlink (symlinks are refused, never followed)."""


class UnavailableError(ServerError):
    """503 ``unavailable``: something the operation depends on is not available right now; the
    message says what. For file transfer: the guest agent connection was lost or timed out, or the
    guest already has as many transfers open as it allows. Retry."""


class DownloadTruncatedError(CoveError):
    """A download whose body did not match its ``Content-Length``.

    A transfer that fails after the server sent ``200`` can only end the body early, so a short
    body is a failed download, never a complete file. ``expected_bytes`` is the file's size,
    ``received_bytes`` what arrived; ``__cause__`` is the transport's error when the connection
    broke.
    """

    def __init__(self, expected_bytes: int, received_bytes: int) -> None:
        if received_bytes > expected_bytes:
            text = (
                f"download sent more than its Content-Length of {expected_bytes} bytes"
            )
        else:
            text = (
                f"download ended after {received_bytes} of {expected_bytes} bytes: "
                "the transfer failed"
            )
        super().__init__(text)
        self.expected_bytes = expected_bytes
        self.received_bytes = received_bytes


class CoveApiVersionWarning(UserWarning):
    """The server's ``x-cove-api-version`` differs from this SDK's ``API_VERSION``.

    Emitted with :func:`warnings.warn` once per client; filter, silence or escalate it with the
    :mod:`warnings` machinery. The SDK never refuses on skew. Defined here, outside both client
    colours, so one class covers the sync and the async client.
    """


@dataclasses.dataclass(frozen=True)
class DenyReason:
    """Why an admission or quota check refused a request (a 409's structured detail).

    ``code`` is the branch's wire code (``ram_headroom_exceeded``, ``user_vm_count_quota_exceeded``,
    ...); ``details`` the branch's own fields (``reservation_mb``, ``current``, ``max``, ...) as a
    read-only mapping.
    """

    code: str
    details: Mapping[str, object]


_STATUS: dict[int, type[CoveAPIError]] = {
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    413: PayloadTooLargeError,
    422: ValidationError,
    429: RateLimitError,
}

# Error codes with a class of their own, each with the one status it comes with; the same code on
# another status falls back to _STATUS. ``validation_failed`` comes with 422 too, which _STATUS
# already maps to ValidationError.
_CODE: dict[str, tuple[int, type[CoveAPIError]]] = {
    "validation_failed": (400, ValidationError),
    "file_too_large": (413, FileTooLargeError),
    "file_path_denied": (403, FilePathDeniedError),
    "file_not_found": (404, VmFileNotFoundError),
    "file_not_regular": (422, FileNotRegularError),
    "unavailable": (503, UnavailableError),
}

_UPGRADE_HINT = (
    "Install the SDK that matches the server from its /public/sdk/index.json "
    "on the Warpgate-fronted URL."
)


def _upgrade_message(server_api_version: int | None) -> str:
    """The SDK's own 426 text. The server's says to run ``cove update``, which is for the CLI.

    Same wording as the TypeScript SDK's ``upgradeMessage``; the server's text stays on ``.body``.
    """
    server = "" if server_api_version is None else f" (server version {server_api_version})"
    return (
        f"This SDK speaks API version {API_VERSION}; the server refused it{server}. "
        f"{_UPGRADE_HINT}"
    )


def _deny_codes() -> frozenset[str]:
    """The DenyReason branch codes, read once from the generated ``DenyReasonType<n>Code`` enums."""
    from ._generated import models

    codes: set[str] = set()
    for name in dir(models):
        if re.fullmatch(r"DenyReasonType\d+Code", name):
            codes.update(str(member.value) for member in getattr(models, name))
    return frozenset(codes)


_DENY_CODES: frozenset[str] | None = None


def _is_deny_code(code: str) -> bool:
    global _DENY_CODES
    if _DENY_CODES is None:
        _DENY_CODES = _deny_codes()
    return code in _DENY_CODES


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for k, v in headers.items():
        if k.lower() == name:
            return v
    return None


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _parse_api_version(header: str | None) -> int | None:
    """An ``x-cove-api-version`` value of plain ASCII digits, else ``None`` (treated as absent).

    Matches the TypeScript SDK's ``parseApiVersion`` (``^\\d{1,9}$`` after trimming): ``int()``
    alone would take ``+5``, ``5_0``, ``-1`` and non-ASCII digits.
    """
    if header is None:
        return None
    trimmed = header.strip()
    if re.fullmatch(r"[0-9]{1,9}", trimmed) is None:
        return None
    return int(trimmed)


def _parse_retry_after(header: str | None) -> int | None:
    """A ``Retry-After`` in delta-seconds (plain ASCII digits), else ``None``.

    The HTTP-date form, a sign, a fraction or anything else reads as absent: the server only sends
    seconds, and a caller should not be handed a guess.
    """
    if header is None:
        return None
    trimmed = header.strip()
    if re.fullmatch(r"[0-9]{1,9}", trimmed) is None:
        return None
    return int(trimmed)


def raise_for(
    status: int,
    headers: Mapping[str, str],
    content: bytes,
    *,
    implied_code: str | None = None,
) -> NoReturn:
    """Raise the :class:`CoveError` for a non-2xx response.

    A response with no body to name its code (a ``HEAD``) names it in ``X-Cove-Error-Code``;
    failing that, ``implied_code`` is the code the status alone implies. Both are used only when
    the body names no code.
    """
    if 300 <= status < 400:
        location = _header(headers, "location") or "no location"
        raise CoveConnectionError(f"Cove never redirects; got {status} to {location}")

    text = content.decode("utf-8", errors="replace")
    body: object = text if text else None
    if text:
        try:
            body = json.loads(text)
        except ValueError:
            pass  # plain-text and HTML bodies stay text

    code: str | None = None
    message: str | None = None
    if isinstance(body, dict):
        if isinstance(body.get("code"), str):
            code = body["code"]
        elif isinstance(body.get("error"), str):
            code = body["error"]
        if isinstance(body.get("message"), str):
            message = body["message"]
        elif isinstance(body.get("error"), str):
            message = body["error"]
    if code is None:
        code = (_header(headers, "x-cove-error-code") or "").strip() or implied_code
        if code is not None:
            message = message or code
    if not message:
        if isinstance(body, str):
            message = body
        elif body is not None:
            message = code or text
        else:
            message = "request failed"

    if status == 426 and code == "CLI_TOO_OLD":
        min_cli = body.get("min_cli_version") if isinstance(body, dict) else None
        server_api_version = _parse_api_version(_header(headers, "x-cove-api-version"))
        raise UpgradeRequiredError(
            status,
            code,
            _upgrade_message(server_api_version),
            body,
            server_api_version=server_api_version,
            min_cli_version=min_cli if isinstance(min_cli, str) else None,
        )
    if status == 409:
        deny: DenyReason | None = None
        retry_after: int | None = None
        if isinstance(body, dict):
            if code is not None and _is_deny_code(code):
                details = {
                    k: v for k, v in body.items() if k not in ("code", "message")
                }
                deny = DenyReason(code, types.MappingProxyType(details))
            retry_after = _int_or_none(body.get("retry_after_secs"))
        raise ConflictError(
            status, code, message, body, deny=deny, retry_after_secs=retry_after
        )
    by_code = _CODE.get(code) if code is not None else None
    cls = (
        by_code[1]
        if by_code is not None and by_code[0] == status
        else _STATUS.get(status) or (ServerError if status >= 500 else CoveAPIError)
    )
    if issubclass(cls, (RateLimitError, ServerError)):
        retry_after_secs = _parse_retry_after(_header(headers, "retry-after"))
        raise cls(status, code, message, body, retry_after_secs=retry_after_secs)
    raise cls(status, code, message, body)
