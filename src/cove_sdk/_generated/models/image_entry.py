from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_pool import ImagePool


T = TypeVar("T", bound="ImageEntry")


@_attrs_define
class ImageEntry:
    """
    Attributes:
        alias (str):
        image (str):
        status (str):
        aliases (list[str] | Unset): Other aliases that resolve to the same `image`. Empty in tests / older servers.
        default (bool | None | Unset):
        pool (ImagePool | None | Unset):
    """

    alias: str
    image: str
    status: str
    aliases: list[str] | Unset = UNSET
    default: bool | None | Unset = UNSET
    pool: ImagePool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.image_pool import ImagePool

        alias = self.alias

        image = self.image

        status = self.status

        aliases: list[str] | Unset = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        default: bool | None | Unset
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        pool: dict[str, Any] | None | Unset
        if isinstance(self.pool, Unset):
            pool = UNSET
        elif isinstance(self.pool, ImagePool):
            pool = self.pool.to_dict()
        else:
            pool = self.pool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alias": alias,
                "image": image,
                "status": status,
            }
        )
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if default is not UNSET:
            field_dict["default"] = default
        if pool is not UNSET:
            field_dict["pool"] = pool

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.image_pool import ImagePool

        d = dict(src_dict)
        alias = d.pop("alias")

        image = d.pop("image")

        status = d.pop("status")

        aliases = cast(list[str], d.pop("aliases", UNSET))

        def _parse_default(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        default = _parse_default(d.pop("default", UNSET))

        def _parse_pool(data: object) -> ImagePool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pool_type_1 = ImagePool.from_dict(data)

                return pool_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ImagePool | None | Unset, data)

        pool = _parse_pool(d.pop("pool", UNSET))

        image_entry = cls(
            alias=alias,
            image=image,
            status=status,
            aliases=aliases,
            default=default,
            pool=pool,
        )

        image_entry.additional_properties = d
        return image_entry

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
