from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.image_entry import ImageEntry
    from ..models.oci_cache_entry import OciCacheEntry


T = TypeVar("T", bound="ImagesResponse")


@_attrs_define
class ImagesResponse:
    """
    Attributes:
        images (list[ImageEntry]):
        oci_cache (list[OciCacheEntry]):
    """

    images: list[ImageEntry]
    oci_cache: list[OciCacheEntry]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        images = []
        for images_item_data in self.images:
            images_item = images_item_data.to_dict()
            images.append(images_item)

        oci_cache = []
        for oci_cache_item_data in self.oci_cache:
            oci_cache_item = oci_cache_item_data.to_dict()
            oci_cache.append(oci_cache_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "images": images,
                "oci_cache": oci_cache,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.image_entry import ImageEntry
        from ..models.oci_cache_entry import OciCacheEntry

        d = dict(src_dict)
        images = []
        _images = d.pop("images")
        for images_item_data in _images:
            images_item = ImageEntry.from_dict(images_item_data)

            images.append(images_item)

        oci_cache = []
        _oci_cache = d.pop("oci_cache")
        for oci_cache_item_data in _oci_cache:
            oci_cache_item = OciCacheEntry.from_dict(oci_cache_item_data)

            oci_cache.append(oci_cache_item)

        images_response = cls(
            images=images,
            oci_cache=oci_cache,
        )

        images_response.additional_properties = d
        return images_response

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
