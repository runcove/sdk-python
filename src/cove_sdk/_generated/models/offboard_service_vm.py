from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="OffboardServiceVm")


@_attrs_define
class OffboardServiceVm:
    """A live VM owned by a service bound to the person.

    Attributes:
        service (str): The service name (`svc:<name>` owns the VM).
        vm (str): The VM's name.
    """

    service: str
    vm: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service = self.service

        vm = self.vm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service": service,
                "vm": vm,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        service = d.pop("service")

        vm = d.pop("vm")

        offboard_service_vm = cls(
            service=service,
            vm=vm,
        )

        offboard_service_vm.additional_properties = d
        return offboard_service_vm

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
