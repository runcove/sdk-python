from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.disk_format import DiskFormat
from ..models.vm_state import VmState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auto_pause_policy_type_0 import AutoPausePolicyType0
    from ..models.auto_pause_policy_type_1 import AutoPausePolicyType1
    from ..models.ttl_policy import TtlPolicy
    from ..models.vm_detail_tags import VmDetailTags


T = TypeVar("T", bound="VmDetail")


@_attrs_define
class VmDetail:
    """GET /vms/{name} response body.

    The elastic-envelope fields (`vcpus_min/max`, `memory_min/max_mb`,
    `current_vcpus`, `current_memory_mb`) and the TTL fields are all
    `#[serde(default)]` so legacy daemons that don't emit them deserialize
    cleanly.

        Attributes:
            auto_pause_policy (AutoPausePolicyType0 | AutoPausePolicyType1): What Cove does with a VM that has gone idle.

                `AutoPause` pauses the VM after `idle_timeout_secs` without traffic:
                scheduling stops, memory stays resident, and the VM resumes instantly on
                the next packet. `AlwaysOn` leaves it running.
            created_at (str):
            disk_size_gb (int):
            image (str):
            mac_address (str):
            memory_mb (int): Memory in MiB the VM boots with on a cold start. Not what the VM has
                now: after a resize, or for a clone of a VM that was resized,
                `current_memory_mb` is the memory the guest holds.
            name (str):
            state (VmState): VM lifecycle state as reported by the Cove REST API and persisted by core.

                Serializes to lowercase JSON strings (`"running"`, `"hibernated"`, …). The
                one exception is `ForceStopping`, which spells its wire value
                `"force_stopping"` — see the variant's own note.

                # One authoritative spelling per state

                [`VmState::as_wire_str`] is the single place a state's wire name is
                written down. `Display`, [`std::str::FromStr`] and every SQL predicate that
                filters the `vms.state` column are all derived from it (via
                [`VmState::ALL`]), so renaming a state is a compile error at each derived
                site rather than a silent behaviour change. Two real defects came from the
                hand-maintained copies this replaces: a reconciler query filtering
                `force_killing`, a spelling no schema version ever held, and
                every hibernated VM rendering as an unstyled badge.

                The serde encoding is the one representation still declared separately
                (attributes cannot call a function); `unit_vm_state_wire_roundtrip` pins the
                two against each other for every variant.

                # What a person is shown is a separate concern

                [`VmState::display_name`] carries the words for a human — `"Force
                stopping"`, not the wire value `force_stopping`. Presentation layers must
                use it verbatim rather than capitalising the wire string, which is how
                `force_stopping` came to be shown as `Force_stopping`.

                # The names the rename retired are gone

                The 2026-07 terminology rename gave four states clearer names —
                `suspending` → `hibernating`, `suspended` → `hibernated`, `restoring` →
                `waking`, `forcekilling` → `force_stopping`. Migration 035 rewrites every
                stored row, so the old spellings exist nowhere after it runs and are now
                **rejected** on the way in, by serde and by `FromStr` alike. There is one
                production environment, a handful of users and no external API consumer, so
                the data was migrated forward instead of being read in two spellings
                indefinitely.
            updated_at (str):
            vcpus (int): vCPUs the VM boots with on a cold start. The VM can be running with
                more after a resize: `current_vcpus` is what it has now.
            vm_id (str):
            agent_capabilities (list[str] | Unset): Capability tokens from the last handshake (`vms.capabilities`).
            agent_handshake_at (None | str | Unset): RFC 3339 time of the last completed agent handshake
                (`vms.agent_handshake_at`). Absent before the first one, and from a
                daemon that predates the field.
            agent_protocol_version (int | None | Unset): Agent wire-protocol version from the handshake
                (`vms.agent_protocol_version`,
                migration 012). `#[serde(default)]` so legacy daemons that omit it
                deserialize cleanly as `None`.
            agent_stale (bool | Unset): The last handshake reported a protocol below the host's
                (`vms.agent_stale`); the reconciler pushes a fresh agent.
            agent_version (None | str | Unset):
            current_memory_mb (int | Unset): Memory in MiB the VM has now: what `free` inside the guest reports
                as its total, give or take what the kernel keeps for itself. Quota is
                charged on this.
            current_vcpus (int | Unset): vCPUs the VM has now. Quota is charged on this.
            degraded (bool | Unset):
            degraded_reason (None | str | Unset):
            deletes_in_secs (int | None | Unset):
            disk_format (DiskFormat | Unset):
            ip_address (None | str | Unset):
            max_life_expires_in_secs (int | None | Unset):
            memory_max_mb (int | Unset): Most memory in MiB a resize can give the VM while it runs.
            memory_min_mb (int | Unset): Least memory in MiB a resize can take the VM down to.
            tags (VmDetailTags | Unset):
            ttl_policy (TtlPolicy | Unset): Per-VM TTL policy bundle. Both knobs default to "off" (`Never` / `None`);
                pool defaults and CLI flags merge into this on create.
            vcpus_max (int | Unset): Most vCPUs a resize can give the VM while it runs.
            vcpus_min (int | Unset): Fewest vCPUs a resize can take the VM down to.
    """

    auto_pause_policy: AutoPausePolicyType0 | AutoPausePolicyType1
    created_at: str
    disk_size_gb: int
    image: str
    mac_address: str
    memory_mb: int
    name: str
    state: VmState
    updated_at: str
    vcpus: int
    vm_id: str
    agent_capabilities: list[str] | Unset = UNSET
    agent_handshake_at: None | str | Unset = UNSET
    agent_protocol_version: int | None | Unset = UNSET
    agent_stale: bool | Unset = UNSET
    agent_version: None | str | Unset = UNSET
    current_memory_mb: int | Unset = UNSET
    current_vcpus: int | Unset = UNSET
    degraded: bool | Unset = UNSET
    degraded_reason: None | str | Unset = UNSET
    deletes_in_secs: int | None | Unset = UNSET
    disk_format: DiskFormat | Unset = UNSET
    ip_address: None | str | Unset = UNSET
    max_life_expires_in_secs: int | None | Unset = UNSET
    memory_max_mb: int | Unset = UNSET
    memory_min_mb: int | Unset = UNSET
    tags: VmDetailTags | Unset = UNSET
    ttl_policy: TtlPolicy | Unset = UNSET
    vcpus_max: int | Unset = UNSET
    vcpus_min: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )

        auto_pause_policy: dict[str, Any]
        if isinstance(self.auto_pause_policy, AutoPausePolicyType0):
            auto_pause_policy = self.auto_pause_policy.to_dict()
        else:
            auto_pause_policy = self.auto_pause_policy.to_dict()

        created_at = self.created_at

        disk_size_gb = self.disk_size_gb

        image = self.image

        mac_address = self.mac_address

        memory_mb = self.memory_mb

        name = self.name

        state = self.state.value

        updated_at = self.updated_at

        vcpus = self.vcpus

        vm_id = self.vm_id

        agent_capabilities: list[str] | Unset = UNSET
        if not isinstance(self.agent_capabilities, Unset):
            agent_capabilities = self.agent_capabilities

        agent_handshake_at: None | str | Unset
        if isinstance(self.agent_handshake_at, Unset):
            agent_handshake_at = UNSET
        else:
            agent_handshake_at = self.agent_handshake_at

        agent_protocol_version: int | None | Unset
        if isinstance(self.agent_protocol_version, Unset):
            agent_protocol_version = UNSET
        else:
            agent_protocol_version = self.agent_protocol_version

        agent_stale = self.agent_stale

        agent_version: None | str | Unset
        if isinstance(self.agent_version, Unset):
            agent_version = UNSET
        else:
            agent_version = self.agent_version

        current_memory_mb = self.current_memory_mb

        current_vcpus = self.current_vcpus

        degraded = self.degraded

        degraded_reason: None | str | Unset
        if isinstance(self.degraded_reason, Unset):
            degraded_reason = UNSET
        else:
            degraded_reason = self.degraded_reason

        deletes_in_secs: int | None | Unset
        if isinstance(self.deletes_in_secs, Unset):
            deletes_in_secs = UNSET
        else:
            deletes_in_secs = self.deletes_in_secs

        disk_format: str | Unset = UNSET
        if not isinstance(self.disk_format, Unset):
            disk_format = self.disk_format.value

        ip_address: None | str | Unset
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        max_life_expires_in_secs: int | None | Unset
        if isinstance(self.max_life_expires_in_secs, Unset):
            max_life_expires_in_secs = UNSET
        else:
            max_life_expires_in_secs = self.max_life_expires_in_secs

        memory_max_mb = self.memory_max_mb

        memory_min_mb = self.memory_min_mb

        tags: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        ttl_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ttl_policy, Unset):
            ttl_policy = self.ttl_policy.to_dict()

        vcpus_max = self.vcpus_max

        vcpus_min = self.vcpus_min

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auto_pause_policy": auto_pause_policy,
                "created_at": created_at,
                "disk_size_gb": disk_size_gb,
                "image": image,
                "mac_address": mac_address,
                "memory_mb": memory_mb,
                "name": name,
                "state": state,
                "updated_at": updated_at,
                "vcpus": vcpus,
                "vm_id": vm_id,
            }
        )
        if agent_capabilities is not UNSET:
            field_dict["agent_capabilities"] = agent_capabilities
        if agent_handshake_at is not UNSET:
            field_dict["agent_handshake_at"] = agent_handshake_at
        if agent_protocol_version is not UNSET:
            field_dict["agent_protocol_version"] = agent_protocol_version
        if agent_stale is not UNSET:
            field_dict["agent_stale"] = agent_stale
        if agent_version is not UNSET:
            field_dict["agent_version"] = agent_version
        if current_memory_mb is not UNSET:
            field_dict["current_memory_mb"] = current_memory_mb
        if current_vcpus is not UNSET:
            field_dict["current_vcpus"] = current_vcpus
        if degraded is not UNSET:
            field_dict["degraded"] = degraded
        if degraded_reason is not UNSET:
            field_dict["degraded_reason"] = degraded_reason
        if deletes_in_secs is not UNSET:
            field_dict["deletes_in_secs"] = deletes_in_secs
        if disk_format is not UNSET:
            field_dict["disk_format"] = disk_format
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if max_life_expires_in_secs is not UNSET:
            field_dict["max_life_expires_in_secs"] = max_life_expires_in_secs
        if memory_max_mb is not UNSET:
            field_dict["memory_max_mb"] = memory_max_mb
        if memory_min_mb is not UNSET:
            field_dict["memory_min_mb"] = memory_min_mb
        if tags is not UNSET:
            field_dict["tags"] = tags
        if ttl_policy is not UNSET:
            field_dict["ttl_policy"] = ttl_policy
        if vcpus_max is not UNSET:
            field_dict["vcpus_max"] = vcpus_max
        if vcpus_min is not UNSET:
            field_dict["vcpus_min"] = vcpus_min

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )
        from ..models.auto_pause_policy_type_1 import (
            AutoPausePolicyType1,
        )
        from ..models.ttl_policy import TtlPolicy
        from ..models.vm_detail_tags import VmDetailTags

        d = dict(src_dict)

        def _parse_auto_pause_policy(
            data: object,
        ) -> AutoPausePolicyType0 | AutoPausePolicyType1:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_auto_pause_policy_type_0 = (
                    AutoPausePolicyType0.from_dict(data)
                )

                return componentsschemas_auto_pause_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_auto_pause_policy_type_1 = AutoPausePolicyType1.from_dict(
                data
            )

            return componentsschemas_auto_pause_policy_type_1

        auto_pause_policy = _parse_auto_pause_policy(d.pop("auto_pause_policy"))

        created_at = d.pop("created_at")

        disk_size_gb = d.pop("disk_size_gb")

        image = d.pop("image")

        mac_address = d.pop("mac_address")

        memory_mb = d.pop("memory_mb")

        name = d.pop("name")

        state = VmState(d.pop("state"))

        updated_at = d.pop("updated_at")

        vcpus = d.pop("vcpus")

        vm_id = d.pop("vm_id")

        agent_capabilities = cast(list[str], d.pop("agent_capabilities", UNSET))

        def _parse_agent_handshake_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_handshake_at = _parse_agent_handshake_at(
            d.pop("agent_handshake_at", UNSET)
        )

        def _parse_agent_protocol_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        agent_protocol_version = _parse_agent_protocol_version(
            d.pop("agent_protocol_version", UNSET)
        )

        agent_stale = d.pop("agent_stale", UNSET)

        def _parse_agent_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_version = _parse_agent_version(d.pop("agent_version", UNSET))

        current_memory_mb = d.pop("current_memory_mb", UNSET)

        current_vcpus = d.pop("current_vcpus", UNSET)

        degraded = d.pop("degraded", UNSET)

        def _parse_degraded_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        degraded_reason = _parse_degraded_reason(d.pop("degraded_reason", UNSET))

        def _parse_deletes_in_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        deletes_in_secs = _parse_deletes_in_secs(d.pop("deletes_in_secs", UNSET))

        _disk_format = d.pop("disk_format", UNSET)
        disk_format: DiskFormat | Unset
        if isinstance(_disk_format, Unset):
            disk_format = UNSET
        else:
            disk_format = DiskFormat(_disk_format)

        def _parse_ip_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        def _parse_max_life_expires_in_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_life_expires_in_secs = _parse_max_life_expires_in_secs(
            d.pop("max_life_expires_in_secs", UNSET)
        )

        memory_max_mb = d.pop("memory_max_mb", UNSET)

        memory_min_mb = d.pop("memory_min_mb", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: VmDetailTags | Unset
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = VmDetailTags.from_dict(_tags)

        _ttl_policy = d.pop("ttl_policy", UNSET)
        ttl_policy: TtlPolicy | Unset
        if isinstance(_ttl_policy, Unset):
            ttl_policy = UNSET
        else:
            ttl_policy = TtlPolicy.from_dict(_ttl_policy)

        vcpus_max = d.pop("vcpus_max", UNSET)

        vcpus_min = d.pop("vcpus_min", UNSET)

        vm_detail = cls(
            auto_pause_policy=auto_pause_policy,
            created_at=created_at,
            disk_size_gb=disk_size_gb,
            image=image,
            mac_address=mac_address,
            memory_mb=memory_mb,
            name=name,
            state=state,
            updated_at=updated_at,
            vcpus=vcpus,
            vm_id=vm_id,
            agent_capabilities=agent_capabilities,
            agent_handshake_at=agent_handshake_at,
            agent_protocol_version=agent_protocol_version,
            agent_stale=agent_stale,
            agent_version=agent_version,
            current_memory_mb=current_memory_mb,
            current_vcpus=current_vcpus,
            degraded=degraded,
            degraded_reason=degraded_reason,
            deletes_in_secs=deletes_in_secs,
            disk_format=disk_format,
            ip_address=ip_address,
            max_life_expires_in_secs=max_life_expires_in_secs,
            memory_max_mb=memory_max_mb,
            memory_min_mb=memory_min_mb,
            tags=tags,
            ttl_policy=ttl_policy,
            vcpus_max=vcpus_max,
            vcpus_min=vcpus_min,
        )

        vm_detail.additional_properties = d
        return vm_detail

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
