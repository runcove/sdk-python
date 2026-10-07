from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import UNSET, Response


def _get_kwargs(
    name: str,
    *,
    path: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/vms/{name}/files".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ApiError | CliTooOldBody]:
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
) -> Response[Any | ApiError | CliTooOldBody]:
    """Size, mode and modification time of one file in a running VM

     The download's headers without its body: the guest stats the file and nothing is read. Not audited,
    except a path the guest denies (`vm.file.refused`). Error responses carry no body (HEAD), so the
    documented ones name their error code in `X-Cove-Error-Code`: the `code` the same `GET` puts in its
    JSON body. A 404 is `vm_not_found` or `file_not_found`; a 403 is `file_path_denied` or
    `scope_denied`.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
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
) -> Any | ApiError | CliTooOldBody | None:
    """Size, mode and modification time of one file in a running VM

     The download's headers without its body: the guest stats the file and nothing is read. Not audited,
    except a path the guest denies (`vm.file.refused`). Error responses carry no body (HEAD), so the
    documented ones name their error code in `X-Cove-Error-Code`: the `code` the same `GET` puts in its
    JSON body. A 404 is `vm_not_found` or `file_not_found`; a 403 is `file_path_denied` or
    `scope_denied`.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
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
) -> Response[Any | ApiError | CliTooOldBody]:
    """Size, mode and modification time of one file in a running VM

     The download's headers without its body: the guest stats the file and nothing is read. Not audited,
    except a path the guest denies (`vm.file.refused`). Error responses carry no body (HEAD), so the
    documented ones name their error code in `X-Cove-Error-Code`: the `code` the same `GET` puts in its
    JSON body. A 404 is `vm_not_found` or `file_not_found`; a 403 is `file_path_denied` or
    `scope_denied`.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
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
) -> Any | ApiError | CliTooOldBody | None:
    """Size, mode and modification time of one file in a running VM

     The download's headers without its body: the guest stats the file and nothing is read. Not audited,
    except a path the guest denies (`vm.file.refused`). Error responses carry no body (HEAD), so the
    documented ones name their error code in `X-Cove-Error-Code`: the `code` the same `GET` puts in its
    JSON body. A 404 is `vm_not_found` or `file_not_found`; a 403 is `file_path_denied` or
    `scope_denied`.

    Args:
        name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            path=path,
        )
    ).parsed
