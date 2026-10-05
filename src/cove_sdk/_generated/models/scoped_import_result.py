from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ScopedImportResult")


@_attrs_define
class ScopedImportResult:
    """`POST /users|teams|projects/{scope}/secrets/import` response body —
    how many submitted entries actually landed, and how many running in-scope
    VMs received the merged fan-out. Named `ScopedImportResult` to match the
    outgoing hand-written spec; same ad-hoc-`json!`-construction
    caveat as `VmCountResult` above.

        Attributes:
            imported (int): Entries actually stored; invalid names are silently skipped
                (best-effort import).
            vm_count (int): Running, in-scope VMs the merged set was pushed to (best-effort).
    """

    imported: int
    vm_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        imported = self.imported

        vm_count = self.vm_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imported": imported,
                "vm_count": vm_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        imported = d.pop("imported")

        vm_count = d.pop("vm_count")

        scoped_import_result = cls(
            imported=imported,
            vm_count=vm_count,
        )

        scoped_import_result.additional_properties = d
        return scoped_import_result

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
