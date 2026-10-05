from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="DiskCapacity")


@_attrs_define
class DiskCapacity:
    """Summary of data-disk space.

    Attributes:
        fs_available_bytes (int):
        fs_total_bytes (int):
        fs_used_bytes (int):
        soft_limit_pct (int):
    """

    fs_available_bytes: int
    fs_total_bytes: int
    fs_used_bytes: int
    soft_limit_pct: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fs_available_bytes = self.fs_available_bytes

        fs_total_bytes = self.fs_total_bytes

        fs_used_bytes = self.fs_used_bytes

        soft_limit_pct = self.soft_limit_pct

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fs_available_bytes": fs_available_bytes,
                "fs_total_bytes": fs_total_bytes,
                "fs_used_bytes": fs_used_bytes,
                "soft_limit_pct": soft_limit_pct,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        fs_available_bytes = d.pop("fs_available_bytes")

        fs_total_bytes = d.pop("fs_total_bytes")

        fs_used_bytes = d.pop("fs_used_bytes")

        soft_limit_pct = d.pop("soft_limit_pct")

        disk_capacity = cls(
            fs_available_bytes=fs_available_bytes,
            fs_total_bytes=fs_total_bytes,
            fs_used_bytes=fs_used_bytes,
            soft_limit_pct=soft_limit_pct,
        )

        disk_capacity.additional_properties = d
        return disk_capacity

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
