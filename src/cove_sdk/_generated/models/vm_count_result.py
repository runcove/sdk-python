from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="VmCountResult")


@_attrs_define
class VmCountResult:
    """`POST /users|teams/{scope}/secrets/{key}` and the project-scoped
    equivalent — best-effort fan-out count for a scoped `set`. Named
    `VmCountResult` to match the outgoing hand-written spec's schema name;
    no Rust caller constructs this type today, the three scoped
    `set_*_secret` handlers build the identical `{"vm_count": N}` shape ad hoc
    via `serde_json::json!` — this type exists purely so the description can
    reference a named schema instead of an inline one.

        Attributes:
            vm_count (int): Running, in-scope VMs the value was pushed to (best-effort — no ack).
    """

    vm_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vm_count = self.vm_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vm_count": vm_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        vm_count = d.pop("vm_count")

        vm_count_result = cls(
            vm_count=vm_count,
        )

        vm_count_result.additional_properties = d
        return vm_count_result

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
