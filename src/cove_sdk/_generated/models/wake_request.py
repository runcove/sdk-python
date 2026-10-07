from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="WakeRequest")


@_attrs_define
class WakeRequest:
    """POST /vms/{name}/wake request body. `checkpoint_id` is optional —
    `None` selects the latest available checkpoint for the VM (server
    chooses), `Some` pins a specific checkpoint UUID v7.

        Attributes:
            checkpoint_id (None | str | Unset): Specific checkpoint id to wake from. `None` → latest
                available for the VM, except on a `Stopped` VM whose latest is
                disk-only: that is refused (`disk_rollback_not_named`), so a disk
                rollback always names its checkpoint. Stringified UUID v7; the
                server parses it.
    """

    checkpoint_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkpoint_id: None | str | Unset
        if isinstance(self.checkpoint_id, Unset):
            checkpoint_id = UNSET
        else:
            checkpoint_id = self.checkpoint_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if checkpoint_id is not UNSET:
            field_dict["checkpoint_id"] = checkpoint_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_checkpoint_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        checkpoint_id = _parse_checkpoint_id(d.pop("checkpoint_id", UNSET))

        wake_request = cls(
            checkpoint_id=checkpoint_id,
        )

        wake_request.additional_properties = d
        return wake_request

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
