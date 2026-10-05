from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.webhook_subscription import WebhookSubscription
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    scope: str | Unset = UNSET,
    vm_id: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["scope"] = scope

    params["vm_id"] = vm_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/webhooks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WebhookSubscription.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    scope: str | Unset = UNSET,
    vm_id: str | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]]:
    """List webhook subscriptions

     Returns the caller's own subscriptions; an admin caller sees every subscription on the server.
    `secret` is always null in this response.

    Args:
        scope (str | Unset):
        vm_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]]
    """

    kwargs = _get_kwargs(
        scope=scope,
        vm_id=vm_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    scope: str | Unset = UNSET,
    vm_id: str | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription] | None:
    """List webhook subscriptions

     Returns the caller's own subscriptions; an admin caller sees every subscription on the server.
    `secret` is always null in this response.

    Args:
        scope (str | Unset):
        vm_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]
    """

    return sync_detailed(
        client=client,
        scope=scope,
        vm_id=vm_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    scope: str | Unset = UNSET,
    vm_id: str | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]]:
    """List webhook subscriptions

     Returns the caller's own subscriptions; an admin caller sees every subscription on the server.
    `secret` is always null in this response.

    Args:
        scope (str | Unset):
        vm_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]]
    """

    kwargs = _get_kwargs(
        scope=scope,
        vm_id=vm_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    scope: str | Unset = UNSET,
    vm_id: str | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription] | None:
    """List webhook subscriptions

     Returns the caller's own subscriptions; an admin caller sees every subscription on the server.
    `secret` is always null in this response.

    Args:
        scope (str | Unset):
        vm_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[WebhookSubscription]
    """

    return (
        await asyncio_detailed(
            client=client,
            scope=scope,
            vm_id=vm_id,
        )
    ).parsed
