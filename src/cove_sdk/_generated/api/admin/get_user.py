from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_user_summary import AdminUserSummary
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/users/{username}".format(
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminUserSummary | ApiError | CliTooOldBody | str | None:
    if response.status_code == 200:
        response_200 = AdminUserSummary.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = response.text
        return response_404

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AdminUserSummary | ApiError | CliTooOldBody | str]:
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
) -> Response[AdminUserSummary | ApiError | CliTooOldBody | str]:
    """Read one account and its resource usage

     One row of `listAllUsers`: when the account was first and last seen, plus its current usage against
    its caps across all four dimensions.

    The 404 here is a plain missing-resource answer, not the existence-hiding 404 that VM routes use —
    every caller who reaches this operation is already an administrator, so there is nothing to hide
    from them. "Not found" means Cove has no record of that username, which usually means they have
    never signed in.

    Usage reflects caps, not what is running: `current` may exceed `max` for someone whose caps were
    lowered after they created their VMs.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminUserSummary | ApiError | CliTooOldBody | str]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> AdminUserSummary | ApiError | CliTooOldBody | str | None:
    """Read one account and its resource usage

     One row of `listAllUsers`: when the account was first and last seen, plus its current usage against
    its caps across all four dimensions.

    The 404 here is a plain missing-resource answer, not the existence-hiding 404 that VM routes use —
    every caller who reaches this operation is already an administrator, so there is nothing to hide
    from them. "Not found" means Cove has no record of that username, which usually means they have
    never signed in.

    Usage reflects caps, not what is running: `current` may exceed `max` for someone whose caps were
    lowered after they created their VMs.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminUserSummary | ApiError | CliTooOldBody | str
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminUserSummary | ApiError | CliTooOldBody | str]:
    """Read one account and its resource usage

     One row of `listAllUsers`: when the account was first and last seen, plus its current usage against
    its caps across all four dimensions.

    The 404 here is a plain missing-resource answer, not the existence-hiding 404 that VM routes use —
    every caller who reaches this operation is already an administrator, so there is nothing to hide
    from them. "Not found" means Cove has no record of that username, which usually means they have
    never signed in.

    Usage reflects caps, not what is running: `current` may exceed `max` for someone whose caps were
    lowered after they created their VMs.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminUserSummary | ApiError | CliTooOldBody | str]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> AdminUserSummary | ApiError | CliTooOldBody | str | None:
    """Read one account and its resource usage

     One row of `listAllUsers`: when the account was first and last seen, plus its current usage against
    its caps across all four dimensions.

    The 404 here is a plain missing-resource answer, not the existence-hiding 404 that VM routes use —
    every caller who reaches this operation is already an administrator, so there is nothing to hide
    from them. "Not found" means Cove has no record of that username, which usually means they have
    never signed in.

    Usage reflects caps, not what is running: `current` may exceed `max` for someone whose caps were
    lowered after they created their VMs.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminUserSummary | ApiError | CliTooOldBody | str
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
