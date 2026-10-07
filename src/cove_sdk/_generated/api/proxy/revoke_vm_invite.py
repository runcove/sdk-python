from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    invite_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/vms/{name}/invites/{invite_id}".format(
            name=quote(str(name), safe=""),
            invite_id=quote(str(invite_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Revoke a share invite

     Revokes an invite link immediately; any URL that embedded it stops working. `invite_id` is checked
    against this VM's own registered proxy targets before the revoke — an invite that resolves but
    belongs to a different VM returns the same 404 as one that does not exist at all, so a caller cannot
    use this endpoint to enumerate other VMs' invites (existence non-leak, applied to the invite
    identifier as well as the VM name).

    A VM that does not exist, or is not visible to the caller, returns the same 404.

    Args:
        name (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        invite_id=invite_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Revoke a share invite

     Revokes an invite link immediately; any URL that embedded it stops working. `invite_id` is checked
    against this VM's own registered proxy targets before the revoke — an invite that resolves but
    belongs to a different VM returns the same 404 as one that does not exist at all, so a caller cannot
    use this endpoint to enumerate other VMs' invites (existence non-leak, applied to the invite
    identifier as well as the VM name).

    A VM that does not exist, or is not visible to the caller, returns the same 404.

    Args:
        name (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        invite_id=invite_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Revoke a share invite

     Revokes an invite link immediately; any URL that embedded it stops working. `invite_id` is checked
    against this VM's own registered proxy targets before the revoke — an invite that resolves but
    belongs to a different VM returns the same 404 as one that does not exist at all, so a caller cannot
    use this endpoint to enumerate other VMs' invites (existence non-leak, applied to the invite
    identifier as well as the VM name).

    A VM that does not exist, or is not visible to the caller, returns the same 404.

    Args:
        name (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        invite_id=invite_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Revoke a share invite

     Revokes an invite link immediately; any URL that embedded it stops working. `invite_id` is checked
    against this VM's own registered proxy targets before the revoke — an invite that resolves but
    belongs to a different VM returns the same 404 as one that does not exist at all, so a caller cannot
    use this endpoint to enumerate other VMs' invites (existence non-leak, applied to the invite
    identifier as well as the VM name).

    A VM that does not exist, or is not visible to the caller, returns the same 404.

    Args:
        name (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            invite_id=invite_id,
            client=client,
        )
    ).parsed
