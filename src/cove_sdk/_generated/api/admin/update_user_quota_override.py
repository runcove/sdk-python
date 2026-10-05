from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_quota_override_request import AdminQuotaOverrideRequest
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    username: str,
    *,
    body: AdminQuotaOverrideRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/admin/quotas/{username}".format(
            username=quote(str(username), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

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
) -> Response[Any | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminQuotaOverrideRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Set one person's resource-cap overrides

     Replaces all four per-person caps at once. **Omitting a dimension is not "leave it alone" — it
    clears that override** and hands the dimension back to the host default. Read the current values
    with `getUserQuotaOverride` first and send them all back if you only mean to change one.

    Raising a cap takes effect on that person's next create; lowering one below what they already run
    does not reclaim anything — existing VMs keep running, and the new cap only blocks further creation.
    Nothing here is validated against current usage.

    Applies to a username whether or not that account exists yet, so a cap can be set before someone's
    first login. The username must be one cove would accept at login: Warpgate's anonymous `<public>`, a
    `team:` name and other invalid names are refused. A VM attributed to a team is charged to the team's
    caps, not the owner's — see `updateTeamQuotaOverride`.

    Args:
        username (str):
        body (AdminQuotaOverrideRequest): `GET/PUT /api/admin/quotas/{username}` body — all four
            dims optional;
            `None` on PUT means "use the host default for that dim" (COALESCE
            semantics, same as `quota_users` today). GET returns the row's current
            values (all `None` when no override row exists).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        username=username,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminQuotaOverrideRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Set one person's resource-cap overrides

     Replaces all four per-person caps at once. **Omitting a dimension is not "leave it alone" — it
    clears that override** and hands the dimension back to the host default. Read the current values
    with `getUserQuotaOverride` first and send them all back if you only mean to change one.

    Raising a cap takes effect on that person's next create; lowering one below what they already run
    does not reclaim anything — existing VMs keep running, and the new cap only blocks further creation.
    Nothing here is validated against current usage.

    Applies to a username whether or not that account exists yet, so a cap can be set before someone's
    first login. The username must be one cove would accept at login: Warpgate's anonymous `<public>`, a
    `team:` name and other invalid names are refused. A VM attributed to a team is charged to the team's
    caps, not the owner's — see `updateTeamQuotaOverride`.

    Args:
        username (str):
        body (AdminQuotaOverrideRequest): `GET/PUT /api/admin/quotas/{username}` body — all four
            dims optional;
            `None` on PUT means "use the host default for that dim" (COALESCE
            semantics, same as `quota_users` today). GET returns the row's current
            values (all `None` when no override row exists).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        username=username,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminQuotaOverrideRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Set one person's resource-cap overrides

     Replaces all four per-person caps at once. **Omitting a dimension is not "leave it alone" — it
    clears that override** and hands the dimension back to the host default. Read the current values
    with `getUserQuotaOverride` first and send them all back if you only mean to change one.

    Raising a cap takes effect on that person's next create; lowering one below what they already run
    does not reclaim anything — existing VMs keep running, and the new cap only blocks further creation.
    Nothing here is validated against current usage.

    Applies to a username whether or not that account exists yet, so a cap can be set before someone's
    first login. The username must be one cove would accept at login: Warpgate's anonymous `<public>`, a
    `team:` name and other invalid names are refused. A VM attributed to a team is charged to the team's
    caps, not the owner's — see `updateTeamQuotaOverride`.

    Args:
        username (str):
        body (AdminQuotaOverrideRequest): `GET/PUT /api/admin/quotas/{username}` body — all four
            dims optional;
            `None` on PUT means "use the host default for that dim" (COALESCE
            semantics, same as `quota_users` today). GET returns the row's current
            values (all `None` when no override row exists).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        username=username,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminQuotaOverrideRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Set one person's resource-cap overrides

     Replaces all four per-person caps at once. **Omitting a dimension is not "leave it alone" — it
    clears that override** and hands the dimension back to the host default. Read the current values
    with `getUserQuotaOverride` first and send them all back if you only mean to change one.

    Raising a cap takes effect on that person's next create; lowering one below what they already run
    does not reclaim anything — existing VMs keep running, and the new cap only blocks further creation.
    Nothing here is validated against current usage.

    Applies to a username whether or not that account exists yet, so a cap can be set before someone's
    first login. The username must be one cove would accept at login: Warpgate's anonymous `<public>`, a
    `team:` name and other invalid names are refused. A VM attributed to a team is charged to the team's
    caps, not the owner's — see `updateTeamQuotaOverride`.

    Args:
        username (str):
        body (AdminQuotaOverrideRequest): `GET/PUT /api/admin/quotas/{username}` body — all four
            dims optional;
            `None` on PUT means "use the host default for that dim" (COALESCE
            semantics, same as `quota_users` today). GET returns the row's current
            values (all `None` when no override row exists).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            body=body,
        )
    ).parsed
