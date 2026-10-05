from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="TagEntry")


@_attrs_define
class TagEntry:
    """A single tag entry returned by `list_tags_for_vm`.

    Attributes:
        key (str):
        set_at (datetime.datetime):
        set_by (str):
        value (str):
    """

    key: str
    set_at: datetime.datetime
    set_by: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        set_at = self.set_at.isoformat()

        set_by = self.set_by

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "set_at": set_at,
                "set_by": set_by,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        key = d.pop("key")

        set_at = datetime.datetime.fromisoformat(d.pop("set_at"))

        set_by = d.pop("set_by")

        value = d.pop("value")

        tag_entry = cls(
            key=key,
            set_at=set_at,
            set_by=set_by,
            value=value,
        )

        tag_entry.additional_properties = d
        return tag_entry

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
