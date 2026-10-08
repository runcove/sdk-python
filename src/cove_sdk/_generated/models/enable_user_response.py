from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="EnableUserResponse")


@_attrs_define
class EnableUserResponse:
    """`POST /api/admin/users/{username}/enable` response: the shut-out record
    that was cleared, as it stood.

        Attributes:
            disabled_at (str): When offboarding shut them out (RFC 3339, UTC).
            disabled_by (str): The administrator whose offboarding shut them out.
            reason (str): Why (`offboarded`).
            username (str): Who was enabled, as the record spelled the name.
    """

    disabled_at: str
    disabled_by: str
    reason: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disabled_at = self.disabled_at

        disabled_by = self.disabled_by

        reason = self.reason

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disabled_at": disabled_at,
                "disabled_by": disabled_by,
                "reason": reason,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        disabled_at = d.pop("disabled_at")

        disabled_by = d.pop("disabled_by")

        reason = d.pop("reason")

        username = d.pop("username")

        enable_user_response = cls(
            disabled_at=disabled_at,
            disabled_by=disabled_by,
            reason=reason,
            username=username,
        )

        enable_user_response.additional_properties = d
        return enable_user_response

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
