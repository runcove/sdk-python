from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.proxy_port_info import ProxyPortInfo


T = TypeVar("T", bound="ProxyUrlInfo")


@_attrs_define
class ProxyUrlInfo:
    """GET /vms/{name}/url response body. See the note on `ProxyPortInfo` above —
    same ONE-gets-`ToSchema` rule applies to `ProxyUrlInfo` / `ProxyInvite`.

        Attributes:
            ports (list[ProxyPortInfo]):
            ssh_url (str):
            vm_name (str):
    """

    ports: list[ProxyPortInfo]
    ssh_url: str
    vm_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            ports.append(ports_item)

        ssh_url = self.ssh_url

        vm_name = self.vm_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ports": ports,
                "ssh_url": ssh_url,
                "vm_name": vm_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.proxy_port_info import ProxyPortInfo

        d = dict(src_dict)
        ports = []
        _ports = d.pop("ports")
        for ports_item_data in _ports:
            ports_item = ProxyPortInfo.from_dict(ports_item_data)

            ports.append(ports_item)

        ssh_url = d.pop("ssh_url")

        vm_name = d.pop("vm_name")

        proxy_url_info = cls(
            ports=ports,
            ssh_url=ssh_url,
            vm_name=vm_name,
        )

        proxy_url_info.additional_properties = d
        return proxy_url_info

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
