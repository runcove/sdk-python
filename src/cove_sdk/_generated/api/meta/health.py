from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cli_too_old_body import CliTooOldBody
from ...models.health_response import HealthResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/health",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CliTooOldBody | HealthResponse | None:
    if response.status_code == 200:
        response_200 = HealthResponse.from_dict(response.json())

        return response_200

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CliTooOldBody | HealthResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CliTooOldBody | HealthResponse]:
    """Health probe (anonymous)

     Anonymous liveness probe: current VM counts, pool availability, uptime, and build/version metadata.
    Load balancers and `cove version`'s server probe use this to confirm the daemon is up and to read
    `min_cli_version` / `api_version` for compatibility.

    `traffic_monitor` says whether auto-pause is configured and whether the traffic monitor it depends
    on is running. The daemon starts even when that monitor fails to load, so deploy checks fail on
    `auto_pause_enabled: true` with any `state` other than `loaded`. Servers that predate the field omit
    it.

    Root `GET /health` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/health` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CliTooOldBody | HealthResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> CliTooOldBody | HealthResponse | None:
    """Health probe (anonymous)

     Anonymous liveness probe: current VM counts, pool availability, uptime, and build/version metadata.
    Load balancers and `cove version`'s server probe use this to confirm the daemon is up and to read
    `min_cli_version` / `api_version` for compatibility.

    `traffic_monitor` says whether auto-pause is configured and whether the traffic monitor it depends
    on is running. The daemon starts even when that monitor fails to load, so deploy checks fail on
    `auto_pause_enabled: true` with any `state` other than `loaded`. Servers that predate the field omit
    it.

    Root `GET /health` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/health` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CliTooOldBody | HealthResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CliTooOldBody | HealthResponse]:
    """Health probe (anonymous)

     Anonymous liveness probe: current VM counts, pool availability, uptime, and build/version metadata.
    Load balancers and `cove version`'s server probe use this to confirm the daemon is up and to read
    `min_cli_version` / `api_version` for compatibility.

    `traffic_monitor` says whether auto-pause is configured and whether the traffic monitor it depends
    on is running. The daemon starts even when that monitor fails to load, so deploy checks fail on
    `auto_pause_enabled: true` with any `state` other than `loaded`. Servers that predate the field omit
    it.

    Root `GET /health` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/health` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CliTooOldBody | HealthResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> CliTooOldBody | HealthResponse | None:
    """Health probe (anonymous)

     Anonymous liveness probe: current VM counts, pool availability, uptime, and build/version metadata.
    Load balancers and `cove version`'s server probe use this to confirm the daemon is up and to read
    `min_cli_version` / `api_version` for compatibility.

    `traffic_monitor` says whether auto-pause is configured and whether the traffic monitor it depends
    on is running. The daemon starts even when that monitor fails to load, so deploy checks fail on
    `auto_pause_enabled: true` with any `state` other than `loaded`. Servers that predate the field omit
    it.

    Root `GET /health` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/health` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CliTooOldBody | HealthResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
