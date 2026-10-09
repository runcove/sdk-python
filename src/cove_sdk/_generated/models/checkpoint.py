from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.checkpoint_state import CheckpointState
from ..types import UNSET, Unset

T = TypeVar("T", bound="Checkpoint")


@_attrs_define
class Checkpoint:
    """GET /checkpoints response entry. Blends core's lifecycle row with the
    service-owned ownership/provenance columns. Additive fields
    carry serde defaults, so older peers keep working.

        Attributes:
            created_at (datetime.datetime): When the checkpoint was started (RFC 3339, UTC).
            id (str): UUID v7 of the checkpoint (spans both core and service tables).
            owner_username (str): Service-owned: who created the checkpoint.
            state (CheckpointState): Where a checkpoint is in its life. Lowercase on the wire, like a VM's
                state.

                The listings and lookups only ever return `available` checkpoints; the
                other states exist so a client can name every value the field may hold.
            vm_id (str): VM the checkpoint was taken from.
            clone_refcount (int | Unset): Number of live clones depending on this checkpoint. `> 0` blocks
                delete with 409.
            completed_at (datetime.datetime | None | Unset): When the checkpoint became `available` (RFC 3339, UTC). Absent
                while
                it is `creating` or `failed`.
            cove_version (str | Unset): Service-owned: the cove release that took the checkpoint, the
                version `GET /health` reports as `server_version`. Empty when the
                daemon did not know its release.
            description (None | str | Unset): Service-owned: human-readable description supplied at create time.
            disk_only (bool | Unset): `true` when the checkpoint captured disk state only (no
                guest RAM / memory snapshot). Disk-only checkpoints are cheaper and
                don't require a `Pausable` CH pause, but cannot be used for a live
                restore. `#[serde(default)]` so a legacy daemon that predates the
                field deserializes to `false` (full checkpoint) — backwards
                compatible.
            distro (str | Unset): Service-owned: distro family at snapshot time (`fedora`, `ubuntu`,
                `alpine`, `sandbox`, …), for portability.
            golden_image_id (str | Unset): Service-owned: golden-image identifier the source VM was launched
                from. Pinned at snapshot time so a future restore can refuse a
                cove-version that no longer ships that image.
            orphaned_at (datetime.datetime | None | Unset): When the checkpoint's source VM was deleted (RFC 3339, UTC).
                Present
                only on an orphan, a checkpoint that outlived its VM (`vm_id` is then
                empty). Absent too on an orphan from a release before this field,
                until the server's orphan-checkpoint reclaim pass first sees it.
            reclaim_at (datetime.datetime | None | Unset): When the server will delete this orphan on its own (RFC 3339,
                UTC):
                `orphaned_at` plus the server's `[service]
                orphan_checkpoint_reclaim_days`. Absent for a checkpoint whose VM
                exists, for an orphan a clone still depends on (it is kept while the
                clone exists), and for every checkpoint when the server does not
                reclaim orphans (the setting is `0`). A time in the past means the
                next reclaim pass deletes it.
            size_bytes (int | None | Unset): On-disk total size in bytes; `None` until the reconciler measures.
            vm_image_at_creation (None | str | Unset): Source VM image captured at creation time.
            vm_name_at_creation (None | str | Unset): Source VM name captured at checkpoint creation time. Survives
                `cove rm` of the source VM. `None` for pre-021 rows.
            vm_name_at_snapshot (str | Unset): Service-owned: VM name captured at snapshot time. Survives source
                rename/delete so `cove restore` can show provenance.
    """

    created_at: datetime.datetime
    id: str
    owner_username: str
    state: CheckpointState
    vm_id: str
    clone_refcount: int | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET
    cove_version: str | Unset = UNSET
    description: None | str | Unset = UNSET
    disk_only: bool | Unset = UNSET
    distro: str | Unset = UNSET
    golden_image_id: str | Unset = UNSET
    orphaned_at: datetime.datetime | None | Unset = UNSET
    reclaim_at: datetime.datetime | None | Unset = UNSET
    size_bytes: int | None | Unset = UNSET
    vm_image_at_creation: None | str | Unset = UNSET
    vm_name_at_creation: None | str | Unset = UNSET
    vm_name_at_snapshot: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        owner_username = self.owner_username

        state = self.state.value

        vm_id = self.vm_id

        clone_refcount = self.clone_refcount

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        cove_version = self.cove_version

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        disk_only = self.disk_only

        distro = self.distro

        golden_image_id = self.golden_image_id

        orphaned_at: None | str | Unset
        if isinstance(self.orphaned_at, Unset):
            orphaned_at = UNSET
        elif isinstance(self.orphaned_at, datetime.datetime):
            orphaned_at = self.orphaned_at.isoformat()
        else:
            orphaned_at = self.orphaned_at

        reclaim_at: None | str | Unset
        if isinstance(self.reclaim_at, Unset):
            reclaim_at = UNSET
        elif isinstance(self.reclaim_at, datetime.datetime):
            reclaim_at = self.reclaim_at.isoformat()
        else:
            reclaim_at = self.reclaim_at

        size_bytes: int | None | Unset
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        vm_image_at_creation: None | str | Unset
        if isinstance(self.vm_image_at_creation, Unset):
            vm_image_at_creation = UNSET
        else:
            vm_image_at_creation = self.vm_image_at_creation

        vm_name_at_creation: None | str | Unset
        if isinstance(self.vm_name_at_creation, Unset):
            vm_name_at_creation = UNSET
        else:
            vm_name_at_creation = self.vm_name_at_creation

        vm_name_at_snapshot = self.vm_name_at_snapshot

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "owner_username": owner_username,
                "state": state,
                "vm_id": vm_id,
            }
        )
        if clone_refcount is not UNSET:
            field_dict["clone_refcount"] = clone_refcount
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if cove_version is not UNSET:
            field_dict["cove_version"] = cove_version
        if description is not UNSET:
            field_dict["description"] = description
        if disk_only is not UNSET:
            field_dict["disk_only"] = disk_only
        if distro is not UNSET:
            field_dict["distro"] = distro
        if golden_image_id is not UNSET:
            field_dict["golden_image_id"] = golden_image_id
        if orphaned_at is not UNSET:
            field_dict["orphaned_at"] = orphaned_at
        if reclaim_at is not UNSET:
            field_dict["reclaim_at"] = reclaim_at
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if vm_image_at_creation is not UNSET:
            field_dict["vm_image_at_creation"] = vm_image_at_creation
        if vm_name_at_creation is not UNSET:
            field_dict["vm_name_at_creation"] = vm_name_at_creation
        if vm_name_at_snapshot is not UNSET:
            field_dict["vm_name_at_snapshot"] = vm_name_at_snapshot

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        owner_username = d.pop("owner_username")

        state = CheckpointState(d.pop("state"))

        vm_id = d.pop("vm_id")

        clone_refcount = d.pop("clone_refcount", UNSET)

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        cove_version = d.pop("cove_version", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        disk_only = d.pop("disk_only", UNSET)

        distro = d.pop("distro", UNSET)

        golden_image_id = d.pop("golden_image_id", UNSET)

        def _parse_orphaned_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                orphaned_at_type_0 = datetime.datetime.fromisoformat(data)

                return orphaned_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        orphaned_at = _parse_orphaned_at(d.pop("orphaned_at", UNSET))

        def _parse_reclaim_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reclaim_at_type_0 = datetime.datetime.fromisoformat(data)

                return reclaim_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        reclaim_at = _parse_reclaim_at(d.pop("reclaim_at", UNSET))

        def _parse_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes", UNSET))

        def _parse_vm_image_at_creation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vm_image_at_creation = _parse_vm_image_at_creation(
            d.pop("vm_image_at_creation", UNSET)
        )

        def _parse_vm_name_at_creation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vm_name_at_creation = _parse_vm_name_at_creation(
            d.pop("vm_name_at_creation", UNSET)
        )

        vm_name_at_snapshot = d.pop("vm_name_at_snapshot", UNSET)

        checkpoint = cls(
            created_at=created_at,
            id=id,
            owner_username=owner_username,
            state=state,
            vm_id=vm_id,
            clone_refcount=clone_refcount,
            completed_at=completed_at,
            cove_version=cove_version,
            description=description,
            disk_only=disk_only,
            distro=distro,
            golden_image_id=golden_image_id,
            orphaned_at=orphaned_at,
            reclaim_at=reclaim_at,
            size_bytes=size_bytes,
            vm_image_at_creation=vm_image_at_creation,
            vm_name_at_creation=vm_name_at_creation,
            vm_name_at_snapshot=vm_name_at_snapshot,
        )

        checkpoint.additional_properties = d
        return checkpoint

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
