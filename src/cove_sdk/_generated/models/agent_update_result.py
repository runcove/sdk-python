from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentUpdateResult")


@_attrs_define
class AgentUpdateResult:
    """One VM's outcome from `POST /admin/update-agents`.

    Published as `AgentUpdateResult`. The Rust name `UpdateResult` is
    far too generic for a public schema name — it says nothing about what was
    updated, and would be the obvious name for a future unrelated type.

        Attributes:
            name (str):
            success (bool):
            vm_id (str):
            error (None | str | Unset):
    """

    name: str
    success: bool
    vm_id: str
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        success = self.success

        vm_id = self.vm_id

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "success": success,
                "vm_id": vm_id,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        success = d.pop("success")

        vm_id = d.pop("vm_id")

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        agent_update_result = cls(
            name=name,
            success=success,
            vm_id=vm_id,
            error=error,
        )

        agent_update_result.additional_properties = d
        return agent_update_result

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
