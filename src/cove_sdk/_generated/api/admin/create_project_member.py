from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_project_member_request import AdminProjectMemberRequest
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    body: AdminProjectMemberRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/projects/{project_id}/members".format(
            project_id=quote(str(project_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | CliTooOldBody | None:
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
) -> Response[Any | ApiError | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminProjectMemberRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Add someone to a project

     **This is an access grant, not bookkeeping.** A project is the scope a set of secrets belongs to, so
    adding someone to a project lets them read and write every secret in it. Membership is re-checked on
    every secret access, so the grant takes effect immediately and revoking it takes effect immediately
    too.

    Idempotent: adding an existing member succeeds and records nothing new. A plain username is not
    checked against any account — a project may name someone who has never signed in, and the grant
    applies on their first login. A service key (`svc:<name>`) is accepted only while its binding is
    live; its own VMs then receive the project's secrets. A team (`team:<slug>`) is accepted. Any other
    name must be a valid user name: one that is empty, longer than 255 bytes, has leading or trailing
    whitespace, has a character outside printable ASCII or one of `<`, `>`, `:`, `/`, `\\`, or is the
    reserved `<public>`, is refused with 422. The `project_id` in the body is **ignored**; the path
    parameter is authoritative.

    A project needs no separate creation step: naming one here is what brings it into existence.

    Args:
        project_id (str):
        body (AdminProjectMemberRequest): `POST /admin/projects/{project_id}/members` request
            body.

            `project_id` is redundant with the path parameter and is **ignored** by the
            server — the handler uses the path value. Kept on the wire for
            compatibility with existing clients that send it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminProjectMemberRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Add someone to a project

     **This is an access grant, not bookkeeping.** A project is the scope a set of secrets belongs to, so
    adding someone to a project lets them read and write every secret in it. Membership is re-checked on
    every secret access, so the grant takes effect immediately and revoking it takes effect immediately
    too.

    Idempotent: adding an existing member succeeds and records nothing new. A plain username is not
    checked against any account — a project may name someone who has never signed in, and the grant
    applies on their first login. A service key (`svc:<name>`) is accepted only while its binding is
    live; its own VMs then receive the project's secrets. A team (`team:<slug>`) is accepted. Any other
    name must be a valid user name: one that is empty, longer than 255 bytes, has leading or trailing
    whitespace, has a character outside printable ASCII or one of `<`, `>`, `:`, `/`, `\\`, or is the
    reserved `<public>`, is refused with 422. The `project_id` in the body is **ignored**; the path
    parameter is authoritative.

    A project needs no separate creation step: naming one here is what brings it into existence.

    Args:
        project_id (str):
        body (AdminProjectMemberRequest): `POST /admin/projects/{project_id}/members` request
            body.

            `project_id` is redundant with the path parameter and is **ignored** by the
            server — the handler uses the path value. Kept on the wire for
            compatibility with existing clients that send it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminProjectMemberRequest,
) -> Response[Any | ApiError | CliTooOldBody]:
    """Add someone to a project

     **This is an access grant, not bookkeeping.** A project is the scope a set of secrets belongs to, so
    adding someone to a project lets them read and write every secret in it. Membership is re-checked on
    every secret access, so the grant takes effect immediately and revoking it takes effect immediately
    too.

    Idempotent: adding an existing member succeeds and records nothing new. A plain username is not
    checked against any account — a project may name someone who has never signed in, and the grant
    applies on their first login. A service key (`svc:<name>`) is accepted only while its binding is
    live; its own VMs then receive the project's secrets. A team (`team:<slug>`) is accepted. Any other
    name must be a valid user name: one that is empty, longer than 255 bytes, has leading or trailing
    whitespace, has a character outside printable ASCII or one of `<`, `>`, `:`, `/`, `\\`, or is the
    reserved `<public>`, is refused with 422. The `project_id` in the body is **ignored**; the path
    parameter is authoritative.

    A project needs no separate creation step: naming one here is what brings it into existence.

    Args:
        project_id (str):
        body (AdminProjectMemberRequest): `POST /admin/projects/{project_id}/members` request
            body.

            `project_id` is redundant with the path parameter and is **ignored** by the
            server — the handler uses the path value. Kept on the wire for
            compatibility with existing clients that send it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AdminProjectMemberRequest,
) -> Any | ApiError | CliTooOldBody | None:
    """Add someone to a project

     **This is an access grant, not bookkeeping.** A project is the scope a set of secrets belongs to, so
    adding someone to a project lets them read and write every secret in it. Membership is re-checked on
    every secret access, so the grant takes effect immediately and revoking it takes effect immediately
    too.

    Idempotent: adding an existing member succeeds and records nothing new. A plain username is not
    checked against any account — a project may name someone who has never signed in, and the grant
    applies on their first login. A service key (`svc:<name>`) is accepted only while its binding is
    live; its own VMs then receive the project's secrets. A team (`team:<slug>`) is accepted. Any other
    name must be a valid user name: one that is empty, longer than 255 bytes, has leading or trailing
    whitespace, has a character outside printable ASCII or one of `<`, `>`, `:`, `/`, `\\`, or is the
    reserved `<public>`, is refused with 422. The `project_id` in the body is **ignored**; the path
    parameter is authoritative.

    A project needs no separate creation step: naming one here is what brings it into existence.

    Args:
        project_id (str):
        body (AdminProjectMemberRequest): `POST /admin/projects/{project_id}/members` request
            body.

            `project_id` is redundant with the path parameter and is **ignored** by the
            server — the handler uses the path value. Kept on the wire for
            compatibility with existing clients that send it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
