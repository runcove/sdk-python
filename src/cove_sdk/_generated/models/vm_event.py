from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmEvent")


@_attrs_define
class VmEvent:
    """One row from `/vms/{name}/events-log`. Mirrors migration 019.

    Attributes:
        id (int):
        kind (str):
        ts (int):
        vm_id (str):
        payload (Any | Unset):
    """

    id: int
    kind: str
    ts: int
    vm_id: str
    payload: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        kind = self.kind

        ts = self.ts

        vm_id = self.vm_id

        payload = self.payload

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "ts": ts,
                "vm_id": vm_id,
            }
        )
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        kind = d.pop("kind")

        ts = d.pop("ts")

        vm_id = d.pop("vm_id")

        payload = d.pop("payload", UNSET)

        vm_event = cls(
            id=id,
            kind=kind,
            ts=ts,
            vm_id=vm_id,
            payload=payload,
        )

        vm_event.additional_properties = d
        return vm_event

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
