from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ProxyInvite")


@_attrs_define
class ProxyInvite:
    """POST /vms/{name}/ports/{port}/invites response body, and an item of
    GET /vms/{name}/share/invites. See the note on `ProxyPortInfo` above.

        Attributes:
            expires_at (datetime.datetime):
            invite_id (str):
            port (int):
            url (str):
            vm_name (str):
    """

    expires_at: datetime.datetime
    invite_id: str
    port: int
    url: str
    vm_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_at = self.expires_at.isoformat()

        invite_id = self.invite_id

        port = self.port

        url = self.url

        vm_name = self.vm_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_at": expires_at,
                "invite_id": invite_id,
                "port": port,
                "url": url,
                "vm_name": vm_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        invite_id = d.pop("invite_id")

        port = d.pop("port")

        url = d.pop("url")

        vm_name = d.pop("vm_name")

        proxy_invite = cls(
            expires_at=expires_at,
            invite_id=invite_id,
            port=port,
            url=url,
            vm_name=vm_name,
        )

        proxy_invite.additional_properties = d
        return proxy_invite

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
