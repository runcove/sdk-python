from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.vm_summary_page import VmSummaryPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    state: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
    tag: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["state"] = state

    params["limit"] = limit

    params["cursor"] = cursor

    json_tag: list[str] | Unset = UNSET
    if not isinstance(tag, Unset):
        json_tag = tag

    params["tag"] = json_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage | None:
    if response.status_code == 200:
        response_200 = VmSummaryPage.from_dict(response.json())

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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    state: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
    tag: list[str] | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage]:
    """List VMs visible to the caller

     Returns the caller's own VMs plus any shared with them, ordered by `name` ascending. Query
    parameters narrow the result. A filter value the server cannot apply — an unknown `state`, a `tag`
    that is not `key=value`, a `limit` of 0 — is refused with **400** `validation_failed` naming the
    parameter in `field`, never ignored: an ignored filter would answer with every VM. The same holds
    for a query key the server does not read: any key other than `state`, `tag`, `limit` and `cursor`
    (`?tags=`, `?status=`, `?State=`; keys are case-sensitive and compared after percent-decoding) is
    refused with **400** `validation_failed`, `field` naming the first such key in query-string order.

    Cursor-paginated: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` to continue, and keep going until it is null to be sure you have every VM. When it is set
    the response also carries a `Link: </api/vms?cursor=...>; rel="next"` header.

    Args:
        state (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):
        tag (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage]
    """

    kwargs = _get_kwargs(
        state=state,
        limit=limit,
        cursor=cursor,
        tag=tag,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    state: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
    tag: list[str] | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage | None:
    """List VMs visible to the caller

     Returns the caller's own VMs plus any shared with them, ordered by `name` ascending. Query
    parameters narrow the result. A filter value the server cannot apply — an unknown `state`, a `tag`
    that is not `key=value`, a `limit` of 0 — is refused with **400** `validation_failed` naming the
    parameter in `field`, never ignored: an ignored filter would answer with every VM. The same holds
    for a query key the server does not read: any key other than `state`, `tag`, `limit` and `cursor`
    (`?tags=`, `?status=`, `?State=`; keys are case-sensitive and compared after percent-decoding) is
    refused with **400** `validation_failed`, `field` naming the first such key in query-string order.

    Cursor-paginated: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` to continue, and keep going until it is null to be sure you have every VM. When it is set
    the response also carries a `Link: </api/vms?cursor=...>; rel="next"` header.

    Args:
        state (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):
        tag (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage
    """

    return sync_detailed(
        client=client,
        state=state,
        limit=limit,
        cursor=cursor,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    state: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
    tag: list[str] | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage]:
    """List VMs visible to the caller

     Returns the caller's own VMs plus any shared with them, ordered by `name` ascending. Query
    parameters narrow the result. A filter value the server cannot apply — an unknown `state`, a `tag`
    that is not `key=value`, a `limit` of 0 — is refused with **400** `validation_failed` naming the
    parameter in `field`, never ignored: an ignored filter would answer with every VM. The same holds
    for a query key the server does not read: any key other than `state`, `tag`, `limit` and `cursor`
    (`?tags=`, `?status=`, `?State=`; keys are case-sensitive and compared after percent-decoding) is
    refused with **400** `validation_failed`, `field` naming the first such key in query-string order.

    Cursor-paginated: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` to continue, and keep going until it is null to be sure you have every VM. When it is set
    the response also carries a `Link: </api/vms?cursor=...>; rel="next"` header.

    Args:
        state (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):
        tag (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage]
    """

    kwargs = _get_kwargs(
        state=state,
        limit=limit,
        cursor=cursor,
        tag=tag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    state: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
    tag: list[str] | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage | None:
    """List VMs visible to the caller

     Returns the caller's own VMs plus any shared with them, ordered by `name` ascending. Query
    parameters narrow the result. A filter value the server cannot apply — an unknown `state`, a `tag`
    that is not `key=value`, a `limit` of 0 — is refused with **400** `validation_failed` naming the
    parameter in `field`, never ignored: an ignored filter would answer with every VM. The same holds
    for a query key the server does not read: any key other than `state`, `tag`, `limit` and `cursor`
    (`?tags=`, `?status=`, `?State=`; keys are case-sensitive and compared after percent-decoding) is
    refused with **400** `validation_failed`, `field` naming the first such key in query-string order.

    Cursor-paginated: at most `limit` rows come back, and `next_cursor` is non-null whenever more
    remain. A non-null `next_cursor` is the *only* signal that the list was cut short — pass it back as
    `?cursor=` to continue, and keep going until it is null to be sure you have every VM. When it is set
    the response also carries a `Link: </api/vms?cursor=...>; rel="next"` header.

    Args:
        state (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):
        tag (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmSummaryPage
    """

    return (
        await asyncio_detailed(
            client=client,
            state=state,
            limit=limit,
            cursor=cursor,
            tag=tag,
        )
    ).parsed
