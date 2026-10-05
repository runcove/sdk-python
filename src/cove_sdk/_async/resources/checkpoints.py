"""``client.checkpoints``: create, list, get, delete checkpoints and hibernate a VM.

Waking a hibernated VM is ``client.vms.wake``; there is no checkpoint-rollback operation.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from typing import Any, cast

from ..._args import build_body, opt
from ..._generated.api.checkpoints import (
    create_checkpoint,
    delete_checkpoint,
    get_checkpoint,
    list_all_checkpoints,
    list_vm_checkpoints,
)
from ..._generated.api.vms import hibernate_vm
from ..._generated.models import Checkpoint, CheckpointCreateRequest, CheckpointPage
from ..._operations import operation
from .._pagination import paginate
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Checkpoints:
    """``client.checkpoints`` — checkpoints of the caller's VMs."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("createCheckpoint")
    async def create(
        self,
        name: str,
        body: CheckpointCreateRequest | Mapping[str, Any] | None = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> Checkpoint:
        """Checkpoint VM ``name`` (``description``, ``disk_only``). Scope ``checkpoints:write``."""
        req = build_body(CheckpointCreateRequest, body, fields)
        cp = await self._t.call(
            create_checkpoint, path={"name": name}, body=req, timeout=timeout
        )
        return cast(Checkpoint, cp)

    @operation("listVmCheckpoints")
    async def list_for_vm(
        self,
        name: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> CheckpointPage:
        """One page of VM ``name``'s checkpoints. Scope ``vms:read``."""
        page = await self._t.call(
            list_vm_checkpoints,
            path={"name": name},
            limit=opt(limit),
            cursor=opt(cursor),
            timeout=timeout,
        )
        return cast(CheckpointPage, page)

    async def iter_for_vm(
        self,
        name: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> AsyncIterator[Checkpoint]:
        """Every checkpoint of VM ``name``, following ``next_cursor``. Scope ``vms:read``."""

        async def fetch(c: str | None) -> CheckpointPage:
            return await self.list_for_vm(name, limit=limit, cursor=c, timeout=timeout)

        async for cp in paginate(fetch, "checkpoints", cursor=cursor):
            yield cp

    @operation("listAllCheckpoints")
    async def list_all(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> CheckpointPage:
        """One page of every checkpoint the caller owns, across VMs. Scope ``vms:read``."""
        page = await self._t.call(
            list_all_checkpoints, limit=opt(limit), cursor=opt(cursor), timeout=timeout
        )
        return cast(CheckpointPage, page)

    async def iter_all(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> AsyncIterator[Checkpoint]:
        """Every checkpoint the caller owns, following ``next_cursor``. Scope ``vms:read``."""

        async def fetch(c: str | None) -> CheckpointPage:
            return await self.list_all(limit=limit, cursor=c, timeout=timeout)

        async for cp in paginate(fetch, "checkpoints", cursor=cursor):
            yield cp

    @operation("getCheckpoint")
    async def get(
        self, id: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> Checkpoint:
        """One checkpoint. Scope ``vms:read``."""
        cp = await self._t.call(get_checkpoint, path={"id": id}, timeout=timeout)
        return cast(Checkpoint, cp)

    @operation("deleteCheckpoint")
    async def delete(self, id: str, *, timeout: CallTimeout = CLIENT_DEFAULT) -> None:
        """Delete a checkpoint. Scope ``checkpoints:write``."""
        await self._t.call(delete_checkpoint, path={"id": id}, timeout=timeout)

    @operation("hibernateVm")
    async def hibernate(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> Checkpoint:
        """Checkpoint VM ``name`` and stop it; ``client.vms.wake`` brings it back. Scope ``vms:write``."""
        cp = await self._t.call(hibernate_vm, path={"name": name}, timeout=timeout)
        return cast(Checkpoint, cp)
