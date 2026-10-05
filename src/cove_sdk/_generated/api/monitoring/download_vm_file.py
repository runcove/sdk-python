from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import UNSET, File, Response


def _get_kwargs(
    name: str,
    *,
    path: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/files".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | File | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | File]:
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
    path: str,
) -> Response[ApiError | CliTooOldBody | File]:
    """Download one file from a running VM

     Streams one regular file out of a running VM. Symlinks are refused, not followed, anywhere in the
    path. `Content-Length` is the file's size. A transfer that fails after the 200 has been sent cannot
    change its status, so the body ends early: **a body shorter than `Content-Length` is a failed
    download**, never a complete one. That includes a download that runs longer than its size allows at
    an average of 256 KiB/s (60 s at least), which is ended so a slow reader cannot hold one of the
    host's transfer slots. An empty file's 200 is sent only once its read has ended, so an empty file
    whose download fails answers with an error status instead of an empty 200: 503 (`unavailable`) for a
    lost, timed-out or busy guest or a too-slow transfer, 409 (`invalid_state_transition`) if the VM
    left the running state, 500 otherwise. Every completed download is recorded in the audit log
    (`vm.file.downloaded`), and so is a path the guest denies (`vm.file.refused`). The caller needs SSH
    access to the VM.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | File]
    """

    kwargs = _get_kwargs(
        name=name,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    path: str,
) -> ApiError | CliTooOldBody | File | None:
    """Download one file from a running VM

     Streams one regular file out of a running VM. Symlinks are refused, not followed, anywhere in the
    path. `Content-Length` is the file's size. A transfer that fails after the 200 has been sent cannot
    change its status, so the body ends early: **a body shorter than `Content-Length` is a failed
    download**, never a complete one. That includes a download that runs longer than its size allows at
    an average of 256 KiB/s (60 s at least), which is ended so a slow reader cannot hold one of the
    host's transfer slots. An empty file's 200 is sent only once its read has ended, so an empty file
    whose download fails answers with an error status instead of an empty 200: 503 (`unavailable`) for a
    lost, timed-out or busy guest or a too-slow transfer, 409 (`invalid_state_transition`) if the VM
    left the running state, 500 otherwise. Every completed download is recorded in the audit log
    (`vm.file.downloaded`), and so is a path the guest denies (`vm.file.refused`). The caller needs SSH
    access to the VM.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | File
    """

    return sync_detailed(
        name=name,
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    path: str,
) -> Response[ApiError | CliTooOldBody | File]:
    """Download one file from a running VM

     Streams one regular file out of a running VM. Symlinks are refused, not followed, anywhere in the
    path. `Content-Length` is the file's size. A transfer that fails after the 200 has been sent cannot
    change its status, so the body ends early: **a body shorter than `Content-Length` is a failed
    download**, never a complete one. That includes a download that runs longer than its size allows at
    an average of 256 KiB/s (60 s at least), which is ended so a slow reader cannot hold one of the
    host's transfer slots. An empty file's 200 is sent only once its read has ended, so an empty file
    whose download fails answers with an error status instead of an empty 200: 503 (`unavailable`) for a
    lost, timed-out or busy guest or a too-slow transfer, 409 (`invalid_state_transition`) if the VM
    left the running state, 500 otherwise. Every completed download is recorded in the audit log
    (`vm.file.downloaded`), and so is a path the guest denies (`vm.file.refused`). The caller needs SSH
    access to the VM.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | File]
    """

    kwargs = _get_kwargs(
        name=name,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    path: str,
) -> ApiError | CliTooOldBody | File | None:
    """Download one file from a running VM

     Streams one regular file out of a running VM. Symlinks are refused, not followed, anywhere in the
    path. `Content-Length` is the file's size. A transfer that fails after the 200 has been sent cannot
    change its status, so the body ends early: **a body shorter than `Content-Length` is a failed
    download**, never a complete one. That includes a download that runs longer than its size allows at
    an average of 256 KiB/s (60 s at least), which is ended so a slow reader cannot hold one of the
    host's transfer slots. An empty file's 200 is sent only once its read has ended, so an empty file
    whose download fails answers with an error status instead of an empty 200: 503 (`unavailable`) for a
    lost, timed-out or busy guest or a too-slow transfer, 409 (`invalid_state_transition`) if the VM
    left the running state, 500 otherwise. Every completed download is recorded in the audit log
    (`vm.file.downloaded`), and so is a path the guest denies (`vm.file.refused`). The caller needs SSH
    access to the VM.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | File
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            path=path,
        )
    ).parsed
