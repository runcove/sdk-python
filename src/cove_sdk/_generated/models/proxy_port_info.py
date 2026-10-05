from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ProxyPortInfo")


@_attrs_define
class ProxyPortInfo:
    """
    Attributes:
        is_primary (bool):
        port (int):
        public (bool):
        url (str):
    """

    is_primary: bool
    port: int
    public: bool
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_primary = self.is_primary

        port = self.port

        public = self.public

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_primary": is_primary,
                "port": port,
                "public": public,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        is_primary = d.pop("is_primary")

        port = d.pop("port")

        public = d.pop("public")

        url = d.pop("url")

        proxy_port_info = cls(
            is_primary=is_primary,
            port=port,
            public=public,
            url=url,
        )

        proxy_port_info.additional_properties = d
        return proxy_port_info

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
