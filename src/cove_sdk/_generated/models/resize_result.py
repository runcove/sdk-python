from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.resize_restart import ResizeRestart
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResizeResult")


@_attrs_define
class ResizeResult:
    """POST /vms/{name}/resize response body. `actual_cpus` / `actual_memory_mb`
    reflect what the hypervisor + guest converged to (which may differ from
    the request when shrink hits pinned pages — `partial=true`, `reason=Some`).

        Attributes:
            actual_cpus (int):
            actual_memory_mb (int):
            partial (bool):
            reason (None | str | Unset):
            restart (None | ResizeRestart | Unset):
    """

    actual_cpus: int
    actual_memory_mb: int
    partial: bool
    reason: None | str | Unset = UNSET
    restart: None | ResizeRestart | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actual_cpus = self.actual_cpus

        actual_memory_mb = self.actual_memory_mb

        partial = self.partial

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        restart: None | str | Unset
        if isinstance(self.restart, Unset):
            restart = UNSET
        elif isinstance(self.restart, ResizeRestart):
            restart = self.restart.value
        else:
            restart = self.restart

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actual_cpus": actual_cpus,
                "actual_memory_mb": actual_memory_mb,
                "partial": partial,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if restart is not UNSET:
            field_dict["restart"] = restart

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        actual_cpus = d.pop("actual_cpus")

        actual_memory_mb = d.pop("actual_memory_mb")

        partial = d.pop("partial")

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_restart(data: object) -> None | ResizeRestart | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                restart_type_1 = ResizeRestart(data)

                return restart_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ResizeRestart | Unset, data)

        restart = _parse_restart(d.pop("restart", UNSET))

        resize_result = cls(
            actual_cpus=actual_cpus,
            actual_memory_mb=actual_memory_mb,
            partial=partial,
            reason=reason,
            restart=restart,
        )

        resize_result.additional_properties = d
        return resize_result

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
