from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.set_secret_request import SetSecretRequest
from ...models.vm_count_result import VmCountResult
from ...types import Response


def _get_kwargs(
    project_id: str,
    key: str,
    *,
    body: SetSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/projects/{project_id}/secrets/{key}".format(
            project_id=quote(str(project_id), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult | None:
    if response.status_code == 200:
        response_200 = VmCountResult.from_dict(response.json())

        return response_200

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

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult]:
    """Set a project-scoped secret

     Insert-or-overwrite on the project scope. Best-effort fans out to every RUNNING VM tagged into the
    project (owner must still be a current project member — re-verified fresh, not cached) immediately,
    in addition to the usual event-driven reinject on each VM's next lifecycle event — the response's
    `vm_count` reports how many running VMs the fan-out reached, with no ack guarantee (contrast
    `rotate`, below, which acks). ACL is member-or-admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        project_id (str):
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
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        key=key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult | None:
    """Set a project-scoped secret

     Insert-or-overwrite on the project scope. Best-effort fans out to every RUNNING VM tagged into the
    project (owner must still be a current project member — re-verified fresh, not cached) immediately,
    in addition to the usual event-driven reinject on each VM's next lifecycle event — the response's
    `vm_count` reports how many running VMs the fan-out reached, with no ack guarantee (contrast
    `rotate`, below, which acks). ACL is member-or-admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        project_id (str):
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
        ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult
    """

    return sync_detailed(
        project_id=project_id,
        key=key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult]:
    """Set a project-scoped secret

     Insert-or-overwrite on the project scope. Best-effort fans out to every RUNNING VM tagged into the
    project (owner must still be a current project member — re-verified fresh, not cached) immediately,
    in addition to the usual event-driven reinject on each VM's next lifecycle event — the response's
    `vm_count` reports how many running VMs the fan-out reached, with no ack guarantee (contrast
    `rotate`, below, which acks). ACL is member-or-admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        project_id (str):
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
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        key=key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult | None:
    """Set a project-scoped secret

     Insert-or-overwrite on the project scope. Best-effort fans out to every RUNNING VM tagged into the
    project (owner must still be a current project member — re-verified fresh, not cached) immediately,
    in addition to the usual event-driven reinject on each VM's next lifecycle event — the response's
    `vm_count` reports how many running VMs the fan-out reached, with no ack guarantee (contrast
    `rotate`, below, which acks). ACL is member-or-admin.

    An API key needs MORE than `secrets:write` to reach a principal it is not. The admin half of the ACL
    above is gated on the key's own grants: writing another user's secrets, or those of a team or
    project the caller is not a member of, requires `admin:secrets:write` IN ADDITION to the
    `secrets:write` this route demands. A key without it gets the same **404** as a stranger, not a 403
    — the refusal must not confirm that the principal exists. Writing your own scope, or one you are a
    member of, needs only `secrets:write`. Interactive sessions (SSH, web, unix socket) carry no scope
    list and are unaffected.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`.

    Args:
        project_id (str):
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
        ApiError | CliTooOldBody | ScopeDeniedBody | VmCountResult
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            key=key,
            client=client,
            body=body,
        )
    ).parsed
