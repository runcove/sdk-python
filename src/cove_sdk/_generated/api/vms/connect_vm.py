from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.connection_info import ConnectionInfo
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/connect".format(
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = ConnectionInfo.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ApiError.from_dict(response.json())

        return response_409

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody]:
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
) -> Response[ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody]:
    """Mint an SSH connection ticket

     Mints a one-time Warpgate ticket for SSH access to the VM. Combine `ticket_secret` with
    `warpgate_host` / `warpgate_port` to connect; pin `warpgate_ssh_host_pubkey` before the first
    connection to avoid a TOFU prompt.

    A **409** issued seconds after `POST /api/vms` means the create is still claiming a pool VM: wait on
    `GET /api/vms/{name}/events` (or poll `GET /api/vms/{name}` until it leaves `creating`) and retry.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody]
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
) -> ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody | None:
    """Mint an SSH connection ticket

     Mints a one-time Warpgate ticket for SSH access to the VM. Combine `ticket_secret` with
    `warpgate_host` / `warpgate_port` to connect; pin `warpgate_ssh_host_pubkey` before the first
    connection to avoid a TOFU prompt.

    A **409** issued seconds after `POST /api/vms` means the create is still claiming a pool VM: wait on
    `GET /api/vms/{name}/events` (or poll `GET /api/vms/{name}` until it leaves `creating`) and retry.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody]:
    """Mint an SSH connection ticket

     Mints a one-time Warpgate ticket for SSH access to the VM. Combine `ticket_secret` with
    `warpgate_host` / `warpgate_port` to connect; pin `warpgate_ssh_host_pubkey` before the first
    connection to avoid a TOFU prompt.

    A **409** issued seconds after `POST /api/vms` means the create is still claiming a pool VM: wait on
    `GET /api/vms/{name}/events` (or poll `GET /api/vms/{name}` until it leaves `creating`) and retry.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody]
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
) -> ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody | None:
    """Mint an SSH connection ticket

     Mints a one-time Warpgate ticket for SSH access to the VM. Combine `ticket_secret` with
    `warpgate_host` / `warpgate_port` to connect; pin `warpgate_ssh_host_pubkey` before the first
    connection to avoid a TOFU prompt.

    A **409** issued seconds after `POST /api/vms` means the create is still claiming a pool VM: wait on
    `GET /api/vms/{name}/events` (or poll `GET /api/vms/{name}` until it leaves `creating`) and retry.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ConnectionInfo | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
