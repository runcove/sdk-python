from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.restore_vm_ref import RestoreVmRef


T = TypeVar("T", bound="RestoreVmsRequest")


@_attrs_define
class RestoreVmsRequest:
    """
    Attributes:
        vms (list[RestoreVmRef]): The VMs to start. An id named twice is started once.
        concurrency (int | None | Unset): Starts in flight at once. Default 4; values outside 1..=16 are clamped.
    """

    vms: list[RestoreVmRef]
    concurrency: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vms = []
        for vms_item_data in self.vms:
            vms_item = vms_item_data.to_dict()
            vms.append(vms_item)

        concurrency: int | None | Unset
        if isinstance(self.concurrency, Unset):
            concurrency = UNSET
        else:
            concurrency = self.concurrency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vms": vms,
            }
        )
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.restore_vm_ref import RestoreVmRef

        d = dict(src_dict)
        vms = []
        _vms = d.pop("vms")
        for vms_item_data in _vms:
            vms_item = RestoreVmRef.from_dict(vms_item_data)

            vms.append(vms_item)

        def _parse_concurrency(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        concurrency = _parse_concurrency(d.pop("concurrency", UNSET))

        restore_vms_request = cls(
            vms=vms,
            concurrency=concurrency,
        )

        restore_vms_request.additional_properties = d
        return restore_vms_request

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
