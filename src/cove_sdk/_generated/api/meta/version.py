from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.build_info import BuildInfo
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/version",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | BuildInfo | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = BuildInfo.from_dict(response.json())

        return response_200

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
) -> Response[ApiError | BuildInfo | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ApiError | BuildInfo | CliTooOldBody]:
    """Server build info (anonymous)

     Anonymous build metadata for the running server binary: name, semver, commit, build timestamp, and
    the API/protocol versions it negotiates over `X-Cove-Api-Version`. `cove version`'s client/server
    compatibility check reads this.

    Root `GET /version` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/version` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | BuildInfo | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> ApiError | BuildInfo | CliTooOldBody | None:
    """Server build info (anonymous)

     Anonymous build metadata for the running server binary: name, semver, commit, build timestamp, and
    the API/protocol versions it negotiates over `X-Cove-Api-Version`. `cove version`'s client/server
    compatibility check reads this.

    Root `GET /version` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/version` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | BuildInfo | CliTooOldBody
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ApiError | BuildInfo | CliTooOldBody]:
    """Server build info (anonymous)

     Anonymous build metadata for the running server binary: name, semver, commit, build timestamp, and
    the API/protocol versions it negotiates over `X-Cove-Api-Version`. `cove version`'s client/server
    compatibility check reads this.

    Root `GET /version` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/version` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | BuildInfo | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> ApiError | BuildInfo | CliTooOldBody | None:
    """Server build info (anonymous)

     Anonymous build metadata for the running server binary: name, semver, commit, build timestamp, and
    the API/protocol versions it negotiates over `X-Cove-Api-Version`. `cove version`'s client/server
    compatibility check reads this.

    Root `GET /version` (no `/api` prefix) answers the identical handler on every listener, for
    infrastructure that cannot be pointed at a prefixed path — it carries no public description (see the
    exclusion list in `crate::openapi`). This `/api/version` operation is the described one, and it is
    reachable only on the external bearer-key listener: the Unix-socket and Warpgate-fronted listeners
    serve this same handler only at the unprefixed root path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | BuildInfo | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
