from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.whoami_response import WhoamiResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/whoami",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | WhoamiResponse | None:
    if response.status_code == 200:
        response_200 = WhoamiResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

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
) -> Response[ApiError | CliTooOldBody | WhoamiResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | WhoamiResponse]:
    """Identity of the calling credential

     Returns the username the current credential resolves to. Useful for confirming which identity a key
    or session is acting as.

    **Prefer this over `GET /api/me` when all you need is the identity.** The two are deliberately
    separate operations. This one is a cheap identity probe: it returns a value the server already holds
    in memory, calls nothing external, and therefore stays available whenever the API itself is. `GET
    /api/me` returns the full caller summary — roles, SSH key count, LDAP linkage, quota — and assembles
    it from several Warpgate administrative calls, so it is only as available as the bastion is.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid credential may read it. `scope_table::lookup` maps this path to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | WhoamiResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | WhoamiResponse | None:
    """Identity of the calling credential

     Returns the username the current credential resolves to. Useful for confirming which identity a key
    or session is acting as.

    **Prefer this over `GET /api/me` when all you need is the identity.** The two are deliberately
    separate operations. This one is a cheap identity probe: it returns a value the server already holds
    in memory, calls nothing external, and therefore stays available whenever the API itself is. `GET
    /api/me` returns the full caller summary — roles, SSH key count, LDAP linkage, quota — and assembles
    it from several Warpgate administrative calls, so it is only as available as the bastion is.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid credential may read it. `scope_table::lookup` maps this path to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | WhoamiResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | WhoamiResponse]:
    """Identity of the calling credential

     Returns the username the current credential resolves to. Useful for confirming which identity a key
    or session is acting as.

    **Prefer this over `GET /api/me` when all you need is the identity.** The two are deliberately
    separate operations. This one is a cheap identity probe: it returns a value the server already holds
    in memory, calls nothing external, and therefore stays available whenever the API itself is. `GET
    /api/me` returns the full caller summary — roles, SSH key count, LDAP linkage, quota — and assembles
    it from several Warpgate administrative calls, so it is only as available as the bastion is.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid credential may read it. `scope_table::lookup` maps this path to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | WhoamiResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | WhoamiResponse | None:
    """Identity of the calling credential

     Returns the username the current credential resolves to. Useful for confirming which identity a key
    or session is acting as.

    **Prefer this over `GET /api/me` when all you need is the identity.** The two are deliberately
    separate operations. This one is a cheap identity probe: it returns a value the server already holds
    in memory, calls nothing external, and therefore stays available whenever the API itself is. `GET
    /api/me` returns the full caller summary — roles, SSH key count, LDAP linkage, quota — and assembles
    it from several Warpgate administrative calls, so it is only as available as the bastion is.

    Carries **no** `x-required-scope`: the only data returned is about the caller themselves, so any
    valid credential may read it. `scope_table::lookup` maps this path to no specific scope, and the
    cross-check test holds the two statements together.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | WhoamiResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
