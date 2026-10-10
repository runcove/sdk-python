from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.proxy_url_info import ProxyUrlInfo
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/url".format(
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = ProxyUrlInfo.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody]:
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
) -> Response[ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody]:
    """Proxy URLs for a VM

     The VM's SSH connection URL plus every registered HTTPS proxy port, each with its `public` flag and
    the URL a caller would actually reach it at (portless for the primary port, shape-specific for the
    rest).

    `web_url` is the address Cove's web app is served on, from the server's configuration
    (`[daemon.cli_releases] public_url`, else `https://<api_external_host>`); the VM's page there is
    `<web_url>/vms/<vm_name>`, and opening it needs a Cove sign-in. It is absent when the server has no
    web address configured.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody]
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
) -> ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody | None:
    """Proxy URLs for a VM

     The VM's SSH connection URL plus every registered HTTPS proxy port, each with its `public` flag and
    the URL a caller would actually reach it at (portless for the primary port, shape-specific for the
    rest).

    `web_url` is the address Cove's web app is served on, from the server's configuration
    (`[daemon.cli_releases] public_url`, else `https://<api_external_host>`); the VM's page there is
    `<web_url>/vms/<vm_name>`, and opening it needs a Cove sign-in. It is absent when the server has no
    web address configured.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody]:
    """Proxy URLs for a VM

     The VM's SSH connection URL plus every registered HTTPS proxy port, each with its `public` flag and
    the URL a caller would actually reach it at (portless for the primary port, shape-specific for the
    rest).

    `web_url` is the address Cove's web app is served on, from the server's configuration
    (`[daemon.cli_releases] public_url`, else `https://<api_external_host>`); the VM's page there is
    `<web_url>/vms/<vm_name>`, and opening it needs a Cove sign-in. It is absent when the server has no
    web address configured.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody]
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
) -> ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody | None:
    """Proxy URLs for a VM

     The VM's SSH connection URL plus every registered HTTPS proxy port, each with its `public` flag and
    the URL a caller would actually reach it at (portless for the primary port, shape-specific for the
    rest).

    `web_url` is the address Cove's web app is served on, from the server's configuration
    (`[daemon.cli_releases] public_url`, else `https://<api_external_host>`); the VM's page there is
    `<web_url>/vms/<vm_name>`, and opening it needs a Cove sign-in. It is absent when the server has no
    web address configured.

    A VM that does not exist, or is not visible to the caller, returns 404 (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ProxyUrlInfo | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
