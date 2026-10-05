from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.vm_console import VmConsole
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    lines: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["lines"] = lines

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/console".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole | None:
    if response.status_code == 200:
        response_200 = VmConsole.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole]:
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
    lines: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole]:
    """Tail of the serial console log

     A point-in-time read of the most recent console lines. For a live tail instead, see `GET
    /api/vms/{name}/console/stream`.

    **Permission note:** the outgoing hand-written description published `vms:read` for this exact path,
    but `scope_table::lookup` has always answered `vms:exec` for it — independently of an earlier bug in
    the nested `/console/stream` path, which lacked the `console` arm and fell through to the read-only
    catch-all. The bare `/console` path was never affected by that bug because it isn't nested; the
    enforcing code required `vms:exec` here before and after that fix. `vms:exec` is declared below to
    match the enforcing code, for the same reason the streaming form requires it: reading a machine's
    serial console is data-plane access to whatever is running inside the VM, not metadata about it.

    The caller needs console access to the VM (`vm.console`). A read by anyone other than the VM's owner
    (a sharee, an administrator) is recorded in the audit log as `vm.console.opened` (`mode` `lines`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole]
    """

    kwargs = _get_kwargs(
        name=name,
        lines=lines,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    lines: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole | None:
    """Tail of the serial console log

     A point-in-time read of the most recent console lines. For a live tail instead, see `GET
    /api/vms/{name}/console/stream`.

    **Permission note:** the outgoing hand-written description published `vms:read` for this exact path,
    but `scope_table::lookup` has always answered `vms:exec` for it — independently of an earlier bug in
    the nested `/console/stream` path, which lacked the `console` arm and fell through to the read-only
    catch-all. The bare `/console` path was never affected by that bug because it isn't nested; the
    enforcing code required `vms:exec` here before and after that fix. `vms:exec` is declared below to
    match the enforcing code, for the same reason the streaming form requires it: reading a machine's
    serial console is data-plane access to whatever is running inside the VM, not metadata about it.

    The caller needs console access to the VM (`vm.console`). A read by anyone other than the VM's owner
    (a sharee, an administrator) is recorded in the audit log as `vm.console.opened` (`mode` `lines`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole
    """

    return sync_detailed(
        name=name,
        client=client,
        lines=lines,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    lines: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole]:
    """Tail of the serial console log

     A point-in-time read of the most recent console lines. For a live tail instead, see `GET
    /api/vms/{name}/console/stream`.

    **Permission note:** the outgoing hand-written description published `vms:read` for this exact path,
    but `scope_table::lookup` has always answered `vms:exec` for it — independently of an earlier bug in
    the nested `/console/stream` path, which lacked the `console` arm and fell through to the read-only
    catch-all. The bare `/console` path was never affected by that bug because it isn't nested; the
    enforcing code required `vms:exec` here before and after that fix. `vms:exec` is declared below to
    match the enforcing code, for the same reason the streaming form requires it: reading a machine's
    serial console is data-plane access to whatever is running inside the VM, not metadata about it.

    The caller needs console access to the VM (`vm.console`). A read by anyone other than the VM's owner
    (a sharee, an administrator) is recorded in the audit log as `vm.console.opened` (`mode` `lines`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole]
    """

    kwargs = _get_kwargs(
        name=name,
        lines=lines,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    lines: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole | None:
    """Tail of the serial console log

     A point-in-time read of the most recent console lines. For a live tail instead, see `GET
    /api/vms/{name}/console/stream`.

    **Permission note:** the outgoing hand-written description published `vms:read` for this exact path,
    but `scope_table::lookup` has always answered `vms:exec` for it — independently of an earlier bug in
    the nested `/console/stream` path, which lacked the `console` arm and fell through to the read-only
    catch-all. The bare `/console` path was never affected by that bug because it isn't nested; the
    enforcing code required `vms:exec` here before and after that fix. `vms:exec` is declared below to
    match the enforcing code, for the same reason the streaming form requires it: reading a machine's
    serial console is data-plane access to whatever is running inside the VM, not metadata about it.

    The caller needs console access to the VM (`vm.console`). A read by anyone other than the VM's owner
    (a sharee, an administrator) is recorded in the audit log as `vm.console.opened` (`mode` `lines`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmConsole
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            lines=lines,
        )
    ).parsed
