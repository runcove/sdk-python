from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.vm_state import VmState
from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminBulkVmTarget")


@_attrs_define
class AdminBulkVmTarget:
    """One entry in [`AdminBulkVmResponse::targets`].

    Attributes:
        result (str): `"stopped"` / `"deleted"` / `"skipped"` (dry-run) / `"failed"` /
            `"timed_out"` (fleet budget elapsed; the stop keeps draining in the
            background).
        state_before (VmState): VM lifecycle state as reported by the Cove REST API and persisted by core.

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
        vm_id (str):
        vm_name (str):
        error (None | str | Unset):
        owner (None | str | Unset): `None` for pooled VMs (no assignment).
    """

    result: str
    state_before: VmState
    vm_id: str
    vm_name: str
    error: None | str | Unset = UNSET
    owner: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = self.result

        state_before = self.state_before.value

        vm_id = self.vm_id

        vm_name = self.vm_name

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        owner: None | str | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "state_before": state_before,
                "vm_id": vm_id,
                "vm_name": vm_name,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        result = d.pop("result")

        state_before = VmState(d.pop("state_before"))

        vm_id = d.pop("vm_id")

        vm_name = d.pop("vm_name")

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_owner(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        admin_bulk_vm_target = cls(
            result=result,
            state_before=state_before,
            vm_id=vm_id,
            vm_name=vm_name,
            error=error,
            owner=owner,
        )

        admin_bulk_vm_target.additional_properties = d
        return admin_bulk_vm_target

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
