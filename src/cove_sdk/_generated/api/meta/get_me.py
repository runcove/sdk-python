from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.profile_summary import ProfileSummary
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/me",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ProfileSummary | None:
    if response.status_code == 200:
        response_200 = ProfileSummary.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ProfileSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ProfileSummary]:
    """Caller profile summary

     Identity, roles, key/session counts, and quota usage for the signed-in caller. Quota lookups
    (`quota`, `team_quotas`) are best-effort: a lookup failure logs a warning and renders zeros rather
    than failing the page.

    `permissions` says what the caller's own credential may do: `{kind:"key",scopes}` for an API key
    (personal or team) — the complete list the key was minted with, the only list the bearer gate reads
    — or `{kind:"session"}` for an SSH, web or local session, which has no scope list. `is_admin` is the
    admin checks' answer: true for a session of a user listed in `[auth] admins`, or for an admin key
    (`--admin`) of one; an admin's ordinary key, or one minted before admin keys existed, reads `false`.
    A key also needs the route's `admin:*` permission in `permissions.scopes`. Neither says whether a
    given VM is reachable. `roles` are gateway roles, a separate thing: a team key has no gateway
    identity, so its `roles` is empty.

    Errors from this endpoint are plain-text bodies, not the `ApiError` JSON envelope.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid bearer may read it. `scope_table::lookup` maps every GET under `/api/me` to no specific scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ProfileSummary]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ProfileSummary | None:
    """Caller profile summary

     Identity, roles, key/session counts, and quota usage for the signed-in caller. Quota lookups
    (`quota`, `team_quotas`) are best-effort: a lookup failure logs a warning and renders zeros rather
    than failing the page.

    `permissions` says what the caller's own credential may do: `{kind:"key",scopes}` for an API key
    (personal or team) — the complete list the key was minted with, the only list the bearer gate reads
    — or `{kind:"session"}` for an SSH, web or local session, which has no scope list. `is_admin` is the
    admin checks' answer: true for a session of a user listed in `[auth] admins`, or for an admin key
    (`--admin`) of one; an admin's ordinary key, or one minted before admin keys existed, reads `false`.
    A key also needs the route's `admin:*` permission in `permissions.scopes`. Neither says whether a
    given VM is reachable. `roles` are gateway roles, a separate thing: a team key has no gateway
    identity, so its `roles` is empty.

    Errors from this endpoint are plain-text bodies, not the `ApiError` JSON envelope.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid bearer may read it. `scope_table::lookup` maps every GET under `/api/me` to no specific scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ProfileSummary
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ProfileSummary]:
    """Caller profile summary

     Identity, roles, key/session counts, and quota usage for the signed-in caller. Quota lookups
    (`quota`, `team_quotas`) are best-effort: a lookup failure logs a warning and renders zeros rather
    than failing the page.

    `permissions` says what the caller's own credential may do: `{kind:"key",scopes}` for an API key
    (personal or team) — the complete list the key was minted with, the only list the bearer gate reads
    — or `{kind:"session"}` for an SSH, web or local session, which has no scope list. `is_admin` is the
    admin checks' answer: true for a session of a user listed in `[auth] admins`, or for an admin key
    (`--admin`) of one; an admin's ordinary key, or one minted before admin keys existed, reads `false`.
    A key also needs the route's `admin:*` permission in `permissions.scopes`. Neither says whether a
    given VM is reachable. `roles` are gateway roles, a separate thing: a team key has no gateway
    identity, so its `roles` is empty.

    Errors from this endpoint are plain-text bodies, not the `ApiError` JSON envelope.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid bearer may read it. `scope_table::lookup` maps every GET under `/api/me` to no specific scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ProfileSummary]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ProfileSummary | None:
    """Caller profile summary

     Identity, roles, key/session counts, and quota usage for the signed-in caller. Quota lookups
    (`quota`, `team_quotas`) are best-effort: a lookup failure logs a warning and renders zeros rather
    than failing the page.

    `permissions` says what the caller's own credential may do: `{kind:"key",scopes}` for an API key
    (personal or team) — the complete list the key was minted with, the only list the bearer gate reads
    — or `{kind:"session"}` for an SSH, web or local session, which has no scope list. `is_admin` is the
    admin checks' answer: true for a session of a user listed in `[auth] admins`, or for an admin key
    (`--admin`) of one; an admin's ordinary key, or one minted before admin keys existed, reads `false`.
    A key also needs the route's `admin:*` permission in `permissions.scopes`. Neither says whether a
    given VM is reachable. `roles` are gateway roles, a separate thing: a team key has no gateway
    identity, so its `roles` is empty.

    Errors from this endpoint are plain-text bodies, not the `ApiError` JSON envelope.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid bearer may read it. `scope_table::lookup` maps every GET under `/api/me` to no specific scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ProfileSummary
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
