from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.grant_share_outcome import GrantShareOutcome
from ...models.grant_share_request import GrantShareRequest
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: GrantShareRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/access".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody | None:
    if response.status_code == 201:
        response_201 = GrantShareOutcome.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: GrantShareRequest,
) -> Response[ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody]:
    """Grant a user or team access to a VM

     Grants a share (owner/admin only — the service op gates on `VmShare`, held by no grantable role). A
    non-permitted caller gets the same 404 as a missing VM (existence-leak guard).

    Returns 201 + `user_known`: `false` when the sharee has no Warpgate account yet (the grant still
    succeeds; access applies on their first SSO login).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        body (GrantShareRequest): Wire body for `POST /vms/{name}/access`.

            Mirrors `cove_api_client::wire_types::GrantShareRequest`: a
            `subject_type` discriminator ("user" | "team"),
            the `subject_id` (username), and the `role` token ("user" |
            "collaborator"). The handler parses + validates before delegating to
            the service op so a malformed body surfaces as 400, not a service
            `Validation` 422 — keeps the contract uniform with other cove
            handlers that validate the wire shape at the edge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: GrantShareRequest,
) -> ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody | None:
    """Grant a user or team access to a VM

     Grants a share (owner/admin only — the service op gates on `VmShare`, held by no grantable role). A
    non-permitted caller gets the same 404 as a missing VM (existence-leak guard).

    Returns 201 + `user_known`: `false` when the sharee has no Warpgate account yet (the grant still
    succeeds; access applies on their first SSO login).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        body (GrantShareRequest): Wire body for `POST /vms/{name}/access`.

            Mirrors `cove_api_client::wire_types::GrantShareRequest`: a
            `subject_type` discriminator ("user" | "team"),
            the `subject_id` (username), and the `role` token ("user" |
            "collaborator"). The handler parses + validates before delegating to
            the service op so a malformed body surfaces as 400, not a service
            `Validation` 422 — keeps the contract uniform with other cove
            handlers that validate the wire shape at the edge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: GrantShareRequest,
) -> Response[ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody]:
    """Grant a user or team access to a VM

     Grants a share (owner/admin only — the service op gates on `VmShare`, held by no grantable role). A
    non-permitted caller gets the same 404 as a missing VM (existence-leak guard).

    Returns 201 + `user_known`: `false` when the sharee has no Warpgate account yet (the grant still
    succeeds; access applies on their first SSO login).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        body (GrantShareRequest): Wire body for `POST /vms/{name}/access`.

            Mirrors `cove_api_client::wire_types::GrantShareRequest`: a
            `subject_type` discriminator ("user" | "team"),
            the `subject_id` (username), and the `role` token ("user" |
            "collaborator"). The handler parses + validates before delegating to
            the service op so a malformed body surfaces as 400, not a service
            `Validation` 422 — keeps the contract uniform with other cove
            handlers that validate the wire shape at the edge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: GrantShareRequest,
) -> ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody | None:
    """Grant a user or team access to a VM

     Grants a share (owner/admin only — the service op gates on `VmShare`, held by no grantable role). A
    non-permitted caller gets the same 404 as a missing VM (existence-leak guard).

    Returns 201 + `user_known`: `false` when the sharee has no Warpgate account yet (the grant still
    succeeds; access applies on their first SSO login).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        body (GrantShareRequest): Wire body for `POST /vms/{name}/access`.

            Mirrors `cove_api_client::wire_types::GrantShareRequest`: a
            `subject_type` discriminator ("user" | "team"),
            the `subject_id` (username), and the `role` token ("user" |
            "collaborator"). The handler parses + validates before delegating to
            the service op so a malformed body surfaces as 400, not a service
            `Validation` 422 — keeps the contract uniform with other cove
            handlers that validate the wire shape at the edge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | GrantShareOutcome | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
