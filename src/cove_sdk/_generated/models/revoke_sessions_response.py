from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RevokeSessionsResponse")


@_attrs_define
class RevokeSessionsResponse:
    """`POST /admin/users/{username}/revoke-sessions` response body.

    A real named type replacing the handler's previous inline
    `serde_json::json!({"revoked": n})`. Byte-identical on the wire; the point
    is that an inline body is invisible to an SDK generator (rule 3 in
    `crate::openapi`'s module docs).

        Attributes:
            revoked (int): How many active sessions were invalidated.
    """

    revoked: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        revoked = self.revoked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "revoked": revoked,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        revoked = d.pop("revoked")

        revoke_sessions_response = cls(
            revoked=revoked,
        )

        revoke_sessions_response.additional_properties = d
        return revoke_sessions_response

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
