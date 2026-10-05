from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cpu_capacity import CpuCapacity
    from ..models.disk_capacity import DiskCapacity
    from ..models.ksm_stats import KsmStats
    from ..models.ram_capacity import RamCapacity
    from ..models.reservation_ref import ReservationRef


T = TypeVar("T", bound="CapacityReport")


@_attrs_define
class CapacityReport:
    """Full capacity report returned by `GET /host/capacity`.

    Attributes:
        active_vms (int):
        cpu (CpuCapacity): Summary of host CPU overcommit numbers.
        disk (DiskCapacity): Summary of data-disk space.
        max_vms (int):
        ram (RamCapacity): Summary of host RAM overcommit numbers, as reported by `GET /host/capacity`.
        reservations (list[ReservationRef]):
        ksm (KsmStats | None | Unset):
    """

    active_vms: int
    cpu: CpuCapacity
    disk: DiskCapacity
    max_vms: int
    ram: RamCapacity
    reservations: list[ReservationRef]
    ksm: KsmStats | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ksm_stats import KsmStats

        active_vms = self.active_vms

        cpu = self.cpu.to_dict()

        disk = self.disk.to_dict()

        max_vms = self.max_vms

        ram = self.ram.to_dict()

        reservations = []
        for reservations_item_data in self.reservations:
            reservations_item = reservations_item_data.to_dict()
            reservations.append(reservations_item)

        ksm: dict[str, Any] | None | Unset
        if isinstance(self.ksm, Unset):
            ksm = UNSET
        elif isinstance(self.ksm, KsmStats):
            ksm = self.ksm.to_dict()
        else:
            ksm = self.ksm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_vms": active_vms,
                "cpu": cpu,
                "disk": disk,
                "max_vms": max_vms,
                "ram": ram,
                "reservations": reservations,
            }
        )
        if ksm is not UNSET:
            field_dict["ksm"] = ksm

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.cpu_capacity import CpuCapacity
        from ..models.disk_capacity import DiskCapacity
        from ..models.ksm_stats import KsmStats
        from ..models.ram_capacity import RamCapacity
        from ..models.reservation_ref import ReservationRef

        d = dict(src_dict)
        active_vms = d.pop("active_vms")

        cpu = CpuCapacity.from_dict(d.pop("cpu"))

        disk = DiskCapacity.from_dict(d.pop("disk"))

        max_vms = d.pop("max_vms")

        ram = RamCapacity.from_dict(d.pop("ram"))

        reservations = []
        _reservations = d.pop("reservations")
        for reservations_item_data in _reservations:
            reservations_item = ReservationRef.from_dict(reservations_item_data)

            reservations.append(reservations_item)

        def _parse_ksm(data: object) -> KsmStats | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ksm_type_1 = KsmStats.from_dict(data)

                return ksm_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(KsmStats | None | Unset, data)

        ksm = _parse_ksm(d.pop("ksm", UNSET))

        capacity_report = cls(
            active_vms=active_vms,
            cpu=cpu,
            disk=disk,
            max_vms=max_vms,
            ram=ram,
            reservations=reservations,
            ksm=ksm,
        )

        capacity_report.additional_properties = d
        return capacity_report

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
