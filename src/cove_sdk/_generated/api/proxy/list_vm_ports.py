from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.proxy_port_info import ProxyPortInfo
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/ports".format(
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProxyPortInfo.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]]:
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]]:
    """List a VM's exposed ports

     Every port registered for this VM's HTTPS proxy, each with its `public` flag and `is_primary`
    marker. The sole read path for port/public state — `PUT .../ports/{port}/public` only writes one
    port's flag and has no GET counterpart.

    Named `listVmPorts` rather than `getVmShareStatus` — the public surface no longer uses the bare word
    `share`, and this is a `list` of the `ports` collection like any other.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo] | None:
    """List a VM's exposed ports

     Every port registered for this VM's HTTPS proxy, each with its `public` flag and `is_primary`
    marker. The sole read path for port/public state — `PUT .../ports/{port}/public` only writes one
    port's flag and has no GET counterpart.

    Named `listVmPorts` rather than `getVmShareStatus` — the public surface no longer uses the bare word
    `share`, and this is a `list` of the `ports` collection like any other.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]]:
    """List a VM's exposed ports

     Every port registered for this VM's HTTPS proxy, each with its `public` flag and `is_primary`
    marker. The sole read path for port/public state — `PUT .../ports/{port}/public` only writes one
    port's flag and has no GET counterpart.

    Named `listVmPorts` rather than `getVmShareStatus` — the public surface no longer uses the bare word
    `share`, and this is a `list` of the `ports` collection like any other.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo] | None:
    """List a VM's exposed ports

     Every port registered for this VM's HTTPS proxy, each with its `public` flag and `is_primary`
    marker. The sole read path for port/public state — `PUT .../ports/{port}/public` only writes one
    port's flag and has no GET counterpart.

    Named `listVmPorts` rather than `getVmShareStatus` — the public surface no longer uses the bare word
    `share`, and this is a `list` of the `ports` collection like any other.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[ProxyPortInfo]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
