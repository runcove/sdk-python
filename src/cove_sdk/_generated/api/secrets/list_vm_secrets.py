from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.secret_entry_dto import SecretEntryDto
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/secrets".format(
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_secret_name_list_item_data in _response_200:
            componentsschemas_secret_name_list_item = SecretEntryDto.from_dict(
                componentsschemas_secret_name_list_item_data
            )

            response_200.append(componentsschemas_secret_name_list_item)

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

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]:
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]:
    """List secret names on a VM

     Returns the names of every secret injected into this VM — never the values, which are never exposed
    over HTTP. Merges nothing: this is the VM's own store only, not the effective merged set it would
    receive at boot (the scope-merge precedence decides that).

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns the same **404** as an existent-but-inaccessible one
    (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto] | None:
    """List secret names on a VM

     Returns the names of every secret injected into this VM — never the values, which are never exposed
    over HTTP. Merges nothing: this is the VM's own store only, not the effective merged set it would
    receive at boot (the scope-merge precedence decides that).

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns the same **404** as an existent-but-inaccessible one
    (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]:
    """List secret names on a VM

     Returns the names of every secret injected into this VM — never the values, which are never exposed
    over HTTP. Merges nothing: this is the VM's own store only, not the effective merged set it would
    receive at boot (the scope-merge precedence decides that).

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns the same **404** as an existent-but-inaccessible one
    (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto] | None:
    """List secret names on a VM

     Returns the names of every secret injected into this VM — never the values, which are never exposed
    over HTTP. Merges nothing: this is the VM's own store only, not the effective merged set it would
    receive at boot (the scope-merge precedence decides that).

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns the same **404** as an existent-but-inaccessible one
    (existence non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
