from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_team_quota_override_response import AdminTeamQuotaOverrideResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    team_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/team-quotas/{team_id}".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminTeamQuotaOverrideResponse.from_dict(response.json())

        return response_200

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
) -> Response[AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody]:
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
) -> Response[AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody]:
    """Read one team's resource-cap overrides

     The same four caps as `getUserQuotaOverride`, for a team instead of a person. A dimension reads
    `null` when the team has no override and the host default applies.

    A team with no overrides at all answers 200 with all four `null`, not 404, and the team need not
    exist.

    Which envelope a VM is charged to is fixed when it is created: a VM attributed to a team counts
    against these caps *instead of* its owner's, never both.

    Args:
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody | None:
    """Read one team's resource-cap overrides

     The same four caps as `getUserQuotaOverride`, for a team instead of a person. A dimension reads
    `null` when the team has no override and the host default applies.

    A team with no overrides at all answers 200 with all four `null`, not 404, and the team need not
    exist.

    Which envelope a VM is charged to is fixed when it is created: a VM attributed to a team counts
    against these caps *instead of* its owner's, never both.

    Args:
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody]:
    """Read one team's resource-cap overrides

     The same four caps as `getUserQuotaOverride`, for a team instead of a person. A dimension reads
    `null` when the team has no override and the host default applies.

    A team with no overrides at all answers 200 with all four `null`, not 404, and the team need not
    exist.

    Which envelope a VM is charged to is fixed when it is created: a VM attributed to a team counts
    against these caps *instead of* its owner's, never both.

    Args:
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody | None:
    """Read one team's resource-cap overrides

     The same four caps as `getUserQuotaOverride`, for a team instead of a person. A dimension reads
    `null` when the team has no override and the host default applies.

    A team with no overrides at all answers 200 with all four `null`, not 404, and the team need not
    exist.

    Which envelope a VM is charged to is fixed when it is created: a VM attributed to a team counts
    against these caps *instead of* its owner's, never both.

    Args:
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminTeamQuotaOverrideResponse | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
