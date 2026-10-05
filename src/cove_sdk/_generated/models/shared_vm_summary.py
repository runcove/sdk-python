from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.vm_state import VmState
from ..types import UNSET, Unset

T = TypeVar("T", bound="SharedVmSummary")


@_attrs_define
class SharedVmSummary:
    """GET /vms/shared-with-me response body.

    A DIFFERENT shape from [`VmSummaryDto`] on purpose, not an oversight: the
    handler (`handlers::shares::get_shared_with_me`) projects the service-side
    `UserVmInfo` directly and never enriches with tags or the share count —
    this is a lighter list endpoint (see the handler's own doc comment). It
    adds `owner` (absent from `VmSummaryDto`, since your own VMs have no
    "owner" distinct from you) and omits `created_at`/`tags`/`share_count`.

    Named here rather than left inline even though no
    prior hand-written spec ever published this operation — the outgoing
    `sdk/openapi.yaml` has no `/vms/shared-with-me` entry at all, so this is a
    first publication, not a migration.

    Every client-side `list_shared_vms` decodes THIS type. Two of them used to
    decode `VmSummaryDto` instead — which parsed cleanly (serde tolerates
    unknown fields) while dropping `owner`, so `cove ls --shared-with-me`
    rendered no sharer at all. If you add a client impl, decode this shape.

        Attributes:
            image (str):
            name (str):
            owner (str): Owner username — always populated for this endpoint (every row here
                is, by definition, a VM the caller does not own).
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
            degraded (bool | Unset):
            degraded_reason (None | str | Unset):
            ip_address (None | str | Unset):
    """

    image: str
    name: str
    owner: str
    state: VmState
    degraded: bool | Unset = UNSET
    degraded_reason: None | str | Unset = UNSET
    ip_address: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        name = self.name

        owner = self.owner

        state = self.state.value

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "name": name,
                "owner": owner,
                "state": state,
            }
        )
        if degraded is not UNSET:
            field_dict["degraded"] = degraded
        if degraded_reason is not UNSET:
            field_dict["degraded_reason"] = degraded_reason
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        image = d.pop("image")

        name = d.pop("name")

        owner = d.pop("owner")

        state = VmState(d.pop("state"))

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

        shared_vm_summary = cls(
            image=image,
            name=name,
            owner=owner,
            state=state,
            degraded=degraded,
            degraded_reason=degraded_reason,
            ip_address=ip_address,
        )

        shared_vm_summary.additional_properties = d
        return shared_vm_summary

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
