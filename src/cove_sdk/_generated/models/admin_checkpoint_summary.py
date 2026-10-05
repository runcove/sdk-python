from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.checkpoint_state import CheckpointState
from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminCheckpointSummary")


@_attrs_define
class AdminCheckpointSummary:
    """`GET /api/admin/checkpoints[?user=&orphaned=]` list entry — the
    admin-scoped cross-owner equivalent of `GET /api/checkpoints`
    (`CheckpointDto`). Backs `cove admin checkpoint ls`. `orphaned` mirrors
    the `checkpoints.vm_id IS NULL` condition (source VM deleted via
    `cove rm`); `size_bytes` is a best-effort on-disk fs scan (informational
    gauge, `0` when the scan failed or the row is missing from it).

        Attributes:
            checkpoint_id (str):
            created_at (datetime.datetime): When the checkpoint was started (RFC 3339, UTC).
            owner_username (str):
            state (CheckpointState): Where a checkpoint is in its life. Lowercase on the wire, like a VM's
                state.

                The listings and lookups only ever return `available` checkpoints; the
                other states exist so a client can name every value the field may hold.
            orphaned (bool | Unset):
            size_bytes (int | Unset):
            vm_name_at_creation (None | str | Unset):
    """

    checkpoint_id: str
    created_at: datetime.datetime
    owner_username: str
    state: CheckpointState
    orphaned: bool | Unset = UNSET
    size_bytes: int | Unset = UNSET
    vm_name_at_creation: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkpoint_id = self.checkpoint_id

        created_at = self.created_at.isoformat()

        owner_username = self.owner_username

        state = self.state.value

        orphaned = self.orphaned

        size_bytes = self.size_bytes

        vm_name_at_creation: None | str | Unset
        if isinstance(self.vm_name_at_creation, Unset):
            vm_name_at_creation = UNSET
        else:
            vm_name_at_creation = self.vm_name_at_creation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkpoint_id": checkpoint_id,
                "created_at": created_at,
                "owner_username": owner_username,
                "state": state,
            }
        )
        if orphaned is not UNSET:
            field_dict["orphaned"] = orphaned
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if vm_name_at_creation is not UNSET:
            field_dict["vm_name_at_creation"] = vm_name_at_creation

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        checkpoint_id = d.pop("checkpoint_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        owner_username = d.pop("owner_username")

        state = CheckpointState(d.pop("state"))

        orphaned = d.pop("orphaned", UNSET)

        size_bytes = d.pop("size_bytes", UNSET)

        def _parse_vm_name_at_creation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vm_name_at_creation = _parse_vm_name_at_creation(
            d.pop("vm_name_at_creation", UNSET)
        )

        admin_checkpoint_summary = cls(
            checkpoint_id=checkpoint_id,
            created_at=created_at,
            owner_username=owner_username,
            state=state,
            orphaned=orphaned,
            size_bytes=size_bytes,
            vm_name_at_creation=vm_name_at_creation,
        )

        admin_checkpoint_summary.additional_properties = d
        return admin_checkpoint_summary

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
