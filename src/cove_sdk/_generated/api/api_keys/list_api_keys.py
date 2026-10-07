from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.key_summary import KeySummary
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team: str | Unset = UNSET,
    service: bool | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["team"] = team

    params["service"] = service

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/api-keys",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | list[KeySummary] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = KeySummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

        return response_422

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
) -> Response[ApiError | CliTooOldBody | list[KeySummary]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    team: str | Unset = UNSET,
    service: bool | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | list[KeySummary]]:
    """List API keys

     Default scope is the caller's own keys; `?team=<slug>` lists a team's keys instead (admin only — the
    admin gate runs BEFORE the team lookup so a non-admin cannot distinguish a nonexistent team from an
    existing one); `?service=true` lists every service key instead (admin only; not with `team`). Each
    summary carries `subject_type` and, for a service key, `bound_team` or `bound_member`. Never
    includes raw tokens.

    Args:
        team (str | Unset):
        service (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[KeySummary]]
    """

    kwargs = _get_kwargs(
        team=team,
        service=service,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    team: str | Unset = UNSET,
    service: bool | Unset = UNSET,
) -> ApiError | CliTooOldBody | list[KeySummary] | None:
    """List API keys

     Default scope is the caller's own keys; `?team=<slug>` lists a team's keys instead (admin only — the
    admin gate runs BEFORE the team lookup so a non-admin cannot distinguish a nonexistent team from an
    existing one); `?service=true` lists every service key instead (admin only; not with `team`). Each
    summary carries `subject_type` and, for a service key, `bound_team` or `bound_member`. Never
    includes raw tokens.

    Args:
        team (str | Unset):
        service (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[KeySummary]
    """

    return sync_detailed(
        client=client,
        team=team,
        service=service,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    team: str | Unset = UNSET,
    service: bool | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | list[KeySummary]]:
    """List API keys

     Default scope is the caller's own keys; `?team=<slug>` lists a team's keys instead (admin only — the
    admin gate runs BEFORE the team lookup so a non-admin cannot distinguish a nonexistent team from an
    existing one); `?service=true` lists every service key instead (admin only; not with `team`). Each
    summary carries `subject_type` and, for a service key, `bound_team` or `bound_member`. Never
    includes raw tokens.

    Args:
        team (str | Unset):
        service (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[KeySummary]]
    """

    kwargs = _get_kwargs(
        team=team,
        service=service,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    team: str | Unset = UNSET,
    service: bool | Unset = UNSET,
) -> ApiError | CliTooOldBody | list[KeySummary] | None:
    """List API keys

     Default scope is the caller's own keys; `?team=<slug>` lists a team's keys instead (admin only — the
    admin gate runs BEFORE the team lookup so a non-admin cannot distinguish a nonexistent team from an
    existing one); `?service=true` lists every service key instead (admin only; not with `team`). Each
    summary carries `subject_type` and, for a service key, `bound_team` or `bound_member`. Never
    includes raw tokens.

    Args:
        team (str | Unset):
        service (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[KeySummary]
    """

    return (
        await asyncio_detailed(
            client=client,
            team=team,
            service=service,
        )
    ).parsed
