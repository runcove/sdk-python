from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.team_summary import TeamSummary
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/teams",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | list[TeamSummary] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TeamSummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ApiError | CliTooOldBody | list[TeamSummary]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[TeamSummary]]:
    """List every team

     Any signed-in session (SSH, web, local socket) may call it. Over an API key it needs an admin key
    (`cove key create --admin`) of a user in `[auth] admins`: a personal key or a team key that is not
    an admin key is refused `403 admin_required`, even when it holds `teams:read`. A member reads their
    own team's roster through `GET /api/teams/{name}/members`.

    `created_by` is sent only to an administrator (a session, or an admin key, of a user in `[auth]
    admins`); for anyone else it is absent, since it would name who the administrators are.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[TeamSummary]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[TeamSummary] | None:
    """List every team

     Any signed-in session (SSH, web, local socket) may call it. Over an API key it needs an admin key
    (`cove key create --admin`) of a user in `[auth] admins`: a personal key or a team key that is not
    an admin key is refused `403 admin_required`, even when it holds `teams:read`. A member reads their
    own team's roster through `GET /api/teams/{name}/members`.

    `created_by` is sent only to an administrator (a session, or an admin key, of a user in `[auth]
    admins`); for anyone else it is absent, since it would name who the administrators are.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[TeamSummary]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[TeamSummary]]:
    """List every team

     Any signed-in session (SSH, web, local socket) may call it. Over an API key it needs an admin key
    (`cove key create --admin`) of a user in `[auth] admins`: a personal key or a team key that is not
    an admin key is refused `403 admin_required`, even when it holds `teams:read`. A member reads their
    own team's roster through `GET /api/teams/{name}/members`.

    `created_by` is sent only to an administrator (a session, or an admin key, of a user in `[auth]
    admins`); for anyone else it is absent, since it would name who the administrators are.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[TeamSummary]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[TeamSummary] | None:
    """List every team

     Any signed-in session (SSH, web, local socket) may call it. Over an API key it needs an admin key
    (`cove key create --admin`) of a user in `[auth] admins`: a personal key or a team key that is not
    an admin key is refused `403 admin_required`, even when it holds `teams:read`. A member reads their
    own team's roster through `GET /api/teams/{name}/members`.

    `created_by` is sent only to an administrator (a session, or an admin key, of a user in `[auth]
    admins`); for anyone else it is absent, since it would name who the administrators are.

    Served on every listener, including the external API listener.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[TeamSummary]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
