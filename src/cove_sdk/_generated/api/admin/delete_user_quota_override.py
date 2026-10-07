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
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/admin/quotas/{username}".format(
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
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Drop one person's resource-cap overrides

     Removes all four overrides so the host defaults apply again. This can raise or lower what that
    person may create, depending on how their overrides compared to the defaults.

    Idempotent: someone with no overrides answers 204 all the same. The response does not say whether
    anything was actually removed.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
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
) -> Any | ApiError | CliTooOldBody | None:
    """Drop one person's resource-cap overrides

     Removes all four overrides so the host defaults apply again. This can raise or lower what that
    person may create, depending on how their overrides compared to the defaults.

    Idempotent: someone with no overrides answers 204 all the same. The response does not say whether
    anything was actually removed.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Drop one person's resource-cap overrides

     Removes all four overrides so the host defaults apply again. This can raise or lower what that
    person may create, depending on how their overrides compared to the defaults.

    Idempotent: someone with no overrides answers 204 all the same. The response does not say whether
    anything was actually removed.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
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
) -> Any | ApiError | CliTooOldBody | None:
    """Drop one person's resource-cap overrides

     Removes all four overrides so the host defaults apply again. This can raise or lower what that
    person may create, depending on how their overrides compared to the defaults.

    Idempotent: someone with no overrides answers 204 all the same. The response does not say whether
    anything was actually removed.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
