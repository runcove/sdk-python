from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.checkpoint_page import CheckpointPage
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
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
        "url": "/api/checkpoints",
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
) -> Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]:
    """List every checkpoint owned by the caller (including orphans)

     Checkpoints the caller owns across every VM, including orphan checkpoints whose source VM was
    deleted. Lets `cove checkpoint ls` (no VM name) work without aggregating per-VM calls.

    An orphan has an empty `vm_id` and carries `orphaned_at`, when its VM was deleted. The server
    deletes an orphan on its own once `[service] orphan_checkpoint_reclaim_days` (default 14) have
    passed since then, unless a clone of it still exists; `reclaim_at` says when, and is absent while a
    clone exists. With that setting at `0` nothing is reclaimed and no checkpoint carries `reclaim_at`.

    Cursor-paginated, with the same envelope, parameters and ordering as the per-VM `GET
    /api/vms/{name}/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever
    more remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it
    back as `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is
    set the response also carries a `Link: </api/checkpoints?cursor=...>; rel="next"` header.

    Args:
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody | None:
    """List every checkpoint owned by the caller (including orphans)

     Checkpoints the caller owns across every VM, including orphan checkpoints whose source VM was
    deleted. Lets `cove checkpoint ls` (no VM name) work without aggregating per-VM calls.

    An orphan has an empty `vm_id` and carries `orphaned_at`, when its VM was deleted. The server
    deletes an orphan on its own once `[service] orphan_checkpoint_reclaim_days` (default 14) have
    passed since then, unless a clone of it still exists; `reclaim_at` says when, and is absent while a
    clone exists. With that setting at `0` nothing is reclaimed and no checkpoint carries `reclaim_at`.

    Cursor-paginated, with the same envelope, parameters and ordering as the per-VM `GET
    /api/vms/{name}/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever
    more remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it
    back as `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is
    set the response also carries a `Link: </api/checkpoints?cursor=...>; rel="next"` header.

    Args:
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]:
    """List every checkpoint owned by the caller (including orphans)

     Checkpoints the caller owns across every VM, including orphan checkpoints whose source VM was
    deleted. Lets `cove checkpoint ls` (no VM name) work without aggregating per-VM calls.

    An orphan has an empty `vm_id` and carries `orphaned_at`, when its VM was deleted. The server
    deletes an orphan on its own once `[service] orphan_checkpoint_reclaim_days` (default 14) have
    passed since then, unless a clone of it still exists; `reclaim_at` says when, and is absent while a
    clone exists. With that setting at `0` nothing is reclaimed and no checkpoint carries `reclaim_at`.

    Cursor-paginated, with the same envelope, parameters and ordering as the per-VM `GET
    /api/vms/{name}/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever
    more remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it
    back as `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is
    set the response also carries a `Link: </api/checkpoints?cursor=...>; rel="next"` header.

    Args:
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ApiError | CheckpointPage | CliTooOldBody | ScopeDeniedBody | None:
    """List every checkpoint owned by the caller (including orphans)

     Checkpoints the caller owns across every VM, including orphan checkpoints whose source VM was
    deleted. Lets `cove checkpoint ls` (no VM name) work without aggregating per-VM calls.

    An orphan has an empty `vm_id` and carries `orphaned_at`, when its VM was deleted. The server
    deletes an orphan on its own once `[service] orphan_checkpoint_reclaim_days` (default 14) have
    passed since then, unless a clone of it still exists; `reclaim_at` says when, and is absent while a
    clone exists. With that setting at `0` nothing is reclaimed and no checkpoint carries `reclaim_at`.

    Cursor-paginated, with the same envelope, parameters and ordering as the per-VM `GET
    /api/vms/{name}/checkpoints`: at most `limit` rows come back, and `next_cursor` is non-null whenever
    more remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it
    back as `?cursor=` and keep going until it is null to be sure you have every checkpoint. When it is
    set the response also carries a `Link: </api/checkpoints?cursor=...>; rel="next"` header.

    Args:
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
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
