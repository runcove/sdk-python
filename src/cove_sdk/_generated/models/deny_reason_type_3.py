from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_3_code import DenyReasonType3Code

T = TypeVar("T", bound="DenyReasonType3")


@_attrs_define
class DenyReasonType3:
    """
    Attributes:
        available_bytes (int):
        code (DenyReasonType3Code):
        needed_bytes (int):
    """

    available_bytes: int
    code: DenyReasonType3Code
    needed_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available_bytes = self.available_bytes

        code = self.code.value

        needed_bytes = self.needed_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available_bytes": available_bytes,
                "code": code,
                "needed_bytes": needed_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        available_bytes = d.pop("available_bytes")

        code = DenyReasonType3Code(d.pop("code"))

        needed_bytes = d.pop("needed_bytes")

        deny_reason_type_3 = cls(
            available_bytes=available_bytes,
            code=code,
            needed_bytes=needed_bytes,
        )

        deny_reason_type_3.additional_properties = d
        return deny_reason_type_3

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
