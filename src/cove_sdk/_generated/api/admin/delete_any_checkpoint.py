from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/admin/checkpoints/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ApiError | SudoRequiredBody | CliTooOldBody | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ApiError.from_dict(response.json())

        return response_409

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
) -> Response[Any | ApiError | SudoRequiredBody | CliTooOldBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | SudoRequiredBody | CliTooOldBody]:
    """Delete any checkpoint, whoever owns it

     Deletes one checkpoint by id regardless of who owns it, including one whose source VM has been
    deleted and which therefore appears in nobody's per-caller listing. `deleteCheckpoint` is the per-
    caller equivalent and only reaches your own.

    **Irreversible, and bounded to the one checkpoint named.** The same safety checks the owner's own
    delete goes through still apply: a checkpoint a live clone still depends on, or one with a restore
    in flight, is refused 409 rather than removed. Only the ownership requirement is lifted.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | ApiError | SudoRequiredBody | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | SudoRequiredBody | CliTooOldBody | None:
    """Delete any checkpoint, whoever owns it

     Deletes one checkpoint by id regardless of who owns it, including one whose source VM has been
    deleted and which therefore appears in nobody's per-caller listing. `deleteCheckpoint` is the per-
    caller equivalent and only reaches your own.

    **Irreversible, and bounded to the one checkpoint named.** The same safety checks the owner's own
    delete goes through still apply: a checkpoint a live clone still depends on, or one with a restore
    in flight, is refused 409 rather than removed. Only the ownership requirement is lifted.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | ApiError | SudoRequiredBody | CliTooOldBody
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ApiError | SudoRequiredBody | CliTooOldBody]:
    """Delete any checkpoint, whoever owns it

     Deletes one checkpoint by id regardless of who owns it, including one whose source VM has been
    deleted and which therefore appears in nobody's per-caller listing. `deleteCheckpoint` is the per-
    caller equivalent and only reaches your own.

    **Irreversible, and bounded to the one checkpoint named.** The same safety checks the owner's own
    delete goes through still apply: a checkpoint a live clone still depends on, or one with a restore
    in flight, is refused 409 rather than removed. Only the ownership requirement is lifted.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ApiError | ApiError | SudoRequiredBody | CliTooOldBody]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ApiError | SudoRequiredBody | CliTooOldBody | None:
    """Delete any checkpoint, whoever owns it

     Deletes one checkpoint by id regardless of who owns it, including one whose source VM has been
    deleted and which therefore appears in nobody's per-caller listing. `deleteCheckpoint` is the per-
    caller equivalent and only reaches your own.

    **Irreversible, and bounded to the one checkpoint named.** The same safety checks the owner's own
    delete goes through still apply: a checkpoint a live clone still depends on, or one with a restore
    in flight, is refused 409 rather than removed. Only the ownership requirement is lifted.

    A CLI caller signed in with a ticket needs a recent interactive login for this operation; a stale
    one is answered 401 `sudo_required` and the CLI re-authenticates and replays. Web and REPL sessions
    get that freshness from the SSO step-up instead. An API key cannot show a recent login, so every key
    — an admin key and a team key included — is answered 401 `sudo_required`, the same body: run this
    over SSH, in the web UI or on the Unix socket.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ApiError | ApiError | SudoRequiredBody | CliTooOldBody
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
