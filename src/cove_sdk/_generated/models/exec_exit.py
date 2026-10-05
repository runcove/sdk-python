from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExecExit")


@_attrs_define
class ExecExit:
    """Data of the terminal `exit` event of `POST /vms/{name}/exec`.

    `timed_out` is `true` when the command ran past `timeout_secs`: the guest
    killed the command's whole process group and `code` is 124. A command
    that exits 124 on its own has `timed_out: false`. A server built before
    the field sends `{"code": N}` only; read its absence as `false`.

        Attributes:
            code (int): The command's exit status; 124 when `timed_out`, -1 when it was
                killed by a signal for any other reason.
            timed_out (bool | Unset): The exec deadline killed the command.
    """

    code: int
    timed_out: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        timed_out = self.timed_out

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
            }
        )
        if timed_out is not UNSET:
            field_dict["timed_out"] = timed_out

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        timed_out = d.pop("timed_out", UNSET)

        exec_exit = cls(
            code=code,
            timed_out=timed_out,
        )

        exec_exit.additional_properties = d
        return exec_exit

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
