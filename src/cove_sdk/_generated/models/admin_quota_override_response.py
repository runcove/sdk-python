from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminQuotaOverrideResponse")


@_attrs_define
class AdminQuotaOverrideResponse:
    """
    Attributes:
        username (str):
        disk_gb_max (int | None | Unset):
        ram_mb_max (int | None | Unset):
        vcpus_max (int | None | Unset):
        vm_count_max (int | None | Unset):
    """

    username: str
    disk_gb_max: int | None | Unset = UNSET
    ram_mb_max: int | None | Unset = UNSET
    vcpus_max: int | None | Unset = UNSET
    vm_count_max: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        disk_gb_max: int | None | Unset
        if isinstance(self.disk_gb_max, Unset):
            disk_gb_max = UNSET
        else:
            disk_gb_max = self.disk_gb_max

        ram_mb_max: int | None | Unset
        if isinstance(self.ram_mb_max, Unset):
            ram_mb_max = UNSET
        else:
            ram_mb_max = self.ram_mb_max

        vcpus_max: int | None | Unset
        if isinstance(self.vcpus_max, Unset):
            vcpus_max = UNSET
        else:
            vcpus_max = self.vcpus_max

        vm_count_max: int | None | Unset
        if isinstance(self.vm_count_max, Unset):
            vm_count_max = UNSET
        else:
            vm_count_max = self.vm_count_max

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
            }
        )
        if disk_gb_max is not UNSET:
            field_dict["disk_gb_max"] = disk_gb_max
        if ram_mb_max is not UNSET:
            field_dict["ram_mb_max"] = ram_mb_max
        if vcpus_max is not UNSET:
            field_dict["vcpus_max"] = vcpus_max
        if vm_count_max is not UNSET:
            field_dict["vm_count_max"] = vm_count_max

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        username = d.pop("username")

        def _parse_disk_gb_max(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        disk_gb_max = _parse_disk_gb_max(d.pop("disk_gb_max", UNSET))

        def _parse_ram_mb_max(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        ram_mb_max = _parse_ram_mb_max(d.pop("ram_mb_max", UNSET))

        def _parse_vcpus_max(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        vcpus_max = _parse_vcpus_max(d.pop("vcpus_max", UNSET))

        def _parse_vm_count_max(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        vm_count_max = _parse_vm_count_max(d.pop("vm_count_max", UNSET))

        admin_quota_override_response = cls(
            username=username,
            disk_gb_max=disk_gb_max,
            ram_mb_max=ram_mb_max,
            vcpus_max=vcpus_max,
            vm_count_max=vm_count_max,
        )

        admin_quota_override_response.additional_properties = d
        return admin_quota_override_response

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
