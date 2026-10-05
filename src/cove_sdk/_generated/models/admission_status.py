from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.capacity_report import CapacityReport
    from ..models.deny_event import DenyEvent
    from ..models.user_quota import UserQuota


T = TypeVar("T", bound="AdmissionStatus")


@_attrs_define
class AdmissionStatus:
    """Response body for `GET /host/admission`.

    Attributes:
        capacity (CapacityReport): Full capacity report returned by `GET /host/capacity`.
        recent_denies (list[DenyEvent] | Unset):
        user_quotas (list[UserQuota] | Unset):
    """

    capacity: CapacityReport
    recent_denies: list[DenyEvent] | Unset = UNSET
    user_quotas: list[UserQuota] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        capacity = self.capacity.to_dict()

        recent_denies: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recent_denies, Unset):
            recent_denies = []
            for recent_denies_item_data in self.recent_denies:
                recent_denies_item = recent_denies_item_data.to_dict()
                recent_denies.append(recent_denies_item)

        user_quotas: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.user_quotas, Unset):
            user_quotas = []
            for user_quotas_item_data in self.user_quotas:
                user_quotas_item = user_quotas_item_data.to_dict()
                user_quotas.append(user_quotas_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "capacity": capacity,
            }
        )
        if recent_denies is not UNSET:
            field_dict["recent_denies"] = recent_denies
        if user_quotas is not UNSET:
            field_dict["user_quotas"] = user_quotas

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.capacity_report import CapacityReport
        from ..models.deny_event import DenyEvent
        from ..models.user_quota import UserQuota

        d = dict(src_dict)
        capacity = CapacityReport.from_dict(d.pop("capacity"))

        _recent_denies = d.pop("recent_denies", UNSET)
        recent_denies: list[DenyEvent] | Unset = UNSET
        if _recent_denies is not UNSET:
            recent_denies = []
            for recent_denies_item_data in _recent_denies:
                recent_denies_item = DenyEvent.from_dict(recent_denies_item_data)

                recent_denies.append(recent_denies_item)

        _user_quotas = d.pop("user_quotas", UNSET)
        user_quotas: list[UserQuota] | Unset = UNSET
        if _user_quotas is not UNSET:
            user_quotas = []
            for user_quotas_item_data in _user_quotas:
                user_quotas_item = UserQuota.from_dict(user_quotas_item_data)

                user_quotas.append(user_quotas_item)

        admission_status = cls(
            capacity=capacity,
            recent_denies=recent_denies,
            user_quotas=user_quotas,
        )

        admission_status.additional_properties = d
        return admission_status

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
