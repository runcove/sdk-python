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
from ...models.resize_request import ResizeRequest
from ...models.resize_result import ResizeResult
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: ResizeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/resize".format(
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
    | ResizeResult
    | ScopeDeniedBody
    | None
):
    if response.status_code == 200:
        response_200 = ResizeResult.from_dict(response.json())

        return response_200

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

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

        return response_422

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
    | ResizeResult
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
    body: ResizeRequest,
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
    | ResizeResult
    | ScopeDeniedBody
]:
    """Resize CPU/memory (running) or grow disk (stopped)

     `disk_size_gb` is mutually exclusive with `cpus`/`memory_mb` (422) — disk resize is stopped-VM-only,
    CPU/RAM resize is running-VM-only. `memory_mb` must be a multiple of 2 (virtio-mem block size). A
    disk grow returns a synthetic `ResizeResult` (`actual_cpus`/`actual_memory_mb` zeroed, `reason`
    describing the grow) rather than the real converged CPU/memory values.

    `restart: true` lets the resize reboot the VM, and only when it must: a running VM cannot go below
    both the vCPUs it runs and the disk queues its boot set up, so Cove stops it gracefully (forced
    after the stop timeout), writes the new boot size and starts it cold. Any other change is resized
    live with no reboot, except on a Mac, which has no live resize: there `restart` reboots a running VM
    for any new vCPU count, leaves one asked for the vCPUs it has as it is, and memory never changes. A
    stopped VM takes the new size and stays stopped; any other state is refused (409). Growth the quota
    or host cannot take is refused before the stop. The result's `restart` says which (`restarted`,
    `not_needed`, `stopped`). Off a Mac, memory asked for in the same request is applied after the
    start, within the VM's range and no lower than its boot memory. If the start fails, the VM keeps the
    new size, is left as a failed start leaves it, and the 500 says it was resized but failed to start.
    If the VM starts but the grow after the start (above its boot vCPUs or memory) fails, the answer is
    still 200, with `restart: restarted`, `partial: true`, the size it runs now, and `reason` saying the
    grow after the start failed and why; off a Mac, send the resize again without `restart` to retry the
    grow. A Mac starts the VM at its new vCPU count and keeps its memory, so nothing grows after the
    start there; should the VM come up at another size, the answer is the same `partial: true`, as the
    live resize that would make it up is refused on a Mac. On a Mac, a reboot is refused with 503 when
    no network owner serves (409 while a VM runs on the other datapath), as a start is: before the stop,
    nothing changes; if the check fails again after the stop, the VM stays stopped at its new size and
    the error says so. A stopped VM, or a resize that needs no reboot, is not checked.

    A request with `restart` can take a stop plus a cold start to answer, longer than a proxy in front
    of Cove may keep the request open; the resize goes on whether or not anyone waits. After a timeout
    or a proxy's 502 to 504, read the VM (`GET /api/vms/{name}`) before sending it again. Without
    `restart` a resize never reboots.

    Args:
        name (str):
        body (ResizeRequest): POST /vms/{name}/resize request body. Either field may be `None` to
            keep
            the current dimension unchanged. `memory_mb` must be a multiple of 2 (the
            virtio-mem block size is 2 MiB). `disk_size_gb` triggers a stopped-VM disk
            grow; it is mutually exclusive with `cpus`/`memory_mb` at ALL
            call sites — the CLI and the server handler — enforced by
            [`ResizeRequest::validate_exclusivity`].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ResizeResult | ScopeDeniedBody]
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
    body: ResizeRequest,
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
    | ResizeResult
    | ScopeDeniedBody
    | None
):
    """Resize CPU/memory (running) or grow disk (stopped)

     `disk_size_gb` is mutually exclusive with `cpus`/`memory_mb` (422) — disk resize is stopped-VM-only,
    CPU/RAM resize is running-VM-only. `memory_mb` must be a multiple of 2 (virtio-mem block size). A
    disk grow returns a synthetic `ResizeResult` (`actual_cpus`/`actual_memory_mb` zeroed, `reason`
    describing the grow) rather than the real converged CPU/memory values.

    `restart: true` lets the resize reboot the VM, and only when it must: a running VM cannot go below
    both the vCPUs it runs and the disk queues its boot set up, so Cove stops it gracefully (forced
    after the stop timeout), writes the new boot size and starts it cold. Any other change is resized
    live with no reboot, except on a Mac, which has no live resize: there `restart` reboots a running VM
    for any new vCPU count, leaves one asked for the vCPUs it has as it is, and memory never changes. A
    stopped VM takes the new size and stays stopped; any other state is refused (409). Growth the quota
    or host cannot take is refused before the stop. The result's `restart` says which (`restarted`,
    `not_needed`, `stopped`). Off a Mac, memory asked for in the same request is applied after the
    start, within the VM's range and no lower than its boot memory. If the start fails, the VM keeps the
    new size, is left as a failed start leaves it, and the 500 says it was resized but failed to start.
    If the VM starts but the grow after the start (above its boot vCPUs or memory) fails, the answer is
    still 200, with `restart: restarted`, `partial: true`, the size it runs now, and `reason` saying the
    grow after the start failed and why; off a Mac, send the resize again without `restart` to retry the
    grow. A Mac starts the VM at its new vCPU count and keeps its memory, so nothing grows after the
    start there; should the VM come up at another size, the answer is the same `partial: true`, as the
    live resize that would make it up is refused on a Mac. On a Mac, a reboot is refused with 503 when
    no network owner serves (409 while a VM runs on the other datapath), as a start is: before the stop,
    nothing changes; if the check fails again after the stop, the VM stays stopped at its new size and
    the error says so. A stopped VM, or a resize that needs no reboot, is not checked.

    A request with `restart` can take a stop plus a cold start to answer, longer than a proxy in front
    of Cove may keep the request open; the resize goes on whether or not anyone waits. After a timeout
    or a proxy's 502 to 504, read the VM (`GET /api/vms/{name}`) before sending it again. Without
    `restart` a resize never reboots.

    Args:
        name (str):
        body (ResizeRequest): POST /vms/{name}/resize request body. Either field may be `None` to
            keep
            the current dimension unchanged. `memory_mb` must be a multiple of 2 (the
            virtio-mem block size is 2 MiB). `disk_size_gb` triggers a stopped-VM disk
            grow; it is mutually exclusive with `cpus`/`memory_mb` at ALL
            call sites — the CLI and the server handler — enforced by
            [`ResizeRequest::validate_exclusivity`].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ResizeResult | ScopeDeniedBody
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
    body: ResizeRequest,
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
    | ResizeResult
    | ScopeDeniedBody
]:
    """Resize CPU/memory (running) or grow disk (stopped)

     `disk_size_gb` is mutually exclusive with `cpus`/`memory_mb` (422) — disk resize is stopped-VM-only,
    CPU/RAM resize is running-VM-only. `memory_mb` must be a multiple of 2 (virtio-mem block size). A
    disk grow returns a synthetic `ResizeResult` (`actual_cpus`/`actual_memory_mb` zeroed, `reason`
    describing the grow) rather than the real converged CPU/memory values.

    `restart: true` lets the resize reboot the VM, and only when it must: a running VM cannot go below
    both the vCPUs it runs and the disk queues its boot set up, so Cove stops it gracefully (forced
    after the stop timeout), writes the new boot size and starts it cold. Any other change is resized
    live with no reboot, except on a Mac, which has no live resize: there `restart` reboots a running VM
    for any new vCPU count, leaves one asked for the vCPUs it has as it is, and memory never changes. A
    stopped VM takes the new size and stays stopped; any other state is refused (409). Growth the quota
    or host cannot take is refused before the stop. The result's `restart` says which (`restarted`,
    `not_needed`, `stopped`). Off a Mac, memory asked for in the same request is applied after the
    start, within the VM's range and no lower than its boot memory. If the start fails, the VM keeps the
    new size, is left as a failed start leaves it, and the 500 says it was resized but failed to start.
    If the VM starts but the grow after the start (above its boot vCPUs or memory) fails, the answer is
    still 200, with `restart: restarted`, `partial: true`, the size it runs now, and `reason` saying the
    grow after the start failed and why; off a Mac, send the resize again without `restart` to retry the
    grow. A Mac starts the VM at its new vCPU count and keeps its memory, so nothing grows after the
    start there; should the VM come up at another size, the answer is the same `partial: true`, as the
    live resize that would make it up is refused on a Mac. On a Mac, a reboot is refused with 503 when
    no network owner serves (409 while a VM runs on the other datapath), as a start is: before the stop,
    nothing changes; if the check fails again after the stop, the VM stays stopped at its new size and
    the error says so. A stopped VM, or a resize that needs no reboot, is not checked.

    A request with `restart` can take a stop plus a cold start to answer, longer than a proxy in front
    of Cove may keep the request open; the resize goes on whether or not anyone waits. After a timeout
    or a proxy's 502 to 504, read the VM (`GET /api/vms/{name}`) before sending it again. Without
    `restart` a resize never reboots.

    Args:
        name (str):
        body (ResizeRequest): POST /vms/{name}/resize request body. Either field may be `None` to
            keep
            the current dimension unchanged. `memory_mb` must be a multiple of 2 (the
            virtio-mem block size is 2 MiB). `disk_size_gb` triggers a stopped-VM disk
            grow; it is mutually exclusive with `cpus`/`memory_mb` at ALL
            call sites — the CLI and the server handler — enforced by
            [`ResizeRequest::validate_exclusivity`].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ResizeResult | ScopeDeniedBody]
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
    body: ResizeRequest,
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
    | ResizeResult
    | ScopeDeniedBody
    | None
):
    """Resize CPU/memory (running) or grow disk (stopped)

     `disk_size_gb` is mutually exclusive with `cpus`/`memory_mb` (422) — disk resize is stopped-VM-only,
    CPU/RAM resize is running-VM-only. `memory_mb` must be a multiple of 2 (virtio-mem block size). A
    disk grow returns a synthetic `ResizeResult` (`actual_cpus`/`actual_memory_mb` zeroed, `reason`
    describing the grow) rather than the real converged CPU/memory values.

    `restart: true` lets the resize reboot the VM, and only when it must: a running VM cannot go below
    both the vCPUs it runs and the disk queues its boot set up, so Cove stops it gracefully (forced
    after the stop timeout), writes the new boot size and starts it cold. Any other change is resized
    live with no reboot, except on a Mac, which has no live resize: there `restart` reboots a running VM
    for any new vCPU count, leaves one asked for the vCPUs it has as it is, and memory never changes. A
    stopped VM takes the new size and stays stopped; any other state is refused (409). Growth the quota
    or host cannot take is refused before the stop. The result's `restart` says which (`restarted`,
    `not_needed`, `stopped`). Off a Mac, memory asked for in the same request is applied after the
    start, within the VM's range and no lower than its boot memory. If the start fails, the VM keeps the
    new size, is left as a failed start leaves it, and the 500 says it was resized but failed to start.
    If the VM starts but the grow after the start (above its boot vCPUs or memory) fails, the answer is
    still 200, with `restart: restarted`, `partial: true`, the size it runs now, and `reason` saying the
    grow after the start failed and why; off a Mac, send the resize again without `restart` to retry the
    grow. A Mac starts the VM at its new vCPU count and keeps its memory, so nothing grows after the
    start there; should the VM come up at another size, the answer is the same `partial: true`, as the
    live resize that would make it up is refused on a Mac. On a Mac, a reboot is refused with 503 when
    no network owner serves (409 while a VM runs on the other datapath), as a start is: before the stop,
    nothing changes; if the check fails again after the stop, the VM stays stopped at its new size and
    the error says so. A stopped VM, or a resize that needs no reboot, is not checked.

    A request with `restart` can take a stop plus a cold start to answer, longer than a proxy in front
    of Cove may keep the request open; the resize goes on whether or not anyone waits. After a timeout
    or a proxy's 502 to 504, read the VM (`GET /api/vms/{name}`) before sending it again. Without
    `restart` a resize never reboots.

    Args:
        name (str):
        body (ResizeRequest): POST /vms/{name}/resize request body. Either field may be `None` to
            keep
            the current dimension unchanged. `memory_mb` must be a multiple of 2 (the
            virtio-mem block size is 2 MiB). `disk_size_gb` triggers a stopped-VM disk
            grow; it is mutually exclusive with `cpus`/`memory_mb` at ALL
            call sites — the CLI and the server handler — enforced by
            [`ResizeRequest::validate_exclusivity`].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | ResizeResult | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
