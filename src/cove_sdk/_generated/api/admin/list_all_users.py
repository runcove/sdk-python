from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_user_summary import AdminUserSummary
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/users",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | list[AdminUserSummary] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AdminUserSummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | list[AdminUserSummary]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[AdminUserSummary]]:
    """List everyone Cove knows, with their resource usage

     Every account Cove has seen, alphabetical by username, each with when it was first seen, when it was
    last seen, and its current usage against its caps across all four dimensions. This is the cross-
    tenant view: it discloses who else uses this host, which is why it is administrator-only.

    Usage is computed live per account, so a large fleet makes this call proportionally more expensive.
    There is no pagination and no filter — the whole list comes back.

    `current` may legitimately exceed `max`: caps block new creation, they never retroactively remove
    what someone already runs. A VM attributed to a team is charged to the team, so it is absent from
    its owner's usage here.

    For the fleet's VMs rather than its people, use `listAllVms`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[AdminUserSummary]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[AdminUserSummary] | None:
    """List everyone Cove knows, with their resource usage

     Every account Cove has seen, alphabetical by username, each with when it was first seen, when it was
    last seen, and its current usage against its caps across all four dimensions. This is the cross-
    tenant view: it discloses who else uses this host, which is why it is administrator-only.

    Usage is computed live per account, so a large fleet makes this call proportionally more expensive.
    There is no pagination and no filter — the whole list comes back.

    `current` may legitimately exceed `max`: caps block new creation, they never retroactively remove
    what someone already runs. A VM attributed to a team is charged to the team, so it is absent from
    its owner's usage here.

    For the fleet's VMs rather than its people, use `listAllVms`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[AdminUserSummary]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | list[AdminUserSummary]]:
    """List everyone Cove knows, with their resource usage

     Every account Cove has seen, alphabetical by username, each with when it was first seen, when it was
    last seen, and its current usage against its caps across all four dimensions. This is the cross-
    tenant view: it discloses who else uses this host, which is why it is administrator-only.

    Usage is computed live per account, so a large fleet makes this call proportionally more expensive.
    There is no pagination and no filter — the whole list comes back.

    `current` may legitimately exceed `max`: caps block new creation, they never retroactively remove
    what someone already runs. A VM attributed to a team is charged to the team, so it is absent from
    its owner's usage here.

    For the fleet's VMs rather than its people, use `listAllVms`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | list[AdminUserSummary]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | list[AdminUserSummary] | None:
    """List everyone Cove knows, with their resource usage

     Every account Cove has seen, alphabetical by username, each with when it was first seen, when it was
    last seen, and its current usage against its caps across all four dimensions. This is the cross-
    tenant view: it discloses who else uses this host, which is why it is administrator-only.

    Usage is computed live per account, so a large fleet makes this call proportionally more expensive.
    There is no pagination and no filter — the whole list comes back.

    `current` may legitimately exceed `max`: caps block new creation, they never retroactively remove
    what someone already runs. A VM attributed to a team is charged to the team, so it is absent from
    its owner's usage here.

    For the fleet's VMs rather than its people, use `listAllVms`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | list[AdminUserSummary]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
