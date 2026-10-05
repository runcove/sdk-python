from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.reservation_kind import ReservationKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReservationRef")


@_attrs_define
class ReservationRef:
    """A single live reservation row.

    Attributes:
        disk_bytes (int):
        flow_id (str):
        id (UUID):
        kind (ReservationKind): What a live reservation is holding capacity for.

            **This is a public wire value, and it is persisted.** It is serialised
            into `GET /host/capacity`'s `reservations[].kind`, deserialised from
            `POST /host/reservations`' request body (nested inside [`PendingAction`]'s
            internal tag), and written into the `reservations.kind` column as a bare
            string via `serde_plain` by `cove-core`'s `ReservationStore`. See the
            module doc for the rename this enum's `Wake` / `WakeFromCheckpoint`
            variants carry, and why the old spellings are rejected rather than
            aliased.
        memory_mb (int):
        ttl_expires_ms (int):
        vcpus (int):
        vm_id (UUID | Unset): Globally unique VM identifier (UUID v7, time-ordered).
    """

    disk_bytes: int
    flow_id: str
    id: UUID
    kind: ReservationKind
    memory_mb: int
    ttl_expires_ms: int
    vcpus: int
    vm_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_bytes = self.disk_bytes

        flow_id = self.flow_id

        id = str(self.id)

        kind = self.kind.value

        memory_mb = self.memory_mb

        ttl_expires_ms = self.ttl_expires_ms

        vcpus = self.vcpus

        vm_id: str | Unset = UNSET
        if not isinstance(self.vm_id, Unset):
            vm_id = str(self.vm_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disk_bytes": disk_bytes,
                "flow_id": flow_id,
                "id": id,
                "kind": kind,
                "memory_mb": memory_mb,
                "ttl_expires_ms": ttl_expires_ms,
                "vcpus": vcpus,
            }
        )
        if vm_id is not UNSET:
            field_dict["vm_id"] = vm_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        disk_bytes = d.pop("disk_bytes")

        flow_id = d.pop("flow_id")

        id = UUID(d.pop("id"))

        kind = ReservationKind(d.pop("kind"))

        memory_mb = d.pop("memory_mb")

        ttl_expires_ms = d.pop("ttl_expires_ms")

        vcpus = d.pop("vcpus")

        _vm_id = d.pop("vm_id", UNSET)
        vm_id: UUID | Unset
        if isinstance(_vm_id, Unset):
            vm_id = UNSET
        else:
            vm_id = UUID(_vm_id)

        reservation_ref = cls(
            disk_bytes=disk_bytes,
            flow_id=flow_id,
            id=id,
            kind=kind,
            memory_mb=memory_mb,
            ttl_expires_ms=ttl_expires_ms,
            vcpus=vcpus,
            vm_id=vm_id,
        )

        reservation_ref.additional_properties = d
        return reservation_ref

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
