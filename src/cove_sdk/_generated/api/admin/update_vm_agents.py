from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.sudo_required_body import SudoRequiredBody
from ...models.update_agents_response import UpdateAgentsResponse
from ...types import File, Response


def _get_kwargs(
    *,
    body: File,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/update-agents",
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse | None:
    if response.status_code == 200:
        response_200 = UpdateAgentsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

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

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: File,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse]:
    """Replace the Cove agent binary inside every running VM

     **Blast radius: every running VM on the host.** The request body is the raw agent binary (a
    statically-linked Linux executable, `application/octet-stream`, no JSON wrapper). Cove pushes those
    exact bytes into every running VM over the host-to-guest channel and restarts the agent there.
    Whatever you upload is what runs, as root, inside every tenant's machine — so this is arbitrary code
    execution across the whole host by design, and the only thing standing between a caller and that is
    the administrator check.

    It also needs a recent interactive login. A CLI caller signed in with a ticket whose login is stale
    is answered 401 `sudo_required` and the CLI re-authenticates and replays; web and REPL sessions get
    that freshness from the SSO step-up. An API key cannot show a recent login, so every key — an admin
    key and a team key included — is answered 401 `sudo_required`, the same body: run this over SSH, in
    the web UI or on the Unix socket.

    Before a single byte is pushed, Cove records who called, the binary's SHA-256 and how many VMs are
    targeted, so an update stays attributable afterwards.

    Per-VM failures do not fail the request: the response is always a per-VM breakdown with `updated` /
    `failed` totals, and a VM whose agent could not be replaced is reported with its error rather than
    rolled back. An agent left mid-update is repaired by pushing a known-good binary again.

    The body limit on the bearer listener is 10 MiB; a larger binary is rejected with 413 before this
    operation runs.

    Args:
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: File,
) -> ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse | None:
    """Replace the Cove agent binary inside every running VM

     **Blast radius: every running VM on the host.** The request body is the raw agent binary (a
    statically-linked Linux executable, `application/octet-stream`, no JSON wrapper). Cove pushes those
    exact bytes into every running VM over the host-to-guest channel and restarts the agent there.
    Whatever you upload is what runs, as root, inside every tenant's machine — so this is arbitrary code
    execution across the whole host by design, and the only thing standing between a caller and that is
    the administrator check.

    It also needs a recent interactive login. A CLI caller signed in with a ticket whose login is stale
    is answered 401 `sudo_required` and the CLI re-authenticates and replays; web and REPL sessions get
    that freshness from the SSO step-up. An API key cannot show a recent login, so every key — an admin
    key and a team key included — is answered 401 `sudo_required`, the same body: run this over SSH, in
    the web UI or on the Unix socket.

    Before a single byte is pushed, Cove records who called, the binary's SHA-256 and how many VMs are
    targeted, so an update stays attributable afterwards.

    Per-VM failures do not fail the request: the response is always a per-VM breakdown with `updated` /
    `failed` totals, and a VM whose agent could not be replaced is reported with its error rather than
    rolled back. An agent left mid-update is repaired by pushing a known-good binary again.

    The body limit on the bearer listener is 10 MiB; a larger binary is rejected with 413 before this
    operation runs.

    Args:
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: File,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse]:
    """Replace the Cove agent binary inside every running VM

     **Blast radius: every running VM on the host.** The request body is the raw agent binary (a
    statically-linked Linux executable, `application/octet-stream`, no JSON wrapper). Cove pushes those
    exact bytes into every running VM over the host-to-guest channel and restarts the agent there.
    Whatever you upload is what runs, as root, inside every tenant's machine — so this is arbitrary code
    execution across the whole host by design, and the only thing standing between a caller and that is
    the administrator check.

    It also needs a recent interactive login. A CLI caller signed in with a ticket whose login is stale
    is answered 401 `sudo_required` and the CLI re-authenticates and replays; web and REPL sessions get
    that freshness from the SSO step-up. An API key cannot show a recent login, so every key — an admin
    key and a team key included — is answered 401 `sudo_required`, the same body: run this over SSH, in
    the web UI or on the Unix socket.

    Before a single byte is pushed, Cove records who called, the binary's SHA-256 and how many VMs are
    targeted, so an update stays attributable afterwards.

    Per-VM failures do not fail the request: the response is always a per-VM breakdown with `updated` /
    `failed` totals, and a VM whose agent could not be replaced is reported with its error rather than
    rolled back. An agent left mid-update is repaired by pushing a known-good binary again.

    The body limit on the bearer listener is 10 MiB; a larger binary is rejected with 413 before this
    operation runs.

    Args:
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: File,
) -> ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse | None:
    """Replace the Cove agent binary inside every running VM

     **Blast radius: every running VM on the host.** The request body is the raw agent binary (a
    statically-linked Linux executable, `application/octet-stream`, no JSON wrapper). Cove pushes those
    exact bytes into every running VM over the host-to-guest channel and restarts the agent there.
    Whatever you upload is what runs, as root, inside every tenant's machine — so this is arbitrary code
    execution across the whole host by design, and the only thing standing between a caller and that is
    the administrator check.

    It also needs a recent interactive login. A CLI caller signed in with a ticket whose login is stale
    is answered 401 `sudo_required` and the CLI re-authenticates and replays; web and REPL sessions get
    that freshness from the SSO step-up. An API key cannot show a recent login, so every key — an admin
    key and a team key included — is answered 401 `sudo_required`, the same body: run this over SSH, in
    the web UI or on the Unix socket.

    Before a single byte is pushed, Cove records who called, the binary's SHA-256 and how many VMs are
    targeted, so an update stays attributable afterwards.

    Per-VM failures do not fail the request: the response is always a per-VM breakdown with `updated` /
    `failed` totals, and a VM whose agent could not be replaced is reported with its error rather than
    rolled back. An agent left mid-update is repaired by pushing a known-good binary again.

    The body limit on the bearer listener is 10 MiB; a larger binary is rejected with 413 before this
    operation runs.

    Args:
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | UpdateAgentsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
