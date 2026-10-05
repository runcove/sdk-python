from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.images_response import ImagesResponse
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/images",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = ImagesResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

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
) -> Response[ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody]:
    """Available images and OCI cache

     Every image the host can create a VM from, alias-first (an alias may resolve to more than one
    underlying image; `aliases` lists the others), plus the build cache of images fetched from an OCI
    registry.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody | None:
    """Available images and OCI cache

     Every image the host can create a VM from, alias-first (an alias may resolve to more than one
    underlying image; `aliases` lists the others), plus the build cache of images fetched from an OCI
    registry.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody]:
    """Available images and OCI cache

     Every image the host can create a VM from, alias-first (an alias may resolve to more than one
    underlying image; `aliases` lists the others), plus the build cache of images fetched from an OCI
    registry.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody | None:
    """Available images and OCI cache

     Every image the host can create a VM from, alias-first (an alias may resolve to more than one
    underlying image; `aliases` lists the others), plus the build cache of images fetched from an OCI
    registry.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ImagesResponse | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
