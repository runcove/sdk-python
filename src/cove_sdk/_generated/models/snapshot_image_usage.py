from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="SnapshotImageUsage")


@_attrs_define
class SnapshotImageUsage:
    """Per-image snapshot disk usage: how many retained `v-<sha>` version dirs an
    image has and their summed apparent on-disk size. `disk_bytes` is
    best-effort (overstates reclaim on CoW-shared extents — same caveat as the
    reaper's `bytes_freed`).

        Attributes:
            disk_bytes (int):
            image (str):
            version_count (int):
    """

    disk_bytes: int
    image: str
    version_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_bytes = self.disk_bytes

        image = self.image

        version_count = self.version_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disk_bytes": disk_bytes,
                "image": image,
                "version_count": version_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        disk_bytes = d.pop("disk_bytes")

        image = d.pop("image")

        version_count = d.pop("version_count")

        snapshot_image_usage = cls(
            disk_bytes=disk_bytes,
            image=image,
            version_count=version_count,
        )

        snapshot_image_usage.additional_properties = d
        return snapshot_image_usage

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
