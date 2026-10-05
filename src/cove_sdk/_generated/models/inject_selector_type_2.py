from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.inject_selector_type_2_kind import InjectSelectorType2Kind

T = TypeVar("T", bound="InjectSelectorType2")


@_attrs_define
class InjectSelectorType2:
    """Inject only `SetupOnly { tag }` secrets, then wipe them after the
    command completes (regardless of exit status).

        Attributes:
            kind (InjectSelectorType2Kind):
            tag (str):
    """

    kind: InjectSelectorType2Kind
    tag: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        tag = self.tag

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "tag": tag,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = InjectSelectorType2Kind(d.pop("kind"))

        tag = d.pop("tag")

        inject_selector_type_2 = cls(
            kind=kind,
            tag=tag,
        )

        inject_selector_type_2.additional_properties = d
        return inject_selector_type_2

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
