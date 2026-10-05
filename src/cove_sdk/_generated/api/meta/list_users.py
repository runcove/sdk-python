from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/users",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | list[str] | None:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | list[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[str]]:
    """List every cove-known username

     Backs the share-modal user picker. Any signed-in session (SSH, web, local socket) may call it. Over
    an API key it needs an admin key (`cove key create --admin`) of a user in `[auth] admins`: a
    personal key or a team key that is not an admin key is refused `403 admin_required`, even when it
    holds `vms:read`.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[str]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[str] | None:
    """List every cove-known username

     Backs the share-modal user picker. Any signed-in session (SSH, web, local socket) may call it. Over
    an API key it needs an admin key (`cove key create --admin`) of a user in `[auth] admins`: a
    personal key or a team key that is not an admin key is refused `403 admin_required`, even when it
    holds `vms:read`.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[str]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[str]]:
    """List every cove-known username

     Backs the share-modal user picker. Any signed-in session (SSH, web, local socket) may call it. Over
    an API key it needs an admin key (`cove key create --admin`) of a user in `[auth] admins`: a
    personal key or a team key that is not an admin key is refused `403 admin_required`, even when it
    holds `vms:read`.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[str]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[str] | None:
    """List every cove-known username

     Backs the share-modal user picker. Any signed-in session (SSH, web, local socket) may call it. Over
    an API key it needs an admin key (`cove key create --admin`) of a user in `[auth] admins`: a
    personal key or a team key that is not an admin key is refused `403 admin_required`, even when it
    holds `vms:read`.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[str]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
