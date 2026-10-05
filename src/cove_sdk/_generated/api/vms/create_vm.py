from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.create_vm_request import CreateVmRequest
from ...models.create_vm_response import CreateVmResponse
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
from ...models.vm_name_taken_body import VmNameTakenBody
from ...types import Response


def _get_kwargs(
    *,
    body: CreateVmRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiError
    | InvalidVmNameBody
    | CliTooOldBody
    | CreateVmResponse
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
    | VmNameTakenBody
    | None
):
    if response.status_code == 202:
        response_202 = CreateVmResponse.from_dict(response.json())

        return response_202

    if response.status_code == 400:

        def _parse_response_400(data: object) -> ApiError | InvalidVmNameBody:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_vm_bad_request_response_type_0 = ApiError.from_dict(
                    data
                )

                return componentsschemas_vm_bad_request_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_vm_bad_request_response_type_1 = (
                InvalidVmNameBody.from_dict(data)
            )

            return componentsschemas_vm_bad_request_response_type_1

        response_400 = _parse_response_400(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 409:

        def _parse_response_409(
            data: object,
        ) -> (
            DenyReasonType0
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
            | VmNameTakenBody
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_vm_create_conflict_response_type_0 = (
                    VmNameTakenBody.from_dict(data)
                )

                return componentsschemas_vm_create_conflict_response_type_0
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
    | InvalidVmNameBody
    | CliTooOldBody
    | CreateVmResponse
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
    | VmNameTakenBody
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateVmRequest,
) -> Response[
    ApiError
    | InvalidVmNameBody
    | CliTooOldBody
    | CreateVmResponse
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
    | VmNameTakenBody
]:
    """Create a VM

     Returns **202** as soon as the pre-flight checks pass; the VM continues building in the background.
    Poll `GET /api/vms/{name}` for the live state.

    Pre-flight failures — a name already taken, a quota or admission denial, an invalid resource request
    — are returned synchronously. Anything that fails *after* the 202 surfaces only as the VM's state,
    never as an error on this response.

    **Names.** `name` is optional; omit it and the server picks one. A name must be **3-30 characters**
    of lowercase ASCII letters, digits and hyphens (`[a-z0-9-]`), and must not start or end with a
    hyphen: `web-1` is a name, `Web_1`, `ab` and `-web` are not. A name outside the rule, or one held by
    a bastion target this server may not take over, is refused with **400** `invalid_vm_name`, with
    `field: "name"` and the rejected name echoed in `name`.

    The **409** is never the usual `ApiError` envelope. It is one of two shapes, published as a union: a
    **taken name** answers `vm_name_taken` with the rejected name and, when the name is in post-delete
    cooldown, the `retry_after_secs` left on it; an **admission or quota denial** answers a
    `DenyReason`, carrying the numbers behind the refusal (what is in use, what was asked for, what the
    cap is) so a caller can decide whether to retry smaller or wait.

    `nested_virt: true` is refused synchronously with **403** `admin_required` unless the caller is in
    the server's `[auth] admins` and, for an API key, the key also holds `admin:vms:nested-virt`. An
    admitted opt-in always cold-boots, so it never takes a VM from the warm pool.

    Args:
        body (CreateVmRequest): POST /vms request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | InvalidVmNameBody | CliTooOldBody | CreateVmResponse | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | VmNameTakenBody]
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
    body: CreateVmRequest,
) -> (
    ApiError
    | InvalidVmNameBody
    | CliTooOldBody
    | CreateVmResponse
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
    | VmNameTakenBody
    | None
):
    """Create a VM

     Returns **202** as soon as the pre-flight checks pass; the VM continues building in the background.
    Poll `GET /api/vms/{name}` for the live state.

    Pre-flight failures — a name already taken, a quota or admission denial, an invalid resource request
    — are returned synchronously. Anything that fails *after* the 202 surfaces only as the VM's state,
    never as an error on this response.

    **Names.** `name` is optional; omit it and the server picks one. A name must be **3-30 characters**
    of lowercase ASCII letters, digits and hyphens (`[a-z0-9-]`), and must not start or end with a
    hyphen: `web-1` is a name, `Web_1`, `ab` and `-web` are not. A name outside the rule, or one held by
    a bastion target this server may not take over, is refused with **400** `invalid_vm_name`, with
    `field: "name"` and the rejected name echoed in `name`.

    The **409** is never the usual `ApiError` envelope. It is one of two shapes, published as a union: a
    **taken name** answers `vm_name_taken` with the rejected name and, when the name is in post-delete
    cooldown, the `retry_after_secs` left on it; an **admission or quota denial** answers a
    `DenyReason`, carrying the numbers behind the refusal (what is in use, what was asked for, what the
    cap is) so a caller can decide whether to retry smaller or wait.

    `nested_virt: true` is refused synchronously with **403** `admin_required` unless the caller is in
    the server's `[auth] admins` and, for an API key, the key also holds `admin:vms:nested-virt`. An
    admitted opt-in always cold-boots, so it never takes a VM from the warm pool.

    Args:
        body (CreateVmRequest): POST /vms request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | InvalidVmNameBody | CliTooOldBody | CreateVmResponse | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | VmNameTakenBody
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateVmRequest,
) -> Response[
    ApiError
    | InvalidVmNameBody
    | CliTooOldBody
    | CreateVmResponse
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
    | VmNameTakenBody
]:
    """Create a VM

     Returns **202** as soon as the pre-flight checks pass; the VM continues building in the background.
    Poll `GET /api/vms/{name}` for the live state.

    Pre-flight failures — a name already taken, a quota or admission denial, an invalid resource request
    — are returned synchronously. Anything that fails *after* the 202 surfaces only as the VM's state,
    never as an error on this response.

    **Names.** `name` is optional; omit it and the server picks one. A name must be **3-30 characters**
    of lowercase ASCII letters, digits and hyphens (`[a-z0-9-]`), and must not start or end with a
    hyphen: `web-1` is a name, `Web_1`, `ab` and `-web` are not. A name outside the rule, or one held by
    a bastion target this server may not take over, is refused with **400** `invalid_vm_name`, with
    `field: "name"` and the rejected name echoed in `name`.

    The **409** is never the usual `ApiError` envelope. It is one of two shapes, published as a union: a
    **taken name** answers `vm_name_taken` with the rejected name and, when the name is in post-delete
    cooldown, the `retry_after_secs` left on it; an **admission or quota denial** answers a
    `DenyReason`, carrying the numbers behind the refusal (what is in use, what was asked for, what the
    cap is) so a caller can decide whether to retry smaller or wait.

    `nested_virt: true` is refused synchronously with **403** `admin_required` unless the caller is in
    the server's `[auth] admins` and, for an API key, the key also holds `admin:vms:nested-virt`. An
    admitted opt-in always cold-boots, so it never takes a VM from the warm pool.

    Args:
        body (CreateVmRequest): POST /vms request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | InvalidVmNameBody | CliTooOldBody | CreateVmResponse | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | VmNameTakenBody]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateVmRequest,
) -> (
    ApiError
    | InvalidVmNameBody
    | CliTooOldBody
    | CreateVmResponse
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
    | VmNameTakenBody
    | None
):
    """Create a VM

     Returns **202** as soon as the pre-flight checks pass; the VM continues building in the background.
    Poll `GET /api/vms/{name}` for the live state.

    Pre-flight failures — a name already taken, a quota or admission denial, an invalid resource request
    — are returned synchronously. Anything that fails *after* the 202 surfaces only as the VM's state,
    never as an error on this response.

    **Names.** `name` is optional; omit it and the server picks one. A name must be **3-30 characters**
    of lowercase ASCII letters, digits and hyphens (`[a-z0-9-]`), and must not start or end with a
    hyphen: `web-1` is a name, `Web_1`, `ab` and `-web` are not. A name outside the rule, or one held by
    a bastion target this server may not take over, is refused with **400** `invalid_vm_name`, with
    `field: "name"` and the rejected name echoed in `name`.

    The **409** is never the usual `ApiError` envelope. It is one of two shapes, published as a union: a
    **taken name** answers `vm_name_taken` with the rejected name and, when the name is in post-delete
    cooldown, the `retry_after_secs` left on it; an **admission or quota denial** answers a
    `DenyReason`, carrying the numbers behind the refusal (what is in use, what was asked for, what the
    cap is) so a caller can decide whether to retry smaller or wait.

    `nested_virt: true` is refused synchronously with **403** `admin_required` unless the caller is in
    the server's `[auth] admins` and, for an API key, the key also holds `admin:vms:nested-virt`. An
    admitted opt-in always cold-boots, so it never takes a VM from the warm pool.

    Args:
        body (CreateVmRequest): POST /vms request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | InvalidVmNameBody | CliTooOldBody | CreateVmResponse | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | VmNameTakenBody
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
