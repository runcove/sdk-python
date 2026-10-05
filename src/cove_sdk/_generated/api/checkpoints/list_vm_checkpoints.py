from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.checkpoint_page import CheckpointPage
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/checkpoints".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = CheckpointPage.from_dict(response.json())

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
) -> Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]:
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
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]:
    """List a VM's checkpoints

     Checkpoints taken of this VM, most recent first.

    Cursor-paginated, with the same envelope, parameters and ordering as the top-level `GET
    /api/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is set the
    response also carries a `Link: </api/vms/{name}/checkpoints?cursor=...>; rel="next"` header.

    Args:
        name (str):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody | None:
    """List a VM's checkpoints

     Checkpoints taken of this VM, most recent first.

    Cursor-paginated, with the same envelope, parameters and ordering as the top-level `GET
    /api/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is set the
    response also carries a `Link: </api/vms/{name}/checkpoints?cursor=...>; rel="next"` header.

    Args:
        name (str):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]:
    """List a VM's checkpoints

     Checkpoints taken of this VM, most recent first.

    Cursor-paginated, with the same envelope, parameters and ordering as the top-level `GET
    /api/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is set the
    response also carries a `Link: </api/vms/{name}/checkpoints?cursor=...>; rel="next"` header.

    Args:
        name (str):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody | None:
    """List a VM's checkpoints

     Checkpoints taken of this VM, most recent first.

    Cursor-paginated, with the same envelope, parameters and ordering as the top-level `GET
    /api/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is set the
    response also carries a `Link: </api/vms/{name}/checkpoints?cursor=...>; rel="next"` header.

    Args:
        name (str):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
