from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.pending_action_type_6_type import PendingActionType6Type

T = TypeVar("T", bound="PendingActionType6")


@_attrs_define
class PendingActionType6:
    """
    Attributes:
        count (int):
        memory_min_mb (int):
        type_ (PendingActionType6Type):
        vcpus_min (int):
    """

    count: int
    memory_min_mb: int
    type_: PendingActionType6Type
    vcpus_min: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        memory_min_mb = self.memory_min_mb

        type_ = self.type_.value

        vcpus_min = self.vcpus_min

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "memory_min_mb": memory_min_mb,
                "type": type_,
                "vcpus_min": vcpus_min,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        count = d.pop("count")

        memory_min_mb = d.pop("memory_min_mb")

        type_ = PendingActionType6Type(d.pop("type"))

        vcpus_min = d.pop("vcpus_min")

        pending_action_type_6 = cls(
            count=count,
            memory_min_mb=memory_min_mb,
            type_=type_,
            vcpus_min=vcpus_min,
        )

        pending_action_type_6.additional_properties = d
        return pending_action_type_6

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
