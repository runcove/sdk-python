"""``client.policies``: a VM's auto-pause and expiry policies, and its idle state."""

from __future__ import annotations

from typing import Any, cast

from ..._args import build_body
from ..._generated.api.vms import (
    get_idle_state,
    get_vm_expiry,
    set_vm_auto_pause,
    set_vm_expiry,
)
from ..._generated.models import (
    IdleState,
    TtlPolicyView,
    UpdateAutoPauseRequest,
    UpdateTtlPolicyRequest,
)
from ..._operations import operation
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Policies:
    """``client.policies`` — per-VM auto-pause and expiry."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("setVmAutoPause")
    async def set_auto_pause(
        self, name: str, policy: Any, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Set the auto-pause policy: ``{"type": "auto_pause", "idle_timeout_secs": n}`` or
        ``{"type": "always_on"}`` (or the generated model). Scope ``vms:write``."""
        req = build_body(UpdateAutoPauseRequest, None, {"policy": policy})
        await self._t.call(
            set_vm_auto_pause, path={"name": name}, body=req, timeout=timeout
        )

    @operation("getIdleState")
    async def get_idle_state(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> IdleState:
        """Whether the VM is idle, by the auto-pause reckoning. Scope ``vms:read``."""
        state = await self._t.call(get_idle_state, path={"name": name}, timeout=timeout)
        return cast(IdleState, state)

    @operation("setVmExpiry")
    async def set_expiry(
        self, name: str, policy: Any, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Set the expiry policy (``TtlPolicy``: ``max_lifetime_secs``, ``on_stop``). Scope ``vms:write``."""
        req = build_body(UpdateTtlPolicyRequest, None, {"policy": policy})
        await self._t.call(
            set_vm_expiry, path={"name": name}, body=req, timeout=timeout
        )

    @operation("getVmExpiry")
    async def get_expiry(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> TtlPolicyView:
        """The VM's expiry policy. Scope ``vms:read``."""
        view = await self._t.call(get_vm_expiry, path={"name": name}, timeout=timeout)
        return cast(TtlPolicyView, view)
