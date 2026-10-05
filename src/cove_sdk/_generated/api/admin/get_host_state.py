from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_host_state_response import AdminHostStateResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/host-state",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminHostStateResponse | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminHostStateResponse.from_dict(response.json())

        return response_200

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
) -> Response[AdminHostStateResponse | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminHostStateResponse | ApiError | CliTooOldBody]:
    """Read the host's administrative gauges

     Four host-wide counters for an administrator's dashboard, all read live and all informational — a
    failure computing any one of them yields a zero or an empty list rather than an error, because a
    broken gauge must not break the page.

    - `ttl_pending_count` — VMs whose expiry has come due and are waiting for the next sweep to remove
    them. Counts a VM once even when both expiry rules (delete-after-stop grace elapsed, maximum-
    lifetime cap exceeded) apply.
    - `audit_emit_failed_total` — audit-log rows this daemon process failed to write. Non-zero means the
    audit trail has gaps; a sustained rise means the audit log is effectively down.
    - `snapshot_images` — per-image disk usage of the retained start-up checkpoints Cove keeps so that
    creating a VM is fast: how many versions are retained per image and their summed apparent size.
    Sizes overstate what deleting them would actually reclaim, because copy-on-write extents are shared.
    - `snapshot_last_reap` — the most recent cleanup pass that actually freed space, or absent if none
    has this process.
    - `broadcast_lag` — per (channel, consumer) counts of events dropped because that consumer fell
    behind. Names which consumer is lagging and by how much.
    - `embedded_agent_version` — the version of the guest agent this daemon embeds for hot-patching, or
    `null` when the build embeds none (the daemon cannot hot-patch then; `POST /api/admin/update-agents`
    can still push an uploaded binary). A VM whose agent reports another version is not running the
    host's agent.

    Counters that say `this process` reset when the daemon restarts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminHostStateResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> AdminHostStateResponse | ApiError | CliTooOldBody | None:
    """Read the host's administrative gauges

     Four host-wide counters for an administrator's dashboard, all read live and all informational — a
    failure computing any one of them yields a zero or an empty list rather than an error, because a
    broken gauge must not break the page.

    - `ttl_pending_count` — VMs whose expiry has come due and are waiting for the next sweep to remove
    them. Counts a VM once even when both expiry rules (delete-after-stop grace elapsed, maximum-
    lifetime cap exceeded) apply.
    - `audit_emit_failed_total` — audit-log rows this daemon process failed to write. Non-zero means the
    audit trail has gaps; a sustained rise means the audit log is effectively down.
    - `snapshot_images` — per-image disk usage of the retained start-up checkpoints Cove keeps so that
    creating a VM is fast: how many versions are retained per image and their summed apparent size.
    Sizes overstate what deleting them would actually reclaim, because copy-on-write extents are shared.
    - `snapshot_last_reap` — the most recent cleanup pass that actually freed space, or absent if none
    has this process.
    - `broadcast_lag` — per (channel, consumer) counts of events dropped because that consumer fell
    behind. Names which consumer is lagging and by how much.
    - `embedded_agent_version` — the version of the guest agent this daemon embeds for hot-patching, or
    `null` when the build embeds none (the daemon cannot hot-patch then; `POST /api/admin/update-agents`
    can still push an uploaded binary). A VM whose agent reports another version is not running the
    host's agent.

    Counters that say `this process` reset when the daemon restarts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminHostStateResponse | ApiError | CliTooOldBody
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminHostStateResponse | ApiError | CliTooOldBody]:
    """Read the host's administrative gauges

     Four host-wide counters for an administrator's dashboard, all read live and all informational — a
    failure computing any one of them yields a zero or an empty list rather than an error, because a
    broken gauge must not break the page.

    - `ttl_pending_count` — VMs whose expiry has come due and are waiting for the next sweep to remove
    them. Counts a VM once even when both expiry rules (delete-after-stop grace elapsed, maximum-
    lifetime cap exceeded) apply.
    - `audit_emit_failed_total` — audit-log rows this daemon process failed to write. Non-zero means the
    audit trail has gaps; a sustained rise means the audit log is effectively down.
    - `snapshot_images` — per-image disk usage of the retained start-up checkpoints Cove keeps so that
    creating a VM is fast: how many versions are retained per image and their summed apparent size.
    Sizes overstate what deleting them would actually reclaim, because copy-on-write extents are shared.
    - `snapshot_last_reap` — the most recent cleanup pass that actually freed space, or absent if none
    has this process.
    - `broadcast_lag` — per (channel, consumer) counts of events dropped because that consumer fell
    behind. Names which consumer is lagging and by how much.
    - `embedded_agent_version` — the version of the guest agent this daemon embeds for hot-patching, or
    `null` when the build embeds none (the daemon cannot hot-patch then; `POST /api/admin/update-agents`
    can still push an uploaded binary). A VM whose agent reports another version is not running the
    host's agent.

    Counters that say `this process` reset when the daemon restarts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminHostStateResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> AdminHostStateResponse | ApiError | CliTooOldBody | None:
    """Read the host's administrative gauges

     Four host-wide counters for an administrator's dashboard, all read live and all informational — a
    failure computing any one of them yields a zero or an empty list rather than an error, because a
    broken gauge must not break the page.

    - `ttl_pending_count` — VMs whose expiry has come due and are waiting for the next sweep to remove
    them. Counts a VM once even when both expiry rules (delete-after-stop grace elapsed, maximum-
    lifetime cap exceeded) apply.
    - `audit_emit_failed_total` — audit-log rows this daemon process failed to write. Non-zero means the
    audit trail has gaps; a sustained rise means the audit log is effectively down.
    - `snapshot_images` — per-image disk usage of the retained start-up checkpoints Cove keeps so that
    creating a VM is fast: how many versions are retained per image and their summed apparent size.
    Sizes overstate what deleting them would actually reclaim, because copy-on-write extents are shared.
    - `snapshot_last_reap` — the most recent cleanup pass that actually freed space, or absent if none
    has this process.
    - `broadcast_lag` — per (channel, consumer) counts of events dropped because that consumer fell
    behind. Names which consumer is lagging and by how much.
    - `embedded_agent_version` — the version of the guest agent this daemon embeds for hot-patching, or
    `null` when the build embeds none (the daemon cannot hot-patch then; `POST /api/admin/update-agents`
    can still push an uploaded binary). A VM whose agent reports another version is not running the
    host's agent.

    Counters that say `this process` reset when the daemon restarts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminHostStateResponse | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
