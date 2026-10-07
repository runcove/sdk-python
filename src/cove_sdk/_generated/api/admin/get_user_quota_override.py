from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_quota_override_response import AdminQuotaOverrideResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/quotas/{username}".format(
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminQuotaOverrideResponse | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminQuotaOverrideResponse.from_dict(response.json())

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
) -> Response[AdminQuotaOverrideResponse | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminQuotaOverrideResponse | ApiError | CliTooOldBody]:
    """Read one person's resource-cap overrides

     The four per-person caps — vCPUs, memory, VM count and disk — as *overrides*, not as effective
    limits. A dimension reads `null` when that person has no override for it and the host default
    applies; read the defaults from `getQuotaDefaults` to work out what a `null` resolves to.

    A person with no overrides at all answers 200 with all four `null`, not 404.

    This reports caps only, not usage. For what someone is actually consuming against those caps, use
    `listAllUsers`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminQuotaOverrideResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> AdminQuotaOverrideResponse | ApiError | CliTooOldBody | None:
    """Read one person's resource-cap overrides

     The four per-person caps — vCPUs, memory, VM count and disk — as *overrides*, not as effective
    limits. A dimension reads `null` when that person has no override for it and the host default
    applies; read the defaults from `getQuotaDefaults` to work out what a `null` resolves to.

    A person with no overrides at all answers 200 with all four `null`, not 404.

    This reports caps only, not usage. For what someone is actually consuming against those caps, use
    `listAllUsers`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminQuotaOverrideResponse | ApiError | CliTooOldBody
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminQuotaOverrideResponse | ApiError | CliTooOldBody]:
    """Read one person's resource-cap overrides

     The four per-person caps — vCPUs, memory, VM count and disk — as *overrides*, not as effective
    limits. A dimension reads `null` when that person has no override for it and the host default
    applies; read the defaults from `getQuotaDefaults` to work out what a `null` resolves to.

    A person with no overrides at all answers 200 with all four `null`, not 404.

    This reports caps only, not usage. For what someone is actually consuming against those caps, use
    `listAllUsers`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminQuotaOverrideResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> AdminQuotaOverrideResponse | ApiError | CliTooOldBody | None:
    """Read one person's resource-cap overrides

     The four per-person caps — vCPUs, memory, VM count and disk — as *overrides*, not as effective
    limits. A dimension reads `null` when that person has no override for it and the host default
    applies; read the defaults from `getQuotaDefaults` to work out what a `null` resolves to.

    A person with no overrides at all answers 200 with all four `null`, not 404.

    This reports caps only, not usage. For what someone is actually consuming against those caps, use
    `listAllUsers`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminQuotaOverrideResponse | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
