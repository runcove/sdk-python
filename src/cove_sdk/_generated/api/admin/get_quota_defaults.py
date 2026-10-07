from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_quota_defaults_response import AdminQuotaDefaultsResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/quota-defaults",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminQuotaDefaultsResponse | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminQuotaDefaultsResponse.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AdminQuotaDefaultsResponse | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminQuotaDefaultsResponse | ApiError | CliTooOldBody]:
    """Read the host-wide default resource caps

     The host's baseline caps for vCPUs, memory, VM count and disk — the values every `null` dimension in
    a per-person or per-team override resolves to. Read this alongside `getUserQuotaOverride` or
    `getTeamQuotaOverride` to see what an override actually changes.

    These come from the host's configuration file, not the database, so they are read-only over the API:
    changing them means editing the host configuration and reloading. Every dimension is always present
    — a default is never absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminQuotaDefaultsResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> AdminQuotaDefaultsResponse | ApiError | CliTooOldBody | None:
    """Read the host-wide default resource caps

     The host's baseline caps for vCPUs, memory, VM count and disk — the values every `null` dimension in
    a per-person or per-team override resolves to. Read this alongside `getUserQuotaOverride` or
    `getTeamQuotaOverride` to see what an override actually changes.

    These come from the host's configuration file, not the database, so they are read-only over the API:
    changing them means editing the host configuration and reloading. Every dimension is always present
    — a default is never absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminQuotaDefaultsResponse | ApiError | CliTooOldBody
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminQuotaDefaultsResponse | ApiError | CliTooOldBody]:
    """Read the host-wide default resource caps

     The host's baseline caps for vCPUs, memory, VM count and disk — the values every `null` dimension in
    a per-person or per-team override resolves to. Read this alongside `getUserQuotaOverride` or
    `getTeamQuotaOverride` to see what an override actually changes.

    These come from the host's configuration file, not the database, so they are read-only over the API:
    changing them means editing the host configuration and reloading. Every dimension is always present
    — a default is never absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminQuotaDefaultsResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> AdminQuotaDefaultsResponse | ApiError | CliTooOldBody | None:
    """Read the host-wide default resource caps

     The host's baseline caps for vCPUs, memory, VM count and disk — the values every `null` dimension in
    a per-person or per-team override resolves to. Read this alongside `getUserQuotaOverride` or
    `getTeamQuotaOverride` to see what an override actually changes.

    These come from the host's configuration file, not the database, so they are read-only over the API:
    changing them means editing the host configuration and reloading. Every dimension is always present
    — a default is never absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminQuotaDefaultsResponse | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
