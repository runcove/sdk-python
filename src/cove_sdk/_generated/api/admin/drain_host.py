from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_drain_response import AdminDrainResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.sudo_required_body import SudoRequiredBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    budget_secs: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["budget_secs"] = budget_secs

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/drain",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminDrainResponse | ApiError | SudoRequiredBody | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminDrainResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:

        def _parse_response_401(data: object) -> ApiError | SudoRequiredBody:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_sensitive_op_unauthorized_response_type_0 = (
                    ApiError.from_dict(data)
                )

                return componentsschemas_sensitive_op_unauthorized_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_sensitive_op_unauthorized_response_type_1 = (
                SudoRequiredBody.from_dict(data)
            )

            return componentsschemas_sensitive_op_unauthorized_response_type_1

        response_401 = _parse_response_401(response.json())

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
) -> Response[AdminDrainResponse | ApiError | SudoRequiredBody | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    budget_secs: int | Unset = UNSET,
) -> Response[AdminDrainResponse | ApiError | SudoRequiredBody | CliTooOldBody]:
    """Stop every VM on the host

     **Blast radius: the entire host, unconditionally.** There is no scope parameter and no dry run. One
    call stops every running and paused VM belonging to every tenant. Disks survive — this is a
    shutdown, not a delete — but every user of the host loses their running machine at once. It exists
    so a host can be powered down or patched without hard-killing anyone's work; the unassigned VMs Cove
    keeps ready so that creation is fast are left alone.

    It is served on the local daemon socket and on the bearer-key listener, which answers every key 401
    `sudo_required`, so in practice a drain runs on the Unix socket. It is never served on the bastion-
    fronted listener, so the web interface and a bastion-proxied CLI cannot reach it.

    Who may call it: a configured administrator on any listener it is served on, **or** an
    unauthenticated caller on the local daemon socket. That second case is deliberate — a freshly
    installed host with no administrators configured must still be able to shut its VMs down — and it
    cannot be reached over the bearer listener, which labels a credential-less caller differently. An
    authenticated non-administrator is refused everywhere, and a team key can never be an administrator.

    Like `bulkStopVms` and `bulkDeleteVms`, a drain needs a recent interactive login: on the Unix socket
    a caller that names a user is checked against its latest CLI ticket, and a stale one is answered 401
    `sudo_required`. The unauthenticated local caller above is not challenged. An API key cannot show a
    recent login, so every key — an admin key and a team key included — is answered 401 `sudo_required`,
    the same body.

    It always answers, and never hangs. The whole fan-out runs under one deadline (`budget_secs`,
    otherwise the host's configured drain budget, default 45 seconds); each individual stop has its own
    shorter timeout. When the deadline passes with stops still running, the response still comes back
    with `timed_out` counting them — those VMs are **absent from `targets`** and keep stopping in the
    background. So a 200 does not by itself mean the fleet is down: check `timed_out == 0`.

    Ctrl-C or a client disconnect does not cancel a drain: it runs to completion and is audited.

    Args:
        budget_secs (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminDrainResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        budget_secs=budget_secs,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    budget_secs: int | Unset = UNSET,
) -> AdminDrainResponse | ApiError | SudoRequiredBody | CliTooOldBody | None:
    """Stop every VM on the host

     **Blast radius: the entire host, unconditionally.** There is no scope parameter and no dry run. One
    call stops every running and paused VM belonging to every tenant. Disks survive — this is a
    shutdown, not a delete — but every user of the host loses their running machine at once. It exists
    so a host can be powered down or patched without hard-killing anyone's work; the unassigned VMs Cove
    keeps ready so that creation is fast are left alone.

    It is served on the local daemon socket and on the bearer-key listener, which answers every key 401
    `sudo_required`, so in practice a drain runs on the Unix socket. It is never served on the bastion-
    fronted listener, so the web interface and a bastion-proxied CLI cannot reach it.

    Who may call it: a configured administrator on any listener it is served on, **or** an
    unauthenticated caller on the local daemon socket. That second case is deliberate — a freshly
    installed host with no administrators configured must still be able to shut its VMs down — and it
    cannot be reached over the bearer listener, which labels a credential-less caller differently. An
    authenticated non-administrator is refused everywhere, and a team key can never be an administrator.

    Like `bulkStopVms` and `bulkDeleteVms`, a drain needs a recent interactive login: on the Unix socket
    a caller that names a user is checked against its latest CLI ticket, and a stale one is answered 401
    `sudo_required`. The unauthenticated local caller above is not challenged. An API key cannot show a
    recent login, so every key — an admin key and a team key included — is answered 401 `sudo_required`,
    the same body.

    It always answers, and never hangs. The whole fan-out runs under one deadline (`budget_secs`,
    otherwise the host's configured drain budget, default 45 seconds); each individual stop has its own
    shorter timeout. When the deadline passes with stops still running, the response still comes back
    with `timed_out` counting them — those VMs are **absent from `targets`** and keep stopping in the
    background. So a 200 does not by itself mean the fleet is down: check `timed_out == 0`.

    Ctrl-C or a client disconnect does not cancel a drain: it runs to completion and is audited.

    Args:
        budget_secs (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminDrainResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody
    """

    return sync_detailed(
        client=client,
        budget_secs=budget_secs,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    budget_secs: int | Unset = UNSET,
) -> Response[AdminDrainResponse | ApiError | SudoRequiredBody | CliTooOldBody]:
    """Stop every VM on the host

     **Blast radius: the entire host, unconditionally.** There is no scope parameter and no dry run. One
    call stops every running and paused VM belonging to every tenant. Disks survive — this is a
    shutdown, not a delete — but every user of the host loses their running machine at once. It exists
    so a host can be powered down or patched without hard-killing anyone's work; the unassigned VMs Cove
    keeps ready so that creation is fast are left alone.

    It is served on the local daemon socket and on the bearer-key listener, which answers every key 401
    `sudo_required`, so in practice a drain runs on the Unix socket. It is never served on the bastion-
    fronted listener, so the web interface and a bastion-proxied CLI cannot reach it.

    Who may call it: a configured administrator on any listener it is served on, **or** an
    unauthenticated caller on the local daemon socket. That second case is deliberate — a freshly
    installed host with no administrators configured must still be able to shut its VMs down — and it
    cannot be reached over the bearer listener, which labels a credential-less caller differently. An
    authenticated non-administrator is refused everywhere, and a team key can never be an administrator.

    Like `bulkStopVms` and `bulkDeleteVms`, a drain needs a recent interactive login: on the Unix socket
    a caller that names a user is checked against its latest CLI ticket, and a stale one is answered 401
    `sudo_required`. The unauthenticated local caller above is not challenged. An API key cannot show a
    recent login, so every key — an admin key and a team key included — is answered 401 `sudo_required`,
    the same body.

    It always answers, and never hangs. The whole fan-out runs under one deadline (`budget_secs`,
    otherwise the host's configured drain budget, default 45 seconds); each individual stop has its own
    shorter timeout. When the deadline passes with stops still running, the response still comes back
    with `timed_out` counting them — those VMs are **absent from `targets`** and keep stopping in the
    background. So a 200 does not by itself mean the fleet is down: check `timed_out == 0`.

    Ctrl-C or a client disconnect does not cancel a drain: it runs to completion and is audited.

    Args:
        budget_secs (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminDrainResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        budget_secs=budget_secs,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    budget_secs: int | Unset = UNSET,
) -> AdminDrainResponse | ApiError | SudoRequiredBody | CliTooOldBody | None:
    """Stop every VM on the host

     **Blast radius: the entire host, unconditionally.** There is no scope parameter and no dry run. One
    call stops every running and paused VM belonging to every tenant. Disks survive — this is a
    shutdown, not a delete — but every user of the host loses their running machine at once. It exists
    so a host can be powered down or patched without hard-killing anyone's work; the unassigned VMs Cove
    keeps ready so that creation is fast are left alone.

    It is served on the local daemon socket and on the bearer-key listener, which answers every key 401
    `sudo_required`, so in practice a drain runs on the Unix socket. It is never served on the bastion-
    fronted listener, so the web interface and a bastion-proxied CLI cannot reach it.

    Who may call it: a configured administrator on any listener it is served on, **or** an
    unauthenticated caller on the local daemon socket. That second case is deliberate — a freshly
    installed host with no administrators configured must still be able to shut its VMs down — and it
    cannot be reached over the bearer listener, which labels a credential-less caller differently. An
    authenticated non-administrator is refused everywhere, and a team key can never be an administrator.

    Like `bulkStopVms` and `bulkDeleteVms`, a drain needs a recent interactive login: on the Unix socket
    a caller that names a user is checked against its latest CLI ticket, and a stale one is answered 401
    `sudo_required`. The unauthenticated local caller above is not challenged. An API key cannot show a
    recent login, so every key — an admin key and a team key included — is answered 401 `sudo_required`,
    the same body.

    It always answers, and never hangs. The whole fan-out runs under one deadline (`budget_secs`,
    otherwise the host's configured drain budget, default 45 seconds); each individual stop has its own
    shorter timeout. When the deadline passes with stops still running, the response still comes back
    with `timed_out` counting them — those VMs are **absent from `targets`** and keep stopping in the
    background. So a 200 does not by itself mean the fleet is down: check `timed_out == 0`.

    Ctrl-C or a client disconnect does not cancel a drain: it runs to completion and is audited.

    Args:
        budget_secs (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminDrainResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
            budget_secs=budget_secs,
        )
    ).parsed
