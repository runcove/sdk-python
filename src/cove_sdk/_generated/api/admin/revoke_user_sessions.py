from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.revoke_sessions_response import RevokeSessionsResponse
from ...types import Response


def _get_kwargs(
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/users/{username}/revoke-sessions".format(
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | RevokeSessionsResponse | None:
    if response.status_code == 200:
        response_200 = RevokeSessionsResponse.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | RevokeSessionsResponse]:
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
) -> Response[ApiError | CliTooOldBody | RevokeSessionsResponse]:
    """Invalidate all of one person's sessions

     Kills every active CLI session that person holds, at the bastion and in Cove's own records, and
    returns how many were killed. Use it when someone leaves: Cove has no single-sign-out callback from
    the bastion, so this is the operator's way to force a departed account's credentials dead now rather
    than waiting for them to expire.

    Revoking zero sessions is a success, not an error — a username with no active sessions (including
    one that has never signed in) answers 200 with `{"revoked": 0}`. It does not touch the person's own
    API keys; revoke those individually; for a full offboarding (own API keys, webhooks, teams, secrets
    and VMs too) use `POST /api/admin/users/{username}/offboard`. It also revokes the person's connected
    apps (MCP clients such as claude.ai they signed in through) and every service key bound to that
    person, ends those bindings, removes those service keys from every project they belonged to, and
    withdraws every share to that person on those service keys' VMs, all in one transaction, and then
    drops each share's bastion access; `revoked` still counts CLI sessions only. A team share on those
    VMs is not theirs to lose: it stays while they remain in the team. The service keys' VMs stay until
    an admin deletes them.

    A CLI session ends only once the bastion confirms it deleted it. A session the bastion refuses to
    delete, or cannot be reached to delete, stays valid, is not marked revoked and is not counted, and
    the call then answers 503 `unavailable`, saying how many survived, even though Cove's own
    revocations (connected apps, service keys, shares) have already committed. Repeat the call once the
    bastion is reachable: it retries only the sessions left, and a 200 means none survived. A share's
    bastion access Cove cannot drop is different: it is retried in the background and logged, not
    returned.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | RevokeSessionsResponse]
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
) -> ApiError | CliTooOldBody | RevokeSessionsResponse | None:
    """Invalidate all of one person's sessions

     Kills every active CLI session that person holds, at the bastion and in Cove's own records, and
    returns how many were killed. Use it when someone leaves: Cove has no single-sign-out callback from
    the bastion, so this is the operator's way to force a departed account's credentials dead now rather
    than waiting for them to expire.

    Revoking zero sessions is a success, not an error — a username with no active sessions (including
    one that has never signed in) answers 200 with `{"revoked": 0}`. It does not touch the person's own
    API keys; revoke those individually; for a full offboarding (own API keys, webhooks, teams, secrets
    and VMs too) use `POST /api/admin/users/{username}/offboard`. It also revokes the person's connected
    apps (MCP clients such as claude.ai they signed in through) and every service key bound to that
    person, ends those bindings, removes those service keys from every project they belonged to, and
    withdraws every share to that person on those service keys' VMs, all in one transaction, and then
    drops each share's bastion access; `revoked` still counts CLI sessions only. A team share on those
    VMs is not theirs to lose: it stays while they remain in the team. The service keys' VMs stay until
    an admin deletes them.

    A CLI session ends only once the bastion confirms it deleted it. A session the bastion refuses to
    delete, or cannot be reached to delete, stays valid, is not marked revoked and is not counted, and
    the call then answers 503 `unavailable`, saying how many survived, even though Cove's own
    revocations (connected apps, service keys, shares) have already committed. Repeat the call once the
    bastion is reachable: it retries only the sessions left, and a 200 means none survived. A share's
    bastion access Cove cannot drop is different: it is retried in the background and logged, not
    returned.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | RevokeSessionsResponse
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | RevokeSessionsResponse]:
    """Invalidate all of one person's sessions

     Kills every active CLI session that person holds, at the bastion and in Cove's own records, and
    returns how many were killed. Use it when someone leaves: Cove has no single-sign-out callback from
    the bastion, so this is the operator's way to force a departed account's credentials dead now rather
    than waiting for them to expire.

    Revoking zero sessions is a success, not an error — a username with no active sessions (including
    one that has never signed in) answers 200 with `{"revoked": 0}`. It does not touch the person's own
    API keys; revoke those individually; for a full offboarding (own API keys, webhooks, teams, secrets
    and VMs too) use `POST /api/admin/users/{username}/offboard`. It also revokes the person's connected
    apps (MCP clients such as claude.ai they signed in through) and every service key bound to that
    person, ends those bindings, removes those service keys from every project they belonged to, and
    withdraws every share to that person on those service keys' VMs, all in one transaction, and then
    drops each share's bastion access; `revoked` still counts CLI sessions only. A team share on those
    VMs is not theirs to lose: it stays while they remain in the team. The service keys' VMs stay until
    an admin deletes them.

    A CLI session ends only once the bastion confirms it deleted it. A session the bastion refuses to
    delete, or cannot be reached to delete, stays valid, is not marked revoked and is not counted, and
    the call then answers 503 `unavailable`, saying how many survived, even though Cove's own
    revocations (connected apps, service keys, shares) have already committed. Repeat the call once the
    bastion is reachable: it retries only the sessions left, and a 200 means none survived. A share's
    bastion access Cove cannot drop is different: it is retried in the background and logged, not
    returned.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | RevokeSessionsResponse]
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
) -> ApiError | CliTooOldBody | RevokeSessionsResponse | None:
    """Invalidate all of one person's sessions

     Kills every active CLI session that person holds, at the bastion and in Cove's own records, and
    returns how many were killed. Use it when someone leaves: Cove has no single-sign-out callback from
    the bastion, so this is the operator's way to force a departed account's credentials dead now rather
    than waiting for them to expire.

    Revoking zero sessions is a success, not an error — a username with no active sessions (including
    one that has never signed in) answers 200 with `{"revoked": 0}`. It does not touch the person's own
    API keys; revoke those individually; for a full offboarding (own API keys, webhooks, teams, secrets
    and VMs too) use `POST /api/admin/users/{username}/offboard`. It also revokes the person's connected
    apps (MCP clients such as claude.ai they signed in through) and every service key bound to that
    person, ends those bindings, removes those service keys from every project they belonged to, and
    withdraws every share to that person on those service keys' VMs, all in one transaction, and then
    drops each share's bastion access; `revoked` still counts CLI sessions only. A team share on those
    VMs is not theirs to lose: it stays while they remain in the team. The service keys' VMs stay until
    an admin deletes them.

    A CLI session ends only once the bastion confirms it deleted it. A session the bastion refuses to
    delete, or cannot be reached to delete, stays valid, is not marked revoked and is not counted, and
    the call then answers 503 `unavailable`, saying how many survived, even though Cove's own
    revocations (connected apps, service keys, shares) have already committed. Repeat the call once the
    bastion is reachable: it retries only the sessions left, and a 200 means none survived. A share's
    bastion access Cove cannot drop is different: it is retried in the background and logged, not
    returned.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | RevokeSessionsResponse
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
