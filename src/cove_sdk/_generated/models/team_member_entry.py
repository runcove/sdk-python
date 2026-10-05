from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamMemberEntry")


@_attrs_define
class TeamMemberEntry:
    """One roster row for `cove team members <name>`.

    This is the ONE `TeamMemberEntry` — no server-side duplicate
    exists (`handlers::teams::get_team_members` builds its `serde_json::json!`
    response by hand from `cove_service::teams::TeamMemberView`).

        Attributes:
            added_at (datetime.datetime):
            username (str):
            added_by (None | str | Unset): The administrator who added the member. `GET /api/teams/{name}/members`
                sends it only to an administrator (a session, or an admin key, of an
                `[auth] admins` user): to a member it would name who the administrators
                are, so the field is absent.
    """

    added_at: datetime.datetime
    username: str
    added_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_at = self.added_at.isoformat()

        username = self.username

        added_by: None | str | Unset
        if isinstance(self.added_by, Unset):
            added_by = UNSET
        else:
            added_by = self.added_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "added_at": added_at,
                "username": username,
            }
        )
        if added_by is not UNSET:
            field_dict["added_by"] = added_by

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        added_at = datetime.datetime.fromisoformat(d.pop("added_at"))

        username = d.pop("username")

        def _parse_added_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        added_by = _parse_added_by(d.pop("added_by", UNSET))

        team_member_entry = cls(
            added_at=added_at,
            username=username,
            added_by=added_by,
        )

        team_member_entry.additional_properties = d
        return team_member_entry

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
