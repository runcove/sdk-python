from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_13_code import DenyReasonType13Code

T = TypeVar("T", bound="DenyReasonType13")


@_attrs_define
class DenyReasonType13:
    """
    Attributes:
        code (DenyReasonType13Code):
        limit (int):
        requested (int):
        used (int):
    """

    code: DenyReasonType13Code
    limit: int
    requested: int
    used: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        limit = self.limit

        requested = self.requested

        used = self.used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "limit": limit,
                "requested": requested,
                "used": used,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType13Code(d.pop("code"))

        limit = d.pop("limit")

        requested = d.pop("requested")

        used = d.pop("used")

        deny_reason_type_13 = cls(
            code=code,
            limit=limit,
            requested=requested,
            used=used,
        )

        deny_reason_type_13.additional_properties = d
        return deny_reason_type_13

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
