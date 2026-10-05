from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.pending_action_type_2_type import PendingActionType2Type

T = TypeVar("T", bound="PendingActionType2")


@_attrs_define
class PendingActionType2:
    """Stopped-only, grow-only disk file resize.
    Carries only the positive disk-byte delta — the grow is a file
    `set_len` on a stopped VM, so there is no memory/vcpu hotplug and
    no pending-resize RAM tier. Distinct from `ResizeUp` so the
    cpu/mem path stays untouched.

        Attributes:
            delta_disk_bytes (int):
            type_ (PendingActionType2Type):
            vm_id (UUID): Globally unique VM identifier (UUID v7, time-ordered).
    """

    delta_disk_bytes: int
    type_: PendingActionType2Type
    vm_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delta_disk_bytes = self.delta_disk_bytes

        type_ = self.type_.value

        vm_id = str(self.vm_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delta_disk_bytes": delta_disk_bytes,
                "type": type_,
                "vm_id": vm_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        delta_disk_bytes = d.pop("delta_disk_bytes")

        type_ = PendingActionType2Type(d.pop("type"))

        vm_id = UUID(d.pop("vm_id"))

        pending_action_type_2 = cls(
            delta_disk_bytes=delta_disk_bytes,
            type_=type_,
            vm_id=vm_id,
        )

        pending_action_type_2.additional_properties = d
        return pending_action_type_2

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
