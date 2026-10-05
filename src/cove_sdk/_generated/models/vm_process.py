from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="VmProcess")


@_attrs_define
class VmProcess:
    """Process entry from GET /vms/{name}/processes.

    Attributes:
        comm (str):
        cpu_percent (float):
        pid (int):
        rss_bytes (int):
    """

    comm: str
    cpu_percent: float
    pid: int
    rss_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comm = self.comm

        cpu_percent = self.cpu_percent

        pid = self.pid

        rss_bytes = self.rss_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "comm": comm,
                "cpu_percent": cpu_percent,
                "pid": pid,
                "rss_bytes": rss_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        comm = d.pop("comm")

        cpu_percent = d.pop("cpu_percent")

        pid = d.pop("pid")

        rss_bytes = d.pop("rss_bytes")

        vm_process = cls(
            comm=comm,
            cpu_percent=cpu_percent,
            pid=pid,
            rss_bytes=rss_bytes,
        )

        vm_process.additional_properties = d
        return vm_process

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
