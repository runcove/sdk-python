from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.port_not_primary_body import PortNotPrimaryBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.set_public_request import SetPublicRequest
from ...types import Response


def _get_kwargs(
    name: str,
    port: int,
    *,
    body: SetPublicRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/vms/{name}/ports/{port}/public".format(
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
) -> Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody | None:
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
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = PortNotPrimaryBody.from_dict(response.json())

        return response_422

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody]:
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
    body: SetPublicRequest,
) -> Response[Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody]:
    """Toggle public (unauthenticated) access on the primary port

     Sets or clears unauthenticated public access on a port. At most one port per VM may be public at a
    time, and only the primary port is eligible — this is the mechanism a public URL comes from,
    distinct from an invite link (a time-limited, per-request URL any port can mint, not gated on this
    flag). Setting `public: false` always succeeds, on any port.

    Returns **422** `port_not_primary` when setting `public: true` on a non-primary port — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the port attempted)
    and `primary_port` (the VM's actual primary). A VM that does not exist, or is not visible to the
    caller, returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):
        body (SetPublicRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody]
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
    body: SetPublicRequest,
) -> Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody | None:
    """Toggle public (unauthenticated) access on the primary port

     Sets or clears unauthenticated public access on a port. At most one port per VM may be public at a
    time, and only the primary port is eligible — this is the mechanism a public URL comes from,
    distinct from an invite link (a time-limited, per-request URL any port can mint, not gated on this
    flag). Setting `public: false` always succeeds, on any port.

    Returns **422** `port_not_primary` when setting `public: true` on a non-primary port — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the port attempted)
    and `primary_port` (the VM's actual primary). A VM that does not exist, or is not visible to the
    caller, returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):
        body (SetPublicRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody
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
    body: SetPublicRequest,
) -> Response[Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody]:
    """Toggle public (unauthenticated) access on the primary port

     Sets or clears unauthenticated public access on a port. At most one port per VM may be public at a
    time, and only the primary port is eligible — this is the mechanism a public URL comes from,
    distinct from an invite link (a time-limited, per-request URL any port can mint, not gated on this
    flag). Setting `public: false` always succeeds, on any port.

    Returns **422** `port_not_primary` when setting `public: true` on a non-primary port — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the port attempted)
    and `primary_port` (the VM's actual primary). A VM that does not exist, or is not visible to the
    caller, returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):
        body (SetPublicRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody]
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
    body: SetPublicRequest,
) -> Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody | None:
    """Toggle public (unauthenticated) access on the primary port

     Sets or clears unauthenticated public access on a port. At most one port per VM may be public at a
    time, and only the primary port is eligible — this is the mechanism a public URL comes from,
    distinct from an invite link (a time-limited, per-request URL any port can mint, not gated on this
    flag). Setting `public: false` always succeeds, on any port.

    Returns **422** `port_not_primary` when setting `public: true` on a non-primary port — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the port attempted)
    and `primary_port` (the VM's actual primary). A VM that does not exist, or is not visible to the
    caller, returns 404 (existence non-leak).

    Args:
        name (str):
        port (int):
        body (SetPublicRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PortNotPrimaryBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            port=port,
            client=client,
            body=body,
        )
    ).parsed
