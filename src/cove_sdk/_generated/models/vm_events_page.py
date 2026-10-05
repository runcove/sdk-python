from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.vm_event import VmEvent


T = TypeVar("T", bound="VmEventsPage")


@_attrs_define
class VmEventsPage:
    """One page of VM events. `next_cursor` is `null` once the caller reaches the
    end of the log; pass it back as `?cursor=` to fetch the next page.

    Like every other page envelope, `next_cursor` is **always serialized** —
    see [`CheckpointPageDto`] and `crate::page`. It carried
    `skip_serializing_if = "Option::is_none"` until this was noticed, which made
    this one envelope omit the field on the last page: the one shape a caller
    cannot distinguish from a listing that does not paginate at all, and exactly
    what the convention exists to prevent. `#[schema(required = true)]` publishes
    the guarantee rather than only asserting it in prose.

        Attributes:
            events (list[VmEvent]):
            next_cursor (None | str):
    """

    events: list[VmEvent]
    next_cursor: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
                "next_cursor": next_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.vm_event import VmEvent

        d = dict(src_dict)
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = VmEvent.from_dict(events_item_data)

            events.append(events_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        vm_events_page = cls(
            events=events,
            next_cursor=next_cursor,
        )

        vm_events_page.additional_properties = d
        return vm_events_page

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
