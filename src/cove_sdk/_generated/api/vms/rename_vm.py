from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.invalid_vm_name_body import InvalidVmNameBody
from ...models.rename_vm_request import RenameVmRequest
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.vm_detail import VmDetail
from ...models.vm_name_taken_body import VmNameTakenBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: RenameVmRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/rename".format(
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
    | InvalidVmNameBody
    | VmNameTakenBody
    | CliTooOldBody
    | ScopeDeniedBody
    | VmDetail
    | None
):
    if response.status_code == 200:
        response_200 = VmDetail.from_dict(response.json())

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
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 409:

        def _parse_response_409(data: object) -> ApiError | VmNameTakenBody:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_vm_rename_conflict_response_type_0 = (
                    VmNameTakenBody.from_dict(data)
                )

                return componentsschemas_vm_rename_conflict_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_vm_rename_conflict_response_type_1 = ApiError.from_dict(
                data
            )

            return componentsschemas_vm_rename_conflict_response_type_1

        response_409 = _parse_response_409(response.json())

        return response_409

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = ApiError.from_dict(response.json())

        return response_502

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
    | VmNameTakenBody
    | CliTooOldBody
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
    body: RenameVmRequest,
) -> Response[
    ApiError
    | InvalidVmNameBody
    | VmNameTakenBody
    | CliTooOldBody
    | ScopeDeniedBody
    | VmDetail
]:
    """Rename a VM

     Gives the VM `new_name`. The VM keeps its id, disk, state and everything attached to it; its SSH and
    HTTP addresses, its DNS name and its hostname move to the new name, and `vm.renamed` is emitted. A
    running VM keeps running. The old name goes into the same cooldown a deleted VM's name does, so
    another VM cannot take it at once.

    Renaming needs the permission to delete the VM. The answer is the VM's detail under its new name,
    the same body `GET /api/vms/{name}` returns.

    A VM that is being created or deleted, or a pool standby, is refused (409); so is one with another
    operation running on it, or whose last rename is still being finished: retry shortly. A failed VM
    can be renamed.

    Args:
        name (str):
        body (RenameVmRequest): Request body for `POST /api/vms/{name}/rename`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | InvalidVmNameBody | ApiError | VmNameTakenBody | CliTooOldBody | ScopeDeniedBody | VmDetail]
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
    body: RenameVmRequest,
) -> (
    ApiError
    | InvalidVmNameBody
    | VmNameTakenBody
    | CliTooOldBody
    | ScopeDeniedBody
    | VmDetail
    | None
):
    """Rename a VM

     Gives the VM `new_name`. The VM keeps its id, disk, state and everything attached to it; its SSH and
    HTTP addresses, its DNS name and its hostname move to the new name, and `vm.renamed` is emitted. A
    running VM keeps running. The old name goes into the same cooldown a deleted VM's name does, so
    another VM cannot take it at once.

    Renaming needs the permission to delete the VM. The answer is the VM's detail under its new name,
    the same body `GET /api/vms/{name}` returns.

    A VM that is being created or deleted, or a pool standby, is refused (409); so is one with another
    operation running on it, or whose last rename is still being finished: retry shortly. A failed VM
    can be renamed.

    Args:
        name (str):
        body (RenameVmRequest): Request body for `POST /api/vms/{name}/rename`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | InvalidVmNameBody | ApiError | VmNameTakenBody | CliTooOldBody | ScopeDeniedBody | VmDetail
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
    body: RenameVmRequest,
) -> Response[
    ApiError
    | InvalidVmNameBody
    | VmNameTakenBody
    | CliTooOldBody
    | ScopeDeniedBody
    | VmDetail
]:
    """Rename a VM

     Gives the VM `new_name`. The VM keeps its id, disk, state and everything attached to it; its SSH and
    HTTP addresses, its DNS name and its hostname move to the new name, and `vm.renamed` is emitted. A
    running VM keeps running. The old name goes into the same cooldown a deleted VM's name does, so
    another VM cannot take it at once.

    Renaming needs the permission to delete the VM. The answer is the VM's detail under its new name,
    the same body `GET /api/vms/{name}` returns.

    A VM that is being created or deleted, or a pool standby, is refused (409); so is one with another
    operation running on it, or whose last rename is still being finished: retry shortly. A failed VM
    can be renamed.

    Args:
        name (str):
        body (RenameVmRequest): Request body for `POST /api/vms/{name}/rename`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | InvalidVmNameBody | ApiError | VmNameTakenBody | CliTooOldBody | ScopeDeniedBody | VmDetail]
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
    body: RenameVmRequest,
) -> (
    ApiError
    | InvalidVmNameBody
    | VmNameTakenBody
    | CliTooOldBody
    | ScopeDeniedBody
    | VmDetail
    | None
):
    """Rename a VM

     Gives the VM `new_name`. The VM keeps its id, disk, state and everything attached to it; its SSH and
    HTTP addresses, its DNS name and its hostname move to the new name, and `vm.renamed` is emitted. A
    running VM keeps running. The old name goes into the same cooldown a deleted VM's name does, so
    another VM cannot take it at once.

    Renaming needs the permission to delete the VM. The answer is the VM's detail under its new name,
    the same body `GET /api/vms/{name}` returns.

    A VM that is being created or deleted, or a pool standby, is refused (409); so is one with another
    operation running on it, or whose last rename is still being finished: retry shortly. A failed VM
    can be renamed.

    Args:
        name (str):
        body (RenameVmRequest): Request body for `POST /api/vms/{name}/rename`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | InvalidVmNameBody | ApiError | VmNameTakenBody | CliTooOldBody | ScopeDeniedBody | VmDetail
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
