from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResizeRequest")


@_attrs_define
class ResizeRequest:
    """POST /vms/{name}/resize request body. Either field may be `None` to keep
    the current dimension unchanged. `memory_mb` must be a multiple of 2 (the
    virtio-mem block size is 2 MiB). `disk_size_gb` triggers a stopped-VM disk
    grow; it is mutually exclusive with `cpus`/`memory_mb` at ALL
    call sites — the CLI and the server handler — enforced by
    [`ResizeRequest::validate_exclusivity`].

        Attributes:
            cpus (int | None | Unset):
            disk_size_gb (int | None | Unset):
            memory_mb (int | None | Unset):
    """

    cpus: int | None | Unset = UNSET
    disk_size_gb: int | None | Unset = UNSET
    memory_mb: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpus: int | None | Unset
        if isinstance(self.cpus, Unset):
            cpus = UNSET
        else:
            cpus = self.cpus

        disk_size_gb: int | None | Unset
        if isinstance(self.disk_size_gb, Unset):
            disk_size_gb = UNSET
        else:
            disk_size_gb = self.disk_size_gb

        memory_mb: int | None | Unset
        if isinstance(self.memory_mb, Unset):
            memory_mb = UNSET
        else:
            memory_mb = self.memory_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if disk_size_gb is not UNSET:
            field_dict["disk_size_gb"] = disk_size_gb
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_cpus(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cpus = _parse_cpus(d.pop("cpus", UNSET))

        def _parse_disk_size_gb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        disk_size_gb = _parse_disk_size_gb(d.pop("disk_size_gb", UNSET))

        def _parse_memory_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb", UNSET))

        resize_request = cls(
            cpus=cpus,
            disk_size_gb=disk_size_gb,
            memory_mb=memory_mb,
        )

        resize_request.additional_properties = d
        return resize_request

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
