from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="TagSummary")


@_attrs_define
class TagSummary:
    """Admin-level / per-caller summary of a distinct tag key.

    Canonical wire shape: `{key,
    distinct_values, vm_count, sample_vms}`. `distinct_values` counts
    distinct values seen for this key across the caller's VMs (one row
    per key, not per (key,value) pair). `vm_count` counts distinct VMs
    carrying the key with any value. `sample_vms` carries up to 5
    representative VM names.

        Attributes:
            distinct_values (int): Number of distinct values observed for this key across the rows.
            key (str):
            sample_vms (list[str]):
            vm_count (int): Number of distinct VMs carrying this key.
    """

    distinct_values: int
    key: str
    sample_vms: list[str]
    vm_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        distinct_values = self.distinct_values

        key = self.key

        sample_vms = self.sample_vms

        vm_count = self.vm_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "distinct_values": distinct_values,
                "key": key,
                "sample_vms": sample_vms,
                "vm_count": vm_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        distinct_values = d.pop("distinct_values")

        key = d.pop("key")

        sample_vms = cast(list[str], d.pop("sample_vms"))

        vm_count = d.pop("vm_count")

        tag_summary = cls(
            distinct_values=distinct_values,
            key=key,
            sample_vms=sample_vms,
            vm_count=vm_count,
        )

        tag_summary.additional_properties = d
        return tag_summary

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
