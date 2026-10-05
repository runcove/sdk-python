from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamSummary")


@_attrs_define
class TeamSummary:
    """One team row for `cove team ls`.

    This is the ONE `TeamSummary` — no server-side duplicate exists
    (`handlers::teams::create_team`/`list_teams` build their `serde_json::json!`
    response by hand from `cove_service::teams::Team`/`TeamWithCount`, which
    carry a `warpgate_role_id` field this wire shape deliberately omits — that
    field is a Warpgate internal (`docs/vocabulary.md`) and must never reach
    the public surface).

        Attributes:
            created_at (datetime.datetime):
            id (str):
            member_count (int):
            name (str):
            created_by (None | str | Unset): The administrator who created the team. `GET /api/teams` sends it only
                to an administrator (a session, or an admin key, of an `[auth] admins`
                user): to anyone else it would name who the administrators are, so the
                field is absent. Creating a team needs an administrator, so the create
                answer always carries it.
    """

    created_at: datetime.datetime
    id: str
    member_count: int
    name: str
    created_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        member_count = self.member_count

        name = self.name

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "member_count": member_count,
                "name": name,
            }
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        member_count = d.pop("member_count")

        name = d.pop("name")

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        team_summary = cls(
            created_at=created_at,
            id=id,
            member_count=member_count,
            name=name,
            created_by=created_by,
        )

        team_summary.additional_properties = d
        return team_summary

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
