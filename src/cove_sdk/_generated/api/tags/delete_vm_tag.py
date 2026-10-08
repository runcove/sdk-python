from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.removal_response import RemovalResponse
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    key: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/vms/{name}/tags/{key}".format(
            name=quote(str(name), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = RemovalResponse.from_dict(response.json())

        return response_200

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
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
) -> Response[Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody]:
    """Delete a tag

     Idempotent, and says what it did: **200** `{"existed": true}` when the key was set, `{"existed":
    false}` when it was not (a typo, or a repeat). Since API version 7: a client sending `X-Cove-Api-
    Version` below 7 gets an empty **204** either way, as before.

    Args:
        name (str):
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        key=key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody | None:
    """Delete a tag

     Idempotent, and says what it did: **200** `{"existed": true}` when the key was set, `{"existed":
    false}` when it was not (a typo, or a repeat). Since API version 7: a client sending `X-Cove-Api-
    Version` below 7 gets an empty **204** either way, as before.

    Args:
        name (str):
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        key=key,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody]:
    """Delete a tag

     Idempotent, and says what it did: **200** `{"existed": true}` when the key was set, `{"existed":
    false}` when it was not (a typo, or a repeat). Since API version 7: a client sending `X-Cove-Api-
    Version` below 7 gets an empty **204** either way, as before.

    Args:
        name (str):
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        key=key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody | None:
    """Delete a tag

     Idempotent, and says what it did: **200** `{"existed": true}` when the key was set, `{"existed":
    false}` when it was not (a typo, or a repeat). Since API version 7: a client sending `X-Cove-Api-
    Version` below 7 gets an empty **204** either way, as before.

    Args:
        name (str):
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | RemovalResponse | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            key=key,
            client=client,
        )
    ).parsed
