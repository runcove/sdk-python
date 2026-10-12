from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocalStatus")


@_attrs_define
class LocalStatus:
    """What a Mac's local daemon runs beside its VMs, within the system status.
    On a Mac `ch_processes` counts the VM helpers (one
    `cove __vz-helper` per running or paused VM), and there are no TAP
    devices or warm pool.

        Attributes:
            bastion_ssh_port (int | None | Unset): The embedded Warpgate's SSH port on `127.0.0.1` when it serves.
            bastion_unavailable (None | str | Unset): Why the embedded Warpgate isn't serving; absent when it is.
            network_owner_gateway (None | str | Unset): The network owner's gateway when it answers its control socket;
                absent when it doesn't.
    """

    bastion_ssh_port: int | None | Unset = UNSET
    bastion_unavailable: None | str | Unset = UNSET
    network_owner_gateway: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bastion_ssh_port: int | None | Unset
        if isinstance(self.bastion_ssh_port, Unset):
            bastion_ssh_port = UNSET
        else:
            bastion_ssh_port = self.bastion_ssh_port

        bastion_unavailable: None | str | Unset
        if isinstance(self.bastion_unavailable, Unset):
            bastion_unavailable = UNSET
        else:
            bastion_unavailable = self.bastion_unavailable

        network_owner_gateway: None | str | Unset
        if isinstance(self.network_owner_gateway, Unset):
            network_owner_gateway = UNSET
        else:
            network_owner_gateway = self.network_owner_gateway

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bastion_ssh_port is not UNSET:
            field_dict["bastion_ssh_port"] = bastion_ssh_port
        if bastion_unavailable is not UNSET:
            field_dict["bastion_unavailable"] = bastion_unavailable
        if network_owner_gateway is not UNSET:
            field_dict["network_owner_gateway"] = network_owner_gateway

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_bastion_ssh_port(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        bastion_ssh_port = _parse_bastion_ssh_port(d.pop("bastion_ssh_port", UNSET))

        def _parse_bastion_unavailable(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bastion_unavailable = _parse_bastion_unavailable(
            d.pop("bastion_unavailable", UNSET)
        )

        def _parse_network_owner_gateway(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        network_owner_gateway = _parse_network_owner_gateway(
            d.pop("network_owner_gateway", UNSET)
        )

        local_status = cls(
            bastion_ssh_port=bastion_ssh_port,
            bastion_unavailable=bastion_unavailable,
            network_owner_gateway=network_owner_gateway,
        )

        local_status.additional_properties = d
        return local_status

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
