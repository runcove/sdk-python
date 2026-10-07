from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.checkpoint import Checkpoint
from ...models.checkpoint_create_request import CheckpointCreateRequest
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: CheckpointCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/checkpoints".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = Checkpoint.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ApiError.from_dict(response.json())

        return response_409

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
) -> Response[ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody]:
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
    body: CheckpointCreateRequest,
) -> Response[ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody]:
    """Checkpoint a VM

     Saves a point in the VM's life that it can later be rolled back to, or cloned from. `disk_only`
    skips the memory capture — cheaper, but the result cannot be used to restore a running VM.

    Args:
        name (str):
        body (CheckpointCreateRequest): POST /vms/{name}/checkpoints request body. `description`
            is the only
            user-supplied field today; `stop_after` is reserved for the hibernate
            flow; it is not a field of this request (ignored if sent).

            `disk_only` is `Option<bool>` with serde default + skip-if-none
            so legacy clients that omit it are treated as a full-checkpoint request
            (`None` → server maps to `false`). `Some(true)` requests a disk-only
            checkpoint (skip memory capture).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody]
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
    body: CheckpointCreateRequest,
) -> ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody | None:
    """Checkpoint a VM

     Saves a point in the VM's life that it can later be rolled back to, or cloned from. `disk_only`
    skips the memory capture — cheaper, but the result cannot be used to restore a running VM.

    Args:
        name (str):
        body (CheckpointCreateRequest): POST /vms/{name}/checkpoints request body. `description`
            is the only
            user-supplied field today; `stop_after` is reserved for the hibernate
            flow; it is not a field of this request (ignored if sent).

            `disk_only` is `Option<bool>` with serde default + skip-if-none
            so legacy clients that omit it are treated as a full-checkpoint request
            (`None` → server maps to `false`). `Some(true)` requests a disk-only
            checkpoint (skip memory capture).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody
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
    body: CheckpointCreateRequest,
) -> Response[ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody]:
    """Checkpoint a VM

     Saves a point in the VM's life that it can later be rolled back to, or cloned from. `disk_only`
    skips the memory capture — cheaper, but the result cannot be used to restore a running VM.

    Args:
        name (str):
        body (CheckpointCreateRequest): POST /vms/{name}/checkpoints request body. `description`
            is the only
            user-supplied field today; `stop_after` is reserved for the hibernate
            flow; it is not a field of this request (ignored if sent).

            `disk_only` is `Option<bool>` with serde default + skip-if-none
            so legacy clients that omit it are treated as a full-checkpoint request
            (`None` → server maps to `false`). `Some(true)` requests a disk-only
            checkpoint (skip memory capture).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody]
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
    body: CheckpointCreateRequest,
) -> ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody | None:
    """Checkpoint a VM

     Saves a point in the VM's life that it can later be rolled back to, or cloned from. `disk_only`
    skips the memory capture — cheaper, but the result cannot be used to restore a running VM.

    Args:
        name (str):
        body (CheckpointCreateRequest): POST /vms/{name}/checkpoints request body. `description`
            is the only
            user-supplied field today; `stop_after` is reserved for the hibernate
            flow; it is not a field of this request (ignored if sent).

            `disk_only` is `Option<bool>` with serde default + skip-if-none
            so legacy clients that omit it are treated as a full-checkpoint request
            (`None` → server maps to `false`). `Some(true)` requests a disk-only
            checkpoint (skip memory capture).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | Checkpoint | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
