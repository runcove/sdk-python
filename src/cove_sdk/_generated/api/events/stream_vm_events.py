from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.deny_reason_type_0 import DenyReasonType0
from ...models.deny_reason_type_1 import DenyReasonType1
from ...models.deny_reason_type_2 import DenyReasonType2
from ...models.deny_reason_type_3 import DenyReasonType3
from ...models.deny_reason_type_4 import DenyReasonType4
from ...models.deny_reason_type_5 import DenyReasonType5
from ...models.deny_reason_type_6 import DenyReasonType6
from ...models.deny_reason_type_7 import DenyReasonType7
from ...models.deny_reason_type_8 import DenyReasonType8
from ...models.deny_reason_type_9 import DenyReasonType9
from ...models.deny_reason_type_10 import DenyReasonType10
from ...models.deny_reason_type_11 import DenyReasonType11
from ...models.deny_reason_type_12 import DenyReasonType12
from ...models.deny_reason_type_13 import DenyReasonType13
from ...models.deny_reason_type_14 import DenyReasonType14
from ...models.deny_reason_type_15 import DenyReasonType15
from ...models.deny_reason_type_16 import DenyReasonType16
from ...models.invalid_vm_name_body import InvalidVmNameBody
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
) -> (
    ApiError
    | DenyReasonType0
    | DenyReasonType1
    | DenyReasonType10
    | DenyReasonType11
    | DenyReasonType12
    | DenyReasonType13
    | DenyReasonType14
    | DenyReasonType15
    | DenyReasonType16
    | DenyReasonType2
    | DenyReasonType3
    | DenyReasonType4
    | DenyReasonType5
    | DenyReasonType6
    | DenyReasonType7
    | DenyReasonType8
    | DenyReasonType9
    | CliTooOldBody
    | InvalidVmNameBody
    | ScopeDeniedBody
    | str
    | None
):
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = InvalidVmNameBody.from_dict(response.json())

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

    if response.status_code == 409:

        def _parse_response_409(
            data: object,
        ) -> (
            ApiError
            | DenyReasonType0
            | DenyReasonType1
            | DenyReasonType10
            | DenyReasonType11
            | DenyReasonType12
            | DenyReasonType13
            | DenyReasonType14
            | DenyReasonType15
            | DenyReasonType16
            | DenyReasonType2
            | DenyReasonType3
            | DenyReasonType4
            | DenyReasonType5
            | DenyReasonType6
            | DenyReasonType7
            | DenyReasonType8
            | DenyReasonType9
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_vm_conflict_response_type_0 = ApiError.from_dict(data)

                return componentsschemas_vm_conflict_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_0 = DenyReasonType0.from_dict(data)

                return componentsschemas_deny_reason_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_1 = DenyReasonType1.from_dict(data)

                return componentsschemas_deny_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_2 = DenyReasonType2.from_dict(data)

                return componentsschemas_deny_reason_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_3 = DenyReasonType3.from_dict(data)

                return componentsschemas_deny_reason_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_4 = DenyReasonType4.from_dict(data)

                return componentsschemas_deny_reason_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_5 = DenyReasonType5.from_dict(data)

                return componentsschemas_deny_reason_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_6 = DenyReasonType6.from_dict(data)

                return componentsschemas_deny_reason_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_7 = DenyReasonType7.from_dict(data)

                return componentsschemas_deny_reason_type_7
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_8 = DenyReasonType8.from_dict(data)

                return componentsschemas_deny_reason_type_8
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_9 = DenyReasonType9.from_dict(data)

                return componentsschemas_deny_reason_type_9
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_10 = DenyReasonType10.from_dict(data)

                return componentsschemas_deny_reason_type_10
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_11 = DenyReasonType11.from_dict(data)

                return componentsschemas_deny_reason_type_11
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_12 = DenyReasonType12.from_dict(data)

                return componentsschemas_deny_reason_type_12
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_13 = DenyReasonType13.from_dict(data)

                return componentsschemas_deny_reason_type_13
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_14 = DenyReasonType14.from_dict(data)

                return componentsschemas_deny_reason_type_14
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deny_reason_type_15 = DenyReasonType15.from_dict(data)

                return componentsschemas_deny_reason_type_15
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_deny_reason_type_16 = DenyReasonType16.from_dict(data)

            return componentsschemas_deny_reason_type_16

        response_409 = _parse_response_409(response.json())

        return response_409

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ApiError.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiError
    | DenyReasonType0
    | DenyReasonType1
    | DenyReasonType10
    | DenyReasonType11
    | DenyReasonType12
    | DenyReasonType13
    | DenyReasonType14
    | DenyReasonType15
    | DenyReasonType16
    | DenyReasonType2
    | DenyReasonType3
    | DenyReasonType4
    | DenyReasonType5
    | DenyReasonType6
    | DenyReasonType7
    | DenyReasonType8
    | DenyReasonType9
    | CliTooOldBody
    | InvalidVmNameBody
    | ScopeDeniedBody
    | str
]:
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
) -> Response[
    ApiError
    | DenyReasonType0
    | DenyReasonType1
    | DenyReasonType10
    | DenyReasonType11
    | DenyReasonType12
    | DenyReasonType13
    | DenyReasonType14
    | DenyReasonType15
    | DenyReasonType16
    | DenyReasonType2
    | DenyReasonType3
    | DenyReasonType4
    | DenyReasonType5
    | DenyReasonType6
    | DenyReasonType7
    | DenyReasonType8
    | DenyReasonType9
    | CliTooOldBody
    | InvalidVmNameBody
    | ScopeDeniedBody
    | str
]:
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`, and with no further frame when the VM is renamed:
    the stream does not follow it to its new name, and a later VM that takes the name is a different VM,
    which needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`, plus `transfer` while a
    long stage runs (a Mac's first-run image download and unpack, sent about once a second): `{"done",
    "total", "bytes_per_sec", "secs_left", "stalled_secs"}`, bytes and seconds. `total`, `bytes_per_sec`
    and `secs_left` are absent until known. `stalled_secs` is present only while the download is
    stalled: how long it has had no data, once that is several seconds; the rate and time left are
    absent then.
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

    A create that `POST /api/vms` accepted and that then failed removes its VM. A stream still waiting
    for the create's VM ends with the failure as an `error`, also when the create was refused before
    core had a VM for it (an admission refusal). For 5 minutes after the failure, a new request for the
    name by the create's owner is answered the failure's own status and body in place of the 404, marked
    with the `x-cove-create-failed` header, as `GET /api/vms/{name}` answers it.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | str]
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
) -> (
    ApiError
    | DenyReasonType0
    | DenyReasonType1
    | DenyReasonType10
    | DenyReasonType11
    | DenyReasonType12
    | DenyReasonType13
    | DenyReasonType14
    | DenyReasonType15
    | DenyReasonType16
    | DenyReasonType2
    | DenyReasonType3
    | DenyReasonType4
    | DenyReasonType5
    | DenyReasonType6
    | DenyReasonType7
    | DenyReasonType8
    | DenyReasonType9
    | CliTooOldBody
    | InvalidVmNameBody
    | ScopeDeniedBody
    | str
    | None
):
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`, and with no further frame when the VM is renamed:
    the stream does not follow it to its new name, and a later VM that takes the name is a different VM,
    which needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`, plus `transfer` while a
    long stage runs (a Mac's first-run image download and unpack, sent about once a second): `{"done",
    "total", "bytes_per_sec", "secs_left", "stalled_secs"}`, bytes and seconds. `total`, `bytes_per_sec`
    and `secs_left` are absent until known. `stalled_secs` is present only while the download is
    stalled: how long it has had no data, once that is several seconds; the rate and time left are
    absent then.
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

    A create that `POST /api/vms` accepted and that then failed removes its VM. A stream still waiting
    for the create's VM ends with the failure as an `error`, also when the create was refused before
    core had a VM for it (an admission refusal). For 5 minutes after the failure, a new request for the
    name by the create's owner is answered the failure's own status and body in place of the 404, marked
    with the `x-cove-create-failed` header, as `GET /api/vms/{name}` answers it.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | str
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    ApiError
    | DenyReasonType0
    | DenyReasonType1
    | DenyReasonType10
    | DenyReasonType11
    | DenyReasonType12
    | DenyReasonType13
    | DenyReasonType14
    | DenyReasonType15
    | DenyReasonType16
    | DenyReasonType2
    | DenyReasonType3
    | DenyReasonType4
    | DenyReasonType5
    | DenyReasonType6
    | DenyReasonType7
    | DenyReasonType8
    | DenyReasonType9
    | CliTooOldBody
    | InvalidVmNameBody
    | ScopeDeniedBody
    | str
]:
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`, and with no further frame when the VM is renamed:
    the stream does not follow it to its new name, and a later VM that takes the name is a different VM,
    which needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`, plus `transfer` while a
    long stage runs (a Mac's first-run image download and unpack, sent about once a second): `{"done",
    "total", "bytes_per_sec", "secs_left", "stalled_secs"}`, bytes and seconds. `total`, `bytes_per_sec`
    and `secs_left` are absent until known. `stalled_secs` is present only while the download is
    stalled: how long it has had no data, once that is several seconds; the rate and time left are
    absent then.
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

    A create that `POST /api/vms` accepted and that then failed removes its VM. A stream still waiting
    for the create's VM ends with the failure as an `error`, also when the create was refused before
    core had a VM for it (an admission refusal). For 5 minutes after the failure, a new request for the
    name by the create's owner is answered the failure's own status and body in place of the 404, marked
    with the `x-cove-create-failed` header, as `GET /api/vms/{name}` answers it.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | str]
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
) -> (
    ApiError
    | DenyReasonType0
    | DenyReasonType1
    | DenyReasonType10
    | DenyReasonType11
    | DenyReasonType12
    | DenyReasonType13
    | DenyReasonType14
    | DenyReasonType15
    | DenyReasonType16
    | DenyReasonType2
    | DenyReasonType3
    | DenyReasonType4
    | DenyReasonType5
    | DenyReasonType6
    | DenyReasonType7
    | DenyReasonType8
    | DenyReasonType9
    | CliTooOldBody
    | InvalidVmNameBody
    | ScopeDeniedBody
    | str
    | None
):
    """Stream creation-progress and state events for one VM (SSE)

     `200 text/event-stream`, scoped to a single named VM — most useful while a VM is still being
    created, before it has a state a client could otherwise poll for.

    SSE event types:
    - `state`: current or new lifecycle state, data `{"state", "timestamp"}` — emitted immediately on
    connect with the VM's state at that moment (or `creating` if the row does not exist yet because
    creation is still in flight), then again on every subsequent transition. The stream ends right after
    the `deleted` state or a failed create's `error`, and with no further frame when the VM is renamed:
    the stream does not follow it to its new name, and a later VM that takes the name is a different VM,
    which needs a new request. A `state` frame is also sent for an advisory about the VM that leaves its
    state where it was (a health degrade or recovery, pause, clone and pool-claim details, the create-
    completed announcement; creation progress arrives as `progress`), so a frame can repeat the previous
    state: treat `state` as idempotent and act on a change, not on a frame.
    - `progress`: a creation stage was reached, data `{"stage", "message"}`, plus `transfer` while a
    long stage runs (a Mac's first-run image download and unpack, sent about once a second): `{"done",
    "total", "bytes_per_sec", "secs_left", "stalled_secs"}`, bytes and seconds. `total`, `bytes_per_sec`
    and `secs_left` are absent until known. `stalled_secs` is present only while the download is
    stalled: how long it has had no data, once that is several seconds; the rate and time left are
    absent then.
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

    A create that `POST /api/vms` accepted and that then failed removes its VM. A stream still waiting
    for the create's VM ends with the failure as an `error`, also when the create was refused before
    core had a VM for it (an admission refusal). For 5 minutes after the failure, a new request for the
    name by the create's owner is answered the failure's own status and body in place of the 404, marked
    with the `x-cove-create-failed` header, as `GET /api/vms/{name}` answers it.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | str
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
