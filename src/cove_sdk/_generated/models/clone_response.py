from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.vm_detail import VmDetail


T = TypeVar("T", bound="CloneResponse")


@_attrs_define
class CloneResponse:
    """POST /vms/{source}/clone response body: the new VM's detail + the
    agent-reported SSH host-key fingerprints (pinned into Warpgate known-hosts
    on registration so the first SSH sees no TOFU prompt).

        Attributes:
            fingerprints (list[str]):
            new_vm (VmDetail): GET /vms/{name} response body.

                The elastic-envelope fields (`vcpus_min/max`, `memory_min/max_mb`,
                `current_vcpus`, `current_memory_mb`) and the TTL fields are all
                `#[serde(default)]` so legacy daemons that don't emit them deserialize
                cleanly.
    """

    fingerprints: list[str]
    new_vm: VmDetail
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fingerprints = self.fingerprints

        new_vm = self.new_vm.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fingerprints": fingerprints,
                "new_vm": new_vm,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.vm_detail import VmDetail

        d = dict(src_dict)
        fingerprints = cast(list[str], d.pop("fingerprints"))

        new_vm = VmDetail.from_dict(d.pop("new_vm"))

        clone_response = cls(
            fingerprints=fingerprints,
            new_vm=new_vm,
        )

        clone_response.additional_properties = d
        return clone_response

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
