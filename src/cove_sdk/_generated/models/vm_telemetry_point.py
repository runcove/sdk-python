from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmTelemetryPoint")


@_attrs_define
class VmTelemetryPoint:
    """One bucketed per-VM telemetry sample. Within a bucket, integer counters
    are MAX'd. All metrics optional (older daemons omit newer columns).

        Attributes:
            ts (int):
            cpu_pct (float | None | Unset):
            ksm_pages_shared (int | None | Unset):
            ksm_pages_sharing (int | None | Unset):
            mem_active_kb (int | None | Unset):
            mem_anonymous_kb (int | None | Unset):
            mem_inactive_kb (int | None | Unset):
            mem_online_blocks (int | None | Unset):
            mem_swap_used_kb (int | None | Unset):
            mem_used_kb (int | None | Unset):
            mglru_max_seq (int | None | Unset):
            mglru_min_seq (int | None | Unset):
            psi_cpu_avg10 (float | None | Unset):
            psi_io_avg10 (float | None | Unset):
            psi_mem_avg10 (float | None | Unset):
    """

    ts: int
    cpu_pct: float | None | Unset = UNSET
    ksm_pages_shared: int | None | Unset = UNSET
    ksm_pages_sharing: int | None | Unset = UNSET
    mem_active_kb: int | None | Unset = UNSET
    mem_anonymous_kb: int | None | Unset = UNSET
    mem_inactive_kb: int | None | Unset = UNSET
    mem_online_blocks: int | None | Unset = UNSET
    mem_swap_used_kb: int | None | Unset = UNSET
    mem_used_kb: int | None | Unset = UNSET
    mglru_max_seq: int | None | Unset = UNSET
    mglru_min_seq: int | None | Unset = UNSET
    psi_cpu_avg10: float | None | Unset = UNSET
    psi_io_avg10: float | None | Unset = UNSET
    psi_mem_avg10: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ts = self.ts

        cpu_pct: float | None | Unset
        if isinstance(self.cpu_pct, Unset):
            cpu_pct = UNSET
        else:
            cpu_pct = self.cpu_pct

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

        mem_active_kb: int | None | Unset
        if isinstance(self.mem_active_kb, Unset):
            mem_active_kb = UNSET
        else:
            mem_active_kb = self.mem_active_kb

        mem_anonymous_kb: int | None | Unset
        if isinstance(self.mem_anonymous_kb, Unset):
            mem_anonymous_kb = UNSET
        else:
            mem_anonymous_kb = self.mem_anonymous_kb

        mem_inactive_kb: int | None | Unset
        if isinstance(self.mem_inactive_kb, Unset):
            mem_inactive_kb = UNSET
        else:
            mem_inactive_kb = self.mem_inactive_kb

        mem_online_blocks: int | None | Unset
        if isinstance(self.mem_online_blocks, Unset):
            mem_online_blocks = UNSET
        else:
            mem_online_blocks = self.mem_online_blocks

        mem_swap_used_kb: int | None | Unset
        if isinstance(self.mem_swap_used_kb, Unset):
            mem_swap_used_kb = UNSET
        else:
            mem_swap_used_kb = self.mem_swap_used_kb

        mem_used_kb: int | None | Unset
        if isinstance(self.mem_used_kb, Unset):
            mem_used_kb = UNSET
        else:
            mem_used_kb = self.mem_used_kb

        mglru_max_seq: int | None | Unset
        if isinstance(self.mglru_max_seq, Unset):
            mglru_max_seq = UNSET
        else:
            mglru_max_seq = self.mglru_max_seq

        mglru_min_seq: int | None | Unset
        if isinstance(self.mglru_min_seq, Unset):
            mglru_min_seq = UNSET
        else:
            mglru_min_seq = self.mglru_min_seq

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
                "ts": ts,
            }
        )
        if cpu_pct is not UNSET:
            field_dict["cpu_pct"] = cpu_pct
        if ksm_pages_shared is not UNSET:
            field_dict["ksm_pages_shared"] = ksm_pages_shared
        if ksm_pages_sharing is not UNSET:
            field_dict["ksm_pages_sharing"] = ksm_pages_sharing
        if mem_active_kb is not UNSET:
            field_dict["mem_active_kb"] = mem_active_kb
        if mem_anonymous_kb is not UNSET:
            field_dict["mem_anonymous_kb"] = mem_anonymous_kb
        if mem_inactive_kb is not UNSET:
            field_dict["mem_inactive_kb"] = mem_inactive_kb
        if mem_online_blocks is not UNSET:
            field_dict["mem_online_blocks"] = mem_online_blocks
        if mem_swap_used_kb is not UNSET:
            field_dict["mem_swap_used_kb"] = mem_swap_used_kb
        if mem_used_kb is not UNSET:
            field_dict["mem_used_kb"] = mem_used_kb
        if mglru_max_seq is not UNSET:
            field_dict["mglru_max_seq"] = mglru_max_seq
        if mglru_min_seq is not UNSET:
            field_dict["mglru_min_seq"] = mglru_min_seq
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
        ts = d.pop("ts")

        def _parse_cpu_pct(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cpu_pct = _parse_cpu_pct(d.pop("cpu_pct", UNSET))

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

        def _parse_mem_active_kb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_active_kb = _parse_mem_active_kb(d.pop("mem_active_kb", UNSET))

        def _parse_mem_anonymous_kb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_anonymous_kb = _parse_mem_anonymous_kb(d.pop("mem_anonymous_kb", UNSET))

        def _parse_mem_inactive_kb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_inactive_kb = _parse_mem_inactive_kb(d.pop("mem_inactive_kb", UNSET))

        def _parse_mem_online_blocks(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_online_blocks = _parse_mem_online_blocks(d.pop("mem_online_blocks", UNSET))

        def _parse_mem_swap_used_kb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_swap_used_kb = _parse_mem_swap_used_kb(d.pop("mem_swap_used_kb", UNSET))

        def _parse_mem_used_kb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mem_used_kb = _parse_mem_used_kb(d.pop("mem_used_kb", UNSET))

        def _parse_mglru_max_seq(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mglru_max_seq = _parse_mglru_max_seq(d.pop("mglru_max_seq", UNSET))

        def _parse_mglru_min_seq(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mglru_min_seq = _parse_mglru_min_seq(d.pop("mglru_min_seq", UNSET))

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

        vm_telemetry_point = cls(
            ts=ts,
            cpu_pct=cpu_pct,
            ksm_pages_shared=ksm_pages_shared,
            ksm_pages_sharing=ksm_pages_sharing,
            mem_active_kb=mem_active_kb,
            mem_anonymous_kb=mem_anonymous_kb,
            mem_inactive_kb=mem_inactive_kb,
            mem_online_blocks=mem_online_blocks,
            mem_swap_used_kb=mem_swap_used_kb,
            mem_used_kb=mem_used_kb,
            mglru_max_seq=mglru_max_seq,
            mglru_min_seq=mglru_min_seq,
            psi_cpu_avg10=psi_cpu_avg10,
            psi_io_avg10=psi_io_avg10,
            psi_mem_avg10=psi_mem_avg10,
        )

        vm_telemetry_point.additional_properties = d
        return vm_telemetry_point

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
