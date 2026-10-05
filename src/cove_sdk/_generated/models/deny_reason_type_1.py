from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_1_code import DenyReasonType1Code

T = TypeVar("T", bound="DenyReasonType1")


@_attrs_define
class DenyReasonType1:
    """
    Attributes:
        code (DenyReasonType1Code):
        committed (int):
        headroom (int):
        requested (int):
    """

    code: DenyReasonType1Code
    committed: int
    headroom: int
    requested: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        committed = self.committed

        headroom = self.headroom

        requested = self.requested

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "committed": committed,
                "headroom": headroom,
                "requested": requested,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType1Code(d.pop("code"))

        committed = d.pop("committed")

        headroom = d.pop("headroom")

        requested = d.pop("requested")

        deny_reason_type_1 = cls(
            code=code,
            committed=committed,
            headroom=headroom,
            requested=requested,
        )

        deny_reason_type_1.additional_properties = d
        return deny_reason_type_1

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
