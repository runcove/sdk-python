from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.new_ssh_key import NewSshKey
from ...models.ssh_key import SshKey
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    *,
    body: NewSshKey,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/me/keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | SshKey | None:
    if response.status_code == 201:
        response_201 = SshKey.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

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

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | SshKey]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewSshKey,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | SshKey]:
    """Register a new SSH key

     Registers a new SSH public key against the caller's own identity. Errors are plain-text bodies, not
    the `ApiError` envelope.

    Never published in the outgoing hand-written spec (only the GET was) and never mounted on the
    external bearer listener — mutation of `/api/me/keys` stays unix/internal only, per the comment in
    `routes.rs` next to this route. No `x-required-scope` because `x-listeners` never includes
    `external`.

    Args:
        body (NewSshKey): Input for add / full replace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | SshKey]
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
    body: NewSshKey,
) -> ApiError | SudoRequiredBody | CliTooOldBody | SshKey | None:
    """Register a new SSH key

     Registers a new SSH public key against the caller's own identity. Errors are plain-text bodies, not
    the `ApiError` envelope.

    Never published in the outgoing hand-written spec (only the GET was) and never mounted on the
    external bearer listener — mutation of `/api/me/keys` stays unix/internal only, per the comment in
    `routes.rs` next to this route. No `x-required-scope` because `x-listeners` never includes
    `external`.

    Args:
        body (NewSshKey): Input for add / full replace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | SshKey
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewSshKey,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | SshKey]:
    """Register a new SSH key

     Registers a new SSH public key against the caller's own identity. Errors are plain-text bodies, not
    the `ApiError` envelope.

    Never published in the outgoing hand-written spec (only the GET was) and never mounted on the
    external bearer listener — mutation of `/api/me/keys` stays unix/internal only, per the comment in
    `routes.rs` next to this route. No `x-required-scope` because `x-listeners` never includes
    `external`.

    Args:
        body (NewSshKey): Input for add / full replace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | SshKey]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: NewSshKey,
) -> ApiError | SudoRequiredBody | CliTooOldBody | SshKey | None:
    """Register a new SSH key

     Registers a new SSH public key against the caller's own identity. Errors are plain-text bodies, not
    the `ApiError` envelope.

    Never published in the outgoing hand-written spec (only the GET was) and never mounted on the
    external bearer listener — mutation of `/api/me/keys` stays unix/internal only, per the comment in
    `routes.rs` next to this route. No `x-required-scope` because `x-listeners` never includes
    `external`.

    Args:
        body (NewSshKey): Input for add / full replace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | SshKey
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
