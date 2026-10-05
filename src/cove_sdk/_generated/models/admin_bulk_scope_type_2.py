from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.admin_bulk_scope_type_2_type import AdminBulkScopeType2Type

T = TypeVar("T", bound="AdminBulkScopeType2")


@_attrs_define
class AdminBulkScopeType2:
    """An admin-picked VM name set (the `/admin/users`
    stale-view checkbox multi-select). Unknown names are silently dropped
    server-side (mirrors the `User` arm's "assignment with no core row is
    dropped" precedent) rather than erroring, since the web caller
    constructs `vm_names` from the very page it just rendered.

        Attributes:
            type_ (AdminBulkScopeType2Type):
            vm_names (list[str]):
    """

    type_: AdminBulkScopeType2Type
    vm_names: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        vm_names = self.vm_names

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "vm_names": vm_names,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = AdminBulkScopeType2Type(d.pop("type"))

        vm_names = cast(list[str], d.pop("vm_names"))

        admin_bulk_scope_type_2 = cls(
            type_=type_,
            vm_names=vm_names,
        )

        admin_bulk_scope_type_2.additional_properties = d
        return admin_bulk_scope_type_2

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
