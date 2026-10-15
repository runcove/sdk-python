from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="RotateSummary")


@_attrs_define
class RotateSummary:
    """Acked push/wipe fan-out summary returned by `cove secret
    rotate` AND `cove secret unset` (both return this one shape).
    `vm_count` is the number of running VMs that confirmed the push
    within the per-VM ack budget; `unconfirmed` carries `"<vm>: <reason>"`
    entries for VMs reached but not acked; `skipped` carries the vm_ids of
    in-scope VMs that could NOT be reached (hibernated/unreachable — no guest
    session), so the change was never delivered there. A skipped VM is never
    reported as confirmed (wipe honesty); the resume converge scrubs it when
    the VM comes back. `unconfirmed`/`skipped` default-empty so an older
    server's `{"vm_count":N}` body still deserialises.

        Attributes:
            vm_count (int):
            existed (bool | None | Unset): Set by a secret delete only: `true` when the secret was stored and is now gone,
                `false` when nothing was stored under that name in that scope (the wipe is still sent; absent from rotate and
                set replies, and from an older server's delete reply).
            skipped (list[str] | Unset):
            unconfirmed (list[str] | Unset):
    """

    vm_count: int
    existed: bool | None | Unset = UNSET
    skipped: list[str] | Unset = UNSET
    unconfirmed: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vm_count = self.vm_count

        existed: bool | None | Unset
        if isinstance(self.existed, Unset):
            existed = UNSET
        else:
            existed = self.existed

        skipped: list[str] | Unset = UNSET
        if not isinstance(self.skipped, Unset):
            skipped = self.skipped

        unconfirmed: list[str] | Unset = UNSET
        if not isinstance(self.unconfirmed, Unset):
            unconfirmed = self.unconfirmed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vm_count": vm_count,
            }
        )
        if existed is not UNSET:
            field_dict["existed"] = existed
        if skipped is not UNSET:
            field_dict["skipped"] = skipped
        if unconfirmed is not UNSET:
            field_dict["unconfirmed"] = unconfirmed

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        vm_count = d.pop("vm_count")

        def _parse_existed(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        existed = _parse_existed(d.pop("existed", UNSET))

        skipped = cast(list[str], d.pop("skipped", UNSET))

        unconfirmed = cast(list[str], d.pop("unconfirmed", UNSET))

        rotate_summary = cls(
            vm_count=vm_count,
            existed=existed,
            skipped=skipped,
            unconfirmed=unconfirmed,
        )

        rotate_summary.additional_properties = d
        return rotate_summary

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
