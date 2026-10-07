from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.revoke_key_by_token_request import RevokeKeyByTokenRequest
from ...types import Response


def _get_kwargs(
    *,
    body: RevokeKeyByTokenRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/api-keys/revoke",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | None:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 413:
        response_413 = cast(Any, None)
        return response_413

    if response.status_code == 415:
        response_415 = ApiError.from_dict(response.json())

        return response_415

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
) -> Response[Any | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RevokeKeyByTokenRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Revoke an API key by presenting it (no other auth)

     Revoke a `cvk_` API key by sending the key itself. Holding the key is the proof, so the request
    needs no other credential: use it when a key has leaked, or as a secret-scanning partner that found
    one.

    The answer is `202 Accepted` with an empty body whether the key was live (it is revoked before the
    response is sent), already revoked, unknown, or not a key at all, so the endpoint tells the caller
    nothing about the key. Revocation ends the key's use everywhere, as its owner's revocation does:
    requests with it are refused at once, and an open event stream ends within its re-check interval.

    A presentation that revokes a live key is audited: the same `keys.revoked` (or `keys.team_revoked`)
    row an owner's revocation writes, plus a `keys.presented` row with the key's id, the source address
    and the `User-Agent` — never the key. Any other presentation writes nothing; it is only counted, in
    `key_presentations_ignored_total` on `GET /api/admin/host-state`.

    On the external listener the route needs no credential and two per-address rate limits apply: the
    listener's general one and this route's tighter one. On the Unix socket and the Warpgate-fronted
    listener it sits behind their session identity like every other route there, so an unauthenticated
    call gets `401` there.

    Args:
        body (RevokeKeyByTokenRequest): `POST /api/api-keys/revoke` request body: the key itself.
            Holding it is the
            proof, so the request carries no other credential. Fields other than
            `token` are ignored, so a secret-scanning partner may send its own
            metadata alongside.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: RevokeKeyByTokenRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Revoke an API key by presenting it (no other auth)

     Revoke a `cvk_` API key by sending the key itself. Holding the key is the proof, so the request
    needs no other credential: use it when a key has leaked, or as a secret-scanning partner that found
    one.

    The answer is `202 Accepted` with an empty body whether the key was live (it is revoked before the
    response is sent), already revoked, unknown, or not a key at all, so the endpoint tells the caller
    nothing about the key. Revocation ends the key's use everywhere, as its owner's revocation does:
    requests with it are refused at once, and an open event stream ends within its re-check interval.

    A presentation that revokes a live key is audited: the same `keys.revoked` (or `keys.team_revoked`)
    row an owner's revocation writes, plus a `keys.presented` row with the key's id, the source address
    and the `User-Agent` — never the key. Any other presentation writes nothing; it is only counted, in
    `key_presentations_ignored_total` on `GET /api/admin/host-state`.

    On the external listener the route needs no credential and two per-address rate limits apply: the
    listener's general one and this route's tighter one. On the Unix socket and the Warpgate-fronted
    listener it sits behind their session identity like every other route there, so an unauthenticated
    call gets `401` there.

    Args:
        body (RevokeKeyByTokenRequest): `POST /api/api-keys/revoke` request body: the key itself.
            Holding it is the
            proof, so the request carries no other credential. Fields other than
            `token` are ignored, so a secret-scanning partner may send its own
            metadata alongside.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RevokeKeyByTokenRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Revoke an API key by presenting it (no other auth)

     Revoke a `cvk_` API key by sending the key itself. Holding the key is the proof, so the request
    needs no other credential: use it when a key has leaked, or as a secret-scanning partner that found
    one.

    The answer is `202 Accepted` with an empty body whether the key was live (it is revoked before the
    response is sent), already revoked, unknown, or not a key at all, so the endpoint tells the caller
    nothing about the key. Revocation ends the key's use everywhere, as its owner's revocation does:
    requests with it are refused at once, and an open event stream ends within its re-check interval.

    A presentation that revokes a live key is audited: the same `keys.revoked` (or `keys.team_revoked`)
    row an owner's revocation writes, plus a `keys.presented` row with the key's id, the source address
    and the `User-Agent` — never the key. Any other presentation writes nothing; it is only counted, in
    `key_presentations_ignored_total` on `GET /api/admin/host-state`.

    On the external listener the route needs no credential and two per-address rate limits apply: the
    listener's general one and this route's tighter one. On the Unix socket and the Warpgate-fronted
    listener it sits behind their session identity like every other route there, so an unauthenticated
    call gets `401` there.

    Args:
        body (RevokeKeyByTokenRequest): `POST /api/api-keys/revoke` request body: the key itself.
            Holding it is the
            proof, so the request carries no other credential. Fields other than
            `token` are ignored, so a secret-scanning partner may send its own
            metadata alongside.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RevokeKeyByTokenRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Revoke an API key by presenting it (no other auth)

     Revoke a `cvk_` API key by sending the key itself. Holding the key is the proof, so the request
    needs no other credential: use it when a key has leaked, or as a secret-scanning partner that found
    one.

    The answer is `202 Accepted` with an empty body whether the key was live (it is revoked before the
    response is sent), already revoked, unknown, or not a key at all, so the endpoint tells the caller
    nothing about the key. Revocation ends the key's use everywhere, as its owner's revocation does:
    requests with it are refused at once, and an open event stream ends within its re-check interval.

    A presentation that revokes a live key is audited: the same `keys.revoked` (or `keys.team_revoked`)
    row an owner's revocation writes, plus a `keys.presented` row with the key's id, the source address
    and the `User-Agent` — never the key. Any other presentation writes nothing; it is only counted, in
    `key_presentations_ignored_total` on `GET /api/admin/host-state`.

    On the external listener the route needs no credential and two per-address rate limits apply: the
    listener's general one and this route's tighter one. On the Unix socket and the Warpgate-fronted
    listener it sits behind their session identity like every other route there, so an unauthenticated
    call gets `401` there.

    Args:
        body (RevokeKeyByTokenRequest): `POST /api/api-keys/revoke` request body: the key itself.
            Holding it is the
            proof, so the request carries no other credential. Fields other than
            `token` are ignored, so a secret-scanning partner may send its own
            metadata alongside.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
