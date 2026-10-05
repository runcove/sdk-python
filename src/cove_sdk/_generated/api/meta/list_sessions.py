from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.session import Session
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/me/sessions",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | list[Session] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Session.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | list[Session]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[Session]]:
    """List the caller's CLI sessions

     All CLI sessions for the caller, active and past. Readable over an API key on the external listener
    too: the only data returned is about the caller themselves, so, like `GET /api/me`, it needs no
    `x-required-scope`. Revoking one (`revokeSession`) is not offered to a key.

    Named `listSessions` rather than `listCliTickets`: the public surface no longer says "ticket" — the
    CLI-session sense becomes **session**. The old path `/api/profile/cli-tickets` has been removed, not
    aliased — it answers 404. Call `GET /api/me/sessions` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[Session]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[Session] | None:
    """List the caller's CLI sessions

     All CLI sessions for the caller, active and past. Readable over an API key on the external listener
    too: the only data returned is about the caller themselves, so, like `GET /api/me`, it needs no
    `x-required-scope`. Revoking one (`revokeSession`) is not offered to a key.

    Named `listSessions` rather than `listCliTickets`: the public surface no longer says "ticket" — the
    CLI-session sense becomes **session**. The old path `/api/profile/cli-tickets` has been removed, not
    aliased — it answers 404. Call `GET /api/me/sessions` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[Session]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[Session]]:
    """List the caller's CLI sessions

     All CLI sessions for the caller, active and past. Readable over an API key on the external listener
    too: the only data returned is about the caller themselves, so, like `GET /api/me`, it needs no
    `x-required-scope`. Revoking one (`revokeSession`) is not offered to a key.

    Named `listSessions` rather than `listCliTickets`: the public surface no longer says "ticket" — the
    CLI-session sense becomes **session**. The old path `/api/profile/cli-tickets` has been removed, not
    aliased — it answers 404. Call `GET /api/me/sessions` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[Session]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[Session] | None:
    """List the caller's CLI sessions

     All CLI sessions for the caller, active and past. Readable over an API key on the external listener
    too: the only data returned is about the caller themselves, so, like `GET /api/me`, it needs no
    `x-required-scope`. Revoking one (`revokeSession`) is not offered to a key.

    Named `listSessions` rather than `listCliTickets`: the public surface no longer says "ticket" — the
    CLI-session sense becomes **session**. The old path `/api/profile/cli-tickets` has been removed, not
    aliased — it answers 404. Call `GET /api/me/sessions` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[Session]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
