from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.vm_state import VmState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_summary_tags import VmSummaryTags


T = TypeVar("T", bound="VmSummary")


@_attrs_define
class VmSummary:
    """GET /vms list item.

    Attributes:
        image (str):
        name (str):
        state (VmState): VM lifecycle state as reported by the Cove REST API and persisted by core.

            Serializes to lowercase JSON strings (`"running"`, `"hibernated"`, …). The
            one exception is `ForceStopping`, which spells its wire value
            `"force_stopping"` — see the variant's own note.

            # One authoritative spelling per state

            [`VmState::as_wire_str`] is the single place a state's wire name is
            written down. `Display`, [`std::str::FromStr`] and every SQL predicate that
            filters the `vms.state` column are all derived from it (via
            [`VmState::ALL`]), so renaming a state is a compile error at each derived
            site rather than a silent behaviour change. Two real defects came from the
            hand-maintained copies this replaces: a reconciler query filtering
            `force_killing`, a spelling no schema version ever held, and
            every hibernated VM rendering as an unstyled badge.

            The serde encoding is the one representation still declared separately
            (attributes cannot call a function); `unit_vm_state_wire_roundtrip` pins the
            two against each other for every variant.

            # What a person is shown is a separate concern

            [`VmState::display_name`] carries the words for a human — `"Force
            stopping"`, not the wire value `force_stopping`. Presentation layers must
            use it verbatim rather than capitalising the wire string, which is how
            `force_stopping` came to be shown as `Force_stopping`.

            # The names the rename retired are gone

            The 2026-07 terminology rename gave four states clearer names —
            `suspending` → `hibernating`, `suspended` → `hibernated`, `restoring` →
            `waking`, `forcekilling` → `force_stopping`. Migration 035 rewrites every
            stored row, so the old spellings exist nowhere after it runs and are now
            **rejected** on the way in, by serde and by `FromStr` alike. There is one
            production environment, a handful of users and no external API consumer, so
            the data was migrated forward instead of being read in two spellings
            indefinitely.
        created_at (None | str | Unset):
        degraded (bool | Unset):
        degraded_reason (None | str | Unset):
        ip_address (None | str | Unset):
        share_count (int | Unset): Number of active shares (grants) on this VM — user + team subjects.
            `0` when unshared or on legacy daemons; the owned-VM
            list row renders a "shared" badge when `> 0`. `#[serde(default)]` so
            older daemons deserialize cleanly.
        tags (VmSummaryTags | Unset): Tags on this VM. Absent on legacy daemons → empty map.
    """

    image: str
    name: str
    state: VmState
    created_at: None | str | Unset = UNSET
    degraded: bool | Unset = UNSET
    degraded_reason: None | str | Unset = UNSET
    ip_address: None | str | Unset = UNSET
    share_count: int | Unset = UNSET
    tags: VmSummaryTags | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        name = self.name

        state = self.state.value

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        degraded = self.degraded

        degraded_reason: None | str | Unset
        if isinstance(self.degraded_reason, Unset):
            degraded_reason = UNSET
        else:
            degraded_reason = self.degraded_reason

        ip_address: None | str | Unset
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        share_count = self.share_count

        tags: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "name": name,
                "state": state,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if degraded is not UNSET:
            field_dict["degraded"] = degraded
        if degraded_reason is not UNSET:
            field_dict["degraded_reason"] = degraded_reason
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if share_count is not UNSET:
            field_dict["share_count"] = share_count
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.vm_summary_tags import VmSummaryTags

        d = dict(src_dict)
        image = d.pop("image")

        name = d.pop("name")

        state = VmState(d.pop("state"))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        degraded = d.pop("degraded", UNSET)

        def _parse_degraded_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        degraded_reason = _parse_degraded_reason(d.pop("degraded_reason", UNSET))

        def _parse_ip_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        share_count = d.pop("share_count", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: VmSummaryTags | Unset
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = VmSummaryTags.from_dict(_tags)

        vm_summary = cls(
            image=image,
            name=name,
            state=state,
            created_at=created_at,
            degraded=degraded,
            degraded_reason=degraded_reason,
            ip_address=ip_address,
            share_count=share_count,
            tags=tags,
        )

        vm_summary.additional_properties = d
        return vm_summary

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
