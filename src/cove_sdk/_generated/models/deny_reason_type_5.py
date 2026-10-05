from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_5_code import DenyReasonType5Code

T = TypeVar("T", bound="DenyReasonType5")


@_attrs_define
class DenyReasonType5:
    """
    Attributes:
        code (DenyReasonType5Code):
        floor_mb (int):
        mem_available_mb (int):
    """

    code: DenyReasonType5Code
    floor_mb: int
    mem_available_mb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        floor_mb = self.floor_mb

        mem_available_mb = self.mem_available_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "floor_mb": floor_mb,
                "mem_available_mb": mem_available_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType5Code(d.pop("code"))

        floor_mb = d.pop("floor_mb")

        mem_available_mb = d.pop("mem_available_mb")

        deny_reason_type_5 = cls(
            code=code,
            floor_mb=floor_mb,
            mem_available_mb=mem_available_mb,
        )

        deny_reason_type_5.additional_properties = d
        return deny_reason_type_5

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
