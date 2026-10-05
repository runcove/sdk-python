from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_0_code import DenyReasonType0Code

T = TypeVar("T", bound="DenyReasonType0")


@_attrs_define
class DenyReasonType0:
    """
    Attributes:
        code (DenyReasonType0Code):
        headroom_mb (int):
        requested_mb (int):
        reservation_mb (int):
    """

    code: DenyReasonType0Code
    headroom_mb: int
    requested_mb: int
    reservation_mb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        headroom_mb = self.headroom_mb

        requested_mb = self.requested_mb

        reservation_mb = self.reservation_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "headroom_mb": headroom_mb,
                "requested_mb": requested_mb,
                "reservation_mb": reservation_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType0Code(d.pop("code"))

        headroom_mb = d.pop("headroom_mb")

        requested_mb = d.pop("requested_mb")

        reservation_mb = d.pop("reservation_mb")

        deny_reason_type_0 = cls(
            code=code,
            headroom_mb=headroom_mb,
            requested_mb=requested_mb,
            reservation_mb=reservation_mb,
        )

        deny_reason_type_0.additional_properties = d
        return deny_reason_type_0

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
