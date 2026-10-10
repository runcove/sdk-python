from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="CloneRequestTagsType0")


@_attrs_define
class CloneRequestTagsType0:
    """Tags for the clone, replacing the source's. Omitted, the clone gets
    the source's tags; an empty object gives it none. Each entry obeys
    the same rules as setting a tag, and at most 50 are allowed; a bad
    one is refused with 400 before anything is cloned. A non-empty set
    needs `tags:write` as well as `vms:write` (403 `scope_denied`
    without it).

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        clone_request_tags_type_0 = cls()

        clone_request_tags_type_0.additional_properties = d
        return clone_request_tags_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
