from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="OciCacheEntry")


@_attrs_define
class OciCacheEntry:
    """
    Attributes:
        base_os (str):
        built_at (str):
        digest_short (str):
        oci_ref (str):
        size_mb (int):
    """

    base_os: str
    built_at: str
    digest_short: str
    oci_ref: str
    size_mb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_os = self.base_os

        built_at = self.built_at

        digest_short = self.digest_short

        oci_ref = self.oci_ref

        size_mb = self.size_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_os": base_os,
                "built_at": built_at,
                "digest_short": digest_short,
                "oci_ref": oci_ref,
                "size_mb": size_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        base_os = d.pop("base_os")

        built_at = d.pop("built_at")

        digest_short = d.pop("digest_short")

        oci_ref = d.pop("oci_ref")

        size_mb = d.pop("size_mb")

        oci_cache_entry = cls(
            base_os=base_os,
            built_at=built_at,
            digest_short=digest_short,
            oci_ref=oci_ref,
            size_mb=size_mb,
        )

        oci_cache_entry.additional_properties = d
        return oci_cache_entry

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
