from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admission_status import AdmissionStatus
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/host/capacity-check",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = AdmissionStatus.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

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
) -> Response[AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Host capacity check

     Whether this host currently has room for a new VM of a given shape, as the same capacity report `GET
    /host/capacity` returns, plus per-user quota usage and a ring of recent capacity refusals — both
    currently always empty placeholders, filled in once multi-user capacity-check policy lands.

    Named `getHostCapacityCheck` rather than `getHostAdmission` — the public surface says "capacity
    check" instead of "admission"; the word stays as internal engineering vocabulary (`CapacityChecker`,
    `try_reserve`). `GET /api/host/admission` has been removed, not aliased — it answers 404. Call `GET
    /api/host/capacity-check` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Host capacity check

     Whether this host currently has room for a new VM of a given shape, as the same capacity report `GET
    /host/capacity` returns, plus per-user quota usage and a ring of recent capacity refusals — both
    currently always empty placeholders, filled in once multi-user capacity-check policy lands.

    Named `getHostCapacityCheck` rather than `getHostAdmission` — the public surface says "capacity
    check" instead of "admission"; the word stays as internal engineering vocabulary (`CapacityChecker`,
    `try_reserve`). `GET /api/host/admission` has been removed, not aliased — it answers 404. Call `GET
    /api/host/capacity-check` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody]:
    """Host capacity check

     Whether this host currently has room for a new VM of a given shape, as the same capacity report `GET
    /host/capacity` returns, plus per-user quota usage and a ring of recent capacity refusals — both
    currently always empty placeholders, filled in once multi-user capacity-check policy lands.

    Named `getHostCapacityCheck` rather than `getHostAdmission` — the public surface says "capacity
    check" instead of "admission"; the word stays as internal engineering vocabulary (`CapacityChecker`,
    `try_reserve`). `GET /api/host/admission` has been removed, not aliased — it answers 404. Call `GET
    /api/host/capacity-check` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody | None:
    """Host capacity check

     Whether this host currently has room for a new VM of a given shape, as the same capacity report `GET
    /host/capacity` returns, plus per-user quota usage and a ring of recent capacity refusals — both
    currently always empty placeholders, filled in once multi-user capacity-check policy lands.

    Named `getHostCapacityCheck` rather than `getHostAdmission` — the public surface says "capacity
    check" instead of "admission"; the word stays as internal engineering vocabulary (`CapacityChecker`,
    `try_reserve`). `GET /api/host/admission` has been removed, not aliased — it answers 404. Call `GET
    /api/host/capacity-check` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdmissionStatus | ApiError | CliTooOldBody | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
