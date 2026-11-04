from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="TeamAdminRevokeResponse")


@_attrs_define
class TeamAdminRevokeResponse:
    """The answer to a team admin revoke.

    Attributes:
        changed (bool): False when the member was not the admin: nothing changed and no audit
            row was written.
        team_keys_minted (list[str]): The ids of the active, unexpired team keys this person minted for this team. They
            keep working; a fleet admin or a remaining team admin rotates any that should not.
    """

    changed: bool
    team_keys_minted: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        changed = self.changed

        team_keys_minted = self.team_keys_minted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "changed": changed,
                "team_keys_minted": team_keys_minted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        changed = d.pop("changed")

        team_keys_minted = cast(list[str], d.pop("team_keys_minted"))

        team_admin_revoke_response = cls(
            changed=changed,
            team_keys_minted=team_keys_minted,
        )

        team_admin_revoke_response.additional_properties = d
        return team_admin_revoke_response

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
