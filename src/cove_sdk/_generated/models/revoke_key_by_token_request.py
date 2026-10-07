from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RevokeKeyByTokenRequest")


@_attrs_define
class RevokeKeyByTokenRequest:
    """`POST /api/api-keys/revoke` request body: the key itself. Holding it is the
    proof, so the request carries no other credential. Fields other than
    `token` are ignored, so a secret-scanning partner may send its own
    metadata alongside.

        Attributes:
            token (str): The full API key, `cvk_` and all. Example: cvk_<43 characters>.
    """

    token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        token = d.pop("token")

        revoke_key_by_token_request = cls(
            token=token,
        )

        revoke_key_by_token_request.additional_properties = d
        return revoke_key_by_token_request

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
