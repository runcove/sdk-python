from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.sudo_required_body import SudoRequiredBody
from ...models.webhook_subscription import WebhookSubscription
from ...models.webhook_update_input import WebhookUpdateInput
from ...types import Response


def _get_kwargs(
    id: UUID,
    *,
    body: WebhookUpdateInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/webhooks/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription | None:
    if response.status_code == 200:
        response_200 = WebhookSubscription.from_dict(response.json())

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
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: WebhookUpdateInput,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]:
    """Update a webhook subscription (partial)

     Omitted fields are left unchanged. For `tag_filter`, `allowed_subnets` and `description`, an
    explicit JSON `null` is indistinguishable from omission — there is no wire-level way to clear these
    fields.

    Args:
        id (UUID):
        body (WebhookUpdateInput): Input for updating an existing subscription (`PUT
            /api/webhooks/{id}`).

            All fields are optional — only provided fields are updated. For
            `tag_filter`, `allowed_subnets` and `description`, an explicit JSON `null`
            is indistinguishable from omission on the wire, hence the `Option<Option<
            _>>` — the outer `Option` is "was this key present at all", checked by
            `serde`'s default-on-missing-field behaviour, not by any wire-visible
            distinction from an inner `null`. The published schema (`#[schema(value_type
            = ...)]` below) flattens that internal detail to a plain nullable field,
            same as every other optional field here — the request body can't express
            "clear this field" any more precisely than that, so the schema shouldn't
            claim it can.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: WebhookUpdateInput,
) -> ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription | None:
    """Update a webhook subscription (partial)

     Omitted fields are left unchanged. For `tag_filter`, `allowed_subnets` and `description`, an
    explicit JSON `null` is indistinguishable from omission — there is no wire-level way to clear these
    fields.

    Args:
        id (UUID):
        body (WebhookUpdateInput): Input for updating an existing subscription (`PUT
            /api/webhooks/{id}`).

            All fields are optional — only provided fields are updated. For
            `tag_filter`, `allowed_subnets` and `description`, an explicit JSON `null`
            is indistinguishable from omission on the wire, hence the `Option<Option<
            _>>` — the outer `Option` is "was this key present at all", checked by
            `serde`'s default-on-missing-field behaviour, not by any wire-visible
            distinction from an inner `null`. The published schema (`#[schema(value_type
            = ...)]` below) flattens that internal detail to a plain nullable field,
            same as every other optional field here — the request body can't express
            "clear this field" any more precisely than that, so the schema shouldn't
            claim it can.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: WebhookUpdateInput,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]:
    """Update a webhook subscription (partial)

     Omitted fields are left unchanged. For `tag_filter`, `allowed_subnets` and `description`, an
    explicit JSON `null` is indistinguishable from omission — there is no wire-level way to clear these
    fields.

    Args:
        id (UUID):
        body (WebhookUpdateInput): Input for updating an existing subscription (`PUT
            /api/webhooks/{id}`).

            All fields are optional — only provided fields are updated. For
            `tag_filter`, `allowed_subnets` and `description`, an explicit JSON `null`
            is indistinguishable from omission on the wire, hence the `Option<Option<
            _>>` — the outer `Option` is "was this key present at all", checked by
            `serde`'s default-on-missing-field behaviour, not by any wire-visible
            distinction from an inner `null`. The published schema (`#[schema(value_type
            = ...)]` below) flattens that internal detail to a plain nullable field,
            same as every other optional field here — the request body can't express
            "clear this field" any more precisely than that, so the schema shouldn't
            claim it can.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: WebhookUpdateInput,
) -> ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription | None:
    """Update a webhook subscription (partial)

     Omitted fields are left unchanged. For `tag_filter`, `allowed_subnets` and `description`, an
    explicit JSON `null` is indistinguishable from omission — there is no wire-level way to clear these
    fields.

    Args:
        id (UUID):
        body (WebhookUpdateInput): Input for updating an existing subscription (`PUT
            /api/webhooks/{id}`).

            All fields are optional — only provided fields are updated. For
            `tag_filter`, `allowed_subnets` and `description`, an explicit JSON `null`
            is indistinguishable from omission on the wire, hence the `Option<Option<
            _>>` — the outer `Option` is "was this key present at all", checked by
            `serde`'s default-on-missing-field behaviour, not by any wire-visible
            distinction from an inner `null`. The published schema (`#[schema(value_type
            = ...)]` below) flattens that internal detail to a plain nullable field,
            same as every other optional field here — the request body can't express
            "clear this field" any more precisely than that, so the schema shouldn't
            claim it can.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | WebhookSubscription
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
