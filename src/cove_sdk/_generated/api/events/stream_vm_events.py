from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/events".format(
            name=quote(str(name), safe=""),
        ),
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

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`: a later VM that reuses the name is a different VM,
    and needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`.
    - `error`: creation failed, data `{"stage": "Failed", "message": "<error>"}`.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. Reconnect to resync — the dropped events are not replayed.

    Distinct from `GET /api/lifecycle-events`, which carries typed, actor- attributed lifecycle events
    across every VM rather than raw state-machine transitions for one.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce.

    Served on every listener, including the external API listener (needs `vms:read`).

    Open to anyone who can view the VM (its owner, a share, a team grant, an administrator (a session,
    or an admin key)); anyone else gets the same 404 as for a VM that does not exist.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`: a later VM that reuses the name is a different VM,
    and needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`.
    - `error`: creation failed, data `{"stage": "Failed", "message": "<error>"}`.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. Reconnect to resync — the dropped events are not replayed.

    Distinct from `GET /api/lifecycle-events`, which carries typed, actor- attributed lifecycle events
    across every VM rather than raw state-machine transitions for one.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce.

    Served on every listener, including the external API listener (needs `vms:read`).

    Open to anyone who can view the VM (its owner, a share, a team grant, an administrator (a session,
    or an admin key)); anyone else gets the same 404 as for a VM that does not exist.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`: a later VM that reuses the name is a different VM,
    and needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`.
    - `error`: creation failed, data `{"stage": "Failed", "message": "<error>"}`.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. Reconnect to resync — the dropped events are not replayed.

    Distinct from `GET /api/lifecycle-events`, which carries typed, actor- attributed lifecycle events
    across every VM rather than raw state-machine transitions for one.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce.

    Served on every listener, including the external API listener (needs `vms:read`).

    Open to anyone who can view the VM (its owner, a share, a team grant, an administrator (a session,
    or an admin key)); anyone else gets the same 404 as for a VM that does not exist.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`: a later VM that reuses the name is a different VM,
    and needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`.
    - `error`: creation failed, data `{"stage": "Failed", "message": "<error>"}`.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. Reconnect to resync — the dropped events are not replayed.

    Distinct from `GET /api/lifecycle-events`, which carries typed, actor- attributed lifecycle events
    across every VM rather than raw state-machine transitions for one.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce.

    Served on every listener, including the external API listener (needs `vms:read`).

    Open to anyone who can view the VM (its owner, a share, a team grant, an administrator (a session,
    or an admin key)); anyone else gets the same 404 as for a VM that does not exist.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
