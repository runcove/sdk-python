from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    project_id: str,
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/admin/projects/{project_id}/members/{username}".format(
            project_id=quote(str(project_id), safe=""),
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
) -> Response[Any | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Remove someone from a project

     Revokes that person's access to every secret in the project. Membership is re-checked on each secret
    access, so the revocation is immediate — but secrets already injected into a running VM stay there
    until that VM's next lifecycle event re-reads them.

    Idempotent: removing someone who is not a member succeeds and records nothing.

    Args:
        project_id (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | None:
    """Remove someone from a project

     Revokes that person's access to every secret in the project. Membership is re-checked on each secret
    access, so the revocation is immediate — but secrets already injected into a running VM stay there
    until that VM's next lifecycle event re-reads them.

    Idempotent: removing someone who is not a member succeeds and records nothing.

    Args:
        project_id (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        project_id=project_id,
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Remove someone from a project

     Revokes that person's access to every secret in the project. Membership is re-checked on each secret
    access, so the revocation is immediate — but secrets already injected into a running VM stay there
    until that VM's next lifecycle event re-reads them.

    Idempotent: removing someone who is not a member succeeds and records nothing.

    Args:
        project_id (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | None:
    """Remove someone from a project

     Revokes that person's access to every secret in the project. Membership is re-checked on each secret
    access, so the revocation is immediate — but secrets already injected into a running VM stay there
    until that VM's next lifecycle event re-reads them.

    Idempotent: removing someone who is not a member succeeds and records nothing.

    Args:
        project_id (str):
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            username=username,
            client=client,
        )
    ).parsed
