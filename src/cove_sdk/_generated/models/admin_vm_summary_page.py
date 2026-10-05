from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.admin_vm_summary import AdminVmSummary


T = TypeVar("T", bound="AdminVmSummaryPage")


@_attrs_define
class AdminVmSummaryPage:
    """One page of `GET /api/admin/vms[?user=]`. Same shape
    as every other cursor-paginated listing: rows under a plural field named
    after the resource, plus `next_cursor`, `null` on the last page.
    Ordering is `vm_name` ascending — VM names are unique per deployment, so
    the name alone is a total order and needs no tiebreak.

    Replaced a bare `Vec<AdminVmSummaryDto>` with no bound at all: every VM on
    the host, cross-tenant, in one response, with no way to signal a cut page.

        Attributes:
            next_cursor (None | str):
            vms (list[AdminVmSummary]):
    """

    next_cursor: None | str
    vms: list[AdminVmSummary]
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
        from ..models.admin_vm_summary import AdminVmSummary

        d = dict(src_dict)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        vms = []
        _vms = d.pop("vms")
        for vms_item_data in _vms:
            vms_item = AdminVmSummary.from_dict(vms_item_data)

            vms.append(vms_item)

        admin_vm_summary_page = cls(
            next_cursor=next_cursor,
            vms=vms,
        )

        admin_vm_summary_page.additional_properties = d
        return admin_vm_summary_page

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
