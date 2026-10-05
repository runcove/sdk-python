from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_status_response import CliStatusResponse
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/me/cli-status",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliStatusResponse | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = CliStatusResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliStatusResponse | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliStatusResponse | CliTooOldBody]:
    """CLI setup status for the caller

     Whether the caller already holds an active CLI session ticket, and the install URL for the `cove`
    binary if the server is configured to serve one (`[cli_releases] public_url`). Backs the browser's
    "install the CLI" nudge.

    Carries **no** `x-required-scope`: the only data returned is about the caller's own session, so it
    is own-data. `scope_table::lookup` maps every GET under `/api/me` to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliStatusResponse | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliStatusResponse | CliTooOldBody | None:
    """CLI setup status for the caller

     Whether the caller already holds an active CLI session ticket, and the install URL for the `cove`
    binary if the server is configured to serve one (`[cli_releases] public_url`). Backs the browser's
    "install the CLI" nudge.

    Carries **no** `x-required-scope`: the only data returned is about the caller's own session, so it
    is own-data. `scope_table::lookup` maps every GET under `/api/me` to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliStatusResponse | CliTooOldBody
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliStatusResponse | CliTooOldBody]:
    """CLI setup status for the caller

     Whether the caller already holds an active CLI session ticket, and the install URL for the `cove`
    binary if the server is configured to serve one (`[cli_releases] public_url`). Backs the browser's
    "install the CLI" nudge.

    Carries **no** `x-required-scope`: the only data returned is about the caller's own session, so it
    is own-data. `scope_table::lookup` maps every GET under `/api/me` to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliStatusResponse | CliTooOldBody]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliStatusResponse | CliTooOldBody | None:
    """CLI setup status for the caller

     Whether the caller already holds an active CLI session ticket, and the install URL for the `cove`
    binary if the server is configured to serve one (`[cli_releases] public_url`). Backs the browser's
    "install the CLI" nudge.

    Carries **no** `x-required-scope`: the only data returned is about the caller's own session, so it
    is own-data. `scope_table::lookup` maps every GET under `/api/me` to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliStatusResponse | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
