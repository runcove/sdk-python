"""``client.host``: the host's status, capacity, reservations, telemetry and images."""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from typing import Any, cast

from ..._args import build_body, opt
from ..._generated.api.host import (
    create_reservation,
    delete_reservation,
    get_host_capacity,
    get_host_capacity_check,
    get_host_telemetry,
    list_images,
)
from ..._generated.api.meta import get_system_status
from ..._generated.models import (
    AdmissionStatus,
    CapacityReport,
    HostTelemetrySeries,
    ImagesResponse,
    ReservationRef,
    SystemStatus,
    TryReserveBody,
)
from ..._operations import operation
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout


class Host:
    """``client.host`` — what the host has and has promised."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("getSystemStatus")
    async def system_status(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> SystemStatus:
        """VM counts by state, processes, memory and the warm pools. Scope ``vms:read``."""
        status = await self._t.call(get_system_status, timeout=timeout)
        return cast(SystemStatus, status)

    @operation("getHostCapacityCheck")
    async def capacity_check(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> AdmissionStatus:
        """Whether the host would admit a VM now, with its capacity report. Scope ``vms:read``."""
        status = await self._t.call(get_host_capacity_check, timeout=timeout)
        return cast(AdmissionStatus, status)

    @operation("getHostCapacity")
    async def capacity(
        self, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> CapacityReport:
        """CPU, RAM and disk headroom, and the live reservations. Scope ``vms:read``."""
        report = await self._t.call(get_host_capacity, timeout=timeout)
        return cast(CapacityReport, report)

    @operation("createReservation")
    async def reserve(
        self,
        body: TryReserveBody | Mapping[str, Any] | None = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> ReservationRef:
        """Reserve capacity for ``action`` under ``flow_id``; a denial raises a 409 ``ConflictError``. Scope ``vms:write``."""
        req = build_body(TryReserveBody, body, fields)
        ref = await self._t.call(create_reservation, body=req, timeout=timeout)
        return cast(ReservationRef, ref)

    @operation("deleteReservation")
    async def release_reservation(
        self, id: str | uuid.UUID, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> None:
        """Release a reservation before its TTL. Scope ``vms:write``."""
        await self._t.call(delete_reservation, path={"id": str(id)}, timeout=timeout)

    @operation("getHostTelemetry")
    async def telemetry(
        self,
        *,
        from_: int | None = None,
        to: int | None = None,
        step: int | None = None,
        limit: int | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> HostTelemetrySeries:
        """The host's telemetry series (``from_`` is sent as ``from``). Scope ``vms:read``."""
        series = await self._t.call(
            get_host_telemetry,
            from_=opt(from_),
            to=opt(to),
            step=opt(step),
            limit=opt(limit),
            timeout=timeout,
        )
        return cast(HostTelemetrySeries, series)

    @operation("listImages")
    async def images(self, *, timeout: CallTimeout = CLIENT_DEFAULT) -> ImagesResponse:
        """The images VMs can be created from, and the OCI cache. Scope ``vms:read``."""
        images = await self._t.call(list_images, timeout=timeout)
        return cast(ImagesResponse, images)
