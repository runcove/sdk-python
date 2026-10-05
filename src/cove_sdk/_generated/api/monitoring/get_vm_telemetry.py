from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.vm_telemetry_series import VmTelemetrySeries
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["from"] = from_

    params["to"] = to

    params["step"] = step

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/vms/{name}/telemetry".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries | None:
    if response.status_code == 200:
        response_200 = VmTelemetrySeries.from_dict(response.json())

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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries]:
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
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries]:
    """Per-VM telemetry time series

     Bucketed CPU/memory/disk/network samples for one VM over a time window. All four query parameters
    are optional: defaults to the last 24 hours in 60-second buckets, capped at 1000 points (5000 max).
    `from` after `to` is accepted and returns an empty series rather than an error.

    Args:
        name (str):
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries]
    """

    kwargs = _get_kwargs(
        name=name,
        from_=from_,
        to=to,
        step=step,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries | None:
    """Per-VM telemetry time series

     Bucketed CPU/memory/disk/network samples for one VM over a time window. All four query parameters
    are optional: defaults to the last 24 hours in 60-second buckets, capped at 1000 points (5000 max).
    `from` after `to` is accepted and returns an empty series rather than an error.

    Args:
        name (str):
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries
    """

    return sync_detailed(
        name=name,
        client=client,
        from_=from_,
        to=to,
        step=step,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries]:
    """Per-VM telemetry time series

     Bucketed CPU/memory/disk/network samples for one VM over a time window. All four query parameters
    are optional: defaults to the last 24 hours in 60-second buckets, capped at 1000 points (5000 max).
    `from` after `to` is accepted and returns an empty series rather than an error.

    Args:
        name (str):
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries]
    """

    kwargs = _get_kwargs(
        name=name,
        from_=from_,
        to=to,
        step=step,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries | None:
    """Per-VM telemetry time series

     Bucketed CPU/memory/disk/network samples for one VM over a time window. All four query parameters
    are optional: defaults to the last 24 hours in 60-second buckets, capped at 1000 points (5000 max).
    `from` after `to` is accepted and returns an empty series rather than an error.

    Args:
        name (str):
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | VmTelemetrySeries
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            from_=from_,
            to=to,
            step=step,
            limit=limit,
        )
    ).parsed
