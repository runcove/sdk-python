from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.sudo_required_body import SudoRequiredBody
from ...models.webhook_create_input import WebhookCreateInput
from ...models.webhook_subscription import WebhookSubscription
from ...types import Response


def _get_kwargs(
    *,
    body: WebhookCreateInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/webhooks",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription | None:
    if response.status_code == 201:
        response_201 = WebhookSubscription.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:

        def _parse_response_401(data: object) -> ApiError | SudoRequiredBody:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_sensitive_op_unauthorized_response_type_0 = (
                    ApiError.from_dict(data)
                )

                return componentsschemas_sensitive_op_unauthorized_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_sensitive_op_unauthorized_response_type_1 = (
                SudoRequiredBody.from_dict(data)
            )

            return componentsschemas_sensitive_op_unauthorized_response_type_1

        response_401 = _parse_response_401(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

        return response_422

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: WebhookCreateInput,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]:
    """Create a webhook subscription

     The `secret` (`whsec_<64 hex>`) is returned exactly once, in this response — capture it now. There
    is no way to retrieve it again afterwards; losing it means rotating (`POST
    /api/webhooks/{id}/rotate`) to mint a new one. `events` entries must exact-match a dispatched event
    kind (e.g. `vm.stopped`); `keys.*` kinds are rejected with 422. A server-wide subscription
    (`scope=server`) receives every user's events, so it is admin-only; anyone else subscribes per VM
    (`scope=vm`) to a VM they own.

    Args:
        body (WebhookCreateInput): Input for creating a new webhook subscription (`POST
            /api/webhooks`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: WebhookCreateInput,
) -> ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription | None:
    """Create a webhook subscription

     The `secret` (`whsec_<64 hex>`) is returned exactly once, in this response — capture it now. There
    is no way to retrieve it again afterwards; losing it means rotating (`POST
    /api/webhooks/{id}/rotate`) to mint a new one. `events` entries must exact-match a dispatched event
    kind (e.g. `vm.stopped`); `keys.*` kinds are rejected with 422. A server-wide subscription
    (`scope=server`) receives every user's events, so it is admin-only; anyone else subscribes per VM
    (`scope=vm`) to a VM they own.

    Args:
        body (WebhookCreateInput): Input for creating a new webhook subscription (`POST
            /api/webhooks`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: WebhookCreateInput,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]:
    """Create a webhook subscription

     The `secret` (`whsec_<64 hex>`) is returned exactly once, in this response — capture it now. There
    is no way to retrieve it again afterwards; losing it means rotating (`POST
    /api/webhooks/{id}/rotate`) to mint a new one. `events` entries must exact-match a dispatched event
    kind (e.g. `vm.stopped`); `keys.*` kinds are rejected with 422. A server-wide subscription
    (`scope=server`) receives every user's events, so it is admin-only; anyone else subscribes per VM
    (`scope=vm`) to a VM they own.

    Args:
        body (WebhookCreateInput): Input for creating a new webhook subscription (`POST
            /api/webhooks`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: WebhookCreateInput,
) -> ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription | None:
    """Create a webhook subscription

     The `secret` (`whsec_<64 hex>`) is returned exactly once, in this response — capture it now. There
    is no way to retrieve it again afterwards; losing it means rotating (`POST
    /api/webhooks/{id}/rotate`) to mint a new one. `events` entries must exact-match a dispatched event
    kind (e.g. `vm.stopped`); `keys.*` kinds are rejected with 422. A server-wide subscription
    (`scope=server`) receives every user's events, so it is admin-only; anyone else subscribes per VM
    (`scope=vm`) to a VM they own.

    Args:
        body (WebhookCreateInput): Input for creating a new webhook subscription (`POST
            /api/webhooks`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
