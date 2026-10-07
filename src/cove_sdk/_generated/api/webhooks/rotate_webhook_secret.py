from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.rotate_webhook_secret_response import RotateWebhookSecretResponse
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/webhooks/{id}/rotate".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | RotateWebhookSecretResponse
    | ScopeDeniedBody
    | None
):
    if response.status_code == 200:
        response_200 = RotateWebhookSecretResponse.from_dict(response.json())

        return response_200

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
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
) -> Response[
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | RotateWebhookSecretResponse
    | ScopeDeniedBody
]:
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
) -> Response[
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | RotateWebhookSecretResponse
    | ScopeDeniedBody
]:
    """Rotate the signing secret

     Mints a fresh HMAC secret and starts the configured dual-signing grace window (`[webhooks]
    secret_rotation_grace_seconds`, default 24h): during grace, deliveries are signed with BOTH the old
    and new secret (space-separated `v1,<hex>` entries in the `Cove-Signature` header) so a receiver
    mid-rollout can accept either. The new secret is returned exactly once, in this response — capture
    it now; it cannot be retrieved again afterwards.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateWebhookSecretResponse | ScopeDeniedBody]
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
) -> (
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | RotateWebhookSecretResponse
    | ScopeDeniedBody
    | None
):
    """Rotate the signing secret

     Mints a fresh HMAC secret and starts the configured dual-signing grace window (`[webhooks]
    secret_rotation_grace_seconds`, default 24h): during grace, deliveries are signed with BOTH the old
    and new secret (space-separated `v1,<hex>` entries in the `Cove-Signature` header) so a receiver
    mid-rollout can accept either. The new secret is returned exactly once, in this response — capture
    it now; it cannot be retrieved again afterwards.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateWebhookSecretResponse | ScopeDeniedBody
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | RotateWebhookSecretResponse
    | ScopeDeniedBody
]:
    """Rotate the signing secret

     Mints a fresh HMAC secret and starts the configured dual-signing grace window (`[webhooks]
    secret_rotation_grace_seconds`, default 24h): during grace, deliveries are signed with BOTH the old
    and new secret (space-separated `v1,<hex>` entries in the `Cove-Signature` header) so a receiver
    mid-rollout can accept either. The new secret is returned exactly once, in this response — capture
    it now; it cannot be retrieved again afterwards.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateWebhookSecretResponse | ScopeDeniedBody]
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
) -> (
    ApiError
    | SudoRequiredBody
    | CliTooOldBody
    | RotateWebhookSecretResponse
    | ScopeDeniedBody
    | None
):
    """Rotate the signing secret

     Mints a fresh HMAC secret and starts the configured dual-signing grace window (`[webhooks]
    secret_rotation_grace_seconds`, default 24h): during grace, deliveries are signed with BOTH the old
    and new secret (space-separated `v1,<hex>` entries in the `Cove-Signature` header) so a receiver
    mid-rollout can accept either. The new secret is returned exactly once, in this response — capture
    it now; it cannot be retrieved again afterwards.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateWebhookSecretResponse | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
