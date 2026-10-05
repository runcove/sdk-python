from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_2_code import DenyReasonType2Code

T = TypeVar("T", bound="DenyReasonType2")


@_attrs_define
class DenyReasonType2:
    """
    Attributes:
        code (DenyReasonType2Code):
        delta_bytes (int):
        soft_limit_bytes (int):
        used_bytes (int):
    """

    code: DenyReasonType2Code
    delta_bytes: int
    soft_limit_bytes: int
    used_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        delta_bytes = self.delta_bytes

        soft_limit_bytes = self.soft_limit_bytes

        used_bytes = self.used_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "delta_bytes": delta_bytes,
                "soft_limit_bytes": soft_limit_bytes,
                "used_bytes": used_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType2Code(d.pop("code"))

        delta_bytes = d.pop("delta_bytes")

        soft_limit_bytes = d.pop("soft_limit_bytes")

        used_bytes = d.pop("used_bytes")

        deny_reason_type_2 = cls(
            code=code,
            delta_bytes=delta_bytes,
            soft_limit_bytes=soft_limit_bytes,
            used_bytes=used_bytes,
        )

        deny_reason_type_2.additional_properties = d
        return deny_reason_type_2

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
