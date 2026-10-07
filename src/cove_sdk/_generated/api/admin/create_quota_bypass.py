from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_force_create_response import AdminForceCreateResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    username: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/quotas/{username}/force-create".format(
            username=quote(str(username), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminForceCreateResponse | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminForceCreateResponse.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AdminForceCreateResponse | ApiError | CliTooOldBody]:
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
) -> Response[AdminForceCreateResponse | ApiError | CliTooOldBody]:
    """Let someone exceed their resource caps once

     Issues a single-use pass that lets one person's next VM creation go ahead even though it would
    otherwise be refused for exceeding their caps. The response names the pass, who granted it and when.

    The pass is spent only if it is needed: the real cap check still runs first, and a creation that
    fits leaves the pass waiting for a later attempt. It is spent by whichever creation first needs it,
    so it is not tied to a particular VM, size or image.

    Each call issues another pass; there is no way to list or withdraw one through the API. Two
    outstanding passes cover two refused creations.

    It bypasses **caps only** — the host's real capacity checks still apply, so a pass cannot conjure
    memory or disk the machine does not have. If the person's next creation is charged to a team, the
    pass is spent against the team's caps even though the pass belongs to the person.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminForceCreateResponse | ApiError | CliTooOldBody]
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
) -> AdminForceCreateResponse | ApiError | CliTooOldBody | None:
    """Let someone exceed their resource caps once

     Issues a single-use pass that lets one person's next VM creation go ahead even though it would
    otherwise be refused for exceeding their caps. The response names the pass, who granted it and when.

    The pass is spent only if it is needed: the real cap check still runs first, and a creation that
    fits leaves the pass waiting for a later attempt. It is spent by whichever creation first needs it,
    so it is not tied to a particular VM, size or image.

    Each call issues another pass; there is no way to list or withdraw one through the API. Two
    outstanding passes cover two refused creations.

    It bypasses **caps only** — the host's real capacity checks still apply, so a pass cannot conjure
    memory or disk the machine does not have. If the person's next creation is charged to a team, the
    pass is spent against the team's caps even though the pass belongs to the person.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminForceCreateResponse | ApiError | CliTooOldBody
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminForceCreateResponse | ApiError | CliTooOldBody]:
    """Let someone exceed their resource caps once

     Issues a single-use pass that lets one person's next VM creation go ahead even though it would
    otherwise be refused for exceeding their caps. The response names the pass, who granted it and when.

    The pass is spent only if it is needed: the real cap check still runs first, and a creation that
    fits leaves the pass waiting for a later attempt. It is spent by whichever creation first needs it,
    so it is not tied to a particular VM, size or image.

    Each call issues another pass; there is no way to list or withdraw one through the API. Two
    outstanding passes cover two refused creations.

    It bypasses **caps only** — the host's real capacity checks still apply, so a pass cannot conjure
    memory or disk the machine does not have. If the person's next creation is charged to a team, the
    pass is spent against the team's caps even though the pass belongs to the person.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminForceCreateResponse | ApiError | CliTooOldBody]
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
) -> AdminForceCreateResponse | ApiError | CliTooOldBody | None:
    """Let someone exceed their resource caps once

     Issues a single-use pass that lets one person's next VM creation go ahead even though it would
    otherwise be refused for exceeding their caps. The response names the pass, who granted it and when.

    The pass is spent only if it is needed: the real cap check still runs first, and a creation that
    fits leaves the pass waiting for a later attempt. It is spent by whichever creation first needs it,
    so it is not tied to a particular VM, size or image.

    Each call issues another pass; there is no way to list or withdraw one through the API. Two
    outstanding passes cover two refused creations.

    It bypasses **caps only** — the host's real capacity checks still apply, so a pass cannot conjure
    memory or disk the machine does not have. If the person's next creation is charged to a team, the
    pass is spent against the team's caps even though the pass belongs to the person.

    Args:
        username (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminForceCreateResponse | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
