from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="GrantShareRequest")


@_attrs_define
class GrantShareRequest:
    """Wire body for `POST /vms/{name}/access`.

    Mirrors `cove_api_client::wire_types::GrantShareRequest`: a
    `subject_type` discriminator ("user" | "team"),
    the `subject_id` (username), and the `role` token ("user" |
    "collaborator"). The handler parses + validates before delegating to
    the service op so a malformed body surfaces as 400, not a service
    `Validation` 422 — keeps the contract uniform with other cove
    handlers that validate the wire shape at the edge.

        Attributes:
            role (str):
            subject_id (str):
            subject_type (str):
    """

    role: str
    subject_id: str
    subject_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        subject_id = self.subject_id

        subject_type = self.subject_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "subject_id": subject_id,
                "subject_type": subject_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        role = d.pop("role")

        subject_id = d.pop("subject_id")

        subject_type = d.pop("subject_type")

        grant_share_request = cls(
            role=role,
            subject_id=subject_id,
            subject_type=subject_type,
        )

        grant_share_request.additional_properties = d
        return grant_share_request

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
