"""``client.audit``: the audit log."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import cast

from ..._args import opt
from ..._generated.api.audit import list_audit
from ..._generated.models import AuditEntry, AuditPage
from ..._operations import operation
from .._pagination import paginate
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Audit:
    """``client.audit`` — who did what, newest first. Scope ``audit:read``."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("listAudit")
    async def list(
        self,
        *,
        vm: str | None = None,
        user: str | None = None,
        kind: str | None = None,
        key_id: str | None = None,
        source_ip: str | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> AuditPage:
        """One page of audit entries matching every filter given. Scope ``audit:read``."""
        page = await self._t.call(
            list_audit,
            vm=opt(vm),
            user=opt(user),
            kind=opt(kind),
            key_id=opt(key_id),
            source_ip=opt(source_ip),
            since=opt(since),
            until=opt(until),
            limit=opt(limit),
            cursor=opt(cursor),
            timeout=timeout,
        )
        return cast(AuditPage, page)

    async def iter(
        self,
        *,
        vm: str | None = None,
        user: str | None = None,
        kind: str | None = None,
        key_id: str | None = None,
        source_ip: str | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> AsyncIterator[AuditEntry]:
        """Every matching audit entry, following ``next_cursor``."""

        async def fetch(c: str | None) -> AuditPage:
            return await self.list(
                vm=vm,
                user=user,
                kind=kind,
                key_id=key_id,
                source_ip=source_ip,
                since=since,
                until=until,
                limit=limit,
                cursor=c,
                timeout=timeout,
            )

        async for entry in paginate(fetch, "entries", cursor=cursor):
            yield entry
