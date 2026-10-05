"""Authentication strategies for the Cove SDK.

A :class:`CoveAuth` is an ``httpx.Auth``: httpx runs its flow after the client's and the caller's
headers are merged, so the headers it sets (``Authorization``, ``X-Cove-Api-Version``, ``Accept``)
always win. httpx calls ``sync_auth_flow`` or ``async_auth_flow`` by client colour, so one class
serves both clients; a strategy that must refresh a credential over I/O overrides
``async_auth_flow``.

Two schemes ship, as in the TypeScript SDK:

- :class:`BearerAuth` -- a ``cvk_`` service key, ``Authorization: Bearer ...``, for the external
  bearer listener.
- :class:`TicketAuth` -- a Warpgate SSO ticket, ``Authorization: Warpgate ...``, for the
  Warpgate-fronted listener.

Credentials never print and never pickle.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import NoReturn

import httpx

from ._meta import API_VERSION
from .errors import CoveConfigError

__all__ = ["BearerAuth", "CoveAuth", "TicketAuth", "resolve_auth"]

# Request extension through which the SDK's stream calls ask for their own Accept header, so the
# auth flow -- the last writer of the request's headers -- sets it.
ACCEPT_EXTENSION = "cove_accept"


class CoveAuth(httpx.Auth):
    """Base class of the SDK's credential strategies. Subclasses implement :meth:`_authorization`."""

    __slots__ = ("_api_version", "_credential")

    def __init__(self, credential: str, *, api_version: int = API_VERSION) -> None:
        if not isinstance(credential, str) or not credential:
            raise CoveConfigError(
                f"{type(self).__name__} requires a non-empty credential"
            )
        self._credential = credential
        self._api_version = api_version

    def _authorization(self) -> str:
        raise NotImplementedError

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = self._authorization()
        request.headers["X-Cove-Api-Version"] = str(self._api_version)
        accept = request.extensions.get(ACCEPT_EXTENSION)
        request.headers["Accept"] = (
            accept if isinstance(accept, str) else "application/json"
        )
        yield request

    def __repr__(self) -> str:
        return f"{type(self).__name__}(<redacted>)"

    __str__ = __repr__

    def __reduce__(self) -> NoReturn:
        raise TypeError("credentials are not picklable")

    def __reduce_ex__(self, protocol: object) -> NoReturn:
        raise TypeError("credentials are not picklable")


class BearerAuth(CoveAuth):
    """``Authorization: Bearer <token>`` -- a ``cvk_`` service key for the external bearer listener."""

    __slots__ = ()

    def _authorization(self) -> str:
        return f"Bearer {self._credential}"


class TicketAuth(CoveAuth):
    """``Authorization: Warpgate <ticket>`` -- the Warpgate SSO ticket ``cove login`` persists.

    Works against a deployment without the bearer listener; sensitive operations may trigger
    Warpgate's interactive sudo step-up, which a headless caller cannot satisfy.
    """

    __slots__ = ()

    def _authorization(self) -> str:
        return f"Warpgate {self._credential}"


def resolve_auth(
    *,
    token: str | None = None,
    ticket: str | None = None,
    auth: CoveAuth | None = None,
    api_version: int = API_VERSION,
) -> CoveAuth:
    """Resolve exactly one of ``token=`` / ``ticket=`` / ``auth=`` into a :class:`CoveAuth`."""
    supplied = [x for x in (token, ticket, auth) if x is not None]
    if len(supplied) != 1:
        raise CoveConfigError(
            "pass exactly one of `token`, `ticket` or `auth`"
            + ("" if supplied else "; no credential was supplied")
        )
    if auth is not None:
        if not isinstance(auth, CoveAuth):
            raise CoveConfigError("`auth` must be a cove_sdk.auth.CoveAuth")
        return auth
    if token is not None:
        return BearerAuth(token, api_version=api_version)
    assert ticket is not None
    return TicketAuth(ticket, api_version=api_version)
