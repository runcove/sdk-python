from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AdminQuotaDefaultsResponse")


@_attrs_define
class AdminQuotaDefaultsResponse:
    """`GET /api/admin/quota-defaults` — the host-wide `[quota]` config
    baseline (admin-ux polish). Read-only; every dim is always populated
    (never `Option`) since these are the values a `None` override dim
    COALESCEs to, not an override themselves.

        Attributes:
            disk_gb_max (int):
            ram_mb_max (int):
            vcpus_max (int):
            vm_count_max (int):
    """

    disk_gb_max: int
    ram_mb_max: int
    vcpus_max: int
    vm_count_max: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_gb_max = self.disk_gb_max

        ram_mb_max = self.ram_mb_max

        vcpus_max = self.vcpus_max

        vm_count_max = self.vm_count_max

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disk_gb_max": disk_gb_max,
                "ram_mb_max": ram_mb_max,
                "vcpus_max": vcpus_max,
                "vm_count_max": vm_count_max,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        disk_gb_max = d.pop("disk_gb_max")

        ram_mb_max = d.pop("ram_mb_max")

        vcpus_max = d.pop("vcpus_max")

        vm_count_max = d.pop("vm_count_max")

        admin_quota_defaults_response = cls(
            disk_gb_max=disk_gb_max,
            ram_mb_max=ram_mb_max,
            vcpus_max=vcpus_max,
            vm_count_max=vm_count_max,
        )

        admin_quota_defaults_response.additional_properties = d
        return admin_quota_defaults_response

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
