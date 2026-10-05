from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AdminProjectMemberRequest")


@_attrs_define
class AdminProjectMemberRequest:
    """`POST /admin/projects/{project_id}/members` request body.

    `project_id` is redundant with the path parameter and is **ignored** by the
    server — the handler uses the path value. Kept on the wire for
    compatibility with existing clients that send it.

        Attributes:
            project_id (str):
            username (str):
    """

    project_id: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        username = d.pop("username")

        admin_project_member_request = cls(
            project_id=project_id,
            username=username,
        )

        admin_project_member_request.additional_properties = d
        return admin_project_member_request

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
