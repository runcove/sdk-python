from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.wake_request import WakeRequest
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: WakeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/wake".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

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
        response_409 = ApiError.from_dict(response.json())

        return response_409

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
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
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
    body: WakeRequest,
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Wake a VM from a checkpoint

     Brings a VM back from a checkpoint. A `Hibernated` VM wakes from a checkpoint with memory: its Cloud
    Hypervisor process is re-spawned from the checkpoint's disk + memory state, with every process where
    it was. A `Stopped` VM wakes from a disk-only checkpoint: its disk is replaced by the checkpoint's,
    losing every write made since, and it boots.

    Omit `checkpoint_id` to wake using the latest checkpoint available for the VM. The one exception is
    a `Stopped` VM whose latest checkpoint is disk-only: that wake would roll the disk back without the
    checkpoint being named, so it is refused with 409 `disk_rollback_not_named` and nothing changes.
    Start the VM (`POST /api/vms/{name}/start`) to boot from its current disk, or wake it again with
    that `checkpoint_id` to roll back on purpose.

    Named `wakeVm` — the public surface reserves `restore` for a future checkpoint-rollback operation
    that does not exist yet. `POST /api/vms/{name}/restore` has been removed, not aliased — it answers
    404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: WakeRequest,
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Wake a VM from a checkpoint

     Brings a VM back from a checkpoint. A `Hibernated` VM wakes from a checkpoint with memory: its Cloud
    Hypervisor process is re-spawned from the checkpoint's disk + memory state, with every process where
    it was. A `Stopped` VM wakes from a disk-only checkpoint: its disk is replaced by the checkpoint's,
    losing every write made since, and it boots.

    Omit `checkpoint_id` to wake using the latest checkpoint available for the VM. The one exception is
    a `Stopped` VM whose latest checkpoint is disk-only: that wake would roll the disk back without the
    checkpoint being named, so it is refused with 409 `disk_rollback_not_named` and nothing changes.
    Start the VM (`POST /api/vms/{name}/start`) to boot from its current disk, or wake it again with
    that `checkpoint_id` to roll back on purpose.

    Named `wakeVm` — the public surface reserves `restore` for a future checkpoint-rollback operation
    that does not exist yet. `POST /api/vms/{name}/restore` has been removed, not aliased — it answers
    404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: WakeRequest,
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Wake a VM from a checkpoint

     Brings a VM back from a checkpoint. A `Hibernated` VM wakes from a checkpoint with memory: its Cloud
    Hypervisor process is re-spawned from the checkpoint's disk + memory state, with every process where
    it was. A `Stopped` VM wakes from a disk-only checkpoint: its disk is replaced by the checkpoint's,
    losing every write made since, and it boots.

    Omit `checkpoint_id` to wake using the latest checkpoint available for the VM. The one exception is
    a `Stopped` VM whose latest checkpoint is disk-only: that wake would roll the disk back without the
    checkpoint being named, so it is refused with 409 `disk_rollback_not_named` and nothing changes.
    Start the VM (`POST /api/vms/{name}/start`) to boot from its current disk, or wake it again with
    that `checkpoint_id` to roll back on purpose.

    Named `wakeVm` — the public surface reserves `restore` for a future checkpoint-rollback operation
    that does not exist yet. `POST /api/vms/{name}/restore` has been removed, not aliased — it answers
    404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: WakeRequest,
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Wake a VM from a checkpoint

     Brings a VM back from a checkpoint. A `Hibernated` VM wakes from a checkpoint with memory: its Cloud
    Hypervisor process is re-spawned from the checkpoint's disk + memory state, with every process where
    it was. A `Stopped` VM wakes from a disk-only checkpoint: its disk is replaced by the checkpoint's,
    losing every write made since, and it boots.

    Omit `checkpoint_id` to wake using the latest checkpoint available for the VM. The one exception is
    a `Stopped` VM whose latest checkpoint is disk-only: that wake would roll the disk back without the
    checkpoint being named, so it is refused with 409 `disk_rollback_not_named` and nothing changes.
    Start the VM (`POST /api/vms/{name}/start`) to boot from its current disk, or wake it again with
    that `checkpoint_id` to roll back on purpose.

    Named `wakeVm` — the public surface reserves `restore` for a future checkpoint-rollback operation
    that does not exist yet. `POST /api/vms/{name}/restore` has been removed, not aliased — it answers
    404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
