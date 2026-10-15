from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="DrainVmDto")


@_attrs_define
class DrainVmDto:
    """One VM a drain looked at, as it stood when the drain began.

    Attributes:
        state_before (str): `"running"` or `"paused"` for a VM the drain set out to stop;
            `"hibernated"` for one it left alone.
        vm_id (str):
        vm_name (str):
        owner (None | str | Unset):
    """

    state_before: str
    vm_id: str
    vm_name: str
    owner: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state_before = self.state_before

        vm_id = self.vm_id

        vm_name = self.vm_name

        owner: None | str | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state_before": state_before,
                "vm_id": vm_id,
                "vm_name": vm_name,
            }
        )
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        state_before = d.pop("state_before")

        vm_id = d.pop("vm_id")

        vm_name = d.pop("vm_name")

        def _parse_owner(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        drain_vm_dto = cls(
            state_before=state_before,
            vm_id=vm_id,
            vm_name=vm_name,
            owner=owner,
        )

        drain_vm_dto.additional_properties = d
        return drain_vm_dto

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
