from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.vm_events_page import VmEventsPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/events-log".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage | None:
    if response.status_code == 200:
        response_200 = VmEventsPage.from_dict(response.json())

        return response_200

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

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage]:
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
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage]:
    """Per-VM event log (cursor-paginated)

     Newest-first slice of persisted lifecycle events for one VM. Distinct from `GET
    /api/vms/{name}/events`, which streams events live over SSE rather than returning a persisted,
    paginated page.

    Args:
        name (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage]
    """

    kwargs = _get_kwargs(
        name=name,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage | None:
    """Per-VM event log (cursor-paginated)

     Newest-first slice of persisted lifecycle events for one VM. Distinct from `GET
    /api/vms/{name}/events`, which streams events live over SSE rather than returning a persisted,
    paginated page.

    Args:
        name (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage
    """

    return sync_detailed(
        name=name,
        client=client,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage]:
    """Per-VM event log (cursor-paginated)

     Newest-first slice of persisted lifecycle events for one VM. Distinct from `GET
    /api/vms/{name}/events`, which streams events live over SSE rather than returning a persisted,
    paginated page.

    Args:
        name (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage]
    """

    kwargs = _get_kwargs(
        name=name,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage | None:
    """Per-VM event log (cursor-paginated)

     Newest-first slice of persisted lifecycle events for one VM. Distinct from `GET
    /api/vms/{name}/events`, which streams events live over SSE rather than returning a persisted,
    paginated page.

    Args:
        name (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmEventsPage
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
