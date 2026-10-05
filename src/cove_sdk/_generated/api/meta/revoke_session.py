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
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/me/sessions/{id}".format(
            id=quote(str(id), safe=""),
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

    if response.status_code == 404:
        response_404 = cast(Any, None)
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
) -> Response[Any | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Revoke a CLI session

     Not mounted on the external API listener, on purpose: an API key may read its owner's sign-in
    sessions (`listSessions`) but never change them, the same rule that keeps SSH-key changes off that
    listener. Revoke a session from an SSH, web or local session instead. See `listSessions` for why
    this uses `session` rather than `ticket` vocabulary in a freshly-minted name.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | None:
    """Revoke a CLI session

     Not mounted on the external API listener, on purpose: an API key may read its owner's sign-in
    sessions (`listSessions`) but never change them, the same rule that keeps SSH-key changes off that
    listener. Revoke a session from an SSH, web or local session instead. See `listSessions` for why
    this uses `session` rather than `ticket` vocabulary in a freshly-minted name.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Revoke a CLI session

     Not mounted on the external API listener, on purpose: an API key may read its owner's sign-in
    sessions (`listSessions`) but never change them, the same rule that keeps SSH-key changes off that
    listener. Revoke a session from an SSH, web or local session instead. See `listSessions` for why
    this uses `session` rather than `ticket` vocabulary in a freshly-minted name.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | None:
    """Revoke a CLI session

     Not mounted on the external API listener, on purpose: an API key may read its owner's sign-in
    sessions (`listSessions`) but never change them, the same rule that keeps SSH-key changes off that
    listener. Revoke a session from an SSH, web or local session instead. See `listSessions` for why
    this uses `session` rather than `ticket` vocabulary in a freshly-minted name.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
