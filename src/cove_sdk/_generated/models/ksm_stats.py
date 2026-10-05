from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="KsmStats")


@_attrs_define
class KsmStats:
    """KSM (kernel same-page merging) sharing counters.

    Attributes:
        full_scans (int):
        pages_shared (int):
        pages_sharing (int):
        pages_unshared (int):
    """

    full_scans: int
    pages_shared: int
    pages_sharing: int
    pages_unshared: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_scans = self.full_scans

        pages_shared = self.pages_shared

        pages_sharing = self.pages_sharing

        pages_unshared = self.pages_unshared

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_scans": full_scans,
                "pages_shared": pages_shared,
                "pages_sharing": pages_sharing,
                "pages_unshared": pages_unshared,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        full_scans = d.pop("full_scans")

        pages_shared = d.pop("pages_shared")

        pages_sharing = d.pop("pages_sharing")

        pages_unshared = d.pop("pages_unshared")

        ksm_stats = cls(
            full_scans=full_scans,
            pages_shared=pages_shared,
            pages_sharing=pages_sharing,
            pages_unshared=pages_unshared,
        )

        ksm_stats.additional_properties = d
        return ksm_stats

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
