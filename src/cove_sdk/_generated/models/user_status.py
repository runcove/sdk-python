from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="UserStatus")


@_attrs_define
class UserStatus:
    """Per-user VM counts within [`SystemStatusDto`].

    Attributes:
        paused (int):
        running (int):
        stopped (int):
        username (str):
    """

    paused: int
    running: int
    stopped: int
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        paused = self.paused

        running = self.running

        stopped = self.stopped

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "paused": paused,
                "running": running,
                "stopped": stopped,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        paused = d.pop("paused")

        running = d.pop("running")

        stopped = d.pop("stopped")

        username = d.pop("username")

        user_status = cls(
            paused=paused,
            running=running,
            stopped=stopped,
            username=username,
        )

        user_status.additional_properties = d
        return user_status

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
