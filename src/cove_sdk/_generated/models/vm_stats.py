from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmStats")


@_attrs_define
class VmStats:
    """GET /vms/{name}/stats response body.

    `timestamp` is the server-side sample time (unix epoch seconds). It is
    always emitted on the wire; consolidating the previously-duplicated client
    and server copies restored it to the client, which had silently dropped it.

        Attributes:
            cpu_percent (float):
            disk_available_bytes (int):
            disk_usage_bytes (int):
            load_avg (list[float]):
            memory_available_bytes (int):
            memory_cached_bytes (int):
            memory_free_bytes (int):
            memory_total_bytes (int):
            net_rx_bytes (int):
            net_tx_bytes (int):
            timestamp (int | Unset):
    """

    cpu_percent: float
    disk_available_bytes: int
    disk_usage_bytes: int
    load_avg: list[float]
    memory_available_bytes: int
    memory_cached_bytes: int
    memory_free_bytes: int
    memory_total_bytes: int
    net_rx_bytes: int
    net_tx_bytes: int
    timestamp: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_percent = self.cpu_percent

        disk_available_bytes = self.disk_available_bytes

        disk_usage_bytes = self.disk_usage_bytes

        load_avg = self.load_avg

        memory_available_bytes = self.memory_available_bytes

        memory_cached_bytes = self.memory_cached_bytes

        memory_free_bytes = self.memory_free_bytes

        memory_total_bytes = self.memory_total_bytes

        net_rx_bytes = self.net_rx_bytes

        net_tx_bytes = self.net_tx_bytes

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu_percent": cpu_percent,
                "disk_available_bytes": disk_available_bytes,
                "disk_usage_bytes": disk_usage_bytes,
                "load_avg": load_avg,
                "memory_available_bytes": memory_available_bytes,
                "memory_cached_bytes": memory_cached_bytes,
                "memory_free_bytes": memory_free_bytes,
                "memory_total_bytes": memory_total_bytes,
                "net_rx_bytes": net_rx_bytes,
                "net_tx_bytes": net_tx_bytes,
            }
        )
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        cpu_percent = d.pop("cpu_percent")

        disk_available_bytes = d.pop("disk_available_bytes")

        disk_usage_bytes = d.pop("disk_usage_bytes")

        load_avg = cast(list[float], d.pop("load_avg"))

        memory_available_bytes = d.pop("memory_available_bytes")

        memory_cached_bytes = d.pop("memory_cached_bytes")

        memory_free_bytes = d.pop("memory_free_bytes")

        memory_total_bytes = d.pop("memory_total_bytes")

        net_rx_bytes = d.pop("net_rx_bytes")

        net_tx_bytes = d.pop("net_tx_bytes")

        timestamp = d.pop("timestamp", UNSET)

        vm_stats = cls(
            cpu_percent=cpu_percent,
            disk_available_bytes=disk_available_bytes,
            disk_usage_bytes=disk_usage_bytes,
            load_avg=load_avg,
            memory_available_bytes=memory_available_bytes,
            memory_cached_bytes=memory_cached_bytes,
            memory_free_bytes=memory_free_bytes,
            memory_total_bytes=memory_total_bytes,
            net_rx_bytes=net_rx_bytes,
            net_tx_bytes=net_tx_bytes,
            timestamp=timestamp,
        )

        vm_stats.additional_properties = d
        return vm_stats

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
