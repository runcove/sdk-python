from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.quota_usage_count import QuotaUsageCount
    from ..models.quota_usage_size import QuotaUsageSize


T = TypeVar("T", bound="TeamQuota")


@_attrs_define
class TeamQuota:
    """Per-team quota usage + caps, four dimensions — same shape as
    [`UserQuota`]. Populated by `QuotaChecker::team_summary` for the
    admin console and the self-view `cove quota --team <name>` path.

        Attributes:
            disk_gb (QuotaUsageSize): A current/max pair for a size dimension, in the unit its field names (`ram_mb`,
                `disk_gb`).
            ram_mb (QuotaUsageSize): A current/max pair for a size dimension, in the unit its field names (`ram_mb`,
                `disk_gb`).
            team_id (str):
            team_name (str):
            vcpus (QuotaUsageCount): A current/max pair for a count dimension (vCPUs, VMs).
            vm_count (QuotaUsageCount): A current/max pair for a count dimension (vCPUs, VMs).
    """

    disk_gb: QuotaUsageSize
    ram_mb: QuotaUsageSize
    team_id: str
    team_name: str
    vcpus: QuotaUsageCount
    vm_count: QuotaUsageCount
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_gb = self.disk_gb.to_dict()

        ram_mb = self.ram_mb.to_dict()

        team_id = self.team_id

        team_name = self.team_name

        vcpus = self.vcpus.to_dict()

        vm_count = self.vm_count.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disk_gb": disk_gb,
                "ram_mb": ram_mb,
                "team_id": team_id,
                "team_name": team_name,
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

        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        vcpus = QuotaUsageCount.from_dict(d.pop("vcpus"))

        vm_count = QuotaUsageCount.from_dict(d.pop("vm_count"))

        team_quota = cls(
            disk_gb=disk_gb,
            ram_mb=ram_mb,
            team_id=team_id,
            team_name=team_name,
            vcpus=vcpus,
            vm_count=vm_count,
        )

        team_quota.additional_properties = d
        return team_quota

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
