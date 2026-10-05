from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_info import BuildInfo
    from ..models.traffic_monitor_status import TrafficMonitorStatus


T = TypeVar("T", bound="HealthResponse")


@_attrs_define
class HealthResponse:
    """
    Attributes:
        pool_available (int):
        status (str):
        uptime_secs (int):
        vms_running (int):
        api_version (int | Unset):
        build_info (BuildInfo | None | Unset):
        min_cli_version (str | Unset):
        server_version (str | Unset):
        traffic_monitor (None | TrafficMonitorStatus | Unset):
    """

    pool_available: int
    status: str
    uptime_secs: int
    vms_running: int
    api_version: int | Unset = UNSET
    build_info: BuildInfo | None | Unset = UNSET
    min_cli_version: str | Unset = UNSET
    server_version: str | Unset = UNSET
    traffic_monitor: None | TrafficMonitorStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.build_info import BuildInfo
        from ..models.traffic_monitor_status import (
            TrafficMonitorStatus,
        )

        pool_available = self.pool_available

        status = self.status

        uptime_secs = self.uptime_secs

        vms_running = self.vms_running

        api_version = self.api_version

        build_info: dict[str, Any] | None | Unset
        if isinstance(self.build_info, Unset):
            build_info = UNSET
        elif isinstance(self.build_info, BuildInfo):
            build_info = self.build_info.to_dict()
        else:
            build_info = self.build_info

        min_cli_version = self.min_cli_version

        server_version = self.server_version

        traffic_monitor: dict[str, Any] | None | Unset
        if isinstance(self.traffic_monitor, Unset):
            traffic_monitor = UNSET
        elif isinstance(self.traffic_monitor, TrafficMonitorStatus):
            traffic_monitor = self.traffic_monitor.to_dict()
        else:
            traffic_monitor = self.traffic_monitor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pool_available": pool_available,
                "status": status,
                "uptime_secs": uptime_secs,
                "vms_running": vms_running,
            }
        )
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if build_info is not UNSET:
            field_dict["build_info"] = build_info
        if min_cli_version is not UNSET:
            field_dict["min_cli_version"] = min_cli_version
        if server_version is not UNSET:
            field_dict["server_version"] = server_version
        if traffic_monitor is not UNSET:
            field_dict["traffic_monitor"] = traffic_monitor

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.build_info import BuildInfo
        from ..models.traffic_monitor_status import (
            TrafficMonitorStatus,
        )

        d = dict(src_dict)
        pool_available = d.pop("pool_available")

        status = d.pop("status")

        uptime_secs = d.pop("uptime_secs")

        vms_running = d.pop("vms_running")

        api_version = d.pop("api_version", UNSET)

        def _parse_build_info(data: object) -> BuildInfo | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                build_info_type_1 = BuildInfo.from_dict(data)

                return build_info_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BuildInfo | None | Unset, data)

        build_info = _parse_build_info(d.pop("build_info", UNSET))

        min_cli_version = d.pop("min_cli_version", UNSET)

        server_version = d.pop("server_version", UNSET)

        def _parse_traffic_monitor(data: object) -> None | TrafficMonitorStatus | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                traffic_monitor_type_1 = TrafficMonitorStatus.from_dict(data)

                return traffic_monitor_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TrafficMonitorStatus | Unset, data)

        traffic_monitor = _parse_traffic_monitor(d.pop("traffic_monitor", UNSET))

        health_response = cls(
            pool_available=pool_available,
            status=status,
            uptime_secs=uptime_secs,
            vms_running=vms_running,
            api_version=api_version,
            build_info=build_info,
            min_cli_version=min_cli_version,
            server_version=server_version,
            traffic_monitor=traffic_monitor,
        )

        health_response.additional_properties = d
        return health_response

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
