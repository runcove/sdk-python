"""``client.secrets``: secrets bound to a VM, a user, a team or a project.

``client.secrets.vm(name)`` (and ``.user(username)``, ``.team(name)``, ``.project(project_id)``)
returns a scope with ``list``, ``set``, ``unset``, ``rotate`` and ``import_`` (``import`` is a
keyword). Each scope is its own class, calling its own generated operations, so every one of the
20 operations is declared where the coverage test can see it. A scope's subject is checked when
it is bound, so ``client.secrets.vm("..")`` raises at once.

``set``/``rotate`` take ``SetSecretRequest``'s fields (``value_b64`` -- the value, base64 -- and
optionally ``exposure``, ``lifetime``, ``setup_tag``, ``target_unit``, ``ttl_seconds``);
``import_`` takes ``entries``. Values never come back: ``list`` returns names.
"""

from __future__ import annotations

import builtins
from collections.abc import Mapping
from typing import Any, cast

from ..._args import build_body
from ..._generated.api.secrets import (
    delete_vm_secret,
    import_project_secrets,
    import_team_secrets,
    import_user_secrets,
    import_vm_secrets,
    list_project_secrets,
    list_team_secrets,
    list_user_secrets,
    list_vm_secrets,
    rotate_project_secret,
    rotate_team_secret,
    rotate_user_secret,
    rotate_vm_secret,
    set_project_secret,
    set_team_secret,
    set_user_secret,
    set_vm_secret,
    unset_project_secret,
    unset_team_secret,
    unset_user_secret,
)
from ..._generated.models import (
    ImportResponse,
    ImportSecretsRequest,
    RotateSummary,
    ScopedImportResult,
    SecretEntryDto,
    SetSecretRequest,
    VmCountResult,
)
from ..._operations import operation
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout, check_segment

SecretBody = SetSecretRequest | Mapping[str, Any] | None
ImportBody = ImportSecretsRequest | Mapping[str, Any] | None


class VmSecrets:
    """Secrets of one VM (``client.secrets.vm(...)``)."""

    def __init__(self, transport: AsyncCoveTransport, subject: str) -> None:
        self._t = transport
        self._subject = check_segment(subject)

    @operation("listVmSecrets")
    async def list(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[SecretEntryDto]:
        """The secrets' names (never their values). Scope ``secrets:read``."""
        names = await self._t.call(
            list_vm_secrets, path={"name": self._subject}, timeout=timeout
        )
        return cast(builtins.list[SecretEntryDto], names)

    @operation("setVmSecret")
    async def set(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> None:
        """Store secret ``key``. Takes effect in the VM at its next lifecycle event; ``rotate`` pushes it live. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        await self._t.call(
            set_vm_secret,
            path={"name": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )

    @operation("deleteVmSecret")
    async def unset(
        self, key: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> RotateSummary:
        """Remove secret ``key``. Scope ``secrets:write``."""
        result = await self._t.call(
            delete_vm_secret, path={"name": self._subject, "key": key}, timeout=timeout
        )
        return cast(RotateSummary, result)

    @operation("rotateVmSecret")
    async def rotate(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> RotateSummary:
        """Replace secret ``key`` and push the new value to running VMs now. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            rotate_vm_secret,
            path={"name": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(RotateSummary, result)

    @operation("importVmSecrets")
    async def import_(
        self,
        body: ImportBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> ImportResponse:
        """Store several secrets at once (``entries``). Scope ``secrets:write``."""
        req = build_body(ImportSecretsRequest, body, fields)
        result = await self._t.call(
            import_vm_secrets, path={"name": self._subject}, body=req, timeout=timeout
        )
        return cast(ImportResponse, result)


class UserSecrets:
    """Secrets of one user (``client.secrets.user(...)``)."""

    def __init__(self, transport: AsyncCoveTransport, subject: str) -> None:
        self._t = transport
        self._subject = check_segment(subject)

    @operation("listUserSecrets")
    async def list(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[SecretEntryDto]:
        """The secrets' names (never their values). Scope ``secrets:read``."""
        names = await self._t.call(
            list_user_secrets, path={"username": self._subject}, timeout=timeout
        )
        return cast(builtins.list[SecretEntryDto], names)

    @operation("setUserSecret")
    async def set(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> VmCountResult:
        """Store secret ``key``. Returns how many VMs it reaches; ``rotate`` pushes it to them live. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            set_user_secret,
            path={"username": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(VmCountResult, result)

    @operation("unsetUserSecret")
    async def unset(
        self, key: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> RotateSummary:
        """Remove secret ``key``. Scope ``secrets:write``."""
        result = await self._t.call(
            unset_user_secret,
            path={"username": self._subject, "key": key},
            timeout=timeout,
        )
        return cast(RotateSummary, result)

    @operation("rotateUserSecret")
    async def rotate(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> RotateSummary:
        """Replace secret ``key`` and push the new value to running VMs now. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            rotate_user_secret,
            path={"username": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(RotateSummary, result)

    @operation("importUserSecrets")
    async def import_(
        self,
        body: ImportBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> ScopedImportResult:
        """Store several secrets at once (``entries``). Scope ``secrets:write``."""
        req = build_body(ImportSecretsRequest, body, fields)
        result = await self._t.call(
            import_user_secrets,
            path={"username": self._subject},
            body=req,
            timeout=timeout,
        )
        return cast(ScopedImportResult, result)


class TeamSecrets:
    """Secrets of one team (``client.secrets.team(...)``)."""

    def __init__(self, transport: AsyncCoveTransport, subject: str) -> None:
        self._t = transport
        self._subject = check_segment(subject)

    @operation("listTeamSecrets")
    async def list(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[SecretEntryDto]:
        """The secrets' names (never their values). Scope ``secrets:read``."""
        names = await self._t.call(
            list_team_secrets, path={"name": self._subject}, timeout=timeout
        )
        return cast(builtins.list[SecretEntryDto], names)

    @operation("setTeamSecret")
    async def set(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> VmCountResult:
        """Store secret ``key``. Returns how many VMs it reaches; ``rotate`` pushes it to them live. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            set_team_secret,
            path={"name": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(VmCountResult, result)

    @operation("unsetTeamSecret")
    async def unset(
        self, key: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> RotateSummary:
        """Remove secret ``key``. Scope ``secrets:write``."""
        result = await self._t.call(
            unset_team_secret, path={"name": self._subject, "key": key}, timeout=timeout
        )
        return cast(RotateSummary, result)

    @operation("rotateTeamSecret")
    async def rotate(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> RotateSummary:
        """Replace secret ``key`` and push the new value to running VMs now. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            rotate_team_secret,
            path={"name": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(RotateSummary, result)

    @operation("importTeamSecrets")
    async def import_(
        self,
        body: ImportBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> ScopedImportResult:
        """Store several secrets at once (``entries``). Scope ``secrets:write``."""
        req = build_body(ImportSecretsRequest, body, fields)
        result = await self._t.call(
            import_team_secrets, path={"name": self._subject}, body=req, timeout=timeout
        )
        return cast(ScopedImportResult, result)


class ProjectSecrets:
    """Secrets of one project (``client.secrets.project(...)``)."""

    def __init__(self, transport: AsyncCoveTransport, subject: str) -> None:
        self._t = transport
        self._subject = check_segment(subject)

    @operation("listProjectSecrets")
    async def list(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[SecretEntryDto]:
        """The secrets' names (never their values). Scope ``secrets:read``."""
        names = await self._t.call(
            list_project_secrets, path={"project_id": self._subject}, timeout=timeout
        )
        return cast(builtins.list[SecretEntryDto], names)

    @operation("setProjectSecret")
    async def set(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> VmCountResult:
        """Store secret ``key``. Returns how many VMs it reaches; ``rotate`` pushes it to them live. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            set_project_secret,
            path={"project_id": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(VmCountResult, result)

    @operation("unsetProjectSecret")
    async def unset(
        self, key: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> RotateSummary:
        """Remove secret ``key``. Scope ``secrets:write``."""
        result = await self._t.call(
            unset_project_secret,
            path={"project_id": self._subject, "key": key},
            timeout=timeout,
        )
        return cast(RotateSummary, result)

    @operation("rotateProjectSecret")
    async def rotate(
        self,
        key: str,
        body: SecretBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> RotateSummary:
        """Replace secret ``key`` and push the new value to running VMs now. Scope ``secrets:write``."""
        req = build_body(SetSecretRequest, body, fields)
        result = await self._t.call(
            rotate_project_secret,
            path={"project_id": self._subject, "key": key},
            body=req,
            timeout=timeout,
        )
        return cast(RotateSummary, result)

    @operation("importProjectSecrets")
    async def import_(
        self,
        body: ImportBody = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> ScopedImportResult:
        """Store several secrets at once (``entries``). Scope ``secrets:write``."""
        req = build_body(ImportSecretsRequest, body, fields)
        result = await self._t.call(
            import_project_secrets,
            path={"project_id": self._subject},
            body=req,
            timeout=timeout,
        )
        return cast(ScopedImportResult, result)


class Secrets:
    """``client.secrets`` — bind a subject, then work on its secrets."""

    __cove_scopes__ = (VmSecrets, UserSecrets, TeamSecrets, ProjectSecrets)

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    def vm(self, name: str) -> VmSecrets:
        """The secrets of VM ``name``."""
        return VmSecrets(self._t, name)

    def user(self, username: str) -> UserSecrets:
        """The secrets of user ``username``."""
        return UserSecrets(self._t, username)

    def team(self, name: str) -> TeamSecrets:
        """The secrets of team ``name``."""
        return TeamSecrets(self._t, name)

    def project(self, project_id: str) -> ProjectSecrets:
        """The secrets of project ``project_id``."""
        return ProjectSecrets(self._t, project_id)
