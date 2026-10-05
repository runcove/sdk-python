from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.import_response import ImportResponse
from ...models.import_secrets_request import ImportSecretsRequest
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: ImportSecretsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/secrets/import".format(
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
    | SudoRequiredBody
    | CliTooOldBody
    | ImportResponse
    | ScopeDeniedBody
    | None
):
    if response.status_code == 200:
        response_200 = ImportResponse.from_dict(response.json())

        return response_200

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

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
    ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody
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
    body: ImportSecretsRequest,
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody
]:
    """Bulk-import secrets onto a VM

     Best-effort — entries with invalid names are silently skipped rather than failing the whole batch.
    Every imported entry lands with the default `exposure = file`, `lifetime = persistent`; use `POST
    /vms/{name}/secrets/{key}` afterwards to route an individual entry differently. `value` is plain
    UTF-8, NOT base64 (unlike `SetSecretRequest`'s `value_b64`) — the CLI parses a `.env` file upstream
    and forwards `(name, value)` pairs verbatim.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        body (ImportSecretsRequest): Wire body for `POST /vms/{name}/secrets/import`. The CLI
            parses
            `.env` upstream and forwards `(name, value)` pairs verbatim.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody]
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
    body: ImportSecretsRequest,
) -> (
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | ImportResponse
    | ScopeDeniedBody
    | None
):
    """Bulk-import secrets onto a VM

     Best-effort — entries with invalid names are silently skipped rather than failing the whole batch.
    Every imported entry lands with the default `exposure = file`, `lifetime = persistent`; use `POST
    /vms/{name}/secrets/{key}` afterwards to route an individual entry differently. `value` is plain
    UTF-8, NOT base64 (unlike `SetSecretRequest`'s `value_b64`) — the CLI parses a `.env` file upstream
    and forwards `(name, value)` pairs verbatim.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        body (ImportSecretsRequest): Wire body for `POST /vms/{name}/secrets/import`. The CLI
            parses
            `.env` upstream and forwards `(name, value)` pairs verbatim.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody
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
    body: ImportSecretsRequest,
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody
]:
    """Bulk-import secrets onto a VM

     Best-effort — entries with invalid names are silently skipped rather than failing the whole batch.
    Every imported entry lands with the default `exposure = file`, `lifetime = persistent`; use `POST
    /vms/{name}/secrets/{key}` afterwards to route an individual entry differently. `value` is plain
    UTF-8, NOT base64 (unlike `SetSecretRequest`'s `value_b64`) — the CLI parses a `.env` file upstream
    and forwards `(name, value)` pairs verbatim.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        body (ImportSecretsRequest): Wire body for `POST /vms/{name}/secrets/import`. The CLI
            parses
            `.env` upstream and forwards `(name, value)` pairs verbatim.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody]
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
    body: ImportSecretsRequest,
) -> (
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | ImportResponse
    | ScopeDeniedBody
    | None
):
    """Bulk-import secrets onto a VM

     Best-effort — entries with invalid names are silently skipped rather than failing the whole batch.
    Every imported entry lands with the default `exposure = file`, `lifetime = persistent`; use `POST
    /vms/{name}/secrets/{key}` afterwards to route an individual entry differently. `value` is plain
    UTF-8, NOT base64 (unlike `SetSecretRequest`'s `value_b64`) — the CLI parses a `.env` file upstream
    and forwards `(name, value)` pairs verbatim.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        body (ImportSecretsRequest): Wire body for `POST /vms/{name}/secrets/import`. The CLI
            parses
            `.env` upstream and forwards `(name, value)` pairs verbatim.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | ImportResponse | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
