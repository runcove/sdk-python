from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.delete_after_stop_type_2_type import DeleteAfterStopType2Type

T = TypeVar("T", bound="DeleteAfterStopType2")


@_attrs_define
class DeleteAfterStopType2:
    """Wait `secs` after `stopped_at` before deleting. Service-layer
    validation enforces `secs >= 60`.

        Attributes:
            secs (int):
            type_ (DeleteAfterStopType2Type):
    """

    secs: int
    type_: DeleteAfterStopType2Type
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        secs = self.secs

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secs": secs,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        secs = d.pop("secs")

        type_ = DeleteAfterStopType2Type(d.pop("type"))

        delete_after_stop_type_2 = cls(
            secs=secs,
            type_=type_,
        )

        delete_after_stop_type_2.additional_properties = d
        return delete_after_stop_type_2

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
