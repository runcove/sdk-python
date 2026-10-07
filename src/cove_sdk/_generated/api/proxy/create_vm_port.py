from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_port_request import AddPortRequest
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.port_not_allowed_body import PortNotAllowedBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: AddPortRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/ports".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody | None:
    if response.status_code == 201:
        response_201 = cast(Any, None)
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
) -> Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody]:
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
    body: AddPortRequest,
) -> Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody]:
    """Expose a guest port through the HTTPS proxy

     Registers a guest port for the HTTPS proxy. The port must be within `[service.proxy].allowed_ports`;
    the resulting proxy target is not public until `PUT .../ports/{port}/public` is also called on the
    primary port.

    Returns **422** `port_not_allowed` when the port is outside the configured allowlist — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the offending port)
    and `allowed` (the configured allowlist). A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        body (AddPortRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody]
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
    body: AddPortRequest,
) -> Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody | None:
    """Expose a guest port through the HTTPS proxy

     Registers a guest port for the HTTPS proxy. The port must be within `[service.proxy].allowed_ports`;
    the resulting proxy target is not public until `PUT .../ports/{port}/public` is also called on the
    primary port.

    Returns **422** `port_not_allowed` when the port is outside the configured allowlist — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the offending port)
    and `allowed` (the configured allowlist). A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        body (AddPortRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody
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
    body: AddPortRequest,
) -> Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody]:
    """Expose a guest port through the HTTPS proxy

     Registers a guest port for the HTTPS proxy. The port must be within `[service.proxy].allowed_ports`;
    the resulting proxy target is not public until `PUT .../ports/{port}/public` is also called on the
    primary port.

    Returns **422** `port_not_allowed` when the port is outside the configured allowlist — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the offending port)
    and `allowed` (the configured allowlist). A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        body (AddPortRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody]
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
    body: AddPortRequest,
) -> Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody | None:
    """Expose a guest port through the HTTPS proxy

     Registers a guest port for the HTTPS proxy. The port must be within `[service.proxy].allowed_ports`;
    the resulting proxy target is not public until `PUT .../ports/{port}/public` is also called on the
    primary port.

    Returns **422** `port_not_allowed` when the port is outside the configured allowlist — the body is
    an `ApiError` envelope with two extra fields not modeled in the schema: `port` (the offending port)
    and `allowed` (the configured allowlist). A VM that does not exist, or is not visible to the caller,
    returns 404 (existence non-leak).

    Args:
        name (str):
        body (AddPortRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PortNotAllowedBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
