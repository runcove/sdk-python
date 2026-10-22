from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.restore_vms_request import RestoreVmsRequest
from ...models.restore_vms_response import RestoreVmsResponse
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    *,
    body: RestoreVmsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/restore-vms",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse | None:
    if response.status_code == 200:
        response_200 = RestoreVmsResponse.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RestoreVmsRequest,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse]:
    """Start the VMs a host drain stopped

     Cold-starts each named VM that is stopped, a few at a time, and answers with one result per VM. It
    is the second half of a host reboot: `drainHost` reports the VMs it set out to stop
    (`attempted_vms`), and this starts them again once the host is back. It is a normal start, not a
    restore from a checkpoint.

    The server also starts the VMs that were running when the host went down by itself, once it is ready
    after a boot, so nothing has to call this after a reboot. It stays for starting a named set of
    stopped VMs by hand.

    It starts any stopped VM it is given, not only ones a drain stopped. Nothing here is an error. A VM
    that no longer exists is `not_found`; one that is already running or paused is `skipped_running`; a
    warm-pool VM is `skipped_pool`; one whose owner was offboarded and disabled is
    `skipped_owner_disabled`, whoever calls (bring one back with an ordinary start); one in any other
    state is `skipped_state`. A VM still stopping, as happens when the host went down mid-stop, is
    waited for up to 150 seconds and then reported `skipped_stopping`, so the caller can try it again.
    Only a start that was attempted and refused reports `failed`.

    Who may call it: the same callers as `drainHost` — a configured administrator on any listener it is
    served on, **or** an unauthenticated caller on the local daemon socket, so a freshly installed host
    with no administrators configured can still bring its VMs back. Like `drainHost`, a caller that
    names a user on the Unix socket needs a recent interactive login (a stale one is answered 401
    `sudo_required`; the unauthenticated local caller is not challenged), and every API key, an admin
    key included, is answered 401 `sudo_required`. It is not served on the bastion-fronted listener.

    The call runs to completion and is audited even if the caller disconnects.

    Args:
        body (RestoreVmsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse]
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
    body: RestoreVmsRequest,
) -> ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse | None:
    """Start the VMs a host drain stopped

     Cold-starts each named VM that is stopped, a few at a time, and answers with one result per VM. It
    is the second half of a host reboot: `drainHost` reports the VMs it set out to stop
    (`attempted_vms`), and this starts them again once the host is back. It is a normal start, not a
    restore from a checkpoint.

    The server also starts the VMs that were running when the host went down by itself, once it is ready
    after a boot, so nothing has to call this after a reboot. It stays for starting a named set of
    stopped VMs by hand.

    It starts any stopped VM it is given, not only ones a drain stopped. Nothing here is an error. A VM
    that no longer exists is `not_found`; one that is already running or paused is `skipped_running`; a
    warm-pool VM is `skipped_pool`; one whose owner was offboarded and disabled is
    `skipped_owner_disabled`, whoever calls (bring one back with an ordinary start); one in any other
    state is `skipped_state`. A VM still stopping, as happens when the host went down mid-stop, is
    waited for up to 150 seconds and then reported `skipped_stopping`, so the caller can try it again.
    Only a start that was attempted and refused reports `failed`.

    Who may call it: the same callers as `drainHost` — a configured administrator on any listener it is
    served on, **or** an unauthenticated caller on the local daemon socket, so a freshly installed host
    with no administrators configured can still bring its VMs back. Like `drainHost`, a caller that
    names a user on the Unix socket needs a recent interactive login (a stale one is answered 401
    `sudo_required`; the unauthenticated local caller is not challenged), and every API key, an admin
    key included, is answered 401 `sudo_required`. It is not served on the bastion-fronted listener.

    The call runs to completion and is audited even if the caller disconnects.

    Args:
        body (RestoreVmsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RestoreVmsRequest,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse]:
    """Start the VMs a host drain stopped

     Cold-starts each named VM that is stopped, a few at a time, and answers with one result per VM. It
    is the second half of a host reboot: `drainHost` reports the VMs it set out to stop
    (`attempted_vms`), and this starts them again once the host is back. It is a normal start, not a
    restore from a checkpoint.

    The server also starts the VMs that were running when the host went down by itself, once it is ready
    after a boot, so nothing has to call this after a reboot. It stays for starting a named set of
    stopped VMs by hand.

    It starts any stopped VM it is given, not only ones a drain stopped. Nothing here is an error. A VM
    that no longer exists is `not_found`; one that is already running or paused is `skipped_running`; a
    warm-pool VM is `skipped_pool`; one whose owner was offboarded and disabled is
    `skipped_owner_disabled`, whoever calls (bring one back with an ordinary start); one in any other
    state is `skipped_state`. A VM still stopping, as happens when the host went down mid-stop, is
    waited for up to 150 seconds and then reported `skipped_stopping`, so the caller can try it again.
    Only a start that was attempted and refused reports `failed`.

    Who may call it: the same callers as `drainHost` — a configured administrator on any listener it is
    served on, **or** an unauthenticated caller on the local daemon socket, so a freshly installed host
    with no administrators configured can still bring its VMs back. Like `drainHost`, a caller that
    names a user on the Unix socket needs a recent interactive login (a stale one is answered 401
    `sudo_required`; the unauthenticated local caller is not challenged), and every API key, an admin
    key included, is answered 401 `sudo_required`. It is not served on the bastion-fronted listener.

    The call runs to completion and is audited even if the caller disconnects.

    Args:
        body (RestoreVmsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RestoreVmsRequest,
) -> ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse | None:
    """Start the VMs a host drain stopped

     Cold-starts each named VM that is stopped, a few at a time, and answers with one result per VM. It
    is the second half of a host reboot: `drainHost` reports the VMs it set out to stop
    (`attempted_vms`), and this starts them again once the host is back. It is a normal start, not a
    restore from a checkpoint.

    The server also starts the VMs that were running when the host went down by itself, once it is ready
    after a boot, so nothing has to call this after a reboot. It stays for starting a named set of
    stopped VMs by hand.

    It starts any stopped VM it is given, not only ones a drain stopped. Nothing here is an error. A VM
    that no longer exists is `not_found`; one that is already running or paused is `skipped_running`; a
    warm-pool VM is `skipped_pool`; one whose owner was offboarded and disabled is
    `skipped_owner_disabled`, whoever calls (bring one back with an ordinary start); one in any other
    state is `skipped_state`. A VM still stopping, as happens when the host went down mid-stop, is
    waited for up to 150 seconds and then reported `skipped_stopping`, so the caller can try it again.
    Only a start that was attempted and refused reports `failed`.

    Who may call it: the same callers as `drainHost` — a configured administrator on any listener it is
    served on, **or** an unauthenticated caller on the local daemon socket, so a freshly installed host
    with no administrators configured can still bring its VMs back. Like `drainHost`, a caller that
    names a user on the Unix socket needs a recent interactive login (a stale one is answered 401
    `sudo_required`; the unauthenticated local caller is not challenged), and every API key, an admin
    key included, is answered 401 `sudo_required`. It is not served on the bastion-fronted listener.

    The call runs to completion and is audited even if the caller disconnects.

    Args:
        body (RestoreVmsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RestoreVmsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
