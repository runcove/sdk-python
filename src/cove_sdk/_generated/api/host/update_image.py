from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.image_update import ImageUpdate
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/images/update",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ImageUpdate | None:
    if response.status_code == 200:
        response_200 = ImageUpdate.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = ImageUpdate.from_dict(response.json())

        return response_202

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ApiError.from_dict(response.json())

        return response_409

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ImageUpdate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ImageUpdate]:
    """Update a Mac's VM image (local mode)

     Local mode on a Mac: start an update of the box (the VM image) to the one the daemon would fetch now
    (`[image] mac_box_url`, else the build's), or join the update already running. Updates are never
    automatic. The box is downloaded beside the installed one (refused unless the disk has the larger of
    twice the download plus 10 GiB, and the new box's full-size disk plus the download plus 10 GiB,
    free), then switched to in one step once no create of its image is under way. Existing VMs keep
    running and keep booting the kernel of the box they were made from; only VMs made afterwards use the
    new box. The answer is `local.image_update` as `GET /api/system/status` then reports it: poll that
    for the progress (`stage`, `message`, `transfer`) and the outcome.

    Not served on the external bearer-key listener: a Mac has none, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ImageUpdate]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ImageUpdate | None:
    """Update a Mac's VM image (local mode)

     Local mode on a Mac: start an update of the box (the VM image) to the one the daemon would fetch now
    (`[image] mac_box_url`, else the build's), or join the update already running. Updates are never
    automatic. The box is downloaded beside the installed one (refused unless the disk has the larger of
    twice the download plus 10 GiB, and the new box's full-size disk plus the download plus 10 GiB,
    free), then switched to in one step once no create of its image is under way. Existing VMs keep
    running and keep booting the kernel of the box they were made from; only VMs made afterwards use the
    new box. The answer is `local.image_update` as `GET /api/system/status` then reports it: poll that
    for the progress (`stage`, `message`, `transfer`) and the outcome.

    Not served on the external bearer-key listener: a Mac has none, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ImageUpdate
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiError | CliTooOldBody | ImageUpdate]:
    """Update a Mac's VM image (local mode)

     Local mode on a Mac: start an update of the box (the VM image) to the one the daemon would fetch now
    (`[image] mac_box_url`, else the build's), or join the update already running. Updates are never
    automatic. The box is downloaded beside the installed one (refused unless the disk has the larger of
    twice the download plus 10 GiB, and the new box's full-size disk plus the download plus 10 GiB,
    free), then switched to in one step once no create of its image is under way. Existing VMs keep
    running and keep booting the kernel of the box they were made from; only VMs made afterwards use the
    new box. The answer is `local.image_update` as `GET /api/system/status` then reports it: poll that
    for the progress (`stage`, `message`, `transfer`) and the outcome.

    Not served on the external bearer-key listener: a Mac has none, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ImageUpdate]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ApiError | CliTooOldBody | ImageUpdate | None:
    """Update a Mac's VM image (local mode)

     Local mode on a Mac: start an update of the box (the VM image) to the one the daemon would fetch now
    (`[image] mac_box_url`, else the build's), or join the update already running. Updates are never
    automatic. The box is downloaded beside the installed one (refused unless the disk has the larger of
    twice the download plus 10 GiB, and the new box's full-size disk plus the download plus 10 GiB,
    free), then switched to in one step once no create of its image is under way. Existing VMs keep
    running and keep booting the kernel of the box they were made from; only VMs made afterwards use the
    new box. The answer is `local.image_update` as `GET /api/system/status` then reports it: poll that
    for the progress (`stage`, `message`, `transfer`) and the outcome.

    Not served on the external bearer-key listener: a Mac has none, so it carries no `x-required-scope`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ImageUpdate
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
