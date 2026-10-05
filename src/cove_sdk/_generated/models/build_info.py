from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildInfo")


@_attrs_define
class BuildInfo:
    """GET /version (and the `build_info` field of `GET /health`) response body.

    Attributes:
        built_at (str):
        commit (str):
        name (str):
        version (str):
        api_version (int | None | Unset):
        protocol_version (int | None | Unset):
    """

    built_at: str
    commit: str
    name: str
    version: str
    api_version: int | None | Unset = UNSET
    protocol_version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        built_at = self.built_at

        commit = self.commit

        name = self.name

        version = self.version

        api_version: int | None | Unset
        if isinstance(self.api_version, Unset):
            api_version = UNSET
        else:
            api_version = self.api_version

        protocol_version: int | None | Unset
        if isinstance(self.protocol_version, Unset):
            protocol_version = UNSET
        else:
            protocol_version = self.protocol_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "built_at": built_at,
                "commit": commit,
                "name": name,
                "version": version,
            }
        )
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if protocol_version is not UNSET:
            field_dict["protocol_version"] = protocol_version

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        built_at = d.pop("built_at")

        commit = d.pop("commit")

        name = d.pop("name")

        version = d.pop("version")

        def _parse_api_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        def _parse_protocol_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        protocol_version = _parse_protocol_version(d.pop("protocol_version", UNSET))

        build_info = cls(
            built_at=built_at,
            commit=commit,
            name=name,
            version=version,
            api_version=api_version,
            protocol_version=protocol_version,
        )

        build_info.additional_properties = d
        return build_info

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
