from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.purge_user_report import PurgeUserReport
from ...models.purge_user_request import PurgeUserRequest
from ...models.sudo_required_body import SudoRequiredBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    username: str,
    *,
    body: PurgeUserRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/users/{username}/purge".format(
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
) -> ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport | None:
    if response.status_code == 200:
        response_200 = PurgeUserReport.from_dict(response.json())

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
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport]:
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
    body: PurgeUserRequest | Unset = UNSET,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport]:
    """Delete an offboarded person's leftover records

     Deletes what a full offboarding leaves behind in Cove's database, in one transaction: the person's
    user record, the records of VMs they had that are already deleted, their revoked API keys, CLI
    tickets, connected apps, webhook subscriptions and queued deliveries, project memberships,
    credential-revocation marker, and the shut-out marker offboarding wrote. Deleting the user record
    also deletes their quota limit and quota overrides; the response counts them. The purge changes no
    record that belongs to someone else or to a team, so it does not remove the person's name
    everywhere: the audit log stays, and so does their name as the actor on other people's and teams'
    records (teams they created, people they added to a team or project, shares they granted, quota
    overrides and tags they set, VM renames and share withdrawals still waiting on Warpgate that they
    asked for, offboardings they ran), deleted VMs of a service key that were charged to them, the
    service keys that were bound to them (a key name is never re-bound, so its binding stays), and the
    secrets they set on a team, project or VM. The response lists every table with the rows deleted (or,
    in a dry run, that would be) and says what is left in place (`left_in_place`).

    Refused (422 `validation_failed`, nothing changed) unless the person is offboarded and nothing of
    theirs is live: no VM they own or are charged for, no active API key, live share to them, connected
    app or CLI ticket not revoked, service-key binding not ended, active webhook subscription, team
    membership, checkpoint they own, or share withdrawal still waiting on Warpgate. Run the offboarding
    again and deal with what it reports. Refused too while the name is in `[auth] admins`, compared
    regardless of ASCII case, since the shut-out marker is all that keeps an offboarded name out and a
    listed name signs in as an administrator: take them out of the list and restart Cove first. The same
    goes for `[auth] nested_virt_users`. Refused until an offboarding run has finished having kept
    nothing (their Warpgate user deleted or not found, every secret in their own scope and every port
    invite they minted on someone else's VM deleted): every run clears that record when it starts, so a
    run that kept something, one still going, or an offboarding from before the upgrade that added the
    record means offboarding them again first. Refused too while any secret is left in the person's own
    scope, or while those secrets cannot be listed, and, on a host with a configured Warpgate, while
    Warpgate has a user under the name (compared regardless of letter case) or cannot be asked: the
    purge asks it each time, before its transaction, as it lists those secrets. Refused too while a
    Warpgate is configured but the daemon started without a client for it (the embedded Warpgate on a
    Mac), since what it holds cannot be read. For port invites the purge trusts the offboarding run's
    record: it does not list Warpgate's tickets itself, so an invite offboarding could not find (one
    with no audit record) is not caught. A dry run reports these with the other reasons. It also waits,
    and says how (purge again, not offboard again): while the name of a deleted VM of theirs is still
    held after the delete (up to `hostname_cooldown_secs`, 60 seconds by default, since a purge would
    free the name early), and while a rename of a deleted VM of theirs has not finished (the purge would
    remove the address its DNS clean-up needs). Also refused: a `svc:` or `team:` name, the
    administrator themselves, and a name stored in more than one spelling that differs only by case, in
    any table that holds a person (the answer names each spelling and where it is; a spelling found only
    in a service-key binding that has ended or a deleted VM's charge does not count, since a purge keeps
    those rows). The name is matched regardless of ASCII case and is not checked against the current
    username rules: it names a record that exists. 404 when Cove has no record of the name.

    The purge also removes the shut-out: if the person is still in the identity provider they can sign
    in again and start from nothing. Remove them there first. Nothing is changed at Warpgate (the purge
    only reads its user list), and no VM is deleted. Offboarding removed the person's role, and their
    Warpgate user unless it kept it: a failed lookup, token-owner check or delete, a user that owns
    Cove's own token, a name several Warpgate users share, tickets in their name on another instance's
    targets or with no target id, or a failed re-listing of those tickets. A kept user keeps its
    password and tokens, which is why a purge needs a run that kept nothing. The audit log stays. A non-
    administrator's audit read matches on the actor's name and starts at that name's last purge, so a
    later user with the same name does not read the earlier person's own records.

    With `{"dry_run": true}` nothing is deleted, and the dry run is refused for the same reasons as a
    real purge, the two waits included. A real purge also ends the person's pending connected-app
    consent pages, and a consent page shown before a purge or an offboarding cannot be completed after
    it (nothing is connected). A completed purge, the dry run included, writes one `user.purged` audit
    row: the administrator, the sudo context, the dry-run flag and the rows per table; a refused purge
    changes nothing and writes none. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else is 400 `validation_failed` and nothing runs.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (PurgeUserRequest | Unset): `POST /api/admin/users/{username}/purge` request body. An
            absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real purge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport]
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
    body: PurgeUserRequest | Unset = UNSET,
) -> ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport | None:
    """Delete an offboarded person's leftover records

     Deletes what a full offboarding leaves behind in Cove's database, in one transaction: the person's
    user record, the records of VMs they had that are already deleted, their revoked API keys, CLI
    tickets, connected apps, webhook subscriptions and queued deliveries, project memberships,
    credential-revocation marker, and the shut-out marker offboarding wrote. Deleting the user record
    also deletes their quota limit and quota overrides; the response counts them. The purge changes no
    record that belongs to someone else or to a team, so it does not remove the person's name
    everywhere: the audit log stays, and so does their name as the actor on other people's and teams'
    records (teams they created, people they added to a team or project, shares they granted, quota
    overrides and tags they set, VM renames and share withdrawals still waiting on Warpgate that they
    asked for, offboardings they ran), deleted VMs of a service key that were charged to them, the
    service keys that were bound to them (a key name is never re-bound, so its binding stays), and the
    secrets they set on a team, project or VM. The response lists every table with the rows deleted (or,
    in a dry run, that would be) and says what is left in place (`left_in_place`).

    Refused (422 `validation_failed`, nothing changed) unless the person is offboarded and nothing of
    theirs is live: no VM they own or are charged for, no active API key, live share to them, connected
    app or CLI ticket not revoked, service-key binding not ended, active webhook subscription, team
    membership, checkpoint they own, or share withdrawal still waiting on Warpgate. Run the offboarding
    again and deal with what it reports. Refused too while the name is in `[auth] admins`, compared
    regardless of ASCII case, since the shut-out marker is all that keeps an offboarded name out and a
    listed name signs in as an administrator: take them out of the list and restart Cove first. The same
    goes for `[auth] nested_virt_users`. Refused until an offboarding run has finished having kept
    nothing (their Warpgate user deleted or not found, every secret in their own scope and every port
    invite they minted on someone else's VM deleted): every run clears that record when it starts, so a
    run that kept something, one still going, or an offboarding from before the upgrade that added the
    record means offboarding them again first. Refused too while any secret is left in the person's own
    scope, or while those secrets cannot be listed, and, on a host with a configured Warpgate, while
    Warpgate has a user under the name (compared regardless of letter case) or cannot be asked: the
    purge asks it each time, before its transaction, as it lists those secrets. Refused too while a
    Warpgate is configured but the daemon started without a client for it (the embedded Warpgate on a
    Mac), since what it holds cannot be read. For port invites the purge trusts the offboarding run's
    record: it does not list Warpgate's tickets itself, so an invite offboarding could not find (one
    with no audit record) is not caught. A dry run reports these with the other reasons. It also waits,
    and says how (purge again, not offboard again): while the name of a deleted VM of theirs is still
    held after the delete (up to `hostname_cooldown_secs`, 60 seconds by default, since a purge would
    free the name early), and while a rename of a deleted VM of theirs has not finished (the purge would
    remove the address its DNS clean-up needs). Also refused: a `svc:` or `team:` name, the
    administrator themselves, and a name stored in more than one spelling that differs only by case, in
    any table that holds a person (the answer names each spelling and where it is; a spelling found only
    in a service-key binding that has ended or a deleted VM's charge does not count, since a purge keeps
    those rows). The name is matched regardless of ASCII case and is not checked against the current
    username rules: it names a record that exists. 404 when Cove has no record of the name.

    The purge also removes the shut-out: if the person is still in the identity provider they can sign
    in again and start from nothing. Remove them there first. Nothing is changed at Warpgate (the purge
    only reads its user list), and no VM is deleted. Offboarding removed the person's role, and their
    Warpgate user unless it kept it: a failed lookup, token-owner check or delete, a user that owns
    Cove's own token, a name several Warpgate users share, tickets in their name on another instance's
    targets or with no target id, or a failed re-listing of those tickets. A kept user keeps its
    password and tokens, which is why a purge needs a run that kept nothing. The audit log stays. A non-
    administrator's audit read matches on the actor's name and starts at that name's last purge, so a
    later user with the same name does not read the earlier person's own records.

    With `{"dry_run": true}` nothing is deleted, and the dry run is refused for the same reasons as a
    real purge, the two waits included. A real purge also ends the person's pending connected-app
    consent pages, and a consent page shown before a purge or an offboarding cannot be completed after
    it (nothing is connected). A completed purge, the dry run included, writes one `user.purged` audit
    row: the administrator, the sudo context, the dry-run flag and the rows per table; a refused purge
    changes nothing and writes none. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else is 400 `validation_failed` and nothing runs.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (PurgeUserRequest | Unset): `POST /api/admin/users/{username}/purge` request body. An
            absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real purge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport
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
    body: PurgeUserRequest | Unset = UNSET,
) -> Response[ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport]:
    """Delete an offboarded person's leftover records

     Deletes what a full offboarding leaves behind in Cove's database, in one transaction: the person's
    user record, the records of VMs they had that are already deleted, their revoked API keys, CLI
    tickets, connected apps, webhook subscriptions and queued deliveries, project memberships,
    credential-revocation marker, and the shut-out marker offboarding wrote. Deleting the user record
    also deletes their quota limit and quota overrides; the response counts them. The purge changes no
    record that belongs to someone else or to a team, so it does not remove the person's name
    everywhere: the audit log stays, and so does their name as the actor on other people's and teams'
    records (teams they created, people they added to a team or project, shares they granted, quota
    overrides and tags they set, VM renames and share withdrawals still waiting on Warpgate that they
    asked for, offboardings they ran), deleted VMs of a service key that were charged to them, the
    service keys that were bound to them (a key name is never re-bound, so its binding stays), and the
    secrets they set on a team, project or VM. The response lists every table with the rows deleted (or,
    in a dry run, that would be) and says what is left in place (`left_in_place`).

    Refused (422 `validation_failed`, nothing changed) unless the person is offboarded and nothing of
    theirs is live: no VM they own or are charged for, no active API key, live share to them, connected
    app or CLI ticket not revoked, service-key binding not ended, active webhook subscription, team
    membership, checkpoint they own, or share withdrawal still waiting on Warpgate. Run the offboarding
    again and deal with what it reports. Refused too while the name is in `[auth] admins`, compared
    regardless of ASCII case, since the shut-out marker is all that keeps an offboarded name out and a
    listed name signs in as an administrator: take them out of the list and restart Cove first. The same
    goes for `[auth] nested_virt_users`. Refused until an offboarding run has finished having kept
    nothing (their Warpgate user deleted or not found, every secret in their own scope and every port
    invite they minted on someone else's VM deleted): every run clears that record when it starts, so a
    run that kept something, one still going, or an offboarding from before the upgrade that added the
    record means offboarding them again first. Refused too while any secret is left in the person's own
    scope, or while those secrets cannot be listed, and, on a host with a configured Warpgate, while
    Warpgate has a user under the name (compared regardless of letter case) or cannot be asked: the
    purge asks it each time, before its transaction, as it lists those secrets. Refused too while a
    Warpgate is configured but the daemon started without a client for it (the embedded Warpgate on a
    Mac), since what it holds cannot be read. For port invites the purge trusts the offboarding run's
    record: it does not list Warpgate's tickets itself, so an invite offboarding could not find (one
    with no audit record) is not caught. A dry run reports these with the other reasons. It also waits,
    and says how (purge again, not offboard again): while the name of a deleted VM of theirs is still
    held after the delete (up to `hostname_cooldown_secs`, 60 seconds by default, since a purge would
    free the name early), and while a rename of a deleted VM of theirs has not finished (the purge would
    remove the address its DNS clean-up needs). Also refused: a `svc:` or `team:` name, the
    administrator themselves, and a name stored in more than one spelling that differs only by case, in
    any table that holds a person (the answer names each spelling and where it is; a spelling found only
    in a service-key binding that has ended or a deleted VM's charge does not count, since a purge keeps
    those rows). The name is matched regardless of ASCII case and is not checked against the current
    username rules: it names a record that exists. 404 when Cove has no record of the name.

    The purge also removes the shut-out: if the person is still in the identity provider they can sign
    in again and start from nothing. Remove them there first. Nothing is changed at Warpgate (the purge
    only reads its user list), and no VM is deleted. Offboarding removed the person's role, and their
    Warpgate user unless it kept it: a failed lookup, token-owner check or delete, a user that owns
    Cove's own token, a name several Warpgate users share, tickets in their name on another instance's
    targets or with no target id, or a failed re-listing of those tickets. A kept user keeps its
    password and tokens, which is why a purge needs a run that kept nothing. The audit log stays. A non-
    administrator's audit read matches on the actor's name and starts at that name's last purge, so a
    later user with the same name does not read the earlier person's own records.

    With `{"dry_run": true}` nothing is deleted, and the dry run is refused for the same reasons as a
    real purge, the two waits included. A real purge also ends the person's pending connected-app
    consent pages, and a consent page shown before a purge or an offboarding cannot be completed after
    it (nothing is connected). A completed purge, the dry run included, writes one `user.purged` audit
    row: the administrator, the sudo context, the dry-run flag and the rows per table; a refused purge
    changes nothing and writes none. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else is 400 `validation_failed` and nothing runs.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (PurgeUserRequest | Unset): `POST /api/admin/users/{username}/purge` request body. An
            absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real purge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport]
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
    body: PurgeUserRequest | Unset = UNSET,
) -> ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport | None:
    """Delete an offboarded person's leftover records

     Deletes what a full offboarding leaves behind in Cove's database, in one transaction: the person's
    user record, the records of VMs they had that are already deleted, their revoked API keys, CLI
    tickets, connected apps, webhook subscriptions and queued deliveries, project memberships,
    credential-revocation marker, and the shut-out marker offboarding wrote. Deleting the user record
    also deletes their quota limit and quota overrides; the response counts them. The purge changes no
    record that belongs to someone else or to a team, so it does not remove the person's name
    everywhere: the audit log stays, and so does their name as the actor on other people's and teams'
    records (teams they created, people they added to a team or project, shares they granted, quota
    overrides and tags they set, VM renames and share withdrawals still waiting on Warpgate that they
    asked for, offboardings they ran), deleted VMs of a service key that were charged to them, the
    service keys that were bound to them (a key name is never re-bound, so its binding stays), and the
    secrets they set on a team, project or VM. The response lists every table with the rows deleted (or,
    in a dry run, that would be) and says what is left in place (`left_in_place`).

    Refused (422 `validation_failed`, nothing changed) unless the person is offboarded and nothing of
    theirs is live: no VM they own or are charged for, no active API key, live share to them, connected
    app or CLI ticket not revoked, service-key binding not ended, active webhook subscription, team
    membership, checkpoint they own, or share withdrawal still waiting on Warpgate. Run the offboarding
    again and deal with what it reports. Refused too while the name is in `[auth] admins`, compared
    regardless of ASCII case, since the shut-out marker is all that keeps an offboarded name out and a
    listed name signs in as an administrator: take them out of the list and restart Cove first. The same
    goes for `[auth] nested_virt_users`. Refused until an offboarding run has finished having kept
    nothing (their Warpgate user deleted or not found, every secret in their own scope and every port
    invite they minted on someone else's VM deleted): every run clears that record when it starts, so a
    run that kept something, one still going, or an offboarding from before the upgrade that added the
    record means offboarding them again first. Refused too while any secret is left in the person's own
    scope, or while those secrets cannot be listed, and, on a host with a configured Warpgate, while
    Warpgate has a user under the name (compared regardless of letter case) or cannot be asked: the
    purge asks it each time, before its transaction, as it lists those secrets. Refused too while a
    Warpgate is configured but the daemon started without a client for it (the embedded Warpgate on a
    Mac), since what it holds cannot be read. For port invites the purge trusts the offboarding run's
    record: it does not list Warpgate's tickets itself, so an invite offboarding could not find (one
    with no audit record) is not caught. A dry run reports these with the other reasons. It also waits,
    and says how (purge again, not offboard again): while the name of a deleted VM of theirs is still
    held after the delete (up to `hostname_cooldown_secs`, 60 seconds by default, since a purge would
    free the name early), and while a rename of a deleted VM of theirs has not finished (the purge would
    remove the address its DNS clean-up needs). Also refused: a `svc:` or `team:` name, the
    administrator themselves, and a name stored in more than one spelling that differs only by case, in
    any table that holds a person (the answer names each spelling and where it is; a spelling found only
    in a service-key binding that has ended or a deleted VM's charge does not count, since a purge keeps
    those rows). The name is matched regardless of ASCII case and is not checked against the current
    username rules: it names a record that exists. 404 when Cove has no record of the name.

    The purge also removes the shut-out: if the person is still in the identity provider they can sign
    in again and start from nothing. Remove them there first. Nothing is changed at Warpgate (the purge
    only reads its user list), and no VM is deleted. Offboarding removed the person's role, and their
    Warpgate user unless it kept it: a failed lookup, token-owner check or delete, a user that owns
    Cove's own token, a name several Warpgate users share, tickets in their name on another instance's
    targets or with no target id, or a failed re-listing of those tickets. A kept user keeps its
    password and tokens, which is why a purge needs a run that kept nothing. The audit log stays. A non-
    administrator's audit read matches on the actor's name and starts at that name's last purge, so a
    later user with the same name does not read the earlier person's own records.

    With `{"dry_run": true}` nothing is deleted, and the dry run is refused for the same reasons as a
    real purge, the two waits included. A real purge also ends the person's pending connected-app
    consent pages, and a consent page shown before a purge or an offboarding cannot be completed after
    it (nothing is connected). A completed purge, the dry run included, writes one `user.purged` audit
    row: the administrator, the sudo context, the dry-run flag and the rows per table; a refused purge
    changes nothing and writes none. A real run is an empty body or `{"dry_run": false}` sent as
    `application/json`; anything else is 400 `validation_failed` and nothing runs.

    Sudo-gated: it runs only from a session with a fresh login (SSH, the web UI or the Unix socket).
    Every API key, an admin key included, gets 401 `sudo_required`.

    Args:
        username (str):
        body (PurgeUserRequest | Unset): `POST /api/admin/users/{username}/purge` request body. An
            absent body
            means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
            is refused, so a misspelt `dry_run` can never run the real purge.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | PurgeUserReport
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            body=body,
        )
    ).parsed
