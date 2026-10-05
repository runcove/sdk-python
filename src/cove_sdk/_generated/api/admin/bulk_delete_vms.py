from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_bulk_vm_request import AdminBulkVmRequest
from ...models.admin_bulk_vm_response import AdminBulkVmResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    *,
    body: AdminBulkVmRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/vms/delete-bulk",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminBulkVmResponse | ApiError | SudoRequiredBody | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminBulkVmResponse.from_dict(response.json())

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

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

        return response_422

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AdminBulkVmResponse | ApiError | SudoRequiredBody | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AdminBulkVmRequest,
) -> Response[AdminBulkVmResponse | ApiError | SudoRequiredBody | CliTooOldBody]:
    """Delete many VMs in one call

     **Irreversible, and the blast radius depends entirely on `scope`.** `{"type": "all"}` deletes every
    VM on the host, across every tenant, and their disks with them. `{"type": "user", "username": "…"}`
    deletes one person's VMs. `{"type": "vms", "vm_names": ["…"]}` deletes a hand-picked set; names that
    do not exist are silently dropped rather than rejected.

    Unlike `bulkStopVms`, this destroys data: each VM's disk goes with it, along with its access grants,
    bastion registration and DNS record. **Send `dry_run: true` first** — it reports the full target set
    with each entry marked as skipped, so you see the reach before anything is destroyed.

    Every VM in scope is attempted regardless of state, so `attempted` is the whole target set. A per-VM
    failure does not fail the call: `succeeded` / `failed` and each entry's own error tell you what
    happened, and a partial failure leaves the rest deleted. `include_pool` additionally reaches the
    unassigned VMs Cove keeps ready so that creation is fast (administrator concept; those have no
    owner). It is only valid with `{"type": "all"}` — combining it with a user scope is rejected 422.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        body (AdminBulkVmRequest): `POST /admin/vms/stop-bulk` / `POST /admin/vms/delete-bulk`
            request body.

            `scope` selects the target set. `dry_run` lists targets without acting.
            `include_pool` is only meaningful with `AdminBulkScope::All` — pool VMs
            have no owner so `User` never touches them (the server rejects the combo).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminBulkVmResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AdminBulkVmRequest,
) -> AdminBulkVmResponse | ApiError | SudoRequiredBody | CliTooOldBody | None:
    """Delete many VMs in one call

     **Irreversible, and the blast radius depends entirely on `scope`.** `{"type": "all"}` deletes every
    VM on the host, across every tenant, and their disks with them. `{"type": "user", "username": "…"}`
    deletes one person's VMs. `{"type": "vms", "vm_names": ["…"]}` deletes a hand-picked set; names that
    do not exist are silently dropped rather than rejected.

    Unlike `bulkStopVms`, this destroys data: each VM's disk goes with it, along with its access grants,
    bastion registration and DNS record. **Send `dry_run: true` first** — it reports the full target set
    with each entry marked as skipped, so you see the reach before anything is destroyed.

    Every VM in scope is attempted regardless of state, so `attempted` is the whole target set. A per-VM
    failure does not fail the call: `succeeded` / `failed` and each entry's own error tell you what
    happened, and a partial failure leaves the rest deleted. `include_pool` additionally reaches the
    unassigned VMs Cove keeps ready so that creation is fast (administrator concept; those have no
    owner). It is only valid with `{"type": "all"}` — combining it with a user scope is rejected 422.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        body (AdminBulkVmRequest): `POST /admin/vms/stop-bulk` / `POST /admin/vms/delete-bulk`
            request body.

            `scope` selects the target set. `dry_run` lists targets without acting.
            `include_pool` is only meaningful with `AdminBulkScope::All` — pool VMs
            have no owner so `User` never touches them (the server rejects the combo).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminBulkVmResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AdminBulkVmRequest,
) -> Response[AdminBulkVmResponse | ApiError | SudoRequiredBody | CliTooOldBody]:
    """Delete many VMs in one call

     **Irreversible, and the blast radius depends entirely on `scope`.** `{"type": "all"}` deletes every
    VM on the host, across every tenant, and their disks with them. `{"type": "user", "username": "…"}`
    deletes one person's VMs. `{"type": "vms", "vm_names": ["…"]}` deletes a hand-picked set; names that
    do not exist are silently dropped rather than rejected.

    Unlike `bulkStopVms`, this destroys data: each VM's disk goes with it, along with its access grants,
    bastion registration and DNS record. **Send `dry_run: true` first** — it reports the full target set
    with each entry marked as skipped, so you see the reach before anything is destroyed.

    Every VM in scope is attempted regardless of state, so `attempted` is the whole target set. A per-VM
    failure does not fail the call: `succeeded` / `failed` and each entry's own error tell you what
    happened, and a partial failure leaves the rest deleted. `include_pool` additionally reaches the
    unassigned VMs Cove keeps ready so that creation is fast (administrator concept; those have no
    owner). It is only valid with `{"type": "all"}` — combining it with a user scope is rejected 422.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        body (AdminBulkVmRequest): `POST /admin/vms/stop-bulk` / `POST /admin/vms/delete-bulk`
            request body.

            `scope` selects the target set. `dry_run` lists targets without acting.
            `include_pool` is only meaningful with `AdminBulkScope::All` — pool VMs
            have no owner so `User` never touches them (the server rejects the combo).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminBulkVmResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AdminBulkVmRequest,
) -> AdminBulkVmResponse | ApiError | SudoRequiredBody | CliTooOldBody | None:
    """Delete many VMs in one call

     **Irreversible, and the blast radius depends entirely on `scope`.** `{"type": "all"}` deletes every
    VM on the host, across every tenant, and their disks with them. `{"type": "user", "username": "…"}`
    deletes one person's VMs. `{"type": "vms", "vm_names": ["…"]}` deletes a hand-picked set; names that
    do not exist are silently dropped rather than rejected.

    Unlike `bulkStopVms`, this destroys data: each VM's disk goes with it, along with its access grants,
    bastion registration and DNS record. **Send `dry_run: true` first** — it reports the full target set
    with each entry marked as skipped, so you see the reach before anything is destroyed.

    Every VM in scope is attempted regardless of state, so `attempted` is the whole target set. A per-VM
    failure does not fail the call: `succeeded` / `failed` and each entry's own error tell you what
    happened, and a partial failure leaves the rest deleted. `include_pool` additionally reaches the
    unassigned VMs Cove keeps ready so that creation is fast (administrator concept; those have no
    owner). It is only valid with `{"type": "all"}` — combining it with a user scope is rejected 422.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        body (AdminBulkVmRequest): `POST /admin/vms/stop-bulk` / `POST /admin/vms/delete-bulk`
            request body.

            `scope` selects the target set. `dry_run` lists targets without acting.
            `include_pool` is only meaningful with `AdminBulkScope::All` — pool VMs
            have no owner so `User` never touches them (the server rejects the combo).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminBulkVmResponse | ApiError | ApiError | SudoRequiredBody | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
