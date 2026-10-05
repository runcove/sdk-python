"""``client.tags``: VM tags and team attribution."""

from __future__ import annotations

import builtins
from typing import cast

from ..._args import build_body
from ..._generated.api.tags import (
    delete_vm_tag,
    list_all_tags,
    list_vm_tags,
    set_vm_tag,
)
from ..._generated.api.vms import set_vm_team, unset_vm_team
from ..._generated.models import SetTagRequest, SetVmTeamRequest, TagEntry, TagSummary
from ..._operations import operation
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Tags:
    """``client.tags`` — key/value tags on VMs, and which team a VM is charged to."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("listVmTags")
    async def list_for_vm(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[TagEntry]:
        """VM ``name``'s tags. Scope ``tags:read``."""
        tags = await self._t.call(list_vm_tags, path={"name": name}, timeout=timeout)
        return cast(builtins.list[TagEntry], tags)

    @operation("setVmTag")
    async def set(
        self, name: str, key: str, value: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Set tag ``key`` to ``value`` on VM ``name``. Scope ``tags:write``."""
        req = build_body(SetTagRequest, None, {"value": value})
        await self._t.call(
            set_vm_tag, path={"name": name, "key": key}, body=req, timeout=timeout
        )

    @operation("deleteVmTag")
    async def delete(
        self, name: str, key: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Remove tag ``key`` from VM ``name``. Scope ``tags:write``."""
        await self._t.call(
            delete_vm_tag, path={"name": name, "key": key}, timeout=timeout
        )

    @operation("listAllTags")
    async def list_all(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> builtins.list[TagSummary]:
        """Every tag key across the caller's VMs, with counts. Scope ``tags:read``."""
        tags = await self._t.call(list_all_tags, timeout=timeout)
        return cast(builtins.list[TagSummary], tags)

    @operation("setVmTeam")
    async def set_team(
        self, name: str, team: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Charge VM ``name`` to ``team``'s quota. Scope ``vms:write``."""
        req = build_body(SetVmTeamRequest, None, {"team": team})
        await self._t.call(set_vm_team, path={"name": name}, body=req, timeout=timeout)

    @operation("unsetVmTeam")
    async def unset_team(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Charge VM ``name`` to its owner again. Scope ``vms:write``."""
        await self._t.call(unset_vm_team, path={"name": name}, timeout=timeout)
