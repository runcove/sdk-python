from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.enable_user_response import EnableUserResponse
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/users/{username}/enable".format(
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse | None:
    if response.status_code == 200:
        response_200 = EnableUserResponse.from_dict(response.json())

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
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse]:
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
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse]:
    """Let an offboarded person back in

     Clears the shut-out a full offboarding leaves on a person. While it is there, every request that
    person makes (SSH shell, web UI, CLI session, API key, connected app) is refused with 403
    `user_disabled`, and nothing that would hand them a credential or a way in (an API key, a webhook, a
    share, a team membership, a service key bound to them, a CLI or connect ticket, an SSH key, a
    connected app, a VM) is created, whoever asks. After this call they can sign in again; nothing
    offboarding ended comes back, so they start from nothing. The name is matched regardless of ASCII
    case, as Warpgate matches it.

    Writes one `user.enabled` audit row in the same transaction: the administrator, the sudo context,
    and when, by whom and why the person had been shut out (also in the response).

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse]
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
) -> ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse | None:
    """Let an offboarded person back in

     Clears the shut-out a full offboarding leaves on a person. While it is there, every request that
    person makes (SSH shell, web UI, CLI session, API key, connected app) is refused with 403
    `user_disabled`, and nothing that would hand them a credential or a way in (an API key, a webhook, a
    share, a team membership, a service key bound to them, a CLI or connect ticket, an SSH key, a
    connected app, a VM) is created, whoever asks. After this call they can sign in again; nothing
    offboarding ended comes back, so they start from nothing. The name is matched regardless of ASCII
    case, as Warpgate matches it.

    Writes one `user.enabled` audit row in the same transaction: the administrator, the sudo context,
    and when, by whom and why the person had been shut out (also in the response).

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse]:
    """Let an offboarded person back in

     Clears the shut-out a full offboarding leaves on a person. While it is there, every request that
    person makes (SSH shell, web UI, CLI session, API key, connected app) is refused with 403
    `user_disabled`, and nothing that would hand them a credential or a way in (an API key, a webhook, a
    share, a team membership, a service key bound to them, a CLI or connect ticket, an SSH key, a
    connected app, a VM) is created, whoever asks. After this call they can sign in again; nothing
    offboarding ended comes back, so they start from nothing. The name is matched regardless of ASCII
    case, as Warpgate matches it.

    Writes one `user.enabled` audit row in the same transaction: the administrator, the sudo context,
    and when, by whom and why the person had been shut out (also in the response).

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse]
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
) -> ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse | None:
    """Let an offboarded person back in

     Clears the shut-out a full offboarding leaves on a person. While it is there, every request that
    person makes (SSH shell, web UI, CLI session, API key, connected app) is refused with 403
    `user_disabled`, and nothing that would hand them a credential or a way in (an API key, a webhook, a
    share, a team membership, a service key bound to them, a CLI or connect ticket, an SSH key, a
    connected app, a VM) is created, whoever asks. After this call they can sign in again; nothing
    offboarding ended comes back, so they start from nothing. The name is matched regardless of ASCII
    case, as Warpgate matches it.

    Writes one `user.enabled` audit row in the same transaction: the administrator, the sudo context,
    and when, by whom and why the person had been shut out (also in the response).

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | EnableUserResponse
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
