from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
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
        "url": "/api/vms/{name}/console/stream".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    if response.status_code == 200:
        response_200 = response.text
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Live serial console stream (SSE)

     `200 text/event-stream`. Emits `lines` historical console lines first, then live-tails indefinitely.

    One event type, `console`; each frame's `data` is a single raw console line. There is no terminal
    event — close the connection to stop. Responses carry `x-accel-buffering: no` so reverse proxies do
    not hold frames back.

    OpenAPI cannot describe the shape of an event stream beyond its media type: the `body` below is the
    wire text, not a per-frame schema. Clients parse SSE framing themselves.

    The caller needs console access to the VM (`vm.console`). A stream opened by anyone other than the
    VM's owner is recorded in the audit log as `vm.console.opened` (`mode` `stream`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Live serial console stream (SSE)

     `200 text/event-stream`. Emits `lines` historical console lines first, then live-tails indefinitely.

    One event type, `console`; each frame's `data` is a single raw console line. There is no terminal
    event — close the connection to stop. Responses carry `x-accel-buffering: no` so reverse proxies do
    not hold frames back.

    OpenAPI cannot describe the shape of an event stream beyond its media type: the `body` below is the
    wire text, not a per-frame schema. Clients parse SSE framing themselves.

    The caller needs console access to the VM (`vm.console`). A stream opened by anyone other than the
    VM's owner is recorded in the audit log as `vm.console.opened` (`mode` `stream`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Live serial console stream (SSE)

     `200 text/event-stream`. Emits `lines` historical console lines first, then live-tails indefinitely.

    One event type, `console`; each frame's `data` is a single raw console line. There is no terminal
    event — close the connection to stop. Responses carry `x-accel-buffering: no` so reverse proxies do
    not hold frames back.

    OpenAPI cannot describe the shape of an event stream beyond its media type: the `body` below is the
    wire text, not a per-frame schema. Clients parse SSE framing themselves.

    The caller needs console access to the VM (`vm.console`). A stream opened by anyone other than the
    VM's owner is recorded in the audit log as `vm.console.opened` (`mode` `stream`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Live serial console stream (SSE)

     `200 text/event-stream`. Emits `lines` historical console lines first, then live-tails indefinitely.

    One event type, `console`; each frame's `data` is a single raw console line. There is no terminal
    event — close the connection to stop. Responses carry `x-accel-buffering: no` so reverse proxies do
    not hold frames back.

    OpenAPI cannot describe the shape of an event stream beyond its media type: the `body` below is the
    wire text, not a per-frame schema. Clients parse SSE framing themselves.

    The caller needs console access to the VM (`vm.console`). A stream opened by anyone other than the
    VM's owner is recorded in the audit log as `vm.console.opened` (`mode` `stream`).

    Args:
        name (str):
        lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            lines=lines,
        )
    ).parsed
