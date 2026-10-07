from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.vm_process import VmProcess
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    top: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["top"] = top

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/processes".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VmProcess.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]]:
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
    top: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]]:
    """Top guest processes

     Ranks the guest's live process list by resource usage, queried on demand over vsock — there is no
    polling or caching involved, so every call reflects the guest's state at the moment it runs.

    **Requires `vms:exec`, not `vms:read`.** A guest's process list is data-plane content — what is
    running inside the machine, and often enough to infer what it is doing — not metadata about the VM.
    `vms:read` covers metadata (list your VMs, look at one's details); the sibling endpoints on the same
    data, `GET /api/vms/{name}/console` and `POST /api/vms/{name}/exec`, are gated at `vms:exec`, and so
    is this. Both the outgoing published contract and `scope_table::lookup` previously agreed on
    `vms:read` — they agreed on the wrong answer, and both were corrected together.

    The caller needs SSH access to the VM (`vm.ssh`), matching that scope: the owner, a sharee, or an
    administrator (an admin-listed user's session or admin key; their ordinary API key or connected app
    is not one).

    Args:
        name (str):
        top (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]]
    """

    kwargs = _get_kwargs(
        name=name,
        top=top,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    top: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess] | None:
    """Top guest processes

     Ranks the guest's live process list by resource usage, queried on demand over vsock — there is no
    polling or caching involved, so every call reflects the guest's state at the moment it runs.

    **Requires `vms:exec`, not `vms:read`.** A guest's process list is data-plane content — what is
    running inside the machine, and often enough to infer what it is doing — not metadata about the VM.
    `vms:read` covers metadata (list your VMs, look at one's details); the sibling endpoints on the same
    data, `GET /api/vms/{name}/console` and `POST /api/vms/{name}/exec`, are gated at `vms:exec`, and so
    is this. Both the outgoing published contract and `scope_table::lookup` previously agreed on
    `vms:read` — they agreed on the wrong answer, and both were corrected together.

    The caller needs SSH access to the VM (`vm.ssh`), matching that scope: the owner, a sharee, or an
    administrator (an admin-listed user's session or admin key; their ordinary API key or connected app
    is not one).

    Args:
        name (str):
        top (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]
    """

    return sync_detailed(
        name=name,
        client=client,
        top=top,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    top: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]]:
    """Top guest processes

     Ranks the guest's live process list by resource usage, queried on demand over vsock — there is no
    polling or caching involved, so every call reflects the guest's state at the moment it runs.

    **Requires `vms:exec`, not `vms:read`.** A guest's process list is data-plane content — what is
    running inside the machine, and often enough to infer what it is doing — not metadata about the VM.
    `vms:read` covers metadata (list your VMs, look at one's details); the sibling endpoints on the same
    data, `GET /api/vms/{name}/console` and `POST /api/vms/{name}/exec`, are gated at `vms:exec`, and so
    is this. Both the outgoing published contract and `scope_table::lookup` previously agreed on
    `vms:read` — they agreed on the wrong answer, and both were corrected together.

    The caller needs SSH access to the VM (`vm.ssh`), matching that scope: the owner, a sharee, or an
    administrator (an admin-listed user's session or admin key; their ordinary API key or connected app
    is not one).

    Args:
        name (str):
        top (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]]
    """

    kwargs = _get_kwargs(
        name=name,
        top=top,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    top: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess] | None:
    """Top guest processes

     Ranks the guest's live process list by resource usage, queried on demand over vsock — there is no
    polling or caching involved, so every call reflects the guest's state at the moment it runs.

    **Requires `vms:exec`, not `vms:read`.** A guest's process list is data-plane content — what is
    running inside the machine, and often enough to infer what it is doing — not metadata about the VM.
    `vms:read` covers metadata (list your VMs, look at one's details); the sibling endpoints on the same
    data, `GET /api/vms/{name}/console` and `POST /api/vms/{name}/exec`, are gated at `vms:exec`, and so
    is this. Both the outgoing published contract and `scope_table::lookup` previously agreed on
    `vms:read` — they agreed on the wrong answer, and both were corrected together.

    The caller needs SSH access to the VM (`vm.ssh`), matching that scope: the owner, a sharee, or an
    administrator (an admin-listed user's session or admin key; their ordinary API key or connected app
    is not one).

    Args:
        name (str):
        top (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[VmProcess]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            top=top,
        )
    ).parsed
