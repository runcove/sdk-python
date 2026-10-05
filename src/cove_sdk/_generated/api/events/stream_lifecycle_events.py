from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/lifecycle-events",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    if response.status_code == 200:
        response_200 = response.text
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Lifecycle event stream (SSE)

     `200 text/event-stream` carrying typed lifecycle events with the acting `Actor` attached — creation,
    state transitions, resizes, deletions.

    Scoped to what the caller may see: administrators receive the whole fleet, everyone else receives
    only events for VMs they owned at subscription time. The owned set is snapshotted when the stream
    opens, so a VM created after that does not appear on an already-open stream; reconnect to pick it
    up.

    Distinct from `GET /api/vms/events`, which carries raw state-machine transitions rather than typed
    lifecycle events.

    Served on every listener, including the external API listener (needs `vms:read`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Lifecycle event stream (SSE)

     `200 text/event-stream` carrying typed lifecycle events with the acting `Actor` attached — creation,
    state transitions, resizes, deletions.

    Scoped to what the caller may see: administrators receive the whole fleet, everyone else receives
    only events for VMs they owned at subscription time. The owned set is snapshotted when the stream
    opens, so a VM created after that does not appear on an already-open stream; reconnect to pick it
    up.

    Distinct from `GET /api/vms/events`, which carries raw state-machine transitions rather than typed
    lifecycle events.

    Served on every listener, including the external API listener (needs `vms:read`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Lifecycle event stream (SSE)

     `200 text/event-stream` carrying typed lifecycle events with the acting `Actor` attached — creation,
    state transitions, resizes, deletions.

    Scoped to what the caller may see: administrators receive the whole fleet, everyone else receives
    only events for VMs they owned at subscription time. The owned set is snapshotted when the stream
    opens, so a VM created after that does not appear on an already-open stream; reconnect to pick it
    up.

    Distinct from `GET /api/vms/events`, which carries raw state-machine transitions rather than typed
    lifecycle events.

    Served on every listener, including the external API listener (needs `vms:read`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Lifecycle event stream (SSE)

     `200 text/event-stream` carrying typed lifecycle events with the acting `Actor` attached — creation,
    state transitions, resizes, deletions.

    Scoped to what the caller may see: administrators receive the whole fleet, everyone else receives
    only events for VMs they owned at subscription time. The owned set is snapshotted when the stream
    opens, so a VM created after that does not appear on an already-open stream; reconnect to pick it
    up.

    Distinct from `GET /api/vms/events`, which carries raw state-machine transitions rather than typed
    lifecycle events.

    Served on every listener, including the external API listener (needs `vms:read`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
