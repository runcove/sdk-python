from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.vm_summary import VmSummary


T = TypeVar("T", bound="VmSummaryPage")


@_attrs_define
class VmSummaryPage:
    """One page of VM summaries — the body of `GET /api/vms`.

    Same envelope shape as `CheckpointPage`: rows under a plural field, plus
    `next_cursor` that is `null` only when this really is the last page.
    Ordering is `name` ascending.

    This replaced a bare `[VmSummary]` array with an `offset`/`limit` query.
    The array could not say it had been cut short, and the handler applied a
    default `limit` of 50 — so a caller with more than 50 VMs received a
    silently partial list that looked complete, and anything aggregating
    per-VM data across that list (checkpoints, most visibly) inherited the
    same silent gap.

        Attributes:
            next_cursor (None | str):
            vms (list[VmSummary]):
    """

    next_cursor: None | str
    vms: list[VmSummary]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        next_cursor: None | str
        next_cursor = self.next_cursor

        vms = []
        for vms_item_data in self.vms:
            vms_item = vms_item_data.to_dict()
            vms.append(vms_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "next_cursor": next_cursor,
                "vms": vms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.vm_summary import VmSummary

        d = dict(src_dict)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        vms = []
        _vms = d.pop("vms")
        for vms_item_data in _vms:
            vms_item = VmSummary.from_dict(vms_item_data)

            vms.append(vms_item)

        vm_summary_page = cls(
            next_cursor=next_cursor,
            vms=vms,
        )

        vm_summary_page.additional_properties = d
        return vm_summary_page

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
