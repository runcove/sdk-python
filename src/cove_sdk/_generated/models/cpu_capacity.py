from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="CpuCapacity")


@_attrs_define
class CpuCapacity:
    """Summary of host CPU overcommit numbers.

    Attributes:
        cpu_ratio (float):
        headroom_vcpus (int):
        host_cores (int):
        reservation_vcpus (int):
    """

    cpu_ratio: float
    headroom_vcpus: int
    host_cores: int
    reservation_vcpus: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_ratio = self.cpu_ratio

        headroom_vcpus = self.headroom_vcpus

        host_cores = self.host_cores

        reservation_vcpus = self.reservation_vcpus

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu_ratio": cpu_ratio,
                "headroom_vcpus": headroom_vcpus,
                "host_cores": host_cores,
                "reservation_vcpus": reservation_vcpus,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        cpu_ratio = d.pop("cpu_ratio")

        headroom_vcpus = d.pop("headroom_vcpus")

        host_cores = d.pop("host_cores")

        reservation_vcpus = d.pop("reservation_vcpus")

        cpu_capacity = cls(
            cpu_ratio=cpu_ratio,
            headroom_vcpus=headroom_vcpus,
            host_cores=host_cores,
            reservation_vcpus=reservation_vcpus,
        )

        cpu_capacity.additional_properties = d
        return cpu_capacity

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
