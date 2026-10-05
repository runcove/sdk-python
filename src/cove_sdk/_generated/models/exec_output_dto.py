from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExecOutputDto")


@_attrs_define
class ExecOutputDto:
    """Non-streaming exec result returned by the `--inject` path after
    inject -> exec -> optional wipe completes.

        Attributes:
            exit_code (int): The command's exit status; 124 when `timed_out`.
            stderr (str):
            stdout (str):
            timed_out (bool | Unset): The command ran past its deadline (`timeout_secs`, default 30): the
                guest killed its whole process group, `exit_code` is 124 and
                `stdout`/`stderr` hold what it wrote before then. A command that
                exits 124 on its own has `timed_out: false`.
    """

    exit_code: int
    stderr: str
    stdout: str
    timed_out: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exit_code = self.exit_code

        stderr = self.stderr

        stdout = self.stdout

        timed_out = self.timed_out

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exit_code": exit_code,
                "stderr": stderr,
                "stdout": stdout,
            }
        )
        if timed_out is not UNSET:
            field_dict["timed_out"] = timed_out

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        exit_code = d.pop("exit_code")

        stderr = d.pop("stderr")

        stdout = d.pop("stdout")

        timed_out = d.pop("timed_out", UNSET)

        exec_output_dto = cls(
            exit_code=exit_code,
            stderr=stderr,
            stdout=stdout,
            timed_out=timed_out,
        )

        exec_output_dto.additional_properties = d
        return exec_output_dto

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
