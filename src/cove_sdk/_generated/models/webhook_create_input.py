from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tag_filter import TagFilter


T = TypeVar("T", bound="WebhookCreateInput")


@_attrs_define
class WebhookCreateInput:
    """Input for creating a new webhook subscription (`POST /api/webhooks`).

    Attributes:
        events (list[str]): Event kind strings to subscribe to. `"server"` scope is scanned for
            exact-match strings (e.g. `"vm.stopped"`); `keys.*` kinds are rejected.
        scope (str): `"server"` or `"vm"`.
        url (str):
        allowed_subnets (None | str | Unset): CSV of CIDR overrides for SSRF guard.
        description (None | str | Unset):
        tag_filter (None | TagFilter | Unset):
        vm_id (None | Unset | UUID): Required when `scope == "vm"`; caller must own the VM.
    """

    events: list[str]
    scope: str
    url: str
    allowed_subnets: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    tag_filter: None | TagFilter | Unset = UNSET
    vm_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.tag_filter import TagFilter

        events = self.events

        scope = self.scope

        url = self.url

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

        tag_filter: dict[str, Any] | None | Unset
        if isinstance(self.tag_filter, Unset):
            tag_filter = UNSET
        elif isinstance(self.tag_filter, TagFilter):
            tag_filter = self.tag_filter.to_dict()
        else:
            tag_filter = self.tag_filter

        vm_id: None | str | Unset
        if isinstance(self.vm_id, Unset):
            vm_id = UNSET
        elif isinstance(self.vm_id, UUID):
            vm_id = str(self.vm_id)
        else:
            vm_id = self.vm_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
                "scope": scope,
                "url": url,
            }
        )
        if allowed_subnets is not UNSET:
            field_dict["allowed_subnets"] = allowed_subnets
        if description is not UNSET:
            field_dict["description"] = description
        if tag_filter is not UNSET:
            field_dict["tag_filter"] = tag_filter
        if vm_id is not UNSET:
            field_dict["vm_id"] = vm_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.tag_filter import TagFilter

        d = dict(src_dict)
        events = cast(list[str], d.pop("events"))

        scope = d.pop("scope")

        url = d.pop("url")

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

        def _parse_vm_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                vm_id_type_0 = UUID(data)

                return vm_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        vm_id = _parse_vm_id(d.pop("vm_id", UNSET))

        webhook_create_input = cls(
            events=events,
            scope=scope,
            url=url,
            allowed_subnets=allowed_subnets,
            description=description,
            tag_filter=tag_filter,
            vm_id=vm_id,
        )

        webhook_create_input.additional_properties = d
        return webhook_create_input

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
