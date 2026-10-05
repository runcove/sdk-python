from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.traffic_monitor_backend import TrafficMonitorBackend
from ..models.traffic_monitor_state import TrafficMonitorState
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrafficMonitorStatus")


@_attrs_define
class TrafficMonitorStatus:
    """What watches guest traffic for auto-pause and wake on this daemon.

    Attributes:
        auto_pause_enabled (bool): `[auto_pause] enabled` in the daemon's configuration.
        backend (TrafficMonitorBackend): The traffic monitor's implementation.
        state (TrafficMonitorState): Whether the traffic monitor is running.
        reason (None | str | Unset): Why the monitor is not `loaded`, when the daemon knows.
    """

    auto_pause_enabled: bool
    backend: TrafficMonitorBackend
    state: TrafficMonitorState
    reason: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_pause_enabled = self.auto_pause_enabled

        backend = self.backend.value

        state = self.state.value

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auto_pause_enabled": auto_pause_enabled,
                "backend": backend,
                "state": state,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        auto_pause_enabled = d.pop("auto_pause_enabled")

        backend = TrafficMonitorBackend(d.pop("backend"))

        state = TrafficMonitorState(d.pop("state"))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        traffic_monitor_status = cls(
            auto_pause_enabled=auto_pause_enabled,
            backend=backend,
            state=state,
            reason=reason,
        )

        traffic_monitor_status.additional_properties = d
        return traffic_monitor_status

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
