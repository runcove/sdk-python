from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CloneRequest")


@_attrs_define
class CloneRequest:
    """POST /vms/{source}/clone request body. The new VM's name is supplied by
    the caller; an optional `source_checkpoint_id` pins which checkpoint to
    reflink from. When omitted the service creates an implicit
    `pre_clone` checkpoint of the source first, then clones from it
    (the caller never has to take a checkpoint themselves).

    Mirrors `cove_service::api_types::CloneRequest`. The wire field name is
    `new_vm_name` (not `new_name`) to match the service mirror — drift here
    breaks the cross-crate roundtrip pinned by `unit_clone_request_*`.

        Attributes:
            new_vm_name (str): The clone's name, under the same rule as a created VM's: 3-30
                characters of lowercase ASCII letters, digits and hyphens, not starting
                or ending with a hyphen. Any other name is refused with 400
                `invalid_vm_name`.
            source_checkpoint_id (None | str | Unset): Stringified UUID v7 of an existing checkpoint. Optional — when
                `None` the server creates an implicit `pre_clone` checkpoint of
                the source before cloning. The server parses the string into a
                `Uuid` and surfaces a 400 on bad syntax.
    """

    new_vm_name: str
    source_checkpoint_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_vm_name = self.new_vm_name

        source_checkpoint_id: None | str | Unset
        if isinstance(self.source_checkpoint_id, Unset):
            source_checkpoint_id = UNSET
        else:
            source_checkpoint_id = self.source_checkpoint_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_vm_name": new_vm_name,
            }
        )
        if source_checkpoint_id is not UNSET:
            field_dict["source_checkpoint_id"] = source_checkpoint_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        new_vm_name = d.pop("new_vm_name")

        def _parse_source_checkpoint_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_checkpoint_id = _parse_source_checkpoint_id(
            d.pop("source_checkpoint_id", UNSET)
        )

        clone_request = cls(
            new_vm_name=new_vm_name,
            source_checkpoint_id=source_checkpoint_id,
        )

        clone_request.additional_properties = d
        return clone_request

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
