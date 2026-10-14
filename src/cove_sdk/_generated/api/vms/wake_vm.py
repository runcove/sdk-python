from http import HTTPStatus
from typing import Any, cast
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
) -> (
    Any
    | ApiError
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
    | ScopeDeniedBody
    | None
):
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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | ApiError
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
    | ScopeDeniedBody
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
    body: WakeRequest,
) -> Response[
    Any
    | ApiError
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
    | ScopeDeniedBody
]:
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

    A VM whose owner is disabled (offboarded) is woken only by an administrator; anyone else gets 403
    `user_disabled` with no `detail`, and nothing changes.

    Waking a `Stopped` VM from a named disk-only checkpoint is the in-place disk rollback: there is no
    separate rollback call. Naming an older checkpoint on a `Hibernated` VM rolls back its disk and
    memory too, and either way the current disk is discarded, not kept. The name `restore` is reserved
    for a future dedicated operation, so this one is `wakeVm`. `POST /api/vms/{name}/restore` has been
    removed, not aliased — it answers 404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ScopeDeniedBody]
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
) -> (
    Any
    | ApiError
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
    | ScopeDeniedBody
    | None
):
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

    A VM whose owner is disabled (offboarded) is woken only by an administrator; anyone else gets 403
    `user_disabled` with no `detail`, and nothing changes.

    Waking a `Stopped` VM from a named disk-only checkpoint is the in-place disk rollback: there is no
    separate rollback call. Naming an older checkpoint on a `Hibernated` VM rolls back its disk and
    memory too, and either way the current disk is discarded, not kept. The name `restore` is reserved
    for a future dedicated operation, so this one is `wakeVm`. `POST /api/vms/{name}/restore` has been
    removed, not aliased — it answers 404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ScopeDeniedBody
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
) -> Response[
    Any
    | ApiError
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
    | ScopeDeniedBody
]:
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

    A VM whose owner is disabled (offboarded) is woken only by an administrator; anyone else gets 403
    `user_disabled` with no `detail`, and nothing changes.

    Waking a `Stopped` VM from a named disk-only checkpoint is the in-place disk rollback: there is no
    separate rollback call. Naming an older checkpoint on a `Hibernated` VM rolls back its disk and
    memory too, and either way the current disk is discarded, not kept. The name `restore` is reserved
    for a future dedicated operation, so this one is `wakeVm`. `POST /api/vms/{name}/restore` has been
    removed, not aliased — it answers 404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ScopeDeniedBody]
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
) -> (
    Any
    | ApiError
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
    | ScopeDeniedBody
    | None
):
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

    A VM whose owner is disabled (offboarded) is woken only by an administrator; anyone else gets 403
    `user_disabled` with no `detail`, and nothing changes.

    Waking a `Stopped` VM from a named disk-only checkpoint is the in-place disk rollback: there is no
    separate rollback call. Naming an older checkpoint on a `Hibernated` VM rolls back its disk and
    memory too, and either way the current disk is discarded, not kept. The name `restore` is reserved
    for a future dedicated operation, so this one is `wakeVm`. `POST /api/vms/{name}/restore` has been
    removed, not aliased — it answers 404. Call `POST /api/vms/{name}/wake` instead.

    Args:
        name (str):
        body (WakeRequest): POST /vms/{name}/wake request body. `checkpoint_id` is optional —
            `None` selects the latest available checkpoint for the VM (server
            chooses), `Some` pins a specific checkpoint UUID v7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
