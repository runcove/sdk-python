from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.offboard_warpgate_role_outcome import OffboardWarpgateRoleOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardWarpgateRole")


@_attrs_define
class OffboardWarpgateRole:
    """Cove's per-user Warpgate role for the person (the one Cove creates for
    each user and binds to their VMs' targets), deleted in the Warpgate step
    just before their Warpgate user. Deleting the user only drops their
    membership; the role and its bindings would survive, and the person
    would get it back on signing in again. Only this role is deleted: any
    other role they hold, even one whose only member is them, stays. The
    VMs' targets stay too.

        Attributes:
            name (str): The role's name at Warpgate.
            outcome (OffboardWarpgateRoleOutcome): What happened to Cove's own Warpgate role for the user. The server sends
                only `deleted`, `not_found` or `failed`; `unknown` is how a client reads
                an outcome newer than itself, and it counts as a failure.
            error (None | str | Unset): Why finding or deleting the role failed, when `outcome` is `failed`.
            id (None | str | Unset): Warpgate's id of the role, when Warpgate has it. Warpgate does not
                keep role names unique: when it held several roles with exactly this
                name, every one is deleted and this lists their ids, comma-separated.
    """

    name: str
    outcome: OffboardWarpgateRoleOutcome
    error: None | str | Unset = UNSET
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        outcome = self.outcome.value

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "outcome": outcome,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        outcome = OffboardWarpgateRoleOutcome(d.pop("outcome"))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        offboard_warpgate_role = cls(
            name=name,
            outcome=outcome,
            error=error,
            id=id,
        )

        offboard_warpgate_role.additional_properties = d
        return offboard_warpgate_role

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
