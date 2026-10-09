from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.rotate_summary import RotateSummary
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.set_secret_request import SetSecretRequest
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    name: str,
    key: str,
    *,
    body: SetSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/teams/{name}/secrets/{key}/rotate".format(
            name=quote(str(name), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody | None
):
    if response.status_code == 200:
        response_200 = RotateSummary.from_dict(response.json())

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
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
]:
    """Rotate a team-scoped secret (acked push)

     Unlike `POST /teams/{name}/secrets/{key}`, this goes through the same acked Push engine as the per-
    VM rotate — it delivers to every running VM owned by a team member immediately and waits for each
    guest to acknowledge, reporting the confirmed count rather than a best-effort one. ACL is member-or-
    admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Needs a fresh login, as a per-VM set does, because a scoped secret reaches every VM in its scope: on
    the daemon socket and the bastion-fronted listener a caller whose CLI login is older than the re-
    auth window gets **401** `sudo_required` and signs in again (the CLI does this itself). API keys are
    exempt, as on the per-VM set.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        key=key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> (
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody | None
):
    """Rotate a team-scoped secret (acked push)

     Unlike `POST /teams/{name}/secrets/{key}`, this goes through the same acked Push engine as the per-
    VM rotate — it delivers to every running VM owned by a team member immediately and waits for each
    guest to acknowledge, reporting the confirmed count rather than a best-effort one. ACL is member-or-
    admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Needs a fresh login, as a per-VM set does, because a scoped secret reaches every VM in its scope: on
    the daemon socket and the bastion-fronted listener a caller whose CLI login is older than the re-
    auth window gets **401** `sudo_required` and signs in again (the CLI does this itself). API keys are
    exempt, as on the per-VM set.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        key=key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
]:
    """Rotate a team-scoped secret (acked push)

     Unlike `POST /teams/{name}/secrets/{key}`, this goes through the same acked Push engine as the per-
    VM rotate — it delivers to every running VM owned by a team member immediately and waits for each
    guest to acknowledge, reporting the confirmed count rather than a best-effort one. ACL is member-or-
    admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Needs a fresh login, as a per-VM set does, because a scoped secret reaches every VM in its scope: on
    the daemon socket and the bastion-fronted listener a caller whose CLI login is older than the re-
    auth window gets **401** `sudo_required` and signs in again (the CLI does this itself). API keys are
    exempt, as on the per-VM set.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        key=key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> (
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody | None
):
    """Rotate a team-scoped secret (acked push)

     Unlike `POST /teams/{name}/secrets/{key}`, this goes through the same acked Push engine as the per-
    VM rotate — it delivers to every running VM owned by a team member immediately and waits for each
    guest to acknowledge, reporting the confirmed count rather than a best-effort one. ACL is member-or-
    admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Needs a fresh login, as a per-VM set does, because a scoped secret reaches every VM in its scope: on
    the daemon socket and the bastion-fronted listener a caller whose CLI login is older than the re-
    auth window gets **401** `sudo_required` and signs in again (the CLI does this itself). API keys are
    exempt, as on the per-VM set.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            key=key,
            client=client,
            body=body,
        )
    ).parsed
