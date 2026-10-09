from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardServiceWebhook")


@_attrs_define
class OffboardServiceWebhook:
    """An active webhook subscription owned by a service bound to the person.

    Attributes:
        id (str):
        scope (str): `vm`, `user` or `server`.
        service (str): The service name (`svc:<name>` owns the subscription).
        vm (None | str | Unset): The VM's name (its id when the VM is gone), for a `vm`-scope
            subscription.
    """

    id: str
    scope: str
    service: str
    vm: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        scope = self.scope

        service = self.service

        vm: None | str | Unset
        if isinstance(self.vm, Unset):
            vm = UNSET
        else:
            vm = self.vm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scope": scope,
                "service": service,
            }
        )
        if vm is not UNSET:
            field_dict["vm"] = vm

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        scope = d.pop("scope")

        service = d.pop("service")

        def _parse_vm(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vm = _parse_vm(d.pop("vm", UNSET))

        offboard_service_webhook = cls(
            id=id,
            scope=scope,
            service=service,
            vm=vm,
        )

        offboard_service_webhook.additional_properties = d
        return offboard_service_webhook

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
