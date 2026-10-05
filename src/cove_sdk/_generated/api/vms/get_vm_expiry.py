from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.ttl_policy_view import TtlPolicyView
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/expiry".format(
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView | None:
    if response.status_code == 200:
        response_200 = TtlPolicyView.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView]:
    """Get the VM's expiry policy and countdowns

     The configured expiry policy plus the live computed countdowns: `deletes_in_secs` (delete-after-stop
    grace, `None` unless stopped) and `max_life_expires_in_secs` (maximum-lifetime cap from creation,
    `None` if disabled).

    Named `getVmExpiry` rather than `getTtlState` — see `setVmExpiry`'s description for why `TTL` is
    retired from the public surface. `GET /api/vms/{name}/ttl-state` has been removed, not aliased — it
    answers 404. Call `GET /api/vms/{name}/expiry` instead.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView]
    """

    kwargs = _get_kwargs(
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView | None:
    """Get the VM's expiry policy and countdowns

     The configured expiry policy plus the live computed countdowns: `deletes_in_secs` (delete-after-stop
    grace, `None` unless stopped) and `max_life_expires_in_secs` (maximum-lifetime cap from creation,
    `None` if disabled).

    Named `getVmExpiry` rather than `getTtlState` — see `setVmExpiry`'s description for why `TTL` is
    retired from the public surface. `GET /api/vms/{name}/ttl-state` has been removed, not aliased — it
    answers 404. Call `GET /api/vms/{name}/expiry` instead.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView]:
    """Get the VM's expiry policy and countdowns

     The configured expiry policy plus the live computed countdowns: `deletes_in_secs` (delete-after-stop
    grace, `None` unless stopped) and `max_life_expires_in_secs` (maximum-lifetime cap from creation,
    `None` if disabled).

    Named `getVmExpiry` rather than `getTtlState` — see `setVmExpiry`'s description for why `TTL` is
    retired from the public surface. `GET /api/vms/{name}/ttl-state` has been removed, not aliased — it
    answers 404. Call `GET /api/vms/{name}/expiry` instead.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView]
    """

    kwargs = _get_kwargs(
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView | None:
    """Get the VM's expiry policy and countdowns

     The configured expiry policy plus the live computed countdowns: `deletes_in_secs` (delete-after-stop
    grace, `None` unless stopped) and `max_life_expires_in_secs` (maximum-lifetime cap from creation,
    `None` if disabled).

    Named `getVmExpiry` rather than `getTtlState` — see `setVmExpiry`'s description for why `TTL` is
    retired from the public surface. `GET /api/vms/{name}/ttl-state` has been removed, not aliased — it
    answers 404. Call `GET /api/vms/{name}/expiry` instead.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | TtlPolicyView
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
