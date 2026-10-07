from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.primary_port_not_removable_body import PrimaryPortNotRemovableBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    port: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/vms/{name}/ports/{port}".format(
            name=quote(str(name), safe=""),
            port=quote(str(port), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | ApiError
    | CliTooOldBody
    | PrimaryPortNotRemovableBody
    | ScopeDeniedBody
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = PrimaryPortNotRemovableBody.from_dict(response.json())

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
) -> Response[
    Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody
]:
    """Remove an exposed port

     Unregisters a guest port from the HTTPS proxy and revokes any invite links minted for it.

    Returns **422** `cannot_remove_primary_port` when `port` is the VM's current primary port — switch
    the primary port first (`PUT .../primary-port`). The body is an `ApiError` envelope with an extra
    `port` field not modeled in the schema. A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        port=port,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
) -> (
    Any
    | ApiError
    | CliTooOldBody
    | PrimaryPortNotRemovableBody
    | ScopeDeniedBody
    | None
):
    """Remove an exposed port

     Unregisters a guest port from the HTTPS proxy and revokes any invite links minted for it.

    Returns **422** `cannot_remove_primary_port` when `port` is the VM's current primary port — switch
    the primary port first (`PUT .../primary-port`). The body is an `ApiError` envelope with an extra
    `port` field not modeled in the schema. A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        port=port,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody
]:
    """Remove an exposed port

     Unregisters a guest port from the HTTPS proxy and revokes any invite links minted for it.

    Returns **422** `cannot_remove_primary_port` when `port` is the VM's current primary port — switch
    the primary port first (`PUT .../primary-port`). The body is an `ApiError` envelope with an extra
    `port` field not modeled in the schema. A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        port=port,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
) -> (
    Any
    | ApiError
    | CliTooOldBody
    | PrimaryPortNotRemovableBody
    | ScopeDeniedBody
    | None
):
    """Remove an exposed port

     Unregisters a guest port from the HTTPS proxy and revokes any invite links minted for it.

    Returns **422** `cannot_remove_primary_port` when `port` is the VM's current primary port — switch
    the primary port first (`PUT .../primary-port`). The body is an `ApiError` envelope with an extra
    `port` field not modeled in the schema. A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PrimaryPortNotRemovableBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            port=port,
            client=client,
        )
    ).parsed
