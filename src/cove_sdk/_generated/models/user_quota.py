from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.quota_usage_count import QuotaUsageCount
    from ..models.quota_usage_size import QuotaUsageSize


T = TypeVar("T", bound="UserQuota")


@_attrs_define
class UserQuota:
    """Per-user quota usage + caps, four dimensions.

    Populated by `QuotaChecker::user_summary` (cove-service) for the profile
    page. v1 wire shape.

    The default value is "all zero" (no usage, no cap). Test fixtures, mock
    API impls, and `unwrap_or_else` fallbacks construct via `Default` to keep
    boilerplate down at the seven `ProfileSummary { … }` sites; the real
    values flow from cove-service.

        Attributes:
            disk_gb (QuotaUsageSize): A current/max pair for a size dimension, in the unit its field names (`ram_mb`,
                `disk_gb`).
            ram_mb (QuotaUsageSize): A current/max pair for a size dimension, in the unit its field names (`ram_mb`,
                `disk_gb`).
            vcpus (QuotaUsageCount): A current/max pair for a count dimension (vCPUs, VMs).
            vm_count (QuotaUsageCount): A current/max pair for a count dimension (vCPUs, VMs).
    """

    disk_gb: QuotaUsageSize
    ram_mb: QuotaUsageSize
    vcpus: QuotaUsageCount
    vm_count: QuotaUsageCount
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_gb = self.disk_gb.to_dict()

        ram_mb = self.ram_mb.to_dict()

        vcpus = self.vcpus.to_dict()

        vm_count = self.vm_count.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disk_gb": disk_gb,
                "ram_mb": ram_mb,
                "vcpus": vcpus,
                "vm_count": vm_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.quota_usage_count import QuotaUsageCount
        from ..models.quota_usage_size import QuotaUsageSize

        d = dict(src_dict)
        disk_gb = QuotaUsageSize.from_dict(d.pop("disk_gb"))

        ram_mb = QuotaUsageSize.from_dict(d.pop("ram_mb"))

        vcpus = QuotaUsageCount.from_dict(d.pop("vcpus"))

        vm_count = QuotaUsageCount.from_dict(d.pop("vm_count"))

        user_quota = cls(
            disk_gb=disk_gb,
            ram_mb=ram_mb,
            vcpus=vcpus,
            vm_count=vm_count,
        )

        user_quota.additional_properties = d
        return user_quota

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
