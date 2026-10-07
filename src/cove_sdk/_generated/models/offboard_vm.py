from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.offboard_vm_outcome import OffboardVmOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardVm")


@_attrs_define
class OffboardVm:
    """The outcome for one VM the user owns. VMs are stopped, never deleted or
    reassigned.

        Attributes:
            outcome (OffboardVmOutcome): What happened to one VM the user owns. The server sends only `stopped`,
                `already_stopped` or `failed`. It never sends `unknown`: that is how a
                client reads an outcome newer than itself, and it counts as a failure.
            vm (str): The VM's name.
            error (None | str | Unset): Why the stop failed, when `outcome` is `failed`.
    """

    outcome: OffboardVmOutcome
    vm: str
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome.value

        vm = self.vm

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "outcome": outcome,
                "vm": vm,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        outcome = OffboardVmOutcome(d.pop("outcome"))

        vm = d.pop("vm")

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        offboard_vm = cls(
            outcome=outcome,
            vm=vm,
            error=error,
        )

        offboard_vm.additional_properties = d
        return offboard_vm

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
