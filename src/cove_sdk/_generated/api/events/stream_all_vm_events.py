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
        "url": "/api/vms/events",
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
    """Stream state-change events for every VM the caller owns (SSE)

     `200 text/event-stream`. One connection covers every VM the caller owns, including one that becomes
    theirs while the stream is open — a create, a warm-pool claim or a clone — from that VM's first
    event on.

    SSE event types:
    - `connected`: first frame, data `{"vm_count": <int>}` — the caller's VM count at subscription time.
    - `vm-update`: any state change, data `{"vm_name", "state", "event_type"}`. It is also sent for an
    advisory about a VM whose state did not change (a health degrade or recovery, creation progress,
    pause, clone and pool-claim details), so a frame can repeat the state the previous one for that VM
    carried: treat `state` as idempotent and act on a change, not on a frame.
    - `vm-created`: a new VM of the caller's is up, sent once per VM — whether it was built for the
    request, claimed from the warm pool or cloned. Its `state` is normally `running`; frames about the
    VM before it (a `creating` `vm-update` while it is built) can precede it.
    - `vm-deleted`: a VM reached the deleted state.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. The dropped events are not replayed — reconnect or re-list to resync.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce — so a quiet stream should not
    be cut by a middlebox before the 5-minute cap.

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
    """Stream state-change events for every VM the caller owns (SSE)

     `200 text/event-stream`. One connection covers every VM the caller owns, including one that becomes
    theirs while the stream is open — a create, a warm-pool claim or a clone — from that VM's first
    event on.

    SSE event types:
    - `connected`: first frame, data `{"vm_count": <int>}` — the caller's VM count at subscription time.
    - `vm-update`: any state change, data `{"vm_name", "state", "event_type"}`. It is also sent for an
    advisory about a VM whose state did not change (a health degrade or recovery, creation progress,
    pause, clone and pool-claim details), so a frame can repeat the state the previous one for that VM
    carried: treat `state` as idempotent and act on a change, not on a frame.
    - `vm-created`: a new VM of the caller's is up, sent once per VM — whether it was built for the
    request, claimed from the warm pool or cloned. Its `state` is normally `running`; frames about the
    VM before it (a `creating` `vm-update` while it is built) can precede it.
    - `vm-deleted`: a VM reached the deleted state.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. The dropped events are not replayed — reconnect or re-list to resync.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce — so a quiet stream should not
    be cut by a middlebox before the 5-minute cap.

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
    """Stream state-change events for every VM the caller owns (SSE)

     `200 text/event-stream`. One connection covers every VM the caller owns, including one that becomes
    theirs while the stream is open — a create, a warm-pool claim or a clone — from that VM's first
    event on.

    SSE event types:
    - `connected`: first frame, data `{"vm_count": <int>}` — the caller's VM count at subscription time.
    - `vm-update`: any state change, data `{"vm_name", "state", "event_type"}`. It is also sent for an
    advisory about a VM whose state did not change (a health degrade or recovery, creation progress,
    pause, clone and pool-claim details), so a frame can repeat the state the previous one for that VM
    carried: treat `state` as idempotent and act on a change, not on a frame.
    - `vm-created`: a new VM of the caller's is up, sent once per VM — whether it was built for the
    request, claimed from the warm pool or cloned. Its `state` is normally `running`; frames about the
    VM before it (a `creating` `vm-update` while it is built) can precede it.
    - `vm-deleted`: a VM reached the deleted state.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. The dropped events are not replayed — reconnect or re-list to resync.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce — so a quiet stream should not
    be cut by a middlebox before the 5-minute cap.

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
    """Stream state-change events for every VM the caller owns (SSE)

     `200 text/event-stream`. One connection covers every VM the caller owns, including one that becomes
    theirs while the stream is open — a create, a warm-pool claim or a clone — from that VM's first
    event on.

    SSE event types:
    - `connected`: first frame, data `{"vm_count": <int>}` — the caller's VM count at subscription time.
    - `vm-update`: any state change, data `{"vm_name", "state", "event_type"}`. It is also sent for an
    advisory about a VM whose state did not change (a health degrade or recovery, creation progress,
    pause, clone and pool-claim details), so a frame can repeat the state the previous one for that VM
    carried: treat `state` as idempotent and act on a change, not on a frame.
    - `vm-created`: a new VM of the caller's is up, sent once per VM — whether it was built for the
    request, claimed from the warm pool or cloned. Its `state` is normally `running`; frames about the
    VM before it (a `creating` `vm-update` while it is built) can precede it.
    - `vm-deleted`: a VM reached the deleted state.
    - `lagged`: the server's broadcast channel dropped events because this connection fell behind, data
    `{"skipped": <int>}`. The dropped events are not replayed — reconnect or re-list to resync.

    Maximum stream duration is 5 minutes, after which the connection closes and the caller must
    reconnect. Sends an SSE keep-alive comment every 15 seconds — comfortably under the ~30 second idle-
    connection cutoff some network paths in front of this daemon enforce — so a quiet stream should not
    be cut by a middlebox before the 5-minute cap.

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
