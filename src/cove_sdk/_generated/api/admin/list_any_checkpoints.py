from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_checkpoint_summary_page import AdminCheckpointSummaryPage
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    user: str | Unset = UNSET,
    orphaned: bool | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["user"] = user

    params["orphaned"] = orphaned

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/checkpoints",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminCheckpointSummaryPage | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminCheckpointSummaryPage.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

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
) -> Response[AdminCheckpointSummaryPage | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    user: str | Unset = UNSET,
    orphaned: bool | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[AdminCheckpointSummaryPage | ApiError | CliTooOldBody]:
    """List every checkpoint on the host

     Every checkpoint across every owner, with the account that owns it, the name the source VM had when
    the checkpoint was taken, whether that VM still exists, and the checkpoint's on-disk size. This is
    the cross-tenant view — it discloses other people's checkpoints and owners — which is why it is
    administrator-only. `listCheckpoints` is the per-caller equivalent.

    Built for reclaiming disk. Pass `orphaned=true` to see only the checkpoints whose source VM has been
    deleted: nobody's per-caller listing shows those any more, so without this they accumulate with no
    way to find them. Pass `user` to narrow to one person's.

    `size_bytes` is a best-effort read of what the checkpoint occupies on disk and is `0` when the scan
    could not see it — informational, like the host gauges, not an accounting figure. `GET
    /api/admin/host-state` reports the orphan count and their total bytes if you only need the summary.

    Cursor-paginated, newest first (ties inside one second broken by checkpoint id, descending): at most
    `limit` rows come back, and `next_cursor` is non-null whenever more remain. A non-null `next_cursor`
    is the *only* signal that the list was cut short — pass it back as `?cursor=` (alongside `?user=`
    and `?orphaned=`, if set) and keep going until it is null to be sure you have every checkpoint. When
    it is set the response also carries a `Link: </api/admin/checkpoints?cursor=...>; rel="next"`
    header.

    Args:
        user (str | Unset):
        orphaned (bool | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminCheckpointSummaryPage | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        user=user,
        orphaned=orphaned,
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
    user: str | Unset = UNSET,
    orphaned: bool | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> AdminCheckpointSummaryPage | ApiError | CliTooOldBody | None:
    """List every checkpoint on the host

     Every checkpoint across every owner, with the account that owns it, the name the source VM had when
    the checkpoint was taken, whether that VM still exists, and the checkpoint's on-disk size. This is
    the cross-tenant view — it discloses other people's checkpoints and owners — which is why it is
    administrator-only. `listCheckpoints` is the per-caller equivalent.

    Built for reclaiming disk. Pass `orphaned=true` to see only the checkpoints whose source VM has been
    deleted: nobody's per-caller listing shows those any more, so without this they accumulate with no
    way to find them. Pass `user` to narrow to one person's.

    `size_bytes` is a best-effort read of what the checkpoint occupies on disk and is `0` when the scan
    could not see it — informational, like the host gauges, not an accounting figure. `GET
    /api/admin/host-state` reports the orphan count and their total bytes if you only need the summary.

    Cursor-paginated, newest first (ties inside one second broken by checkpoint id, descending): at most
    `limit` rows come back, and `next_cursor` is non-null whenever more remain. A non-null `next_cursor`
    is the *only* signal that the list was cut short — pass it back as `?cursor=` (alongside `?user=`
    and `?orphaned=`, if set) and keep going until it is null to be sure you have every checkpoint. When
    it is set the response also carries a `Link: </api/admin/checkpoints?cursor=...>; rel="next"`
    header.

    Args:
        user (str | Unset):
        orphaned (bool | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminCheckpointSummaryPage | ApiError | CliTooOldBody
    """

    return sync_detailed(
        client=client,
        user=user,
        orphaned=orphaned,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    user: str | Unset = UNSET,
    orphaned: bool | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[AdminCheckpointSummaryPage | ApiError | CliTooOldBody]:
    """List every checkpoint on the host

     Every checkpoint across every owner, with the account that owns it, the name the source VM had when
    the checkpoint was taken, whether that VM still exists, and the checkpoint's on-disk size. This is
    the cross-tenant view — it discloses other people's checkpoints and owners — which is why it is
    administrator-only. `listCheckpoints` is the per-caller equivalent.

    Built for reclaiming disk. Pass `orphaned=true` to see only the checkpoints whose source VM has been
    deleted: nobody's per-caller listing shows those any more, so without this they accumulate with no
    way to find them. Pass `user` to narrow to one person's.

    `size_bytes` is a best-effort read of what the checkpoint occupies on disk and is `0` when the scan
    could not see it — informational, like the host gauges, not an accounting figure. `GET
    /api/admin/host-state` reports the orphan count and their total bytes if you only need the summary.

    Cursor-paginated, newest first (ties inside one second broken by checkpoint id, descending): at most
    `limit` rows come back, and `next_cursor` is non-null whenever more remain. A non-null `next_cursor`
    is the *only* signal that the list was cut short — pass it back as `?cursor=` (alongside `?user=`
    and `?orphaned=`, if set) and keep going until it is null to be sure you have every checkpoint. When
    it is set the response also carries a `Link: </api/admin/checkpoints?cursor=...>; rel="next"`
    header.

    Args:
        user (str | Unset):
        orphaned (bool | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminCheckpointSummaryPage | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        user=user,
        orphaned=orphaned,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    user: str | Unset = UNSET,
    orphaned: bool | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> AdminCheckpointSummaryPage | ApiError | CliTooOldBody | None:
    """List every checkpoint on the host

     Every checkpoint across every owner, with the account that owns it, the name the source VM had when
    the checkpoint was taken, whether that VM still exists, and the checkpoint's on-disk size. This is
    the cross-tenant view — it discloses other people's checkpoints and owners — which is why it is
    administrator-only. `listCheckpoints` is the per-caller equivalent.

    Built for reclaiming disk. Pass `orphaned=true` to see only the checkpoints whose source VM has been
    deleted: nobody's per-caller listing shows those any more, so without this they accumulate with no
    way to find them. Pass `user` to narrow to one person's.

    `size_bytes` is a best-effort read of what the checkpoint occupies on disk and is `0` when the scan
    could not see it — informational, like the host gauges, not an accounting figure. `GET
    /api/admin/host-state` reports the orphan count and their total bytes if you only need the summary.

    Cursor-paginated, newest first (ties inside one second broken by checkpoint id, descending): at most
    `limit` rows come back, and `next_cursor` is non-null whenever more remain. A non-null `next_cursor`
    is the *only* signal that the list was cut short — pass it back as `?cursor=` (alongside `?user=`
    and `?orphaned=`, if set) and keep going until it is null to be sure you have every checkpoint. When
    it is set the response also carries a `Link: </api/admin/checkpoints?cursor=...>; rel="next"`
    header.

    Args:
        user (str | Unset):
        orphaned (bool | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminCheckpointSummaryPage | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
            user=user,
            orphaned=orphaned,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
