from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.create_key_request import CreateKeyRequest
from ...models.created_key import CreatedKey
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    *,
    body: CreateKeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/api-keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey | None:
    if response.status_code == 201:
        response_201 = CreatedKey.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]:
    """Create an API key

     The `raw_token` in the response is shown exactly once. Team keys (admin-only, `team` field set)
    require an expiry and cannot hold `keys:manage`, `admin`, or any `admin:*` scope.

    **Admin keys:** a key may hold `admin` or any `admin:*` permission only when `admin_key` is `true`
    (`cove key create --admin`), and such a key must expire within `[auth] admin_max_key_lifetime_days`
    (default 30). Only an admin key is ever an administrator at `/api/admin/*`. A team key is never an
    admin key. An admin key is minted (and rotated) only from a signed-in session: an API key caller,
    admin key or not, gets 403. An admin key can still mint ordinary keys.

    **Service keys:** `service` (with exactly one of `team` or `member`) mints a **service key**,
    `svc:<service>`: admin only, expiry required, never `keys:manage`, `access:write`, `admin` or
    `admin:*`, and never an admin key. `team` binds it to a team (its VMs count against the team's
    quota); `member` binds it to one person (its VMs count against theirs, and they control them). A
    name is bound once: re-minting it with a different binding, or after its binding ended, is refused.
    `member` without `service` is refused.

    **A key never outlives the API key minting it:** when the caller is an API key that expires, any key
    it mints (personal, team or service) expires no later than the caller does. A mint that leaves
    `expires_in_secs` out gets the caller's own expiry. A longer one is refused with 422
    `validation_failed`, `field: "expires_in_secs"`, never shortened silently. A caller key with no
    expiry adds no limit of its own, and a signed-in session is not affected.

    **422 validation failures (one shape):** the handler's own label/scopes/admin_key/expires_in_secs
    pre-checks, and `create_key`'s service-layer rules (team-key expiry and forbidden scopes; the admin-
    key expiry cap and a flag with no admin permission; the service-key rules: binding, expiry,
    forbidden scopes, name already bound, a pre-existing `svc:` row), both answer `{code:
    "validation_failed", message, field?}` — `field` names the offending request field when the failure
    is scoped to one (`label`, `scopes`, `admin_key`, `expires_in_secs`, `member`), and is absent for
    the other service-layer rules, which are cross-field. The one service-layer rule that names a field
    is the caller-lifetime rule above: `expires_in_secs`.

    Args:
        body (CreateKeyRequest): `POST /api/keys` request body.

            This is the ONE `CreateKeyRequest` that gets `ToSchema`. The
            server-side `cove_service::ops::keys::CreateKeyRequest` is a stale
            duplicate — `handlers::keys::create_key` deserializes THIS type (aliased
            `WireCKR`) and converts it to the service type itself; see the NOTE on
            that duplicate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]
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
    body: CreateKeyRequest,
) -> ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey | None:
    """Create an API key

     The `raw_token` in the response is shown exactly once. Team keys (admin-only, `team` field set)
    require an expiry and cannot hold `keys:manage`, `admin`, or any `admin:*` scope.

    **Admin keys:** a key may hold `admin` or any `admin:*` permission only when `admin_key` is `true`
    (`cove key create --admin`), and such a key must expire within `[auth] admin_max_key_lifetime_days`
    (default 30). Only an admin key is ever an administrator at `/api/admin/*`. A team key is never an
    admin key. An admin key is minted (and rotated) only from a signed-in session: an API key caller,
    admin key or not, gets 403. An admin key can still mint ordinary keys.

    **Service keys:** `service` (with exactly one of `team` or `member`) mints a **service key**,
    `svc:<service>`: admin only, expiry required, never `keys:manage`, `access:write`, `admin` or
    `admin:*`, and never an admin key. `team` binds it to a team (its VMs count against the team's
    quota); `member` binds it to one person (its VMs count against theirs, and they control them). A
    name is bound once: re-minting it with a different binding, or after its binding ended, is refused.
    `member` without `service` is refused.

    **A key never outlives the API key minting it:** when the caller is an API key that expires, any key
    it mints (personal, team or service) expires no later than the caller does. A mint that leaves
    `expires_in_secs` out gets the caller's own expiry. A longer one is refused with 422
    `validation_failed`, `field: "expires_in_secs"`, never shortened silently. A caller key with no
    expiry adds no limit of its own, and a signed-in session is not affected.

    **422 validation failures (one shape):** the handler's own label/scopes/admin_key/expires_in_secs
    pre-checks, and `create_key`'s service-layer rules (team-key expiry and forbidden scopes; the admin-
    key expiry cap and a flag with no admin permission; the service-key rules: binding, expiry,
    forbidden scopes, name already bound, a pre-existing `svc:` row), both answer `{code:
    "validation_failed", message, field?}` — `field` names the offending request field when the failure
    is scoped to one (`label`, `scopes`, `admin_key`, `expires_in_secs`, `member`), and is absent for
    the other service-layer rules, which are cross-field. The one service-layer rule that names a field
    is the caller-lifetime rule above: `expires_in_secs`.

    Args:
        body (CreateKeyRequest): `POST /api/keys` request body.

            This is the ONE `CreateKeyRequest` that gets `ToSchema`. The
            server-side `cove_service::ops::keys::CreateKeyRequest` is a stale
            duplicate — `handlers::keys::create_key` deserializes THIS type (aliased
            `WireCKR`) and converts it to the service type itself; see the NOTE on
            that duplicate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]:
    """Create an API key

     The `raw_token` in the response is shown exactly once. Team keys (admin-only, `team` field set)
    require an expiry and cannot hold `keys:manage`, `admin`, or any `admin:*` scope.

    **Admin keys:** a key may hold `admin` or any `admin:*` permission only when `admin_key` is `true`
    (`cove key create --admin`), and such a key must expire within `[auth] admin_max_key_lifetime_days`
    (default 30). Only an admin key is ever an administrator at `/api/admin/*`. A team key is never an
    admin key. An admin key is minted (and rotated) only from a signed-in session: an API key caller,
    admin key or not, gets 403. An admin key can still mint ordinary keys.

    **Service keys:** `service` (with exactly one of `team` or `member`) mints a **service key**,
    `svc:<service>`: admin only, expiry required, never `keys:manage`, `access:write`, `admin` or
    `admin:*`, and never an admin key. `team` binds it to a team (its VMs count against the team's
    quota); `member` binds it to one person (its VMs count against theirs, and they control them). A
    name is bound once: re-minting it with a different binding, or after its binding ended, is refused.
    `member` without `service` is refused.

    **A key never outlives the API key minting it:** when the caller is an API key that expires, any key
    it mints (personal, team or service) expires no later than the caller does. A mint that leaves
    `expires_in_secs` out gets the caller's own expiry. A longer one is refused with 422
    `validation_failed`, `field: "expires_in_secs"`, never shortened silently. A caller key with no
    expiry adds no limit of its own, and a signed-in session is not affected.

    **422 validation failures (one shape):** the handler's own label/scopes/admin_key/expires_in_secs
    pre-checks, and `create_key`'s service-layer rules (team-key expiry and forbidden scopes; the admin-
    key expiry cap and a flag with no admin permission; the service-key rules: binding, expiry,
    forbidden scopes, name already bound, a pre-existing `svc:` row), both answer `{code:
    "validation_failed", message, field?}` — `field` names the offending request field when the failure
    is scoped to one (`label`, `scopes`, `admin_key`, `expires_in_secs`, `member`), and is absent for
    the other service-layer rules, which are cross-field. The one service-layer rule that names a field
    is the caller-lifetime rule above: `expires_in_secs`.

    Args:
        body (CreateKeyRequest): `POST /api/keys` request body.

            This is the ONE `CreateKeyRequest` that gets `ToSchema`. The
            server-side `cove_service::ops::keys::CreateKeyRequest` is a stale
            duplicate — `handlers::keys::create_key` deserializes THIS type (aliased
            `WireCKR`) and converts it to the service type itself; see the NOTE on
            that duplicate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey | None:
    """Create an API key

     The `raw_token` in the response is shown exactly once. Team keys (admin-only, `team` field set)
    require an expiry and cannot hold `keys:manage`, `admin`, or any `admin:*` scope.

    **Admin keys:** a key may hold `admin` or any `admin:*` permission only when `admin_key` is `true`
    (`cove key create --admin`), and such a key must expire within `[auth] admin_max_key_lifetime_days`
    (default 30). Only an admin key is ever an administrator at `/api/admin/*`. A team key is never an
    admin key. An admin key is minted (and rotated) only from a signed-in session: an API key caller,
    admin key or not, gets 403. An admin key can still mint ordinary keys.

    **Service keys:** `service` (with exactly one of `team` or `member`) mints a **service key**,
    `svc:<service>`: admin only, expiry required, never `keys:manage`, `access:write`, `admin` or
    `admin:*`, and never an admin key. `team` binds it to a team (its VMs count against the team's
    quota); `member` binds it to one person (its VMs count against theirs, and they control them). A
    name is bound once: re-minting it with a different binding, or after its binding ended, is refused.
    `member` without `service` is refused.

    **A key never outlives the API key minting it:** when the caller is an API key that expires, any key
    it mints (personal, team or service) expires no later than the caller does. A mint that leaves
    `expires_in_secs` out gets the caller's own expiry. A longer one is refused with 422
    `validation_failed`, `field: "expires_in_secs"`, never shortened silently. A caller key with no
    expiry adds no limit of its own, and a signed-in session is not affected.

    **422 validation failures (one shape):** the handler's own label/scopes/admin_key/expires_in_secs
    pre-checks, and `create_key`'s service-layer rules (team-key expiry and forbidden scopes; the admin-
    key expiry cap and a flag with no admin permission; the service-key rules: binding, expiry,
    forbidden scopes, name already bound, a pre-existing `svc:` row), both answer `{code:
    "validation_failed", message, field?}` — `field` names the offending request field when the failure
    is scoped to one (`label`, `scopes`, `admin_key`, `expires_in_secs`, `member`), and is absent for
    the other service-layer rules, which are cross-field. The one service-layer rule that names a field
    is the caller-lifetime rule above: `expires_in_secs`.

    Args:
        body (CreateKeyRequest): `POST /api/keys` request body.

            This is the ONE `CreateKeyRequest` that gets `ToSchema`. The
            server-side `cove_service::ops::keys::CreateKeyRequest` is a stale
            duplicate — `handlers::keys::create_key` deserializes THIS type (aliased
            `WireCKR`) and converts it to the service type itself; see the NOTE on
            that duplicate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
