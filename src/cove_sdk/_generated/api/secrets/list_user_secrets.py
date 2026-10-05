from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.secret_entry_dto import SecretEntryDto
from ...types import Response


def _get_kwargs(
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/users/{username}/secrets".format(
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_secret_name_list_item_data in _response_200:
            componentsschemas_secret_name_list_item = SecretEntryDto.from_dict(
                componentsschemas_secret_name_list_item_data
            )

            response_200.append(componentsschemas_secret_name_list_item)

        return response_200

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

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]:
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
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]:
    """List user-scoped secret names

     Names only — values are never exposed via HTTP. ACL is self-or-admin: the named user, or an admin,
    may read this; anyone else gets the same 404 an unknown username would (existence non-leak). A user-
    scoped secret is one input to the merge a VM receives at inject time — the precedence is `Vm > User
    > Team > Project`, most-specific wins.

    An API key needs MORE than `secrets:read` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: listing another user's names, or those of a team or project
    the caller is not a member of, requires `admin:secrets:read` IN ADDITION to the `secrets:read` this
    route demands. A key without it gets the same **404** as a stranger, not a 403 — the refusal must
    not confirm that the principal exists. Reading your own scope, or one you are a member of, needs
    only `secrets:read`. Interactive sessions (SSH, web, unix socket) carry no scope list and are
    unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto] | None:
    """List user-scoped secret names

     Names only — values are never exposed via HTTP. ACL is self-or-admin: the named user, or an admin,
    may read this; anyone else gets the same 404 an unknown username would (existence non-leak). A user-
    scoped secret is one input to the merge a VM receives at inject time — the precedence is `Vm > User
    > Team > Project`, most-specific wins.

    An API key needs MORE than `secrets:read` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: listing another user's names, or those of a team or project
    the caller is not a member of, requires `admin:secrets:read` IN ADDITION to the `secrets:read` this
    route demands. A key without it gets the same **404** as a stranger, not a 403 — the refusal must
    not confirm that the principal exists. Reading your own scope, or one you are a member of, needs
    only `secrets:read`. Interactive sessions (SSH, web, unix socket) carry no scope list and are
    unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]:
    """List user-scoped secret names

     Names only — values are never exposed via HTTP. ACL is self-or-admin: the named user, or an admin,
    may read this; anyone else gets the same 404 an unknown username would (existence non-leak). A user-
    scoped secret is one input to the merge a VM receives at inject time — the precedence is `Vm > User
    > Team > Project`, most-specific wins.

    An API key needs MORE than `secrets:read` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: listing another user's names, or those of a team or project
    the caller is not a member of, requires `admin:secrets:read` IN ADDITION to the `secrets:read` this
    route demands. A key without it gets the same **404** as a stranger, not a 403 — the refusal must
    not confirm that the principal exists. Reading your own scope, or one you are a member of, needs
    only `secrets:read`. Interactive sessions (SSH, web, unix socket) carry no scope list and are
    unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]]
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
) -> ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto] | None:
    """List user-scoped secret names

     Names only — values are never exposed via HTTP. ACL is self-or-admin: the named user, or an admin,
    may read this; anyone else gets the same 404 an unknown username would (existence non-leak). A user-
    scoped secret is one input to the merge a VM receives at inject time — the precedence is `Vm > User
    > Team > Project`, most-specific wins.

    An API key needs MORE than `secrets:read` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: listing another user's names, or those of a team or project
    the caller is not a member of, requires `admin:secrets:read` IN ADDITION to the `secrets:read` this
    route demands. A key without it gets the same **404** as a stranger, not a 403 — the refusal must
    not confirm that the principal exists. Reading your own scope, or one you are a member of, needs
    only `secrets:read`. Interactive sessions (SSH, web, unix socket) carry no scope list and are
    unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | list[SecretEntryDto]
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
