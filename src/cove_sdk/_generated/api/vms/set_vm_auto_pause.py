from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.update_auto_pause_request import UpdateAutoPauseRequest
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: UpdateAutoPauseRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/auto-pause".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateAutoPauseRequest,
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Set the auto-pause policy

     Replaces the VM's auto-pause policy — `always_on`, or `auto_pause` with an idle timeout. Takes
    effect immediately for the running idle-detector.

    Auto-pause **pauses** the VM: scheduling stops but the guest's memory stays resident on the host, so
    it resumes instantly on the next packet. It does not hibernate the VM and does not free any RAM —
    which is why it is no longer called `auto-suspend`. `{"type":"auto_suspend"}` has been removed, not
    aliased — it is rejected as an unrecognised policy type. Send `{"type":"auto_pause"}` instead.

    Args:
        name (str):
        body (UpdateAutoPauseRequest): POST /vms/{name}/auto-pause request body (was
            `/vms/{name}/suspend-policy`, and was named `UpdateSuspendPolicyRequest`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateAutoPauseRequest,
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Set the auto-pause policy

     Replaces the VM's auto-pause policy — `always_on`, or `auto_pause` with an idle timeout. Takes
    effect immediately for the running idle-detector.

    Auto-pause **pauses** the VM: scheduling stops but the guest's memory stays resident on the host, so
    it resumes instantly on the next packet. It does not hibernate the VM and does not free any RAM —
    which is why it is no longer called `auto-suspend`. `{"type":"auto_suspend"}` has been removed, not
    aliased — it is rejected as an unrecognised policy type. Send `{"type":"auto_pause"}` instead.

    Args:
        name (str):
        body (UpdateAutoPauseRequest): POST /vms/{name}/auto-pause request body (was
            `/vms/{name}/suspend-policy`, and was named `UpdateSuspendPolicyRequest`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateAutoPauseRequest,
) -> Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Set the auto-pause policy

     Replaces the VM's auto-pause policy — `always_on`, or `auto_pause` with an idle timeout. Takes
    effect immediately for the running idle-detector.

    Auto-pause **pauses** the VM: scheduling stops but the guest's memory stays resident on the host, so
    it resumes instantly on the next packet. It does not hibernate the VM and does not free any RAM —
    which is why it is no longer called `auto-suspend`. `{"type":"auto_suspend"}` has been removed, not
    aliased — it is rejected as an unrecognised policy type. Send `{"type":"auto_pause"}` instead.

    Args:
        name (str):
        body (UpdateAutoPauseRequest): POST /vms/{name}/auto-pause request body (was
            `/vms/{name}/suspend-policy`, and was named `UpdateSuspendPolicyRequest`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateAutoPauseRequest,
) -> Any | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Set the auto-pause policy

     Replaces the VM's auto-pause policy — `always_on`, or `auto_pause` with an idle timeout. Takes
    effect immediately for the running idle-detector.

    Auto-pause **pauses** the VM: scheduling stops but the guest's memory stays resident on the host, so
    it resumes instantly on the next packet. It does not hibernate the VM and does not free any RAM —
    which is why it is no longer called `auto-suspend`. `{"type":"auto_suspend"}` has been removed, not
    aliased — it is rejected as an unrecognised policy type. Send `{"type":"auto_pause"}` instead.

    Args:
        name (str):
        body (UpdateAutoPauseRequest): POST /vms/{name}/auto-pause request body (was
            `/vms/{name}/suspend-policy`, and was named `UpdateSuspendPolicyRequest`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
