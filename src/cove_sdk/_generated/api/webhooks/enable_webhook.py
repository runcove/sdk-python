from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.webhook_subscription import WebhookSubscription
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/webhooks/{id}/enable".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | WebhookSubscription | None:
    if response.status_code == 200:
        response_200 = WebhookSubscription.from_dict(response.json())

        return response_200

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
) -> Response[ApiError | CliTooOldBody | WebhookSubscription]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | WebhookSubscription]:
    """Re-enable a subscription

     Re-enables a subscription (whether disabled by an operator or by the outbox's auto-disable) and
    resets `consec_fail_count` to zero, so the next single failure does not immediately re-trip auto-
    disable. Emits a `webhook.enabled` audit-log row. A server-wide subscription is admin-only, so one
    the daemon disabled because its owner is not an administrator (`disabled_reason`
    `server_scope_admin_only`) cannot be re-enabled.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | WebhookSubscription]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | WebhookSubscription | None:
    """Re-enable a subscription

     Re-enables a subscription (whether disabled by an operator or by the outbox's auto-disable) and
    resets `consec_fail_count` to zero, so the next single failure does not immediately re-trip auto-
    disable. Emits a `webhook.enabled` audit-log row. A server-wide subscription is admin-only, so one
    the daemon disabled because its owner is not an administrator (`disabled_reason`
    `server_scope_admin_only`) cannot be re-enabled.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | WebhookSubscription
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | WebhookSubscription]:
    """Re-enable a subscription

     Re-enables a subscription (whether disabled by an operator or by the outbox's auto-disable) and
    resets `consec_fail_count` to zero, so the next single failure does not immediately re-trip auto-
    disable. Emits a `webhook.enabled` audit-log row. A server-wide subscription is admin-only, so one
    the daemon disabled because its owner is not an administrator (`disabled_reason`
    `server_scope_admin_only`) cannot be re-enabled.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | WebhookSubscription]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | WebhookSubscription | None:
    """Re-enable a subscription

     Re-enables a subscription (whether disabled by an operator or by the outbox's auto-disable) and
    resets `consec_fail_count` to zero, so the next single failure does not immediately re-trip auto-
    disable. Emits a `webhook.enabled` audit-log row. A server-wide subscription is admin-only, so one
    the daemon disabled because its owner is not an administrator (`disabled_reason`
    `server_scope_admin_only`) cannot be re-enabled.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | WebhookSubscription
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
