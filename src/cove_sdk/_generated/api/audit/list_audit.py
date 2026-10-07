from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.audit_page import AuditPage
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    vm: str | Unset = UNSET,
    user: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    key_id: str | Unset = UNSET,
    source_ip: str | Unset = UNSET,
    since: str | Unset = UNSET,
    until: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["vm"] = vm

    params["user"] = user

    params["kind"] = kind

    params["key_id"] = key_id

    params["source_ip"] = source_ip

    params["since"] = since

    params["until"] = until

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/audit",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = AuditPage.from_dict(response.json())

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

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

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
) -> Response[ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    vm: str | Unset = UNSET,
    user: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    key_id: str | Unset = UNSET,
    source_ip: str | Unset = UNSET,
    since: str | Unset = UNSET,
    until: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody]:
    """Query the audit log

     Cursor-paginated. Non-admin callers only see their own entries; a `user` filter naming someone else
    yields an empty page rather than an error — cross-user existence is not disclosed. When another page
    is available the response also carries a `Link: </api/audit?cursor=...>; rel="next"` header.

    Args:
        vm (str | Unset):
        user (str | Unset):
        kind (str | Unset):
        key_id (str | Unset):
        source_ip (str | Unset):
        since (str | Unset):
        until (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        vm=vm,
        user=user,
        kind=kind,
        key_id=key_id,
        source_ip=source_ip,
        since=since,
        until=until,
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
    vm: str | Unset = UNSET,
    user: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    key_id: str | Unset = UNSET,
    source_ip: str | Unset = UNSET,
    since: str | Unset = UNSET,
    until: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody | None:
    """Query the audit log

     Cursor-paginated. Non-admin callers only see their own entries; a `user` filter naming someone else
    yields an empty page rather than an error — cross-user existence is not disclosed. When another page
    is available the response also carries a `Link: </api/audit?cursor=...>; rel="next"` header.

    Args:
        vm (str | Unset):
        user (str | Unset):
        kind (str | Unset):
        key_id (str | Unset):
        source_ip (str | Unset):
        since (str | Unset):
        until (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        client=client,
        vm=vm,
        user=user,
        kind=kind,
        key_id=key_id,
        source_ip=source_ip,
        since=since,
        until=until,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    vm: str | Unset = UNSET,
    user: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    key_id: str | Unset = UNSET,
    source_ip: str | Unset = UNSET,
    since: str | Unset = UNSET,
    until: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody]:
    """Query the audit log

     Cursor-paginated. Non-admin callers only see their own entries; a `user` filter naming someone else
    yields an empty page rather than an error — cross-user existence is not disclosed. When another page
    is available the response also carries a `Link: </api/audit?cursor=...>; rel="next"` header.

    Args:
        vm (str | Unset):
        user (str | Unset):
        kind (str | Unset):
        key_id (str | Unset):
        source_ip (str | Unset):
        since (str | Unset):
        until (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        vm=vm,
        user=user,
        kind=kind,
        key_id=key_id,
        source_ip=source_ip,
        since=since,
        until=until,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    vm: str | Unset = UNSET,
    user: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    key_id: str | Unset = UNSET,
    source_ip: str | Unset = UNSET,
    since: str | Unset = UNSET,
    until: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody | None:
    """Query the audit log

     Cursor-paginated. Non-admin callers only see their own entries; a `user` filter naming someone else
    yields an empty page rather than an error — cross-user existence is not disclosed. When another page
    is available the response also carries a `Link: </api/audit?cursor=...>; rel="next"` header.

    Args:
        vm (str | Unset):
        user (str | Unset):
        kind (str | Unset):
        key_id (str | Unset):
        source_ip (str | Unset):
        since (str | Unset):
        until (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | AuditPage | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            client=client,
            vm=vm,
            user=user,
            kind=kind,
            key_id=key_id,
            source_ip=source_ip,
            since=since,
            until=until,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
