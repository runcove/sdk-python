from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.remove_member_outcome import RemoveMemberOutcome
from ...types import Response


def _get_kwargs(
    name: str,
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/teams/{name}/members/{username}".format(
            name=quote(str(name), safe=""),
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | RemoveMemberOutcome | None:
    if response.status_code == 200:
        response_200 = RemoveMemberOutcome.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
) -> Response[ApiError | CliTooOldBody | RemoveMemberOutcome]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | RemoveMemberOutcome]:
    """Remove a member from a team

     Admin only. Does not invalidate any team API key the departing member could reach (team-bound, not
    member-bound). Returns the fail-loud sweep outcome.

    Served on every listener, including the external API listener.

    Args:
        name (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | RemoveMemberOutcome]
    """

    kwargs = _get_kwargs(
        name=name,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | RemoveMemberOutcome | None:
    """Remove a member from a team

     Admin only. Does not invalidate any team API key the departing member could reach (team-bound, not
    member-bound). Returns the fail-loud sweep outcome.

    Served on every listener, including the external API listener.

    Args:
        name (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | RemoveMemberOutcome
    """

    return sync_detailed(
        name=name,
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | RemoveMemberOutcome]:
    """Remove a member from a team

     Admin only. Does not invalidate any team API key the departing member could reach (team-bound, not
    member-bound). Returns the fail-loud sweep outcome.

    Served on every listener, including the external API listener.

    Args:
        name (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | RemoveMemberOutcome]
    """

    kwargs = _get_kwargs(
        name=name,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | RemoveMemberOutcome | None:
    """Remove a member from a team

     Admin only. Does not invalidate any team API key the departing member could reach (team-bound, not
    member-bound). Returns the fail-loud sweep outcome.

    Served on every listener, including the external API listener.

    Args:
        name (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | RemoveMemberOutcome
    """

    return (
        await asyncio_detailed(
            name=name,
            username=username,
            client=client,
        )
    ).parsed
