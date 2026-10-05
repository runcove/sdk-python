from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.port_not_allowed_body import PortNotAllowedBody
from ...models.put_primary_port_body import PutPrimaryPortBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: PutPrimaryPortBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/vms/{name}/primary-port".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | PortNotAllowedBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = PortNotAllowedBody.from_dict(response.json())

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
) -> Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody]:
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
    body: PutPrimaryPortBody,
) -> Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody]:
    """Switch a VM's primary port

     Changes which registered port is the VM's primary port. The primary port is the one that renders the
    portless URL (`<vm>.<base>/`) and the only port eligible to be made public (`setVmPortPublic`);
    switching primary demotes the old one's `public` flag to `false` and re-issues both ports' Warpgate
    targets so their external URL shape flips.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports` — the
    body is `PortNotAllowedBody`, carrying `port` / `allowed` alongside `code`. A VM that does not
    exist, or is not visible to the caller, returns 404 (existence non-leak).

    Not served on the external bearer-key listener — see `x-listeners` — so this operation carries no
    `x-required-scope`.

    Args:
        name (str):
        body (PutPrimaryPortBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody]
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
    body: PutPrimaryPortBody,
) -> Any | ApiError | CliTooOldBody | PortNotAllowedBody | None:
    """Switch a VM's primary port

     Changes which registered port is the VM's primary port. The primary port is the one that renders the
    portless URL (`<vm>.<base>/`) and the only port eligible to be made public (`setVmPortPublic`);
    switching primary demotes the old one's `public` flag to `false` and re-issues both ports' Warpgate
    targets so their external URL shape flips.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports` — the
    body is `PortNotAllowedBody`, carrying `port` / `allowed` alongside `code`. A VM that does not
    exist, or is not visible to the caller, returns 404 (existence non-leak).

    Not served on the external bearer-key listener — see `x-listeners` — so this operation carries no
    `x-required-scope`.

    Args:
        name (str):
        body (PutPrimaryPortBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PortNotAllowedBody
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
    body: PutPrimaryPortBody,
) -> Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody]:
    """Switch a VM's primary port

     Changes which registered port is the VM's primary port. The primary port is the one that renders the
    portless URL (`<vm>.<base>/`) and the only port eligible to be made public (`setVmPortPublic`);
    switching primary demotes the old one's `public` flag to `false` and re-issues both ports' Warpgate
    targets so their external URL shape flips.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports` — the
    body is `PortNotAllowedBody`, carrying `port` / `allowed` alongside `code`. A VM that does not
    exist, or is not visible to the caller, returns 404 (existence non-leak).

    Not served on the external bearer-key listener — see `x-listeners` — so this operation carries no
    `x-required-scope`.

    Args:
        name (str):
        body (PutPrimaryPortBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | PortNotAllowedBody]
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
    body: PutPrimaryPortBody,
) -> Any | ApiError | CliTooOldBody | PortNotAllowedBody | None:
    """Switch a VM's primary port

     Changes which registered port is the VM's primary port. The primary port is the one that renders the
    portless URL (`<vm>.<base>/`) and the only port eligible to be made public (`setVmPortPublic`);
    switching primary demotes the old one's `public` flag to `false` and re-issues both ports' Warpgate
    targets so their external URL shape flips.

    Returns **422** `port_not_allowed` when the port is outside `[service.proxy].allowed_ports` — the
    body is `PortNotAllowedBody`, carrying `port` / `allowed` alongside `code`. A VM that does not
    exist, or is not visible to the caller, returns 404 (existence non-leak).

    Not served on the external bearer-key listener — see `x-listeners` — so this operation carries no
    `x-required-scope`.

    Args:
        name (str):
        body (PutPrimaryPortBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | PortNotAllowedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
