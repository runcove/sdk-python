from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ProjectMember")


@_attrs_define
class ProjectMember:
    """One row of `GET /admin/projects/{project_id}/members`.

    Published as `ProjectMember` — the `Dto` suffix is a Rust-side
    artifact, not a public name (same treatment as `SecretSpecWire` →
    `SecretSpec` and `IdleStateDto` → `IdleState`).

        Attributes:
            added_at (str):
            added_by (str):
            project_id (str):
            username (str):
    """

    added_at: str
    added_by: str
    project_id: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_at = self.added_at

        added_by = self.added_by

        project_id = self.project_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "added_at": added_at,
                "added_by": added_by,
                "project_id": project_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        added_at = d.pop("added_at")

        added_by = d.pop("added_by")

        project_id = d.pop("project_id")

        username = d.pop("username")

        project_member = cls(
            added_at=added_at,
            added_by=added_by,
            project_id=project_id,
            username=username,
        )

        project_member.additional_properties = d
        return project_member

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
