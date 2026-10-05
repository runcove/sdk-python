from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckpointCreateRequest")


@_attrs_define
class CheckpointCreateRequest:
    """POST /vms/{name}/checkpoints request body. `description` is the only
    user-supplied field today; `stop_after` is reserved for the hibernate
    flow; it is not a field of this request (ignored if sent).

    `disk_only` is `Option<bool>` with serde default + skip-if-none
    so legacy clients that omit it are treated as a full-checkpoint request
    (`None` → server maps to `false`). `Some(true)` requests a disk-only
    checkpoint (skip memory capture).

        Attributes:
            description (None | str | Unset):
            disk_only (bool | None | Unset):
    """

    description: None | str | Unset = UNSET
    disk_only: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        disk_only: bool | None | Unset
        if isinstance(self.disk_only, Unset):
            disk_only = UNSET
        else:
            disk_only = self.disk_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if disk_only is not UNSET:
            field_dict["disk_only"] = disk_only

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_disk_only(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        disk_only = _parse_disk_only(d.pop("disk_only", UNSET))

        checkpoint_create_request = cls(
            description=description,
            disk_only=disk_only,
        )

        checkpoint_create_request.additional_properties = d
        return checkpoint_create_request

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
