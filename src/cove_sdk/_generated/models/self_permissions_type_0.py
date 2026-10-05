from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.self_permissions_type_0_kind import SelfPermissionsType0Kind

T = TypeVar("T", bound="SelfPermissionsType0")


@_attrs_define
class SelfPermissionsType0:
    """
    Attributes:
        kind (SelfPermissionsType0Kind):
        scopes (list[str]):
    """

    kind: SelfPermissionsType0Kind
    scopes: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        scopes = self.scopes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "scopes": scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = SelfPermissionsType0Kind(d.pop("kind"))

        scopes = cast(list[str], d.pop("scopes"))

        self_permissions_type_0 = cls(
            kind=kind,
            scopes=scopes,
        )

        self_permissions_type_0.additional_properties = d
        return self_permissions_type_0

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
