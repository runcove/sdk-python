from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.pending_action_type_4_type import PendingActionType4Type

T = TypeVar("T", bound="PendingActionType4")


@_attrs_define
class PendingActionType4:
    """
    Attributes:
        checkpoint_id (UUID):
        disk_bytes (int):
        memory_min_mb (int):
        type_ (PendingActionType4Type):
        vcpus_min (int):
    """

    checkpoint_id: UUID
    disk_bytes: int
    memory_min_mb: int
    type_: PendingActionType4Type
    vcpus_min: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkpoint_id = str(self.checkpoint_id)

        disk_bytes = self.disk_bytes

        memory_min_mb = self.memory_min_mb

        type_ = self.type_.value

        vcpus_min = self.vcpus_min

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkpoint_id": checkpoint_id,
                "disk_bytes": disk_bytes,
                "memory_min_mb": memory_min_mb,
                "type": type_,
                "vcpus_min": vcpus_min,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        checkpoint_id = UUID(d.pop("checkpoint_id"))

        disk_bytes = d.pop("disk_bytes")

        memory_min_mb = d.pop("memory_min_mb")

        type_ = PendingActionType4Type(d.pop("type"))

        vcpus_min = d.pop("vcpus_min")

        pending_action_type_4 = cls(
            checkpoint_id=checkpoint_id,
            disk_bytes=disk_bytes,
            memory_min_mb=memory_min_mb,
            type_=type_,
            vcpus_min=vcpus_min,
        )

        pending_action_type_4.additional_properties = d
        return pending_action_type_4

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
