from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_retimeout_request import AdminRetimeoutRequest
from ...models.admin_retimeout_response import AdminRetimeoutResponse
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    *,
    body: AdminRetimeoutRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/auto-pause/retimeout",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdminRetimeoutResponse | ApiError | CliTooOldBody | None:
    if response.status_code == 200:
        response_200 = AdminRetimeoutResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiError.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = ApiError.from_dict(response.json())

        return response_422

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
) -> Response[AdminRetimeoutResponse | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AdminRetimeoutRequest,
) -> Response[AdminRetimeoutResponse | ApiError | CliTooOldBody]:
    """Re-apply the idle timeout across every auto-pausing VM

     Rewrites the idle timeout on every VM configured to pause itself when idle, in one pass. `to_secs`
    sets the new value; omit it to use the host's configured default. `from_secs` narrows the change to
    VMs currently sitting on that exact value, which is how you migrate one cohort without disturbing
    operators who picked their own number.

    Send `dry_run: true` first. The response is identical either way — the same `changed` and
    `skipped_custom` lists, the same `by_current_value` spread of how many VMs sit on each timeout today
    — so a dry run tells you exactly what a real run would do. Only `dry_run: false` writes.

    `skipped_custom` names the VMs a filtered run left alone. Every VM that is changed gets its own
    record of the change.

    Args:
        body (AdminRetimeoutRequest): `POST /admin/auto-pause/retimeout` request body. Filters and
            target for
            the bulk-rewrite of the idle timeout across every existing auto-pausing VM.

            * `from_secs` — when `Some(F)`, only flip rows whose current
              `idle_timeout_secs == F`. When `None`, flip every auto-pausing row
              whose current value differs from the resolved target.
            * `to_secs` — when `Some(T)`, target value. When `None`, the server uses
              `[auto_pause] default_idle_timeout_secs` from `cove.toml`.
            * `dry_run` — when `true`, the response describes the change set without
              mutating any rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminRetimeoutResponse | ApiError | CliTooOldBody]
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
    body: AdminRetimeoutRequest,
) -> AdminRetimeoutResponse | ApiError | CliTooOldBody | None:
    """Re-apply the idle timeout across every auto-pausing VM

     Rewrites the idle timeout on every VM configured to pause itself when idle, in one pass. `to_secs`
    sets the new value; omit it to use the host's configured default. `from_secs` narrows the change to
    VMs currently sitting on that exact value, which is how you migrate one cohort without disturbing
    operators who picked their own number.

    Send `dry_run: true` first. The response is identical either way — the same `changed` and
    `skipped_custom` lists, the same `by_current_value` spread of how many VMs sit on each timeout today
    — so a dry run tells you exactly what a real run would do. Only `dry_run: false` writes.

    `skipped_custom` names the VMs a filtered run left alone. Every VM that is changed gets its own
    record of the change.

    Args:
        body (AdminRetimeoutRequest): `POST /admin/auto-pause/retimeout` request body. Filters and
            target for
            the bulk-rewrite of the idle timeout across every existing auto-pausing VM.

            * `from_secs` — when `Some(F)`, only flip rows whose current
              `idle_timeout_secs == F`. When `None`, flip every auto-pausing row
              whose current value differs from the resolved target.
            * `to_secs` — when `Some(T)`, target value. When `None`, the server uses
              `[auto_pause] default_idle_timeout_secs` from `cove.toml`.
            * `dry_run` — when `true`, the response describes the change set without
              mutating any rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminRetimeoutResponse | ApiError | CliTooOldBody
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AdminRetimeoutRequest,
) -> Response[AdminRetimeoutResponse | ApiError | CliTooOldBody]:
    """Re-apply the idle timeout across every auto-pausing VM

     Rewrites the idle timeout on every VM configured to pause itself when idle, in one pass. `to_secs`
    sets the new value; omit it to use the host's configured default. `from_secs` narrows the change to
    VMs currently sitting on that exact value, which is how you migrate one cohort without disturbing
    operators who picked their own number.

    Send `dry_run: true` first. The response is identical either way — the same `changed` and
    `skipped_custom` lists, the same `by_current_value` spread of how many VMs sit on each timeout today
    — so a dry run tells you exactly what a real run would do. Only `dry_run: false` writes.

    `skipped_custom` names the VMs a filtered run left alone. Every VM that is changed gets its own
    record of the change.

    Args:
        body (AdminRetimeoutRequest): `POST /admin/auto-pause/retimeout` request body. Filters and
            target for
            the bulk-rewrite of the idle timeout across every existing auto-pausing VM.

            * `from_secs` — when `Some(F)`, only flip rows whose current
              `idle_timeout_secs == F`. When `None`, flip every auto-pausing row
              whose current value differs from the resolved target.
            * `to_secs` — when `Some(T)`, target value. When `None`, the server uses
              `[auto_pause] default_idle_timeout_secs` from `cove.toml`.
            * `dry_run` — when `true`, the response describes the change set without
              mutating any rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminRetimeoutResponse | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AdminRetimeoutRequest,
) -> AdminRetimeoutResponse | ApiError | CliTooOldBody | None:
    """Re-apply the idle timeout across every auto-pausing VM

     Rewrites the idle timeout on every VM configured to pause itself when idle, in one pass. `to_secs`
    sets the new value; omit it to use the host's configured default. `from_secs` narrows the change to
    VMs currently sitting on that exact value, which is how you migrate one cohort without disturbing
    operators who picked their own number.

    Send `dry_run: true` first. The response is identical either way — the same `changed` and
    `skipped_custom` lists, the same `by_current_value` spread of how many VMs sit on each timeout today
    — so a dry run tells you exactly what a real run would do. Only `dry_run: false` writes.

    `skipped_custom` names the VMs a filtered run left alone. Every VM that is changed gets its own
    record of the change.

    Args:
        body (AdminRetimeoutRequest): `POST /admin/auto-pause/retimeout` request body. Filters and
            target for
            the bulk-rewrite of the idle timeout across every existing auto-pausing VM.

            * `from_secs` — when `Some(F)`, only flip rows whose current
              `idle_timeout_secs == F`. When `None`, flip every auto-pausing row
              whose current value differs from the resolved target.
            * `to_secs` — when `Some(T)`, target value. When `None`, the server uses
              `[auto_pause] default_idle_timeout_secs` from `cove.toml`.
            * `dry_run` — when `true`, the response describes the change set without
              mutating any rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminRetimeoutResponse | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
