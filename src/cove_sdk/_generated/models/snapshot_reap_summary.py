from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="SnapshotReapSummary")


@_attrs_define
class SnapshotReapSummary:
    """Summary of the most recent non-dry-run reaper pass that actually deleted at
    least one version dir. Feeds the "freed X at HH:MM" line on the admin card.

        Attributes:
            at (datetime.datetime):
            bytes_freed (int):
            version_count (int):
    """

    at: datetime.datetime
    bytes_freed: int
    version_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        bytes_freed = self.bytes_freed

        version_count = self.version_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "bytes_freed": bytes_freed,
                "version_count": version_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        at = datetime.datetime.fromisoformat(d.pop("at"))

        bytes_freed = d.pop("bytes_freed")

        version_count = d.pop("version_count")

        snapshot_reap_summary = cls(
            at=at,
            bytes_freed=bytes_freed,
            version_count=version_count,
        )

        snapshot_reap_summary.additional_properties = d
        return snapshot_reap_summary

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
