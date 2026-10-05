from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tag_filter import TagFilter


T = TypeVar("T", bound="WebhookUpdateInput")


@_attrs_define
class WebhookUpdateInput:
    """Input for updating an existing subscription (`PUT /api/webhooks/{id}`).

    All fields are optional — only provided fields are updated. For
    `tag_filter`, `allowed_subnets` and `description`, an explicit JSON `null`
    is indistinguishable from omission on the wire, hence the `Option<Option<
    _>>` — the outer `Option` is "was this key present at all", checked by
    `serde`'s default-on-missing-field behaviour, not by any wire-visible
    distinction from an inner `null`. The published schema (`#[schema(value_type
    = ...)]` below) flattens that internal detail to a plain nullable field,
    same as every other optional field here — the request body can't express
    "clear this field" any more precisely than that, so the schema shouldn't
    claim it can.

        Attributes:
            allowed_subnets (None | str | Unset): CSV of CIDR overrides for SSRF guard.
            description (None | str | Unset):
            events (list[str] | None | Unset):
            tag_filter (None | TagFilter | Unset):
            url (None | str | Unset):
    """

    allowed_subnets: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    events: list[str] | None | Unset = UNSET
    tag_filter: None | TagFilter | Unset = UNSET
    url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.tag_filter import TagFilter

        allowed_subnets: None | str | Unset
        if isinstance(self.allowed_subnets, Unset):
            allowed_subnets = UNSET
        else:
            allowed_subnets = self.allowed_subnets

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        events: list[str] | None | Unset
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, list):
            events = self.events

        else:
            events = self.events

        tag_filter: dict[str, Any] | None | Unset
        if isinstance(self.tag_filter, Unset):
            tag_filter = UNSET
        elif isinstance(self.tag_filter, TagFilter):
            tag_filter = self.tag_filter.to_dict()
        else:
            tag_filter = self.tag_filter

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_subnets is not UNSET:
            field_dict["allowed_subnets"] = allowed_subnets
        if description is not UNSET:
            field_dict["description"] = description
        if events is not UNSET:
            field_dict["events"] = events
        if tag_filter is not UNSET:
            field_dict["tag_filter"] = tag_filter
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.tag_filter import TagFilter

        d = dict(src_dict)

        def _parse_allowed_subnets(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        allowed_subnets = _parse_allowed_subnets(d.pop("allowed_subnets", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_events(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = cast(list[str], data)

                return events_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        events = _parse_events(d.pop("events", UNSET))

        def _parse_tag_filter(data: object) -> None | TagFilter | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tag_filter_type_1 = TagFilter.from_dict(data)

                return tag_filter_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TagFilter | Unset, data)

        tag_filter = _parse_tag_filter(d.pop("tag_filter", UNSET))

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        webhook_update_input = cls(
            allowed_subnets=allowed_subnets,
            description=description,
            events=events,
            tag_filter=tag_filter,
            url=url,
        )

        webhook_update_input.additional_properties = d
        return webhook_update_input

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
