from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="CreateInviteRequest")


@_attrs_define
class CreateInviteRequest:
    """POST /vms/{name}/ports/{port}/invites request body. `port` is not
    repeated here — it comes from the path. Not to be confused with
    `cove_service::proxy_types::CreateInviteRequest`, an unused duplicate with
    a different shape (see the note there).

        Attributes:
            ttl_secs (int):
    """

    ttl_secs: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ttl_secs = self.ttl_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ttl_secs": ttl_secs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        ttl_secs = d.pop("ttl_secs")

        create_invite_request = cls(
            ttl_secs=ttl_secs,
        )

        create_invite_request.additional_properties = d
        return create_invite_request

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
