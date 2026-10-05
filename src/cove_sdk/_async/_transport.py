"""The SDK's HTTP transport: one httpx client per Cove client, shared by generated and hand-written calls.

Written once for the async client; ``scripts/sync-sdk-python.sh`` mirrors it to ``_sync/`` with
unasync, so this module imports no colour-specific primitive (``tests/test_unit_static.py``).

What lives here (spec section 3.3.1, each a port of the TypeScript SDK's ``http.ts``):

- the path-segment guard (:func:`check_segment`) and the one encoder of hand-written paths
  (:func:`api_path`);
- error decoding in an httpx *response* event hook: every status >= 300 is read and raised as its
  :class:`~cove_sdk.errors.CoveError` before a generated ``_parse_response`` can see it, so a
  non-JSON error body (a proxy's HTML 502, a ``text/plain`` 404) never reaches generated code that
  would call ``response.json()`` on it, and a 3xx is refused rather than followed;
- version skew: the server's ``x-cove-api-version`` is recorded and a differing one warned about
  once per transport;
- the base-URL rule (HTTPS unless the host is loopback, or ``allow_insecure_http=True``);
- timeouts, and wrapping httpx's transport failures as ``CoveConnectionError`` /
  ``CoveTimeoutError``. Cancellation is never caught.
"""

from __future__ import annotations

import contextvars
import enum
import ipaddress
import warnings
from collections.abc import AsyncIterable, AsyncIterator, Mapping
from contextlib import asynccontextmanager
from types import ModuleType
from urllib.parse import quote

import httpx

from .._colour import CALL_TIMEOUT
from .._generated.client import Client
from .._meta import API_VERSION
from ..auth import ACCEPT_EXTENSION, CoveAuth
from ..errors import (
    CoveApiVersionWarning,
    CoveConfigError,
    CoveConnectionError,
    CoveDecodeError,
    CoveError,
    CoveTimeoutError,
    _parse_api_version,
    raise_for,
)

# No whole-call deadline by default, as in TypeScript: only the connect phase is bounded.
DEFAULT_TIMEOUT = httpx.Timeout(connect=10.0, read=None, write=None, pool=None)
# A stream bounds connect only. A caller's timeout= on a stream becomes httpx's read timeout,
# which httpx applies to every read: an idle bound between chunks, not a header deadline.
STREAM_TIMEOUT = httpx.Timeout(connect=10.0, read=None, write=None, pool=None)

TimeoutArg = httpx.Timeout | float | None


IMPLIED_CODES_EXTENSION = "cove_implied_codes"
"""Request extension: a status-to-code map for an error response with no body to name its code
(a ``HEAD``), applied by :func:`~cove_sdk.errors.raise_for` when the body names none."""

# The response the event hook last saw in this call's context: call() uses it to tell a failure
# of the generated parser (a response arrived) from a bad argument (none did), and to report it.
_RESPONSE: contextvars.ContextVar[httpx.Response | None] = contextvars.ContextVar(
    "cove_sdk_response", default=None
)


class _Default(enum.Enum):
    CLIENT = 0


CLIENT_DEFAULT = _Default.CLIENT
"""Sentinel for ``timeout=``: use the client's timeout (``None`` means no timeout at all)."""

CallTimeout = TimeoutArg | _Default
"""What a resource method's ``timeout=`` takes: a timeout, ``None`` (none), or ``CLIENT_DEFAULT``."""


def check_segment(value: str | int) -> str:
    """Return ``value`` as a path segment, refusing ``""``, ``"."`` and ``".."``.

    Encoding is no defence: the generated calls quote with ``quote(str(v), safe="")``, which leaves
    ``..`` unchanged, and httpx then normalises ``/api/vms/..`` to ``/api``. Only rejection works.
    """
    segment = str(value)
    if segment in ("", ".", ".."):
        raise CoveError(
            f"Invalid path segment {segment!r}: empty and dot segments retarget the request"
        )
    return segment


def api_path(template: str, **segments: str | int) -> str:
    """Fill ``template``'s ``{name}`` fields, each guarded and percent-encoded as one segment."""
    return template.format(
        **{k: quote(check_segment(v), safe="") for k, v in segments.items()}
    )


def _is_loopback(host: str) -> bool:
    # The parsed host, compared exactly -- never a string prefix, which would accept
    # 127.evil.example or localhost.evil.example.
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(
            host
        ).is_loopback  # 127.0.0.0/8 and ::1 (no brackets here)
    except ValueError:
        return False


def _check_base_url(base_url: str, allow_insecure_http: bool) -> str:
    stripped = base_url.rstrip("/")
    try:
        url = httpx.URL(stripped)
    except (httpx.InvalidURL, TypeError) as exc:
        raise CoveConfigError(f"invalid base_url {base_url!r}: {exc}") from exc
    if url.scheme not in ("http", "https") or not url.host:
        raise CoveConfigError(
            f"base_url must be an http(s) URL with a host, got {base_url!r}"
        )
    if url.scheme == "http" and not allow_insecure_http and not _is_loopback(url.host):
        raise CoveConfigError(
            f"base_url {base_url!r} is plain http to a non-loopback host; use https, "
            "or pass allow_insecure_http=True"
        )
    return stripped


def _as_timeout(value: TimeoutArg) -> httpx.Timeout:
    return value if isinstance(value, httpx.Timeout) else httpx.Timeout(value)


def _query(
    params: Mapping[str, object] | None,
) -> list[tuple[str, str | int | float | bool | None]]:
    # None drops the key; a list or tuple repeats it (b=1&b=2), as the TypeScript query builder.
    out: list[tuple[str, str | int | float | bool | None]] = []
    for key, value in (params or {}).items():
        values = value if isinstance(value, (list, tuple)) else [value]
        for v in values:
            if v is None:
                continue
            if not isinstance(v, (str, int, float, bool)):
                raise CoveError(
                    f"query parameter {key!r} has unsupported type {type(v).__name__}"
                )
            out.append((key, v))
    return out


class AsyncCoveTransport:
    """The SDK's HTTP transport. Internal: the clients hold one each."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: CoveAuth,
        timeout: TimeoutArg = DEFAULT_TIMEOUT,
        allow_insecure_http: bool = False,
        transport: httpx.AsyncBaseTransport | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.base_url = _check_base_url(base_url, allow_insecure_http)
        self.server_api_version: int | None = None
        self._warned_skew = False
        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            auth=auth,
            timeout=_as_timeout(timeout),
            follow_redirects=False,  # the httpx default, set explicitly: Cove never redirects
            transport=transport,
            headers=dict(headers or {}),
            event_hooks={
                "request": [self._on_request],
                "response": [self._on_response],
            },
        )
        self._gen = Client(base_url=self.base_url, raise_on_unexpected_status=False)
        self._gen.set_async_httpx_client(self._http)

    async def _on_request(self, request: httpx.Request) -> None:
        # Generated calls take no timeout, so call() passes its per-call one through CALL_TIMEOUT.
        override = CALL_TIMEOUT.get()
        if isinstance(override, httpx.Timeout):
            request.extensions["timeout"] = override.as_dict()

    async def _on_response(self, response: httpx.Response) -> None:
        _RESPONSE.set(response)
        self._record_version(response.headers.get("x-cove-api-version"))
        if response.status_code >= 300:
            await response.aread()
            implied: Mapping[int, str] = response.request.extensions.get(
                IMPLIED_CODES_EXTENSION, {}
            )
            raise_for(
                response.status_code,
                response.headers,
                response.content,
                implied_code=implied.get(response.status_code),
            )

    def _record_version(self, header: str | None) -> None:
        version = _parse_api_version(header)
        if version is None:
            return
        self.server_api_version = version
        if version != API_VERSION and not self._warned_skew:
            self._warned_skew = True
            warnings.warn(
                f"Cove server speaks API version {version}; this SDK speaks {API_VERSION}. "
                "Calls proceed, but install the SDK from this deployment's /public/sdk/ to match.",
                CoveApiVersionWarning,
            )

    async def call(
        self,
        op: ModuleType,
        *,
        path: Mapping[str, str | int] | None = None,
        timeout: TimeoutArg | _Default = CLIENT_DEFAULT,
        **kwargs: object,
    ) -> object:
        """Run a generated operation module's call and return its parsed 2xx body (``None`` if empty).

        Every ``path`` value passes :func:`check_segment` before anything is sent; the generated
        call does the encoding.
        """
        segments = {k: check_segment(v) for k, v in (path or {}).items()}
        token = CALL_TIMEOUT.set(
            None if timeout is CLIENT_DEFAULT else _as_timeout(timeout)
        )
        seen_token = _RESPONSE.set(None)
        try:
            response = await op.asyncio_detailed(client=self._gen, **segments, **kwargs)
        except httpx.TimeoutException as exc:
            raise CoveTimeoutError(f"request timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise CoveConnectionError(
                f"request to {self.base_url} failed: {exc}"
            ) from exc
        except CoveError:
            raise
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            # The generated parser runs inside asyncio_detailed, after a 2xx got past the response
            # hook. With no response seen, the failure is the caller's (a bad argument): not ours.
            seen = _RESPONSE.get()
            if seen is None:
                raise
            try:
                body = seen.text
            except httpx.ResponseNotRead:
                body = ""
            name = getattr(op, "__name__", "operation").rpartition(".")[2]
            raise CoveDecodeError(
                seen.status_code,
                f"could not decode the {name} response body: {exc!r}",
                body,
            ) from exc
        finally:
            CALL_TIMEOUT.reset(token)
            _RESPONSE.reset(seen_token)
        parsed: object = response.parsed
        if parsed is None and response.content:
            # raise_on_unexpected_status=False: a 2xx the operation does not document parses to
            # None. Returning that would drop a body the caller was never shown.
            name = getattr(op, "__name__", "operation").rpartition(".")[2]
            raise CoveDecodeError(
                response.status_code,
                f"could not decode the {name} response body: "
                f"unmodelled {response.status_code}",
                response.content.decode("utf-8", errors="replace"),
            )
        return parsed

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, object] | None = None,
        json: object = None,
        content: bytes | AsyncIterable[bytes] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: TimeoutArg | _Default = CLIENT_DEFAULT,
        implied_codes: Mapping[int, str] | None = None,
    ) -> httpx.Response:
        """A hand-written call. ``path`` must already be built with :func:`api_path`.

        ``content`` streamed from an iterable goes out chunked unless ``headers`` declares its
        ``Content-Length``. ``implied_codes`` names the code an error status implies when the
        response has no body to name one (a ``HEAD``).
        """
        seen_token = _RESPONSE.set(None)
        try:
            return await self._http.request(
                method,
                path,
                # None, not an empty list: httpx rebuilds the URL's query from any params it is
                # given, which would drop a query the path already carries (vms.files).
                params=_query(params) or None,
                json=json,
                content=content,
                headers=dict(headers or {}),
                timeout=httpx.USE_CLIENT_DEFAULT
                if timeout is CLIENT_DEFAULT
                else timeout,
                extensions={IMPLIED_CODES_EXTENSION: implied_codes}
                if implied_codes
                else None,
            )
        except httpx.TimeoutException as exc:
            raise CoveTimeoutError(f"request timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise CoveConnectionError(
                f"request to {self.base_url} failed: {exc}"
            ) from exc
        finally:
            _RESPONSE.reset(seen_token)

    @asynccontextmanager
    async def stream(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, object] | None = None,
        json: object = None,
        timeout: TimeoutArg = None,
        accept: str = "text/event-stream",
        headers: Mapping[str, str] | None = None,
    ) -> AsyncIterator[httpx.Response]:
        """A streamed call: a context-managed response asking for ``accept`` (an SSE stream unless
        told otherwise; a file download asks for ``application/octet-stream``).

        ``timeout=None`` (the default) bounds connect only; a number becomes httpx's read
        timeout, an idle bound between chunks; an ``httpx.Timeout`` is used as given.
        """
        if isinstance(timeout, httpx.Timeout):
            stream_timeout = timeout
        elif timeout is None:
            stream_timeout = STREAM_TIMEOUT
        else:
            stream_timeout = httpx.Timeout(
                connect=10.0, read=timeout, write=None, pool=None
            )
        seen_token = _RESPONSE.set(None)
        try:
            async with self._http.stream(
                method,
                path,
                # None, not an empty list: httpx rebuilds the URL's query from any params it is
                # given, which would drop a query the path already carries (vms.files).
                params=_query(params) or None,
                json=json,
                headers=dict(headers or {}),
                timeout=stream_timeout,
                extensions={ACCEPT_EXTENSION: accept},
            ) as response:
                yield response
        except httpx.TimeoutException as exc:
            raise CoveTimeoutError(f"stream timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise CoveConnectionError(
                f"stream from {self.base_url} failed: {exc}"
            ) from exc
        finally:
            _RESPONSE.reset(seen_token)

    async def aclose(self) -> None:
        await self._http.aclose()

    @property
    def is_closed(self) -> bool:
        return self._http.is_closed

    def __repr__(self) -> str:
        return f"{type(self).__name__}(base_url={self.base_url!r})"


__all__ = [
    "CLIENT_DEFAULT",
    "DEFAULT_TIMEOUT",
    "STREAM_TIMEOUT",
    "AsyncCoveTransport",
    "CallTimeout",
    "api_path",
    "check_segment",
]
