from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardSession")


@_attrs_define
class OffboardSession:
    """One of the user's live Warpgate sessions, on any target (the shell, the
    web UI or a VM), closed. An open session never asks the identity provider
    again, so offboarding closes every one.

        Attributes:
            id (str): Warpgate's session id; `*` when the user's sessions could not be
                listed, or when sessions kept appearing (see `error`).
            ok (bool):
            error (None | str | Unset): Why closing (or listing) failed, when `ok` is false: the session is
                still open.
            targets (list[str] | Unset): Warpgate's ids of the targets the session is connected to (none
                for a sign-in with no connection yet).
    """

    id: str
    ok: bool
    error: None | str | Unset = UNSET
    targets: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        ok = self.ok

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        targets: list[str] | Unset = UNSET
        if not isinstance(self.targets, Unset):
            targets = self.targets

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
        if targets is not UNSET:
            field_dict["targets"] = targets

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

        targets = cast(list[str], d.pop("targets", UNSET))

        offboard_session = cls(
            id=id,
            ok=ok,
            error=error,
            targets=targets,
        )

        offboard_session.additional_properties = d
        return offboard_session

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
