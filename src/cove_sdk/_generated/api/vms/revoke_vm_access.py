from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.revoke_share_outcome import RevokeShareOutcome
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    subject_type: str,
    subject_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/vms/{name}/access/{subject_type}/{subject_id}".format(
            name=quote(str(name), safe=""),
            subject_type=quote(str(subject_type), safe=""),
            subject_id=quote(str(subject_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = RevokeShareOutcome.from_dict(response.json())

        return response_200

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    subject_type: str,
    subject_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody]:
    """Revoke a user or team's access to a VM

     Revokes a share (owner/admin only, same authz chokepoint as the grant). Returns 200 with the fail-
    loud sweep outcome: `revoked` plus `unconfirmed_edges` / `unconfirmed_sessions` for anything the
    synchronous sweep could not confirm dead (the reconciler retries them).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        subject_type (str):
        subject_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        subject_type=subject_type,
        subject_id=subject_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    subject_type: str,
    subject_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody | None:
    """Revoke a user or team's access to a VM

     Revokes a share (owner/admin only, same authz chokepoint as the grant). Returns 200 with the fail-
    loud sweep outcome: `revoked` plus `unconfirmed_edges` / `unconfirmed_sessions` for anything the
    synchronous sweep could not confirm dead (the reconciler retries them).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        subject_type (str):
        subject_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        subject_type=subject_type,
        subject_id=subject_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    subject_type: str,
    subject_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody]:
    """Revoke a user or team's access to a VM

     Revokes a share (owner/admin only, same authz chokepoint as the grant). Returns 200 with the fail-
    loud sweep outcome: `revoked` plus `unconfirmed_edges` / `unconfirmed_sessions` for anything the
    synchronous sweep could not confirm dead (the reconciler retries them).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        subject_type (str):
        subject_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        subject_type=subject_type,
        subject_id=subject_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    subject_type: str,
    subject_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody | None:
    """Revoke a user or team's access to a VM

     Revokes a share (owner/admin only, same authz chokepoint as the grant). Returns 200 with the fail-
    loud sweep outcome: `revoked` plus `unconfirmed_edges` / `unconfirmed_sessions` for anything the
    synchronous sweep could not confirm dead (the reconciler retries them).

    Served on every listener, including the external API listener.

    Args:
        name (str):
        subject_type (str):
        subject_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | RevokeShareOutcome | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            subject_type=subject_type,
            subject_id=subject_id,
            client=client,
        )
    ).parsed
