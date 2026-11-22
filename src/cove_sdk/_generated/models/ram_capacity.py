from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="RamCapacity")


@_attrs_define
class RamCapacity:
    """Summary of host RAM overcommit numbers, as reported by `GET /host/capacity`.

    Attributes:
        headroom_mb (int):
        host_total_mb (int):
        mem_available_mb (int): `MemAvailable` on Linux. 0 on a Mac, like the swap and PSI fields:
            a Mac's admission does not read host memory pressure (its guest-RAM
            guard caps the VMs instead), so none of them is sampled there.
        pending_resize_mb (int):
        psi_mem_avg10_pct (float):
        ratio (float):
        reservation_mb (int): Memory, in MB, held by the live reservations: the short-lived rows a
            create, clone, wake or grow holds while it is in flight, released
            when it ends. A VM that is already running holds none. A clone, a
            grow or a wake is admitted when this sum plus its own memory fits in
            `headroom_mb`.
        reserved_mb (int):
        swap_total_mb (int):
        swap_used_mb (int):
        committed_mb (int | None | Unset): The guest memory this cove instance has committed, in MB: every VM
            that holds its guest RAM (creating, running, paused, pooled or
            stopping, part way through a pause, resume, checkpoint, hibernate,
            wake, forced stop or delete, or being woken; not hibernated, stopped
            or failed) at its current size, or its boot size if larger, plus each
            live reservation no such VM accounts for. A grow's reservation counts on top of its VM until released.
            Compare it with `headroom_mb`, the `[overcommit] ratio` budget.
            It covers this instance only: two cove instances on one host each
            budget the whole host and neither counts the other's VMs. Reported
            only: nothing is refused on it yet. Absent from a server that
            predates it.
    """

    headroom_mb: int
    host_total_mb: int
    mem_available_mb: int
    pending_resize_mb: int
    psi_mem_avg10_pct: float
    ratio: float
    reservation_mb: int
    reserved_mb: int
    swap_total_mb: int
    swap_used_mb: int
    committed_mb: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        headroom_mb = self.headroom_mb

        host_total_mb = self.host_total_mb

        mem_available_mb = self.mem_available_mb

        pending_resize_mb = self.pending_resize_mb

        psi_mem_avg10_pct = self.psi_mem_avg10_pct

        ratio = self.ratio

        reservation_mb = self.reservation_mb

        reserved_mb = self.reserved_mb

        swap_total_mb = self.swap_total_mb

        swap_used_mb = self.swap_used_mb

        committed_mb: int | None | Unset
        if isinstance(self.committed_mb, Unset):
            committed_mb = UNSET
        else:
            committed_mb = self.committed_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "headroom_mb": headroom_mb,
                "host_total_mb": host_total_mb,
                "mem_available_mb": mem_available_mb,
                "pending_resize_mb": pending_resize_mb,
                "psi_mem_avg10_pct": psi_mem_avg10_pct,
                "ratio": ratio,
                "reservation_mb": reservation_mb,
                "reserved_mb": reserved_mb,
                "swap_total_mb": swap_total_mb,
                "swap_used_mb": swap_used_mb,
            }
        )
        if committed_mb is not UNSET:
            field_dict["committed_mb"] = committed_mb

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        headroom_mb = d.pop("headroom_mb")

        host_total_mb = d.pop("host_total_mb")

        mem_available_mb = d.pop("mem_available_mb")

        pending_resize_mb = d.pop("pending_resize_mb")

        psi_mem_avg10_pct = d.pop("psi_mem_avg10_pct")

        ratio = d.pop("ratio")

        reservation_mb = d.pop("reservation_mb")

        reserved_mb = d.pop("reserved_mb")

        swap_total_mb = d.pop("swap_total_mb")

        swap_used_mb = d.pop("swap_used_mb")

        def _parse_committed_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        committed_mb = _parse_committed_mb(d.pop("committed_mb", UNSET))

        ram_capacity = cls(
            headroom_mb=headroom_mb,
            host_total_mb=host_total_mb,
            mem_available_mb=mem_available_mb,
            pending_resize_mb=pending_resize_mb,
            psi_mem_avg10_pct=psi_mem_avg10_pct,
            ratio=ratio,
            reservation_mb=reservation_mb,
            reserved_mb=reserved_mb,
            swap_total_mb=swap_total_mb,
            swap_used_mb=swap_used_mb,
            committed_mb=committed_mb,
        )

        ram_capacity.additional_properties = d
        return ram_capacity

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
