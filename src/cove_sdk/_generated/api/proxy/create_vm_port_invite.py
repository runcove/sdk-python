from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.create_invite_request import CreateInviteRequest
from ...models.port_not_allowed_body import PortNotAllowedBody
from ...models.proxy_invite import ProxyInvite
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    port: int,
    *,
    body: CreateInviteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/ports/{port}/invites".format(
            name=quote(str(name), safe=""),
            port=quote(str(port), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody | None
):
    if response.status_code == 201:
        response_201 = ProxyInvite.from_dict(response.json())

        return response_201

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

    if response.status_code == 422:
        response_422 = PortNotAllowedBody.from_dict(response.json())

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
    ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateInviteRequest,
) -> Response[
    ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody
]:
    """Mint a time-limited invite link for a port

     Mints a time-limited invite link for the port — a Warpgate ticket appended to the port's proxy URL
    as a query parameter, letting an unauthenticated recipient reach it until it expires. Independent of
    the port's `public` flag: an invite link works whether or not the port is public.

    Returns **400** when `ttl_secs` cannot produce a valid expiry timestamp — an astronomically large
    value would otherwise overflow the arithmetic Warpgate ticket minting does internally.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports`, exactly
    as `createVmPort` / `setVmPortPublic` / `setVmPrimaryPort` do — the body is an `ApiError` envelope
    with two extra fields not modeled in the schema: `port` (the offending port) and `allowed` (the
    configured allowlist). A VM that does not exist, or is not visible to the caller, returns 404
    (existence non-leak).

    Named `createVmPortInvite` rather than `createPortInvite` — it was missing its `Vm` segment,
    inconsistent with the sibling `setVmPortPublic` on the same nested path.

    Args:
        name (str):
        port (int):
        body (CreateInviteRequest): POST /vms/{name}/ports/{port}/invites request body. `port` is
            not
            repeated here — it comes from the path. Not to be confused with
            `cove_service::proxy_types::CreateInviteRequest`, an unused duplicate with
            a different shape (see the note there).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        port=port,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateInviteRequest,
) -> (
    ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody | None
):
    """Mint a time-limited invite link for a port

     Mints a time-limited invite link for the port — a Warpgate ticket appended to the port's proxy URL
    as a query parameter, letting an unauthenticated recipient reach it until it expires. Independent of
    the port's `public` flag: an invite link works whether or not the port is public.

    Returns **400** when `ttl_secs` cannot produce a valid expiry timestamp — an astronomically large
    value would otherwise overflow the arithmetic Warpgate ticket minting does internally.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports`, exactly
    as `createVmPort` / `setVmPortPublic` / `setVmPrimaryPort` do — the body is an `ApiError` envelope
    with two extra fields not modeled in the schema: `port` (the offending port) and `allowed` (the
    configured allowlist). A VM that does not exist, or is not visible to the caller, returns 404
    (existence non-leak).

    Named `createVmPortInvite` rather than `createPortInvite` — it was missing its `Vm` segment,
    inconsistent with the sibling `setVmPortPublic` on the same nested path.

    Args:
        name (str):
        port (int):
        body (CreateInviteRequest): POST /vms/{name}/ports/{port}/invites request body. `port` is
            not
            repeated here — it comes from the path. Not to be confused with
            `cove_service::proxy_types::CreateInviteRequest`, an unused duplicate with
            a different shape (see the note there).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        port=port,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateInviteRequest,
) -> Response[
    ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody
]:
    """Mint a time-limited invite link for a port

     Mints a time-limited invite link for the port — a Warpgate ticket appended to the port's proxy URL
    as a query parameter, letting an unauthenticated recipient reach it until it expires. Independent of
    the port's `public` flag: an invite link works whether or not the port is public.

    Returns **400** when `ttl_secs` cannot produce a valid expiry timestamp — an astronomically large
    value would otherwise overflow the arithmetic Warpgate ticket minting does internally.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports`, exactly
    as `createVmPort` / `setVmPortPublic` / `setVmPrimaryPort` do — the body is an `ApiError` envelope
    with two extra fields not modeled in the schema: `port` (the offending port) and `allowed` (the
    configured allowlist). A VM that does not exist, or is not visible to the caller, returns 404
    (existence non-leak).

    Named `createVmPortInvite` rather than `createPortInvite` — it was missing its `Vm` segment,
    inconsistent with the sibling `setVmPortPublic` on the same nested path.

    Args:
        name (str):
        port (int):
        body (CreateInviteRequest): POST /vms/{name}/ports/{port}/invites request body. `port` is
            not
            repeated here — it comes from the path. Not to be confused with
            `cove_service::proxy_types::CreateInviteRequest`, an unused duplicate with
            a different shape (see the note there).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        port=port,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateInviteRequest,
) -> (
    ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody | None
):
    """Mint a time-limited invite link for a port

     Mints a time-limited invite link for the port — a Warpgate ticket appended to the port's proxy URL
    as a query parameter, letting an unauthenticated recipient reach it until it expires. Independent of
    the port's `public` flag: an invite link works whether or not the port is public.

    Returns **400** when `ttl_secs` cannot produce a valid expiry timestamp — an astronomically large
    value would otherwise overflow the arithmetic Warpgate ticket minting does internally.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports`, exactly
    as `createVmPort` / `setVmPortPublic` / `setVmPrimaryPort` do — the body is an `ApiError` envelope
    with two extra fields not modeled in the schema: `port` (the offending port) and `allowed` (the
    configured allowlist). A VM that does not exist, or is not visible to the caller, returns 404
    (existence non-leak).

    Named `createVmPortInvite` rather than `createPortInvite` — it was missing its `Vm` segment,
    inconsistent with the sibling `setVmPortPublic` on the same nested path.

    Args:
        name (str):
        port (int):
        body (CreateInviteRequest): POST /vms/{name}/ports/{port}/invites request body. `port` is
            not
            repeated here — it comes from the path. Not to be confused with
            `cove_service::proxy_types::CreateInviteRequest`, an unused duplicate with
            a different shape (see the note there).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | PortNotAllowedBody | ProxyInvite | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            port=port,
            client=client,
            body=body,
        )
    ).parsed
