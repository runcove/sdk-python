"""``client.teams``: teams and their members.

Every listener serves them. Where a method says administrators only, an API key must be an admin
key (``keys.create(admin_key=True)``) of an ``[auth] admins`` user; an ordinary key of that user
acts as the user only.
"""

from __future__ import annotations

import builtins
from typing import cast

from ..._generated.api.meta import (
    create_team,
    create_team_member,
    delete_team,
    delete_team_member,
    list_team_members,
    list_teams,
)
from ..._generated.models import (
    AddMemberRequest,
    CreateTeamRequest,
    RemoveMemberOutcome,
    TeamDeleteOutcome,
    TeamMemberEntry,
    TeamSummary,
)
from ..._operations import operation
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Teams:
    """``client.teams`` — teams, and who is in them."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("listTeams")
    async def list(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[TeamSummary]:
        """Every team. Scope ``teams:read``.

        Over an API key this full listing also needs an admin key
        (``cove key create --admin``) of an administrator; any other key gets
        403 ``admin_required``. Sessions are unchanged. ``created_by`` is set
        only for an administrator.
        """
        out = await self._t.call(list_teams, timeout=timeout)
        return cast(builtins.list[TeamSummary], out)

    @operation("createTeam")
    async def create(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> TeamSummary:
        """Create team ``name``. Administrators only. Scope ``teams:write``."""
        out = await self._t.call(
            create_team, body=CreateTeamRequest(name=name), timeout=timeout
        )
        return cast(TeamSummary, out)

    @operation("deleteTeam")
    async def delete(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> TeamDeleteOutcome:
        """Delete team ``name`` and revoke its team API keys. Administrators only. Scope ``teams:write``.
        A 409 ``ConflictError`` while VMs the team owns are live.
        """
        out = await self._t.call(delete_team, path={"name": name}, timeout=timeout)
        return cast(TeamDeleteOutcome, out)

    @operation("listTeamMembers")
    async def members(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[TeamMemberEntry]:
        """Who is in team ``name``. Administrators and the team's members. Scope ``teams:read``.

        ``added_by`` is set only for an administrator.
        """
        out = await self._t.call(
            list_team_members, path={"name": name}, timeout=timeout
        )
        return cast(builtins.list[TeamMemberEntry], out)

    @operation("createTeamMember")
    async def add_member(
        self, name: str, username: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Add ``username`` to team ``name``. Administrators only. Scope ``teams:write``."""
        await self._t.call(
            create_team_member,
            path={"name": name},
            body=AddMemberRequest(username=username),
            timeout=timeout,
        )

    @operation("deleteTeamMember")
    async def remove_member(
        self, name: str, username: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> RemoveMemberOutcome:
        """Remove ``username`` from team ``name``. Administrators only. Scope ``teams:write``.

        Team API keys stay valid: they are bound to the team, not to its members.
        """
        out = await self._t.call(
            delete_team_member,
            path={"name": name, "username": username},
            timeout=timeout,
        )
        return cast(RemoveMemberOutcome, out)
