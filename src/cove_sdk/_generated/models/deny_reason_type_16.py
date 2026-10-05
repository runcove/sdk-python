from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_16_code import DenyReasonType16Code

T = TypeVar("T", bound="DenyReasonType16")


@_attrs_define
class DenyReasonType16:
    """
    Attributes:
        code (DenyReasonType16Code):
        limit_gb (int):
        requested_gb (int):
        used_gb (int):
    """

    code: DenyReasonType16Code
    limit_gb: int
    requested_gb: int
    used_gb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        limit_gb = self.limit_gb

        requested_gb = self.requested_gb

        used_gb = self.used_gb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "limit_gb": limit_gb,
                "requested_gb": requested_gb,
                "used_gb": used_gb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType16Code(d.pop("code"))

        limit_gb = d.pop("limit_gb")

        requested_gb = d.pop("requested_gb")

        used_gb = d.pop("used_gb")

        deny_reason_type_16 = cls(
            code=code,
            limit_gb=limit_gb,
            requested_gb=requested_gb,
            used_gb=used_gb,
        )

        deny_reason_type_16.additional_properties = d
        return deny_reason_type_16

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
