from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

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
            derived_from_mac (bool | None | Unset): `Some(true)` when the baseline above was derived
                from the host Mac's own resources (macOS local mode with no
                `[quota]` block in cove.toml), `Some(false)` when it was not (a
                `[quota]` block overrides that derivation, or the Mac's figures could
                not be read and the compiled-in defaults apply), `None` off local mode — every non-macOS
                daemon, which never derives a quota from host resources. Optional so
                a daemon predating this field, or a non-Mac one, keeps emitting
                exactly its old JSON (the key is absent, not `false`).
    """

    disk_gb_max: int
    ram_mb_max: int
    vcpus_max: int
    vm_count_max: int
    derived_from_mac: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_gb_max = self.disk_gb_max

        ram_mb_max = self.ram_mb_max

        vcpus_max = self.vcpus_max

        vm_count_max = self.vm_count_max

        derived_from_mac: bool | None | Unset
        if isinstance(self.derived_from_mac, Unset):
            derived_from_mac = UNSET
        else:
            derived_from_mac = self.derived_from_mac

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
        if derived_from_mac is not UNSET:
            field_dict["derived_from_mac"] = derived_from_mac

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        disk_gb_max = d.pop("disk_gb_max")

        ram_mb_max = d.pop("ram_mb_max")

        vcpus_max = d.pop("vcpus_max")

        vm_count_max = d.pop("vm_count_max")

        def _parse_derived_from_mac(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        derived_from_mac = _parse_derived_from_mac(d.pop("derived_from_mac", UNSET))

        admin_quota_defaults_response = cls(
            disk_gb_max=disk_gb_max,
            ram_mb_max=ram_mb_max,
            vcpus_max=vcpus_max,
            vm_count_max=vm_count_max,
            derived_from_mac=derived_from_mac,
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
