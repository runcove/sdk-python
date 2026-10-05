from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_7_code import DenyReasonType7Code

T = TypeVar("T", bound="DenyReasonType7")


@_attrs_define
class DenyReasonType7:
    """
    Attributes:
        code (DenyReasonType7Code):
        swap_used_pct (float):
        threshold_pct (float):
    """

    code: DenyReasonType7Code
    swap_used_pct: float
    threshold_pct: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        swap_used_pct = self.swap_used_pct

        threshold_pct = self.threshold_pct

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "swap_used_pct": swap_used_pct,
                "threshold_pct": threshold_pct,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType7Code(d.pop("code"))

        swap_used_pct = d.pop("swap_used_pct")

        threshold_pct = d.pop("threshold_pct")

        deny_reason_type_7 = cls(
            code=code,
            swap_used_pct=swap_used_pct,
            threshold_pct=threshold_pct,
        )

        deny_reason_type_7.additional_properties = d
        return deny_reason_type_7

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
