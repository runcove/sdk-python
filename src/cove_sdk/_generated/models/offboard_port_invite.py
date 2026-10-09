from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="OffboardPortInvite")


@_attrs_define
class OffboardPortInvite:
    """A port invite the person made on a VM that is not theirs.

    Attributes:
        created_at (str): When the person made it (RFC 3339 / SQLite timestamp as recorded).
        id (str): The invite's id (the Warpgate ticket id).
        port (int): The proxied port the invite opens.
        vm (str): The VM's name.
    """

    created_at: str
    id: str
    port: int
    vm: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        id = self.id

        port = self.port

        vm = self.vm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "port": port,
                "vm": vm,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        created_at = d.pop("created_at")

        id = d.pop("id")

        port = d.pop("port")

        vm = d.pop("vm")

        offboard_port_invite = cls(
            created_at=created_at,
            id=id,
            port=port,
            vm=vm,
        )

        offboard_port_invite.additional_properties = d
        return offboard_port_invite

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
