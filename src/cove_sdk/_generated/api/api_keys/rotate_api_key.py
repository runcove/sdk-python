from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.created_key import CreatedKey
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/api-keys/{id}/rotate".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey | None:
    if response.status_code == 200:
        response_200 = CreatedKey.from_dict(response.json())

        return response_200

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
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]:
    """Rotate an API key (atomic mint + revoke)

     Atomically creates a replacement key and revokes the original. A non-owned key returns 404,
    identically to a missing one. An admin key is rotated only from a signed-in session: an API key
    caller, admin key or not, gets 403 `admin_required`. The replacement keeps the original's expiry, so
    an API key caller that expires may rotate only a key that expires no later than it does (a key
    rotating itself always may); otherwise 422 `validation_failed` with `field: "id"`. A signed-in
    session is not affected.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]
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
) -> ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey | None:
    """Rotate an API key (atomic mint + revoke)

     Atomically creates a replacement key and revokes the original. A non-owned key returns 404,
    identically to a missing one. An admin key is rotated only from a signed-in session: an API key
    caller, admin key or not, gets 403 `admin_required`. The replacement keeps the original's expiry, so
    an API key caller that expires may rotate only a key that expires no later than it does (a key
    rotating itself always may); otherwise 422 `validation_failed` with `field: "id"`. A signed-in
    session is not affected.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]:
    """Rotate an API key (atomic mint + revoke)

     Atomically creates a replacement key and revokes the original. A non-owned key returns 404,
    identically to a missing one. An admin key is rotated only from a signed-in session: an API key
    caller, admin key or not, gets 403 `admin_required`. The replacement keeps the original's expiry, so
    an API key caller that expires may rotate only a key that expires no later than it does (a key
    rotating itself always may); otherwise 422 `validation_failed` with `field: "id"`. A signed-in
    session is not affected.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey]
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
) -> ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey | None:
    """Rotate an API key (atomic mint + revoke)

     Atomically creates a replacement key and revokes the original. A non-owned key returns 404,
    identically to a missing one. An admin key is rotated only from a signed-in session: an API key
    caller, admin key or not, gets 403 `admin_required`. The replacement keeps the original's expiry, so
    an API key caller that expires may rotate only a key that expires no later than it does (a key
    rotating itself always may); otherwise 422 `validation_failed` with `field: "id"`. A signed-in
    session is not affected.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | CreatedKey
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
