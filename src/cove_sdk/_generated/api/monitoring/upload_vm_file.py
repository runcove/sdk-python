from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.file_uploaded import FileUploaded
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    name: str,
    *,
    body: File,
    path: str,
    mode: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["path"] = path

    params["mode"] = mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/vms/{name}/files".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | FileUploaded | None:
    if response.status_code == 200:
        response_200 = FileUploaded.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

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
        response_409 = ApiError.from_dict(response.json())

        return response_409

    if response.status_code == 411:
        response_411 = ApiError.from_dict(response.json())

        return response_411

    if response.status_code == 413:
        response_413 = ApiError.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

        return response_422

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if response.status_code == 507:
        response_507 = ApiError.from_dict(response.json())

        return response_507

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | FileUploaded]:
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
    body: File,
    path: str,
    mode: str | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | FileUploaded]:
    """Upload one file into a running VM

     Writes the request body to one regular file in a running VM, creating it or replacing it whole: the
    guest writes a temporary file and renames it into place only once every byte has arrived, so a
    failed upload leaves the old file untouched. The size is the request's `Content-Length`, which is
    required. The file is owned by root; its mode is `mode` when given, else the replaced file's
    permission bits, else `0644`. Symlinks are refused, not followed, anywhere in the path. Every
    committed upload is recorded in the audit log (`vm.file.uploaded`, with the SHA-256), and so is a
    path the guest denies (`vm.file.refused`). The caller needs SSH access to the VM; writing a file as
    root can run code, so `files:write` is as strong as `vms:exec`.

    Args:
        name (str):
        path (str):
        mode (str | Unset):
        body (File): The file's raw bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | FileUploaded]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
        path=path,
        mode=mode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    path: str,
    mode: str | Unset = UNSET,
) -> ApiError | CliTooOldBody | FileUploaded | None:
    """Upload one file into a running VM

     Writes the request body to one regular file in a running VM, creating it or replacing it whole: the
    guest writes a temporary file and renames it into place only once every byte has arrived, so a
    failed upload leaves the old file untouched. The size is the request's `Content-Length`, which is
    required. The file is owned by root; its mode is `mode` when given, else the replaced file's
    permission bits, else `0644`. Symlinks are refused, not followed, anywhere in the path. Every
    committed upload is recorded in the audit log (`vm.file.uploaded`, with the SHA-256), and so is a
    path the guest denies (`vm.file.refused`). The caller needs SSH access to the VM; writing a file as
    root can run code, so `files:write` is as strong as `vms:exec`.

    Args:
        name (str):
        path (str):
        mode (str | Unset):
        body (File): The file's raw bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | FileUploaded
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
        path=path,
        mode=mode,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    path: str,
    mode: str | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | FileUploaded]:
    """Upload one file into a running VM

     Writes the request body to one regular file in a running VM, creating it or replacing it whole: the
    guest writes a temporary file and renames it into place only once every byte has arrived, so a
    failed upload leaves the old file untouched. The size is the request's `Content-Length`, which is
    required. The file is owned by root; its mode is `mode` when given, else the replaced file's
    permission bits, else `0644`. Symlinks are refused, not followed, anywhere in the path. Every
    committed upload is recorded in the audit log (`vm.file.uploaded`, with the SHA-256), and so is a
    path the guest denies (`vm.file.refused`). The caller needs SSH access to the VM; writing a file as
    root can run code, so `files:write` is as strong as `vms:exec`.

    Args:
        name (str):
        path (str):
        mode (str | Unset):
        body (File): The file's raw bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | FileUploaded]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
        path=path,
        mode=mode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    path: str,
    mode: str | Unset = UNSET,
) -> ApiError | CliTooOldBody | FileUploaded | None:
    """Upload one file into a running VM

     Writes the request body to one regular file in a running VM, creating it or replacing it whole: the
    guest writes a temporary file and renames it into place only once every byte has arrived, so a
    failed upload leaves the old file untouched. The size is the request's `Content-Length`, which is
    required. The file is owned by root; its mode is `mode` when given, else the replaced file's
    permission bits, else `0644`. Symlinks are refused, not followed, anywhere in the path. Every
    committed upload is recorded in the audit log (`vm.file.uploaded`, with the SHA-256), and so is a
    path the guest denies (`vm.file.refused`). The caller needs SSH access to the VM; writing a file as
    root can run code, so `files:write` is as strong as `vms:exec`.

    Args:
        name (str):
        path (str):
        mode (str | Unset):
        body (File): The file's raw bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | FileUploaded
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
            path=path,
            mode=mode,
        )
    ).parsed
