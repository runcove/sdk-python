from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AdminForceCreateResponse")


@_attrs_define
class AdminForceCreateResponse:
    """`POST /api/admin/quotas/{username}/force-create` — issues a one-shot
    bypass row. No request body (the target user is the path param).

        Attributes:
            bypass_id (str):
            granted_at (str):
            granted_by (str):
            username (str):
    """

    bypass_id: str
    granted_at: str
    granted_by: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bypass_id = self.bypass_id

        granted_at = self.granted_at

        granted_by = self.granted_by

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bypass_id": bypass_id,
                "granted_at": granted_at,
                "granted_by": granted_by,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        bypass_id = d.pop("bypass_id")

        granted_at = d.pop("granted_at")

        granted_by = d.pop("granted_by")

        username = d.pop("username")

        admin_force_create_response = cls(
            bypass_id=bypass_id,
            granted_at=granted_at,
            granted_by=granted_by,
            username=username,
        )

        admin_force_create_response.additional_properties = d
        return admin_force_create_response

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
