from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_vm_summary_page import AdminVmSummaryPage
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    user: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["user"] = user

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/vms",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminVmSummaryPage | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminVmSummaryPage.from_dict(response.json())

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
) -> Response[AdminVmSummaryPage | ApiError | CliTooOldBody]:
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
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[AdminVmSummaryPage | ApiError | CliTooOldBody]:
    """List every VM on the host

     Every VM across every tenant, with its owner, state, image, expiry settings and three timestamps.
    Pass `user` to narrow it to one person's VMs. This is the cross-tenant view — it discloses other
    people's VM names and owners — which is why it is administrator-only. `listVms` is the per-caller
    equivalent.

    Built for finding abandoned machines. `last_activity_at` is the reliable idleness signal but is
    absent until Cove has observed the VM being used at least once, and stays absent for VMs configured
    never to pause; `updated_at` is the fallback, and moves on every state change rather than on real
    use. Sort by `last_activity_at` falling back to `updated_at`, and treat `created_at` as age rather
    than idleness.

    `degraded` marks a VM Cove can see but cannot reach cleanly. `owner` is absent for the unassigned
    VMs Cove keeps ready so creation is fast; those also report the `pooled` state, which is an
    administrator-only concept and never appears in a per-caller listing.

    Cursor-paginated, ordered `vm_name` ascending: at most `limit` rows come back, and `next_cursor` is
    non-null whenever more remain. A non-null `next_cursor` is the *only* signal that the list was cut
    short — pass it back as `?cursor=` (alongside `?user=`, if set) and keep going until it is null to
    be sure you have every VM. When it is set the response also carries a `Link:
    </api/admin/vms?cursor=...>; rel="next"` header.

    Args:
        user (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminVmSummaryPage | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        user=user,
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
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> AdminVmSummaryPage | ApiError | CliTooOldBody | None:
    """List every VM on the host

     Every VM across every tenant, with its owner, state, image, expiry settings and three timestamps.
    Pass `user` to narrow it to one person's VMs. This is the cross-tenant view — it discloses other
    people's VM names and owners — which is why it is administrator-only. `listVms` is the per-caller
    equivalent.

    Built for finding abandoned machines. `last_activity_at` is the reliable idleness signal but is
    absent until Cove has observed the VM being used at least once, and stays absent for VMs configured
    never to pause; `updated_at` is the fallback, and moves on every state change rather than on real
    use. Sort by `last_activity_at` falling back to `updated_at`, and treat `created_at` as age rather
    than idleness.

    `degraded` marks a VM Cove can see but cannot reach cleanly. `owner` is absent for the unassigned
    VMs Cove keeps ready so creation is fast; those also report the `pooled` state, which is an
    administrator-only concept and never appears in a per-caller listing.

    Cursor-paginated, ordered `vm_name` ascending: at most `limit` rows come back, and `next_cursor` is
    non-null whenever more remain. A non-null `next_cursor` is the *only* signal that the list was cut
    short — pass it back as `?cursor=` (alongside `?user=`, if set) and keep going until it is null to
    be sure you have every VM. When it is set the response also carries a `Link:
    </api/admin/vms?cursor=...>; rel="next"` header.

    Args:
        user (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminVmSummaryPage | ApiError | CliTooOldBody
    """

    return sync_detailed(
        client=client,
        user=user,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    user: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[AdminVmSummaryPage | ApiError | CliTooOldBody]:
    """List every VM on the host

     Every VM across every tenant, with its owner, state, image, expiry settings and three timestamps.
    Pass `user` to narrow it to one person's VMs. This is the cross-tenant view — it discloses other
    people's VM names and owners — which is why it is administrator-only. `listVms` is the per-caller
    equivalent.

    Built for finding abandoned machines. `last_activity_at` is the reliable idleness signal but is
    absent until Cove has observed the VM being used at least once, and stays absent for VMs configured
    never to pause; `updated_at` is the fallback, and moves on every state change rather than on real
    use. Sort by `last_activity_at` falling back to `updated_at`, and treat `created_at` as age rather
    than idleness.

    `degraded` marks a VM Cove can see but cannot reach cleanly. `owner` is absent for the unassigned
    VMs Cove keeps ready so creation is fast; those also report the `pooled` state, which is an
    administrator-only concept and never appears in a per-caller listing.

    Cursor-paginated, ordered `vm_name` ascending: at most `limit` rows come back, and `next_cursor` is
    non-null whenever more remain. A non-null `next_cursor` is the *only* signal that the list was cut
    short — pass it back as `?cursor=` (alongside `?user=`, if set) and keep going until it is null to
    be sure you have every VM. When it is set the response also carries a `Link:
    </api/admin/vms?cursor=...>; rel="next"` header.

    Args:
        user (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminVmSummaryPage | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        user=user,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    user: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> AdminVmSummaryPage | ApiError | CliTooOldBody | None:
    """List every VM on the host

     Every VM across every tenant, with its owner, state, image, expiry settings and three timestamps.
    Pass `user` to narrow it to one person's VMs. This is the cross-tenant view — it discloses other
    people's VM names and owners — which is why it is administrator-only. `listVms` is the per-caller
    equivalent.

    Built for finding abandoned machines. `last_activity_at` is the reliable idleness signal but is
    absent until Cove has observed the VM being used at least once, and stays absent for VMs configured
    never to pause; `updated_at` is the fallback, and moves on every state change rather than on real
    use. Sort by `last_activity_at` falling back to `updated_at`, and treat `created_at` as age rather
    than idleness.

    `degraded` marks a VM Cove can see but cannot reach cleanly. `owner` is absent for the unassigned
    VMs Cove keeps ready so creation is fast; those also report the `pooled` state, which is an
    administrator-only concept and never appears in a per-caller listing.

    Cursor-paginated, ordered `vm_name` ascending: at most `limit` rows come back, and `next_cursor` is
    non-null whenever more remain. A non-null `next_cursor` is the *only* signal that the list was cut
    short — pass it back as `?cursor=` (alongside `?user=`, if set) and keep going until it is null to
    be sure you have every VM. When it is set the response also carries a `Link:
    </api/admin/vms?cursor=...>; rel="next"` header.

    Args:
        user (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminVmSummaryPage | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
            user=user,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
