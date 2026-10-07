from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.offboard_warpgate_user_outcome import OffboardWarpgateUserOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardWarpgateUser")


@_attrs_define
class OffboardWarpgateUser:
    """The person's Warpgate user, deleted first in the Warpgate step. A user
    API token, password, one-time code or certificate of theirs signs in
    without the identity provider, and their roles reach every target; all
    of it goes with the user. If they sign in again through the identity
    provider, Warpgate provisions a new user for them.

        Attributes:
            outcome (OffboardWarpgateUserOutcome): What happened to the user's Warpgate user. The server sends only
                `deleted`, `not_found` or `failed`. It never sends `unknown`: that is how a
                client reads an outcome newer than itself, and it counts as a failure.
            error (None | str | Unset): Why finding or deleting the user failed, when `outcome` is `failed`.
            id (None | str | Unset): Warpgate's id of the user, when Warpgate has one for them.
    """

    outcome: OffboardWarpgateUserOutcome
    error: None | str | Unset = UNSET
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
        outcome = OffboardWarpgateUserOutcome(d.pop("outcome"))

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

        offboard_warpgate_user = cls(
            outcome=outcome,
            error=error,
            id=id,
        )

        offboard_warpgate_user.additional_properties = d
        return offboard_warpgate_user

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
