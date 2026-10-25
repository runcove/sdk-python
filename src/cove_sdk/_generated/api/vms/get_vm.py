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
from ...models.vm_detail import VmDetail
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}".format(
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
    | VmDetail
    | None
):
    if response.status_code == 200:
        response_200 = VmDetail.from_dict(response.json())

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
    | VmDetail
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
    | VmDetail
]:
    """Get one VM

     Full detail for a single VM, including the live TTL countdowns merged in from the TTL sweeper.

    During the cold-create window a VM exists as a reservation before the hypervisor knows about it.
    Rather than 500, this returns a minimal document with `state: creating`, so a client polling after
    `POST /api/vms` sees a stable state throughout. The state stays `creating` after the VM boots, until
    its SSH access is registered. Treat only `running` as a created VM.

    A create that `POST /api/vms` accepted and that then failed (an admission refusal, a failed boot, a
    failed SSH registration) removes its VM. For 5 minutes after, the name answers the create's owner
    with the failure's own status and body in place of the **404**, marked with the `x-cove-create-
    failed` header: usually a **409**, **503** or **500**, or a **400** when the name is refused. Anyone
    else gets the **404**, and so does the owner once the 5 minutes pass, a new create of the name is
    accepted or the daemon restarts.

    A VM that exists but is not yours returns the same **404** as one that does not exist (existence
    non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | VmDetail]
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
    | VmDetail
    | None
):
    """Get one VM

     Full detail for a single VM, including the live TTL countdowns merged in from the TTL sweeper.

    During the cold-create window a VM exists as a reservation before the hypervisor knows about it.
    Rather than 500, this returns a minimal document with `state: creating`, so a client polling after
    `POST /api/vms` sees a stable state throughout. The state stays `creating` after the VM boots, until
    its SSH access is registered. Treat only `running` as a created VM.

    A create that `POST /api/vms` accepted and that then failed (an admission refusal, a failed boot, a
    failed SSH registration) removes its VM. For 5 minutes after, the name answers the create's owner
    with the failure's own status and body in place of the **404**, marked with the `x-cove-create-
    failed` header: usually a **409**, **503** or **500**, or a **400** when the name is refused. Anyone
    else gets the **404**, and so does the owner once the 5 minutes pass, a new create of the name is
    accepted or the daemon restarts.

    A VM that exists but is not yours returns the same **404** as one that does not exist (existence
    non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | VmDetail
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
    | VmDetail
]:
    """Get one VM

     Full detail for a single VM, including the live TTL countdowns merged in from the TTL sweeper.

    During the cold-create window a VM exists as a reservation before the hypervisor knows about it.
    Rather than 500, this returns a minimal document with `state: creating`, so a client polling after
    `POST /api/vms` sees a stable state throughout. The state stays `creating` after the VM boots, until
    its SSH access is registered. Treat only `running` as a created VM.

    A create that `POST /api/vms` accepted and that then failed (an admission refusal, a failed boot, a
    failed SSH registration) removes its VM. For 5 minutes after, the name answers the create's owner
    with the failure's own status and body in place of the **404**, marked with the `x-cove-create-
    failed` header: usually a **409**, **503** or **500**, or a **400** when the name is refused. Anyone
    else gets the **404**, and so does the owner once the 5 minutes pass, a new create of the name is
    accepted or the daemon restarts.

    A VM that exists but is not yours returns the same **404** as one that does not exist (existence
    non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | VmDetail]
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
    | VmDetail
    | None
):
    """Get one VM

     Full detail for a single VM, including the live TTL countdowns merged in from the TTL sweeper.

    During the cold-create window a VM exists as a reservation before the hypervisor knows about it.
    Rather than 500, this returns a minimal document with `state: creating`, so a client polling after
    `POST /api/vms` sees a stable state throughout. The state stays `creating` after the VM boots, until
    its SSH access is registered. Treat only `running` as a created VM.

    A create that `POST /api/vms` accepted and that then failed (an admission refusal, a failed boot, a
    failed SSH registration) removes its VM. For 5 minutes after, the name answers the create's owner
    with the failure's own status and body in place of the **404**, marked with the `x-cove-create-
    failed` header: usually a **409**, **503** or **500**, or a **400** when the name is refused. Anyone
    else gets the **404**, and so does the owner once the 5 minutes pass, a new create of the name is
    accepted or the daemon restarts.

    A VM that exists but is not yours returns the same **404** as one that does not exist (existence
    non-leak).

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | CliTooOldBody | InvalidVmNameBody | ScopeDeniedBody | VmDetail
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
