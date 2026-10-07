from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardTicket")


@_attrs_define
class OffboardTicket:
    """One Warpgate ticket in the user's name, deleted: a connect ticket, a
    port invite on one of their VMs, a CLI ticket Cove did not record, or one
    they requested at Warpgate. A ticket signs in without the identity
    provider, so offboarding deletes every one.

        Attributes:
            id (str): Warpgate's ticket id; `*` when the tickets could not be listed, or
                when tickets kept appearing (see `error`).
            ok (bool):
            error (None | str | Unset): Why deleting (or listing) failed, when `ok` is false: the ticket
                still works.
            target (None | str | Unset): The name of the target the ticket opens.
    """

    id: str
    ok: bool
    error: None | str | Unset = UNSET
    target: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        ok = self.ok

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        target: None | str | Unset
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ok": ok,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        ok = d.pop("ok")

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_target(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target = _parse_target(d.pop("target", UNSET))

        offboard_ticket = cls(
            id=id,
            ok=ok,
            error=error,
            target=target,
        )

        offboard_ticket.additional_properties = d
        return offboard_ticket

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
