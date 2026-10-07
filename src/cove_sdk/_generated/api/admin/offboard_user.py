from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.offboard_user_report import OffboardUserReport
from ...models.offboard_user_request import OffboardUserRequest
from ...models.sudo_required_body import SudoRequiredBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    username: str,
    *,
    body: OffboardUserRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/users/{username}/offboard".format(
            username=quote(str(username), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport | None:
    if response.status_code == 200:
        response_200 = OffboardUserReport.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

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
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport]:
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
    body: OffboardUserRequest | Unset = UNSET,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport]:
    """Offboard one person

     Ends everything one person holds in Cove and reports each item. First, in one transaction: every CLI
    session, connected app and service key bound to them, every direct share to them on any VM (their
    Warpgate access to it is then dropped, retried until Warpgate confirms it), every personal and admin
    API key they own, and every webhook subscription they own, of any scope, which is disabled with
    reason `owner-offboarded` (its deliveries not yet sent are dropped, and it cannot be re-enabled,
    changed or replayed). A CLI session Warpgate cannot delete still works: it is listed in
    `cli_sessions_failed`, a failed item. If any of the Cove-side changes fails, none of it lands and
    the call fails. Only an administrator can offboard, and only a person: a `svc:` or `team:` name is
    404. Then, one item at a time: first Cove's own Warpgate role for them (the one Cove binds to their
    VMs' targets) is deleted (`warpgate_role`), which unbinds those targets; the targets stay, and no
    other role is touched, even one whose only member is them. No such role is `not_found`, and a role
    that could not be found or deleted is a failed item. Next their Warpgate user is deleted
    (`warpgate_user`), which takes their Warpgate roles, user API tokens, passwords, one-time codes and
    certificates with it, each of which signs in without the identity provider; Warpgate having no such
    user is reported as `not_found`, not a failure, and a user that could not be found or deleted is a
    failed item (delete it in Warpgate, then run the call again); so is, deleting nothing, the user that
    owns Cove's own Warpgate token, or a name several users share regardless of case. Then, belt and
    braces, every SSH public key of theirs at Warpgate is deleted (`ssh_keys_deleted`), every Warpgate
    ticket in their name, whatever minted it, is deleted (`tickets_deleted`), and every live Warpgate
    session of theirs is closed, on every target: the shell, the web UI and each VM (`sessions_closed`),
    since a key or a ticket signs in without the identity provider and an open session never asks it
    again. A session open until the close could add a key or mint a ticket, so keys, tickets and
    sessions are handled again until a pass finds nothing new, three passes at most; every pass's items
    are reported, and a list still finding new ones in the third pass gets a failed `*` entry. The
    credential step then runs once more, so a key, webhook or share such a session created in between is
    ended and reported too; if that sweep fails, `second_sweep_error` says why, a failed item. Then they
    are removed from every team they belong to, every secret in their own (user) scope is deleted (team,
    project and VM secrets stay with the team, project or VM), and every VM they own is stopped, under
    its lifecycle lock and as read again under it: one in the middle of a transition then is not touched
    and is a failed item. VMs are never deleted or reassigned. On a host with the secrets feature off,
    the secrets entry is one failed item (`name` `*`, `secrets feature disabled; nothing deleted`). A
    failure of one of these items is reported in its entry and does not stop the others, so the response
    is 200 even when some items failed; run the call again to retry them. A failed item is an entry with
    `ok` false, a VM whose `outcome` is `failed`, a `warpgate_role` or `warpgate_user` whose `outcome`
    is `failed`, any `cli_sessions_failed` entry, or a `second_sweep_error`.

    With `{"dry_run": true}` the response is the same report and nothing is changed: no record, no write
    to Warpgate (it only names the Warpgate role and user it would delete and lists their keys, tickets
    and sessions), no VM stopped. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else (no `dry_run`, a non-boolean one, another field, a non-object, a
    body without a JSON content type) is 400 `validation_failed` and nothing runs. Every call, the dry
    run included, writes one `user.offboarded` audit row: the administrator, the sudo context, the size
    of each list, the Warpgate ids ended and the number of failed items.

    Signing in through the identity provider again gives the person a new Warpgate user, and while they
    own VMs Cove re-creates its role for them whenever it next sets up access to one (at its next start,
    say), so remove them from the identity provider too and reassign or delete their VMs. `POST
    /api/admin/users/{username}/revoke-sessions` is the credential-only subset.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (OffboardUserRequest | Unset): `POST /api/admin/users/{username}/offboard` request
            body. An absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real offboarding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport]
    """

    kwargs = _get_kwargs(
        username=username,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: OffboardUserRequest | Unset = UNSET,
) -> ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport | None:
    """Offboard one person

     Ends everything one person holds in Cove and reports each item. First, in one transaction: every CLI
    session, connected app and service key bound to them, every direct share to them on any VM (their
    Warpgate access to it is then dropped, retried until Warpgate confirms it), every personal and admin
    API key they own, and every webhook subscription they own, of any scope, which is disabled with
    reason `owner-offboarded` (its deliveries not yet sent are dropped, and it cannot be re-enabled,
    changed or replayed). A CLI session Warpgate cannot delete still works: it is listed in
    `cli_sessions_failed`, a failed item. If any of the Cove-side changes fails, none of it lands and
    the call fails. Only an administrator can offboard, and only a person: a `svc:` or `team:` name is
    404. Then, one item at a time: first Cove's own Warpgate role for them (the one Cove binds to their
    VMs' targets) is deleted (`warpgate_role`), which unbinds those targets; the targets stay, and no
    other role is touched, even one whose only member is them. No such role is `not_found`, and a role
    that could not be found or deleted is a failed item. Next their Warpgate user is deleted
    (`warpgate_user`), which takes their Warpgate roles, user API tokens, passwords, one-time codes and
    certificates with it, each of which signs in without the identity provider; Warpgate having no such
    user is reported as `not_found`, not a failure, and a user that could not be found or deleted is a
    failed item (delete it in Warpgate, then run the call again); so is, deleting nothing, the user that
    owns Cove's own Warpgate token, or a name several users share regardless of case. Then, belt and
    braces, every SSH public key of theirs at Warpgate is deleted (`ssh_keys_deleted`), every Warpgate
    ticket in their name, whatever minted it, is deleted (`tickets_deleted`), and every live Warpgate
    session of theirs is closed, on every target: the shell, the web UI and each VM (`sessions_closed`),
    since a key or a ticket signs in without the identity provider and an open session never asks it
    again. A session open until the close could add a key or mint a ticket, so keys, tickets and
    sessions are handled again until a pass finds nothing new, three passes at most; every pass's items
    are reported, and a list still finding new ones in the third pass gets a failed `*` entry. The
    credential step then runs once more, so a key, webhook or share such a session created in between is
    ended and reported too; if that sweep fails, `second_sweep_error` says why, a failed item. Then they
    are removed from every team they belong to, every secret in their own (user) scope is deleted (team,
    project and VM secrets stay with the team, project or VM), and every VM they own is stopped, under
    its lifecycle lock and as read again under it: one in the middle of a transition then is not touched
    and is a failed item. VMs are never deleted or reassigned. On a host with the secrets feature off,
    the secrets entry is one failed item (`name` `*`, `secrets feature disabled; nothing deleted`). A
    failure of one of these items is reported in its entry and does not stop the others, so the response
    is 200 even when some items failed; run the call again to retry them. A failed item is an entry with
    `ok` false, a VM whose `outcome` is `failed`, a `warpgate_role` or `warpgate_user` whose `outcome`
    is `failed`, any `cli_sessions_failed` entry, or a `second_sweep_error`.

    With `{"dry_run": true}` the response is the same report and nothing is changed: no record, no write
    to Warpgate (it only names the Warpgate role and user it would delete and lists their keys, tickets
    and sessions), no VM stopped. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else (no `dry_run`, a non-boolean one, another field, a non-object, a
    body without a JSON content type) is 400 `validation_failed` and nothing runs. Every call, the dry
    run included, writes one `user.offboarded` audit row: the administrator, the sudo context, the size
    of each list, the Warpgate ids ended and the number of failed items.

    Signing in through the identity provider again gives the person a new Warpgate user, and while they
    own VMs Cove re-creates its role for them whenever it next sets up access to one (at its next start,
    say), so remove them from the identity provider too and reassign or delete their VMs. `POST
    /api/admin/users/{username}/revoke-sessions` is the credential-only subset.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (OffboardUserRequest | Unset): `POST /api/admin/users/{username}/offboard` request
            body. An absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real offboarding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport
    """

    return sync_detailed(
        username=username,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: OffboardUserRequest | Unset = UNSET,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport]:
    """Offboard one person

     Ends everything one person holds in Cove and reports each item. First, in one transaction: every CLI
    session, connected app and service key bound to them, every direct share to them on any VM (their
    Warpgate access to it is then dropped, retried until Warpgate confirms it), every personal and admin
    API key they own, and every webhook subscription they own, of any scope, which is disabled with
    reason `owner-offboarded` (its deliveries not yet sent are dropped, and it cannot be re-enabled,
    changed or replayed). A CLI session Warpgate cannot delete still works: it is listed in
    `cli_sessions_failed`, a failed item. If any of the Cove-side changes fails, none of it lands and
    the call fails. Only an administrator can offboard, and only a person: a `svc:` or `team:` name is
    404. Then, one item at a time: first Cove's own Warpgate role for them (the one Cove binds to their
    VMs' targets) is deleted (`warpgate_role`), which unbinds those targets; the targets stay, and no
    other role is touched, even one whose only member is them. No such role is `not_found`, and a role
    that could not be found or deleted is a failed item. Next their Warpgate user is deleted
    (`warpgate_user`), which takes their Warpgate roles, user API tokens, passwords, one-time codes and
    certificates with it, each of which signs in without the identity provider; Warpgate having no such
    user is reported as `not_found`, not a failure, and a user that could not be found or deleted is a
    failed item (delete it in Warpgate, then run the call again); so is, deleting nothing, the user that
    owns Cove's own Warpgate token, or a name several users share regardless of case. Then, belt and
    braces, every SSH public key of theirs at Warpgate is deleted (`ssh_keys_deleted`), every Warpgate
    ticket in their name, whatever minted it, is deleted (`tickets_deleted`), and every live Warpgate
    session of theirs is closed, on every target: the shell, the web UI and each VM (`sessions_closed`),
    since a key or a ticket signs in without the identity provider and an open session never asks it
    again. A session open until the close could add a key or mint a ticket, so keys, tickets and
    sessions are handled again until a pass finds nothing new, three passes at most; every pass's items
    are reported, and a list still finding new ones in the third pass gets a failed `*` entry. The
    credential step then runs once more, so a key, webhook or share such a session created in between is
    ended and reported too; if that sweep fails, `second_sweep_error` says why, a failed item. Then they
    are removed from every team they belong to, every secret in their own (user) scope is deleted (team,
    project and VM secrets stay with the team, project or VM), and every VM they own is stopped, under
    its lifecycle lock and as read again under it: one in the middle of a transition then is not touched
    and is a failed item. VMs are never deleted or reassigned. On a host with the secrets feature off,
    the secrets entry is one failed item (`name` `*`, `secrets feature disabled; nothing deleted`). A
    failure of one of these items is reported in its entry and does not stop the others, so the response
    is 200 even when some items failed; run the call again to retry them. A failed item is an entry with
    `ok` false, a VM whose `outcome` is `failed`, a `warpgate_role` or `warpgate_user` whose `outcome`
    is `failed`, any `cli_sessions_failed` entry, or a `second_sweep_error`.

    With `{"dry_run": true}` the response is the same report and nothing is changed: no record, no write
    to Warpgate (it only names the Warpgate role and user it would delete and lists their keys, tickets
    and sessions), no VM stopped. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else (no `dry_run`, a non-boolean one, another field, a non-object, a
    body without a JSON content type) is 400 `validation_failed` and nothing runs. Every call, the dry
    run included, writes one `user.offboarded` audit row: the administrator, the sudo context, the size
    of each list, the Warpgate ids ended and the number of failed items.

    Signing in through the identity provider again gives the person a new Warpgate user, and while they
    own VMs Cove re-creates its role for them whenever it next sets up access to one (at its next start,
    say), so remove them from the identity provider too and reassign or delete their VMs. `POST
    /api/admin/users/{username}/revoke-sessions` is the credential-only subset.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (OffboardUserRequest | Unset): `POST /api/admin/users/{username}/offboard` request
            body. An absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real offboarding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport]
    """

    kwargs = _get_kwargs(
        username=username,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: OffboardUserRequest | Unset = UNSET,
) -> ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport | None:
    """Offboard one person

     Ends everything one person holds in Cove and reports each item. First, in one transaction: every CLI
    session, connected app and service key bound to them, every direct share to them on any VM (their
    Warpgate access to it is then dropped, retried until Warpgate confirms it), every personal and admin
    API key they own, and every webhook subscription they own, of any scope, which is disabled with
    reason `owner-offboarded` (its deliveries not yet sent are dropped, and it cannot be re-enabled,
    changed or replayed). A CLI session Warpgate cannot delete still works: it is listed in
    `cli_sessions_failed`, a failed item. If any of the Cove-side changes fails, none of it lands and
    the call fails. Only an administrator can offboard, and only a person: a `svc:` or `team:` name is
    404. Then, one item at a time: first Cove's own Warpgate role for them (the one Cove binds to their
    VMs' targets) is deleted (`warpgate_role`), which unbinds those targets; the targets stay, and no
    other role is touched, even one whose only member is them. No such role is `not_found`, and a role
    that could not be found or deleted is a failed item. Next their Warpgate user is deleted
    (`warpgate_user`), which takes their Warpgate roles, user API tokens, passwords, one-time codes and
    certificates with it, each of which signs in without the identity provider; Warpgate having no such
    user is reported as `not_found`, not a failure, and a user that could not be found or deleted is a
    failed item (delete it in Warpgate, then run the call again); so is, deleting nothing, the user that
    owns Cove's own Warpgate token, or a name several users share regardless of case. Then, belt and
    braces, every SSH public key of theirs at Warpgate is deleted (`ssh_keys_deleted`), every Warpgate
    ticket in their name, whatever minted it, is deleted (`tickets_deleted`), and every live Warpgate
    session of theirs is closed, on every target: the shell, the web UI and each VM (`sessions_closed`),
    since a key or a ticket signs in without the identity provider and an open session never asks it
    again. A session open until the close could add a key or mint a ticket, so keys, tickets and
    sessions are handled again until a pass finds nothing new, three passes at most; every pass's items
    are reported, and a list still finding new ones in the third pass gets a failed `*` entry. The
    credential step then runs once more, so a key, webhook or share such a session created in between is
    ended and reported too; if that sweep fails, `second_sweep_error` says why, a failed item. Then they
    are removed from every team they belong to, every secret in their own (user) scope is deleted (team,
    project and VM secrets stay with the team, project or VM), and every VM they own is stopped, under
    its lifecycle lock and as read again under it: one in the middle of a transition then is not touched
    and is a failed item. VMs are never deleted or reassigned. On a host with the secrets feature off,
    the secrets entry is one failed item (`name` `*`, `secrets feature disabled; nothing deleted`). A
    failure of one of these items is reported in its entry and does not stop the others, so the response
    is 200 even when some items failed; run the call again to retry them. A failed item is an entry with
    `ok` false, a VM whose `outcome` is `failed`, a `warpgate_role` or `warpgate_user` whose `outcome`
    is `failed`, any `cli_sessions_failed` entry, or a `second_sweep_error`.

    With `{"dry_run": true}` the response is the same report and nothing is changed: no record, no write
    to Warpgate (it only names the Warpgate role and user it would delete and lists their keys, tickets
    and sessions), no VM stopped. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else (no `dry_run`, a non-boolean one, another field, a non-object, a
    body without a JSON content type) is 400 `validation_failed` and nothing runs. Every call, the dry
    run included, writes one `user.offboarded` audit row: the administrator, the sudo context, the size
    of each list, the Warpgate ids ended and the number of failed items.

    Signing in through the identity provider again gives the person a new Warpgate user, and while they
    own VMs Cove re-creates its role for them whenever it next sets up access to one (at its next start,
    say), so remove them from the identity provider too and reassign or delete their VMs. `POST
    /api/admin/users/{username}/revoke-sessions` is the credential-only subset.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (OffboardUserRequest | Unset): `POST /api/admin/users/{username}/offboard` request
            body. An absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real offboarding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | OffboardUserReport
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            body=body,
        )
    ).parsed
