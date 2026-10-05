from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AdminRetimeoutVm")


@_attrs_define
class AdminRetimeoutVm:
    """One entry in [`AdminRetimeoutResponse::changed`] /
    [`AdminRetimeoutResponse::skipped_custom`].

        Attributes:
            current_secs (int):
            vm_id (str):
            vm_name (str):
    """

    current_secs: int
    vm_id: str
    vm_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_secs = self.current_secs

        vm_id = self.vm_id

        vm_name = self.vm_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_secs": current_secs,
                "vm_id": vm_id,
                "vm_name": vm_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        current_secs = d.pop("current_secs")

        vm_id = d.pop("vm_id")

        vm_name = d.pop("vm_name")

        admin_retimeout_vm = cls(
            current_secs=current_secs,
            vm_id=vm_id,
            vm_name=vm_name,
        )

        admin_retimeout_vm.additional_properties = d
        return admin_retimeout_vm

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
