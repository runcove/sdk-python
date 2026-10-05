from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="HostTelemetryPoint")


@_attrs_define
class HostTelemetryPoint:
    """One bucketed sample from `/host/telemetry`. Columns mirror migration
    018 (`host_telemetry`).

        Attributes:
            cpu_pct (float):
            mem_total_kb (int):
            mem_used_kb (int):
            pending_resize_mb (int):
            pool_available (int):
            reservation_mb (int):
            ts (int):
            vms_running (int):
            ksm_pages_shared (int | None | Unset):
            ksm_pages_sharing (int | None | Unset):
            mem_swap_used_kb (int | None | Unset):
            psi_cpu_avg10 (float | None | Unset):
            psi_io_avg10 (float | None | Unset):
            psi_mem_avg10 (float | None | Unset):
    """

    cpu_pct: float
    mem_total_kb: int
    mem_used_kb: int
    pending_resize_mb: int
    pool_available: int
    reservation_mb: int
    ts: int
    vms_running: int
    ksm_pages_shared: int | None | Unset = UNSET
    ksm_pages_sharing: int | None | Unset = UNSET
    mem_swap_used_kb: int | None | Unset = UNSET
    psi_cpu_avg10: float | None | Unset = UNSET
    psi_io_avg10: float | None | Unset = UNSET
    psi_mem_avg10: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_pct = self.cpu_pct

        mem_total_kb = self.mem_total_kb

        mem_used_kb = self.mem_used_kb

        pending_resize_mb = self.pending_resize_mb

        pool_available = self.pool_available

        reservation_mb = self.reservation_mb

        ts = self.ts

        vms_running = self.vms_running

        ksm_pages_shared: int | None | Unset
        if isinstance(self.ksm_pages_shared, Unset):
            ksm_pages_shared = UNSET
        else:
            ksm_pages_shared = self.ksm_pages_shared

        ksm_pages_sharing: int | None | Unset
        if isinstance(self.ksm_pages_sharing, Unset):
            ksm_pages_sharing = UNSET
        else:
            ksm_pages_sharing = self.ksm_pages_sharing

        mem_swap_used_kb: int | None | Unset
        if isinstance(self.mem_swap_used_kb, Unset):
            mem_swap_used_kb = UNSET
        else:
            mem_swap_used_kb = self.mem_swap_used_kb

        psi_cpu_avg10: float | None | Unset
        if isinstance(self.psi_cpu_avg10, Unset):
            psi_cpu_avg10 = UNSET
        else:
            psi_cpu_avg10 = self.psi_cpu_avg10

        psi_io_avg10: float | None | Unset
        if isinstance(self.psi_io_avg10, Unset):
            psi_io_avg10 = UNSET
        else:
            psi_io_avg10 = self.psi_io_avg10

        psi_mem_avg10: float | None | Unset
        if isinstance(self.psi_mem_avg10, Unset):
            psi_mem_avg10 = UNSET
        else:
            psi_mem_avg10 = self.psi_mem_avg10

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu_pct": cpu_pct,
                "mem_total_kb": mem_total_kb,
                "mem_used_kb": mem_used_kb,
                "pending_resize_mb": pending_resize_mb,
                "pool_available": pool_available,
                "reservation_mb": reservation_mb,
                "ts": ts,
                "vms_running": vms_running,
            }
        )
        if ksm_pages_shared is not UNSET:
            field_dict["ksm_pages_shared"] = ksm_pages_shared
        if ksm_pages_sharing is not UNSET:
            field_dict["ksm_pages_sharing"] = ksm_pages_sharing
        if mem_swap_used_kb is not UNSET:
            field_dict["mem_swap_used_kb"] = mem_swap_used_kb
        if psi_cpu_avg10 is not UNSET:
            field_dict["psi_cpu_avg10"] = psi_cpu_avg10
        if psi_io_avg10 is not UNSET:
            field_dict["psi_io_avg10"] = psi_io_avg10
        if psi_mem_avg10 is not UNSET:
            field_dict["psi_mem_avg10"] = psi_mem_avg10

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        cpu_pct = d.pop("cpu_pct")

        mem_total_kb = d.pop("mem_total_kb")

        mem_used_kb = d.pop("mem_used_kb")

        pending_resize_mb = d.pop("pending_resize_mb")

        pool_available = d.pop("pool_available")

        reservation_mb = d.pop("reservation_mb")

        ts = d.pop("ts")

        vms_running = d.pop("vms_running")

        def _parse_ksm_pages_shared(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        ksm_pages_shared = _parse_ksm_pages_shared(d.pop("ksm_pages_shared", UNSET))

        def _parse_ksm_pages_sharing(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        ksm_pages_sharing = _parse_ksm_pages_sharing(d.pop("ksm_pages_sharing", UNSET))

        def _parse_mem_swap_used_kb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_swap_used_kb = _parse_mem_swap_used_kb(d.pop("mem_swap_used_kb", UNSET))

        def _parse_psi_cpu_avg10(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        psi_cpu_avg10 = _parse_psi_cpu_avg10(d.pop("psi_cpu_avg10", UNSET))

        def _parse_psi_io_avg10(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        psi_io_avg10 = _parse_psi_io_avg10(d.pop("psi_io_avg10", UNSET))

        def _parse_psi_mem_avg10(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        psi_mem_avg10 = _parse_psi_mem_avg10(d.pop("psi_mem_avg10", UNSET))

        host_telemetry_point = cls(
            cpu_pct=cpu_pct,
            mem_total_kb=mem_total_kb,
            mem_used_kb=mem_used_kb,
            pending_resize_mb=pending_resize_mb,
            pool_available=pool_available,
            reservation_mb=reservation_mb,
            ts=ts,
            vms_running=vms_running,
            ksm_pages_shared=ksm_pages_shared,
            ksm_pages_sharing=ksm_pages_sharing,
            mem_swap_used_kb=mem_swap_used_kb,
            psi_cpu_avg10=psi_cpu_avg10,
            psi_io_avg10=psi_io_avg10,
            psi_mem_avg10=psi_mem_avg10,
        )

        host_telemetry_point.additional_properties = d
        return host_telemetry_point

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
