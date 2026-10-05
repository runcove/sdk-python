from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_10_code import DenyReasonType10Code

T = TypeVar("T", bound="DenyReasonType10")


@_attrs_define
class DenyReasonType10:
    """
    Attributes:
        code (DenyReasonType10Code):
        limit_mb (int):
        requested_mb (int):
        used_mb (int):
    """

    code: DenyReasonType10Code
    limit_mb: int
    requested_mb: int
    used_mb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        limit_mb = self.limit_mb

        requested_mb = self.requested_mb

        used_mb = self.used_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "limit_mb": limit_mb,
                "requested_mb": requested_mb,
                "used_mb": used_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType10Code(d.pop("code"))

        limit_mb = d.pop("limit_mb")

        requested_mb = d.pop("requested_mb")

        used_mb = d.pop("used_mb")

        deny_reason_type_10 = cls(
            code=code,
            limit_mb=limit_mb,
            requested_mb=requested_mb,
            used_mb=used_mb,
        )

        deny_reason_type_10.additional_properties = d
        return deny_reason_type_10

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
