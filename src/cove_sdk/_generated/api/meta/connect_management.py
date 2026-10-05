from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.connection_info import ConnectionInfo
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/management/connect",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo | None:
    if response.status_code == 200:
        response_200 = ConnectionInfo.from_dict(response.json())

        return response_200

    if response.status_code == 401:

        def _parse_response_401(data: object) -> ApiError | SudoRequiredBody:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_sensitive_op_unauthorized_response_type_0 = (
                    ApiError.from_dict(data)
                )

                return componentsschemas_sensitive_op_unauthorized_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_sensitive_op_unauthorized_response_type_1 = (
                SudoRequiredBody.from_dict(data)
            )

            return componentsschemas_sensitive_op_unauthorized_response_type_1

        response_401 = _parse_response_401(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = cast(Any, None)
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
) -> Response[Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo]:
    """Mint an SSH connection ticket for the daemon's management target

     Mints a Warpgate ticket for the daemon's configured `[daemon] management_target` (the browser
    Lobby's cove-shell REPL target) rather than a specific VM. Open to every authenticated user: the
    REPL it connects to is itself per-user-scoped, so the ticket grants no privilege beyond the caller's
    existing scope. Every attempt — reached or not — is recorded via
    `LifecycleEventKind::ManagementConnectAttempted`.

    Not served on the external bearer-key listener: this is a browser/SSH-session concept, not an
    orchestrator surface, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo | None:
    """Mint an SSH connection ticket for the daemon's management target

     Mints a Warpgate ticket for the daemon's configured `[daemon] management_target` (the browser
    Lobby's cove-shell REPL target) rather than a specific VM. Open to every authenticated user: the
    REPL it connects to is itself per-user-scoped, so the ticket grants no privilege beyond the caller's
    existing scope. Every attempt — reached or not — is recorded via
    `LifecycleEventKind::ManagementConnectAttempted`.

    Not served on the external bearer-key listener: this is a browser/SSH-session concept, not an
    orchestrator surface, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo]:
    """Mint an SSH connection ticket for the daemon's management target

     Mints a Warpgate ticket for the daemon's configured `[daemon] management_target` (the browser
    Lobby's cove-shell REPL target) rather than a specific VM. Open to every authenticated user: the
    REPL it connects to is itself per-user-scoped, so the ticket grants no privilege beyond the caller's
    existing scope. Every attempt — reached or not — is recorded via
    `LifecycleEventKind::ManagementConnectAttempted`.

    Not served on the external bearer-key listener: this is a browser/SSH-session concept, not an
    orchestrator surface, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo | None:
    """Mint an SSH connection ticket for the daemon's management target

     Mints a Warpgate ticket for the daemon's configured `[daemon] management_target` (the browser
    Lobby's cove-shell REPL target) rather than a specific VM. Open to every authenticated user: the
    REPL it connects to is itself per-user-scoped, so the ticket grants no privilege beyond the caller's
    existing scope. Every attempt — reached or not — is recorded via
    `LifecycleEventKind::ManagementConnectAttempted`.

    Not served on the external bearer-key listener: this is a browser/SSH-session concept, not an
    orchestrator surface, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | SudoRequiredBody | CliTooOldBody | ConnectionInfo
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
