from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.deny_reason_type_8_code import DenyReasonType8Code

T = TypeVar("T", bound="DenyReasonType8")


@_attrs_define
class DenyReasonType8:
    """
    Attributes:
        code (DenyReasonType8Code):
        mem_available_mb (int):
        pending_mb (int):
        requested_mb (int):
    """

    code: DenyReasonType8Code
    mem_available_mb: int
    pending_mb: int
    requested_mb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        mem_available_mb = self.mem_available_mb

        pending_mb = self.pending_mb

        requested_mb = self.requested_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "mem_available_mb": mem_available_mb,
                "pending_mb": pending_mb,
                "requested_mb": requested_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = DenyReasonType8Code(d.pop("code"))

        mem_available_mb = d.pop("mem_available_mb")

        pending_mb = d.pop("pending_mb")

        requested_mb = d.pop("requested_mb")

        deny_reason_type_8 = cls(
            code=code,
            mem_available_mb=mem_available_mb,
            pending_mb=pending_mb,
            requested_mb=requested_mb,
        )

        deny_reason_type_8.additional_properties = d
        return deny_reason_type_8

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
