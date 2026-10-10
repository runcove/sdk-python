from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="CreateVmRequestInitialTags")


@_attrs_define
class CreateVmRequestInitialTags:
    """Tags the new VM gets, on it by the time it is `running`. A JSON object
    of key to value, the same shape as `VmDetail.tags` (a list of
    `[key, value]` pairs until API version 5). Each entry must pass the
    rules `PUT /api/vms/{name}/tags/{key}` applies, checked before anything
    is reserved: a bad entry is refused with 400 (a key starting `cove:`,
    which only Cove sets, with `tag_reserved_prefix`), and more than 50
    tags with 409 `too_many_tags`. A non-empty set needs `tags:write` as
    well as `vms:write`: a key without it is refused with 403
    `scope_denied`. A VM an agent creates (through hosted MCP, or with a
    connected app's token) also gets `cove:created-by: agent`, which
    counts toward the 50. Absent means no tags.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        create_vm_request_initial_tags = cls()

        create_vm_request_initial_tags.additional_properties = d
        return create_vm_request_initial_tags

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
