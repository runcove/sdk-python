from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ConnectionInfo")


@_attrs_define
class ConnectionInfo:
    """POST /vms/{name}/connect response body.

    `warpgate_host`/`warpgate_port`/`warpgate_ssh_host_pubkey` renamed to
    `bastion_host`/`bastion_port`/`bastion_ssh_host_pubkey`. "Warpgate" is a
    banned public word in this product — an implementation choice, not
    something a user should ever see — and these fields are the wire contract
    itself, so they were the most visible remaining violation. No serde
    alias: there is no external API consumer yet (the SDK has not shipped),
    so the old spelling is removed rather than carried forward.

        Attributes:
            bastion_host (str):
            bastion_port (int):
            bastion_ssh_host_pubkey (str): OpenSSH-format bastion host pubkey for client-side pinning.
            ticket_secret (str):
    """

    bastion_host: str
    bastion_port: int
    bastion_ssh_host_pubkey: str
    ticket_secret: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bastion_host = self.bastion_host

        bastion_port = self.bastion_port

        bastion_ssh_host_pubkey = self.bastion_ssh_host_pubkey

        ticket_secret = self.ticket_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bastion_host": bastion_host,
                "bastion_port": bastion_port,
                "bastion_ssh_host_pubkey": bastion_ssh_host_pubkey,
                "ticket_secret": ticket_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        bastion_host = d.pop("bastion_host")

        bastion_port = d.pop("bastion_port")

        bastion_ssh_host_pubkey = d.pop("bastion_ssh_host_pubkey")

        ticket_secret = d.pop("ticket_secret")

        connection_info = cls(
            bastion_host=bastion_host,
            bastion_port=bastion_port,
            bastion_ssh_host_pubkey=bastion_ssh_host_pubkey,
            ticket_secret=ticket_secret,
        )

        connection_info.additional_properties = d
        return connection_info

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
