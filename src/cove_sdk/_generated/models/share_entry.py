from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ShareEntry")


@_attrs_define
class ShareEntry:
    """One share row for `cove share users <vm>` / the web shared-users panel.

    This is the ONE `ShareEntry` — no server-side duplicate exists
    (`handlers::shares::get_shares` projects `cove_service::ops::share::ShareRow`,
    which carries no serde derives at all, straight into this shape by hand).

        Attributes:
            granted_at (datetime.datetime):
            granted_by (str):
            role (str):
            subject_id (str):
            subject_type (str):
    """

    granted_at: datetime.datetime
    granted_by: str
    role: str
    subject_id: str
    subject_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        granted_at = self.granted_at.isoformat()

        granted_by = self.granted_by

        role = self.role

        subject_id = self.subject_id

        subject_type = self.subject_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "granted_at": granted_at,
                "granted_by": granted_by,
                "role": role,
                "subject_id": subject_id,
                "subject_type": subject_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        granted_at = datetime.datetime.fromisoformat(d.pop("granted_at"))

        granted_by = d.pop("granted_by")

        role = d.pop("role")

        subject_id = d.pop("subject_id")

        subject_type = d.pop("subject_type")

        share_entry = cls(
            granted_at=granted_at,
            granted_by=granted_by,
            role=role,
            subject_id=subject_id,
            subject_type=subject_type,
        )

        share_entry.additional_properties = d
        return share_entry

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
