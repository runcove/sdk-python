from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ImportResponse")


@_attrs_define
class ImportResponse:
    """POST /vms/{name}/secrets/import response body. Reports how many of the
    submitted entries actually landed (invalid names are silently skipped:
    import is best-effort). The server-side duplicate this
    replaces used `usize`; the client-side one used `u64` — harmless on a
    64-bit target (both serialize as the same JSON number) but still a type
    mismatch a genuinely shared definition can't have.

        Attributes:
            imported (int):
    """

    imported: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        imported = self.imported

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imported": imported,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        imported = d.pop("imported")

        import_response = cls(
            imported=imported,
        )

        import_response.additional_properties = d
        return import_response

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
