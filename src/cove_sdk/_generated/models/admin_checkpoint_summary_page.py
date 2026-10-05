from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.admin_checkpoint_summary import AdminCheckpointSummary


T = TypeVar("T", bound="AdminCheckpointSummaryPage")


@_attrs_define
class AdminCheckpointSummaryPage:
    """One page of `GET /api/admin/checkpoints[?user=&orphaned=]`. Same shape as
    every other cursor-paginated listing: rows under a plural field named after
    the resource, plus `next_cursor`, `null` on the last page. Ordering is
    `(created_at, checkpoint_id)` descending — newest first, with the id
    breaking ties between checkpoints taken in the same second.

        Attributes:
            checkpoints (list[AdminCheckpointSummary]):
            next_cursor (None | str):
    """

    checkpoints: list[AdminCheckpointSummary]
    next_cursor: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkpoints = []
        for checkpoints_item_data in self.checkpoints:
            checkpoints_item = checkpoints_item_data.to_dict()
            checkpoints.append(checkpoints_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkpoints": checkpoints,
                "next_cursor": next_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.admin_checkpoint_summary import (
            AdminCheckpointSummary,
        )

        d = dict(src_dict)
        checkpoints = []
        _checkpoints = d.pop("checkpoints")
        for checkpoints_item_data in _checkpoints:
            checkpoints_item = AdminCheckpointSummary.from_dict(checkpoints_item_data)

            checkpoints.append(checkpoints_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        admin_checkpoint_summary_page = cls(
            checkpoints=checkpoints,
            next_cursor=next_cursor,
        )

        admin_checkpoint_summary_page.additional_properties = d
        return admin_checkpoint_summary_page

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
