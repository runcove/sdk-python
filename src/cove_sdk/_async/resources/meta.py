"""``client.meta``: health, version, who the caller is and what it may do, its sessions, the
usernames, and the API description."""

from __future__ import annotations

import builtins
from typing import Any, cast

from ..._generated.api.meta import (
    get_cli_status,
    get_me,
    get_openapi_document,
    health,
    list_sessions,
    list_ssh_keys,
    list_users,
    version,
    whoami,
)
from ..._generated.models import (
    BuildInfo,
    CliStatusResponse,
    GetOpenapiDocumentResponse200,
    HealthResponse,
    ProfileSummary,
    Session,
    SshKey,
    WhoamiResponse,
)
from ..._operations import operation
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Meta:
    """``client.meta`` — the server and the caller."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("health")
    async def health(self, *, timeout: CallTimeout = CLIENT_DEFAULT) -> HealthResponse:
        """Liveness, uptime and pool availability."""
        result = await self._t.call(health, timeout=timeout)
        return cast(HealthResponse, result)

    @operation("version")
    async def version(self, *, timeout: CallTimeout = CLIENT_DEFAULT) -> BuildInfo:
        """The server's build."""
        result = await self._t.call(version, timeout=timeout)
        return cast(BuildInfo, result)

    @operation("whoami")
    async def whoami(self, *, timeout: CallTimeout = CLIENT_DEFAULT) -> WhoamiResponse:
        """The username the server sees for this credential."""
        result = await self._t.call(whoami, timeout=timeout)
        return cast(WhoamiResponse, result)

    @operation("getMe")
    async def me(self, *, timeout: CallTimeout = CLIENT_DEFAULT) -> ProfileSummary:
        """The caller's profile: roles, key counts, LDAP link, and what this credential may do.

        ``permissions`` is a key's complete scope list (``kind="key"``) or ``kind="session"`` for a
        session, which has no list; ``is_admin`` is the admin checks' answer.
        :func:`cove_sdk.has_scope` reads both for you. Both are absent from servers older than
        them. No scope beyond a valid credential.
        """
        result = await self._t.call(get_me, timeout=timeout)
        return cast(ProfileSummary, result)

    @operation("listSshKeys")
    async def me_keys(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[SshKey]:
        """The caller's registered SSH public keys."""
        result = await self._t.call(list_ssh_keys, timeout=timeout)
        return cast(builtins.list[SshKey], result)

    @operation("listSessions")
    async def sessions(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[Session]:
        """The caller's own sign-in sessions, active and past.

        No scope beyond a valid credential: the data is about the caller alone. Revoking a session
        is not offered over an API key (the bearer listener does not serve it).
        """
        result = await self._t.call(list_sessions, timeout=timeout)
        return cast(builtins.list[Session], result)

    @operation("getCliStatus")
    async def cli_status(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> CliStatusResponse:
        """Whether the caller holds a CLI ticket."""
        result = await self._t.call(get_cli_status, timeout=timeout)
        return cast(CliStatusResponse, result)

    @operation("listUsers")
    async def users(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[str]:
        """Every username Cove knows, sorted. Scope ``vms:read``.

        Over an API key this full listing also needs an admin key
        (``cove key create --admin``) of an administrator; any other key gets
        403 ``admin_required``. Sessions are unchanged.
        """
        result = await self._t.call(list_users, timeout=timeout)
        return cast(builtins.list[str], result)

    @operation("getOpenapiDocument")
    async def openapi(self, *, timeout: CallTimeout = CLIENT_DEFAULT) -> dict[str, Any]:
        """The server's OpenAPI 3.1 description of itself, parsed into a ``dict``.

        The same contract as the matching release's ``sdk/openapi.yaml``. Served without a
        credential.
        """
        result = await self._t.call(get_openapi_document, timeout=timeout)
        return cast(GetOpenapiDocumentResponse200, result).to_dict()
