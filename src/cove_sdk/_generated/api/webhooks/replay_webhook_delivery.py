from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.replay_webhook_delivery_response import ReplayWebhookDeliveryResponse
from ...types import Response


def _get_kwargs(
    id: UUID,
    delivery_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/webhooks/{id}/deliveries/{delivery_id}/replay".format(
            id=quote(str(id), safe=""),
            delivery_id=quote(str(delivery_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse | None:
    if response.status_code == 202:
        response_202 = ReplayWebhookDeliveryResponse.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    delivery_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse]:
    """Replay a delivery

     Re-enqueues the event for delivery under a fresh `delivery_id`, preserving the original `ce_id` so
    the receiver's idempotency key is stable across the replay. A server-wide subscription is admin-
    only, so its deliveries can be replayed only by an administrator, and only while its owner is one.

    Args:
        id (UUID):
        delivery_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        delivery_id=delivery_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    delivery_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse | None:
    """Replay a delivery

     Re-enqueues the event for delivery under a fresh `delivery_id`, preserving the original `ce_id` so
    the receiver's idempotency key is stable across the replay. A server-wide subscription is admin-
    only, so its deliveries can be replayed only by an administrator, and only while its owner is one.

    Args:
        id (UUID):
        delivery_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse
    """

    return sync_detailed(
        id=id,
        delivery_id=delivery_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    delivery_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse]:
    """Replay a delivery

     Re-enqueues the event for delivery under a fresh `delivery_id`, preserving the original `ce_id` so
    the receiver's idempotency key is stable across the replay. A server-wide subscription is admin-
    only, so its deliveries can be replayed only by an administrator, and only while its owner is one.

    Args:
        id (UUID):
        delivery_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        delivery_id=delivery_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    delivery_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse | None:
    """Replay a delivery

     Re-enqueues the event for delivery under a fresh `delivery_id`, preserving the original `ce_id` so
    the receiver's idempotency key is stable across the replay. A server-wide subscription is admin-
    only, so its deliveries can be replayed only by an administrator, and only while its owner is one.

    Args:
        id (UUID):
        delivery_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ReplayWebhookDeliveryResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            delivery_id=delivery_id,
            client=client,
        )
    ).parsed
