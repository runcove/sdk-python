from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_team_quota_override_request import AdminTeamQuotaOverrideRequest
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    team_id: str,
    *,
    body: AdminTeamQuotaOverrideRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/admin/team-quotas/{team_id}".format(
            team_id=quote(str(team_id), safe=""),
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
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminTeamQuotaOverrideRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Set one team's resource-cap overrides

     Replaces all four team caps at once, with the same semantics as `updateUserQuotaOverride`: **an
    omitted dimension is cleared, not preserved**, and falls back to the host default. Read the current
    values first if you only mean to change one.

    Lowering a cap below what the team already runs does not reclaim anything — the team stays
    legitimately over its cap and only further creation is blocked. That overage is expected and
    visible; it also happens on its own when a member leaves a team, since their team-attributed VMs
    revert to being charged to them personally.

    Accepts a team identifier whether or not the team exists.

    Args:
        team_id (str):
        body (AdminTeamQuotaOverrideRequest): `GET/PUT /api/admin/team-quotas/{team_id}` — same
            shape, team-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminTeamQuotaOverrideRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Set one team's resource-cap overrides

     Replaces all four team caps at once, with the same semantics as `updateUserQuotaOverride`: **an
    omitted dimension is cleared, not preserved**, and falls back to the host default. Read the current
    values first if you only mean to change one.

    Lowering a cap below what the team already runs does not reclaim anything — the team stays
    legitimately over its cap and only further creation is blocked. That overage is expected and
    visible; it also happens on its own when a member leaves a team, since their team-attributed VMs
    revert to being charged to them personally.

    Accepts a team identifier whether or not the team exists.

    Args:
        team_id (str):
        body (AdminTeamQuotaOverrideRequest): `GET/PUT /api/admin/team-quotas/{team_id}` — same
            shape, team-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminTeamQuotaOverrideRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Set one team's resource-cap overrides

     Replaces all four team caps at once, with the same semantics as `updateUserQuotaOverride`: **an
    omitted dimension is cleared, not preserved**, and falls back to the host default. Read the current
    values first if you only mean to change one.

    Lowering a cap below what the team already runs does not reclaim anything — the team stays
    legitimately over its cap and only further creation is blocked. That overage is expected and
    visible; it also happens on its own when a member leaves a team, since their team-attributed VMs
    revert to being charged to them personally.

    Accepts a team identifier whether or not the team exists.

    Args:
        team_id (str):
        body (AdminTeamQuotaOverrideRequest): `GET/PUT /api/admin/team-quotas/{team_id}` — same
            shape, team-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminTeamQuotaOverrideRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Set one team's resource-cap overrides

     Replaces all four team caps at once, with the same semantics as `updateUserQuotaOverride`: **an
    omitted dimension is cleared, not preserved**, and falls back to the host default. Read the current
    values first if you only mean to change one.

    Lowering a cap below what the team already runs does not reclaim anything — the team stays
    legitimately over its cap and only further creation is blocked. That overage is expected and
    visible; it also happens on its own when a member leaves a team, since their team-attributed VMs
    revert to being charged to them personally.

    Accepts a team identifier whether or not the team exists.

    Args:
        team_id (str):
        body (AdminTeamQuotaOverrideRequest): `GET/PUT /api/admin/team-quotas/{team_id}` — same
            shape, team-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
