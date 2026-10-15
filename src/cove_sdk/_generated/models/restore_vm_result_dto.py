from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="RestoreVmResultDto")


@_attrs_define
class RestoreVmResultDto:
    """
    Attributes:
        result (str): `started`, `skipped_running` (already running or paused),
            `skipped_pool`, `skipped_owner_disabled`, `skipped_stopping` (still
            stopping after the wait), `skipped_state` (not stopped: failed,
            hibernated or mid-transition), `not_found` or `failed`.
        vm_id (str): The id the request named.
        vm_name (str): Empty when the VM does not exist.
        error (None | str | Unset):
    """

    result: str
    vm_id: str
    vm_name: str
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = self.result

        vm_id = self.vm_id

        vm_name = self.vm_name

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "vm_id": vm_id,
                "vm_name": vm_name,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        result = d.pop("result")

        vm_id = d.pop("vm_id")

        vm_name = d.pop("vm_name")

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        restore_vm_result_dto = cls(
            result=result,
            vm_id=vm_id,
            vm_name=vm_name,
            error=error,
        )

        restore_vm_result_dto.additional_properties = d
        return restore_vm_result_dto

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
