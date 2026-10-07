from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.connected_app_summary import ConnectedAppSummary
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/me/connected-apps",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | list[ConnectedAppSummary] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ConnectedAppSummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

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
) -> Response[ApiError | CliTooOldBody | list[ConnectedAppSummary]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[ConnectedAppSummary]]:
    """Caller's connected apps

     The MCP clients (for example claude.ai) the caller has signed in to Cove through and not revoked,
    newest first. Each one's actions appear in the audit log with `actor_source` `connected_app` and
    `actor_key_id` the app's `id`.

    Carries **no** `x-required-scope`, same own-data reasoning as `GET /api/me`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[ConnectedAppSummary]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[ConnectedAppSummary] | None:
    """Caller's connected apps

     The MCP clients (for example claude.ai) the caller has signed in to Cove through and not revoked,
    newest first. Each one's actions appear in the audit log with `actor_source` `connected_app` and
    `actor_key_id` the app's `id`.

    Carries **no** `x-required-scope`, same own-data reasoning as `GET /api/me`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[ConnectedAppSummary]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[ConnectedAppSummary]]:
    """Caller's connected apps

     The MCP clients (for example claude.ai) the caller has signed in to Cove through and not revoked,
    newest first. Each one's actions appear in the audit log with `actor_source` `connected_app` and
    `actor_key_id` the app's `id`.

    Carries **no** `x-required-scope`, same own-data reasoning as `GET /api/me`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[ConnectedAppSummary]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[ConnectedAppSummary] | None:
    """Caller's connected apps

     The MCP clients (for example claude.ai) the caller has signed in to Cove through and not revoked,
    newest first. Each one's actions appear in the audit log with `actor_source` `connected_app` and
    `actor_key_id` the app's `id`.

    Carries **no** `x-required-scope`, same own-data reasoning as `GET /api/me`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[ConnectedAppSummary]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
