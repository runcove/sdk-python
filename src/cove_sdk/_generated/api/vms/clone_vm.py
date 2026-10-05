from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.clone_request import CloneRequest
from ...models.clone_response import CloneResponse
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
from ...types import Response


def _get_kwargs(
    source: str,
    *,
    body: CloneRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{source}/clone".format(
            source=quote(str(source), safe=""),
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
    | InvalidVmNameBody
    | CliTooOldBody
    | CloneResponse
    | None
):
    if response.status_code == 200:
        response_200 = CloneResponse.from_dict(response.json())

        return response_200

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
    | InvalidVmNameBody
    | CliTooOldBody
    | CloneResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    source: str,
    *,
    client: AuthenticatedClient | Client,
    body: CloneRequest,
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
    | InvalidVmNameBody
    | CliTooOldBody
    | CloneResponse
]:
    """Clone a VM

     Clones `source` into a new VM. When `source_checkpoint_id` is omitted, the service first takes an
    implicit `pre_clone` checkpoint of `source` and clones from that — callers never have to take a
    checkpoint themselves. The response's `fingerprints` are the clone's SSH host-key fingerprints,
    pinned into Warpgate's known-hosts on registration so the first SSH sees no TOFU prompt.

    `new_vm_name` follows the same rule as a created VM's name: **3-30 characters** of lowercase ASCII
    letters, digits and hyphens, not starting or ending with a hyphen. Any other name is refused with
    **400** `invalid_vm_name` before `source` is looked up.

    Args:
        source (str):
        body (CloneRequest): POST /vms/{source}/clone request body. The new VM's name is supplied
            by
            the caller; an optional `source_checkpoint_id` pins which checkpoint to
            reflink from. When omitted the service creates an implicit
            `pre_clone` checkpoint of the source first, then clones from it
            (the caller never has to take a checkpoint themselves).

            Mirrors `cove_service::api_types::CloneRequest`. The wire field name is
            `new_vm_name` (not `new_name`) to match the service mirror — drift here
            breaks the cross-crate roundtrip pinned by `unit_clone_request_*`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | ApiError | InvalidVmNameBody | CliTooOldBody | CloneResponse]
    """

    kwargs = _get_kwargs(
        source=source,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    source: str,
    *,
    client: AuthenticatedClient | Client,
    body: CloneRequest,
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
    | InvalidVmNameBody
    | CliTooOldBody
    | CloneResponse
    | None
):
    """Clone a VM

     Clones `source` into a new VM. When `source_checkpoint_id` is omitted, the service first takes an
    implicit `pre_clone` checkpoint of `source` and clones from that — callers never have to take a
    checkpoint themselves. The response's `fingerprints` are the clone's SSH host-key fingerprints,
    pinned into Warpgate's known-hosts on registration so the first SSH sees no TOFU prompt.

    `new_vm_name` follows the same rule as a created VM's name: **3-30 characters** of lowercase ASCII
    letters, digits and hyphens, not starting or ending with a hyphen. Any other name is refused with
    **400** `invalid_vm_name` before `source` is looked up.

    Args:
        source (str):
        body (CloneRequest): POST /vms/{source}/clone request body. The new VM's name is supplied
            by
            the caller; an optional `source_checkpoint_id` pins which checkpoint to
            reflink from. When omitted the service creates an implicit
            `pre_clone` checkpoint of the source first, then clones from it
            (the caller never has to take a checkpoint themselves).

            Mirrors `cove_service::api_types::CloneRequest`. The wire field name is
            `new_vm_name` (not `new_name`) to match the service mirror — drift here
            breaks the cross-crate roundtrip pinned by `unit_clone_request_*`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | ApiError | InvalidVmNameBody | CliTooOldBody | CloneResponse
    """

    return sync_detailed(
        source=source,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    source: str,
    *,
    client: AuthenticatedClient | Client,
    body: CloneRequest,
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
    | InvalidVmNameBody
    | CliTooOldBody
    | CloneResponse
]:
    """Clone a VM

     Clones `source` into a new VM. When `source_checkpoint_id` is omitted, the service first takes an
    implicit `pre_clone` checkpoint of `source` and clones from that — callers never have to take a
    checkpoint themselves. The response's `fingerprints` are the clone's SSH host-key fingerprints,
    pinned into Warpgate's known-hosts on registration so the first SSH sees no TOFU prompt.

    `new_vm_name` follows the same rule as a created VM's name: **3-30 characters** of lowercase ASCII
    letters, digits and hyphens, not starting or ending with a hyphen. Any other name is refused with
    **400** `invalid_vm_name` before `source` is looked up.

    Args:
        source (str):
        body (CloneRequest): POST /vms/{source}/clone request body. The new VM's name is supplied
            by
            the caller; an optional `source_checkpoint_id` pins which checkpoint to
            reflink from. When omitted the service creates an implicit
            `pre_clone` checkpoint of the source first, then clones from it
            (the caller never has to take a checkpoint themselves).

            Mirrors `cove_service::api_types::CloneRequest`. The wire field name is
            `new_vm_name` (not `new_name`) to match the service mirror — drift here
            breaks the cross-crate roundtrip pinned by `unit_clone_request_*`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | ApiError | InvalidVmNameBody | CliTooOldBody | CloneResponse]
    """

    kwargs = _get_kwargs(
        source=source,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    source: str,
    *,
    client: AuthenticatedClient | Client,
    body: CloneRequest,
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
    | InvalidVmNameBody
    | CliTooOldBody
    | CloneResponse
    | None
):
    """Clone a VM

     Clones `source` into a new VM. When `source_checkpoint_id` is omitted, the service first takes an
    implicit `pre_clone` checkpoint of `source` and clones from that — callers never have to take a
    checkpoint themselves. The response's `fingerprints` are the clone's SSH host-key fingerprints,
    pinned into Warpgate's known-hosts on registration so the first SSH sees no TOFU prompt.

    `new_vm_name` follows the same rule as a created VM's name: **3-30 characters** of lowercase ASCII
    letters, digits and hyphens, not starting or ending with a hyphen. Any other name is refused with
    **400** `invalid_vm_name` before `source` is looked up.

    Args:
        source (str):
        body (CloneRequest): POST /vms/{source}/clone request body. The new VM's name is supplied
            by
            the caller; an optional `source_checkpoint_id` pins which checkpoint to
            reflink from. When omitted the service creates an implicit
            `pre_clone` checkpoint of the source first, then clones from it
            (the caller never has to take a checkpoint themselves).

            Mirrors `cove_service::api_types::CloneRequest`. The wire field name is
            `new_vm_name` (not `new_name`) to match the service mirror — drift here
            breaks the cross-crate roundtrip pinned by `unit_clone_request_*`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | DenyReasonType0 | DenyReasonType1 | DenyReasonType10 | DenyReasonType11 | DenyReasonType12 | DenyReasonType13 | DenyReasonType14 | DenyReasonType15 | DenyReasonType16 | DenyReasonType2 | DenyReasonType3 | DenyReasonType4 | DenyReasonType5 | DenyReasonType6 | DenyReasonType7 | DenyReasonType8 | DenyReasonType9 | ApiError | InvalidVmNameBody | CliTooOldBody | CloneResponse
    """

    return (
        await asyncio_detailed(
            source=source,
            client=client,
            body=body,
        )
    ).parsed
