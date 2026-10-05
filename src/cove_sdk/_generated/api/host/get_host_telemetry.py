from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.host_telemetry_series import HostTelemetrySeries
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
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
        "url": "/api/host/telemetry",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = HostTelemetrySeries.from_dict(response.json())

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

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody]:
    """Host telemetry time series

     Bucketed host-wide CPU/memory/pool/reservation samples over a time window. Same query envelope and
    defaults as `GET /api/vms/{name}/telemetry` — see that operation's parameter descriptions.

    Args:
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody | None:
    """Host telemetry time series

     Bucketed host-wide CPU/memory/pool/reservation samples over a time window. Same query envelope and
    defaults as `GET /api/vms/{name}/telemetry` — see that operation's parameter descriptions.

    Args:
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody
    """

    return sync_detailed(
        client=client,
        from_=from_,
        to=to,
        step=step,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody]:
    """Host telemetry time series

     Bucketed host-wide CPU/memory/pool/reservation samples over a time window. Same query envelope and
    defaults as `GET /api/vms/{name}/telemetry` — see that operation's parameter descriptions.

    Args:
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        step=step,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    from_: int | Unset = UNSET,
    to: int | Unset = UNSET,
    step: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody | None:
    """Host telemetry time series

     Bucketed host-wide CPU/memory/pool/reservation samples over a time window. Same query envelope and
    defaults as `GET /api/vms/{name}/telemetry` — see that operation's parameter descriptions.

    Args:
        from_ (int | Unset):
        to (int | Unset):
        step (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | HostTelemetrySeries | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            to=to,
            step=step,
            limit=limit,
        )
    ).parsed
