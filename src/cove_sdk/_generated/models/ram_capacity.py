from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RamCapacity")


@_attrs_define
class RamCapacity:
    """Summary of host RAM overcommit numbers, as reported by `GET /host/capacity`.

    Attributes:
        headroom_mb (int):
        host_total_mb (int):
        mem_available_mb (int):
        pending_resize_mb (int):
        psi_mem_avg10_pct (float):
        ratio (float):
        reservation_mb (int):
        reserved_mb (int):
        swap_total_mb (int):
        swap_used_mb (int):
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
