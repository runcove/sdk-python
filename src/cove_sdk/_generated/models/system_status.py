from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pool_status import PoolStatus
    from ..models.user_status import UserStatus


T = TypeVar("T", bound="SystemStatus")


@_attrs_define
class SystemStatus:
    """`GET /system/status` response body: host-wide VM + resource counts.

    Attributes:
        ch_processes (int):
        memory_total_mb (int):
        memory_used_mb (int):
        paused (int):
        pool (list[PoolStatus]):
        running (int):
        stopped (int):
        tap_devices (int):
        users (list[UserStatus] | Unset):
    """

    ch_processes: int
    memory_total_mb: int
    memory_used_mb: int
    paused: int
    pool: list[PoolStatus]
    running: int
    stopped: int
    tap_devices: int
    users: list[UserStatus] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ch_processes = self.ch_processes

        memory_total_mb = self.memory_total_mb

        memory_used_mb = self.memory_used_mb

        paused = self.paused

        pool = []
        for pool_item_data in self.pool:
            pool_item = pool_item_data.to_dict()
            pool.append(pool_item)

        running = self.running

        stopped = self.stopped

        tap_devices = self.tap_devices

        users: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ch_processes": ch_processes,
                "memory_total_mb": memory_total_mb,
                "memory_used_mb": memory_used_mb,
                "paused": paused,
                "pool": pool,
                "running": running,
                "stopped": stopped,
                "tap_devices": tap_devices,
            }
        )
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.pool_status import PoolStatus
        from ..models.user_status import UserStatus

        d = dict(src_dict)
        ch_processes = d.pop("ch_processes")

        memory_total_mb = d.pop("memory_total_mb")

        memory_used_mb = d.pop("memory_used_mb")

        paused = d.pop("paused")

        pool = []
        _pool = d.pop("pool")
        for pool_item_data in _pool:
            pool_item = PoolStatus.from_dict(pool_item_data)

            pool.append(pool_item)

        running = d.pop("running")

        stopped = d.pop("stopped")

        tap_devices = d.pop("tap_devices")

        _users = d.pop("users", UNSET)
        users: list[UserStatus] | Unset = UNSET
        if _users is not UNSET:
            users = []
            for users_item_data in _users:
                users_item = UserStatus.from_dict(users_item_data)

                users.append(users_item)

        system_status = cls(
            ch_processes=ch_processes,
            memory_total_mb=memory_total_mb,
            memory_used_mb=memory_used_mb,
            paused=paused,
            pool=pool,
            running=running,
            stopped=stopped,
            tap_devices=tap_devices,
            users=users,
        )

        system_status.additional_properties = d
        return system_status

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
