from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.vm_state import VmState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ttl_policy import TtlPolicy


T = TypeVar("T", bound="AdminVmSummary")


@_attrs_define
class AdminVmSummary:
    """`GET /api/admin/vms[?user=]` list entry (the stale-VM view).
    `created_at` is the age anchor; `updated_at` is the last-activity
    fallback (touched on every state transition — start/stop/pause/resume/
    resize); `last_activity_at` is the durable last-activity
    signal, `None` until the idle detector's first Active observation. The
    stale-VM sort orders by `COALESCE(last_activity_at, updated_at)`.

    Published as `AdminVmSummary` (the `Dto` suffix is a Rust-side
    artifact). This is the copy that gets `ToSchema`: the handler serializes
    THIS type, converting from the identically-named `cove_service` value via
    `vm_to_wire` — see the NOTE on that duplicate.

        Attributes:
            created_at (str):
            image (str):
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
            updated_at (str):
            vm_id (str):
            vm_name (str):
            degraded (bool | Unset):
            last_activity_at (None | str | Unset):
            owner (None | str | Unset):
            ttl_policy (TtlPolicy | Unset): Per-VM TTL policy bundle. Both knobs default to "off" (`Never` / `None`);
                pool defaults and CLI flags merge into this on create.
    """

    created_at: str
    image: str
    state: VmState
    updated_at: str
    vm_id: str
    vm_name: str
    degraded: bool | Unset = UNSET
    last_activity_at: None | str | Unset = UNSET
    owner: None | str | Unset = UNSET
    ttl_policy: TtlPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        image = self.image

        state = self.state.value

        updated_at = self.updated_at

        vm_id = self.vm_id

        vm_name = self.vm_name

        degraded = self.degraded

        last_activity_at: None | str | Unset
        if isinstance(self.last_activity_at, Unset):
            last_activity_at = UNSET
        else:
            last_activity_at = self.last_activity_at

        owner: None | str | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        ttl_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ttl_policy, Unset):
            ttl_policy = self.ttl_policy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "image": image,
                "state": state,
                "updated_at": updated_at,
                "vm_id": vm_id,
                "vm_name": vm_name,
            }
        )
        if degraded is not UNSET:
            field_dict["degraded"] = degraded
        if last_activity_at is not UNSET:
            field_dict["last_activity_at"] = last_activity_at
        if owner is not UNSET:
            field_dict["owner"] = owner
        if ttl_policy is not UNSET:
            field_dict["ttl_policy"] = ttl_policy

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ttl_policy import TtlPolicy

        d = dict(src_dict)
        created_at = d.pop("created_at")

        image = d.pop("image")

        state = VmState(d.pop("state"))

        updated_at = d.pop("updated_at")

        vm_id = d.pop("vm_id")

        vm_name = d.pop("vm_name")

        degraded = d.pop("degraded", UNSET)

        def _parse_last_activity_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_activity_at = _parse_last_activity_at(d.pop("last_activity_at", UNSET))

        def _parse_owner(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        _ttl_policy = d.pop("ttl_policy", UNSET)
        ttl_policy: TtlPolicy | Unset
        if isinstance(_ttl_policy, Unset):
            ttl_policy = UNSET
        else:
            ttl_policy = TtlPolicy.from_dict(_ttl_policy)

        admin_vm_summary = cls(
            created_at=created_at,
            image=image,
            state=state,
            updated_at=updated_at,
            vm_id=vm_id,
            vm_name=vm_name,
            degraded=degraded,
            last_activity_at=last_activity_at,
            owner=owner,
            ttl_policy=ttl_policy,
        )

        admin_vm_summary.additional_properties = d
        return admin_vm_summary

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
