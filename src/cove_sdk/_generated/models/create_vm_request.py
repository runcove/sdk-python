from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auto_pause_policy_type_0 import AutoPausePolicyType0
    from ..models.auto_pause_policy_type_1 import AutoPausePolicyType1
    from ..models.create_vm_request_initial_tags import CreateVmRequestInitialTags
    from ..models.secret_spec import SecretSpec
    from ..models.ttl_policy import TtlPolicy


T = TypeVar("T", bound="CreateVmRequest")


@_attrs_define
class CreateVmRequest:
    """POST /vms request body.

    Attributes:
        auto_pause_policy (AutoPausePolicyType0 | AutoPausePolicyType1 | None | Unset):
        cpus (int | None | Unset): Requested vCPU count. `None` → service uses the configured default.
            Additive, backward-compatible (older clients omit the field).
        disk_size_gb (int | None | Unset): Requested root disk size in GB. `None` → service uses the configured
            default. When `Some`, the service validates against `disk_size_gb_min/max`
            and charges quota against the requested size.
        image (None | str | Unset):
        initial_secrets (list[SecretSpec] | Unset): Secrets to inject after VM creation succeeds. Older
            clients omit the field; the server treats absence as empty (additive,
            backward-compatible).
        initial_tags (CreateVmRequestInitialTags | Unset): Tags to set immediately after VM creation. A JSON object
            of key to value, the same shape as `VmDetail.tags` (a list of
            `[key, value]` pairs until API version 5). Each entry is validated
            server-side via the public `validate_user_tag_key` /
            `validate_tag_value` validators. Absent means no tags.
        memory_mb (int | None | Unset): Requested memory in MiB. `None` → service uses the configured default.
        name (None | str | Unset): The new VM's name. Omit it and the server picks one. A name must be
            3-30 characters of lowercase ASCII letters, digits and hyphens, and
            must not start or end with a hyphen; any other name is refused with
            400 `invalid_vm_name`.
        nested_virt (bool | Unset): Expose nested virtualisation (VMX/SVM) to the
            new VM's guest. Off unless `true`; administrators only (anyone else is
            refused 403). An opted-in VM is always cold-booted, never claimed from
            the warm pool, and keeps the setting across every later cold boot.
            Additive, backward-compatible: older clients omit the field and get
            `false`, and `false` is not serialised.
        ports (list[int] | Unset): Per-VM HTTP proxy ports to register with Warpgate after VM creation.
            Each port must appear in `[proxy].allowed_ports` in `cove.toml`.
            Empty by default — older clients omit the field and the server treats
            it as no proxy ports requested.
        team (None | str | Unset): Team name for at-create attribution
            (`cove new --team <name>`): the VM charges the TEAM quota envelope
            instead of the owner's personal one. Requires the creator to be a
            member of the named team (checked service-side). Additive,
            backward-compatible (older clients omit the field).
        ttl_policy (None | TtlPolicy | Unset):
    """

    auto_pause_policy: AutoPausePolicyType0 | AutoPausePolicyType1 | None | Unset = (
        UNSET
    )
    cpus: int | None | Unset = UNSET
    disk_size_gb: int | None | Unset = UNSET
    image: None | str | Unset = UNSET
    initial_secrets: list[SecretSpec] | Unset = UNSET
    initial_tags: CreateVmRequestInitialTags | Unset = UNSET
    memory_mb: int | None | Unset = UNSET
    name: None | str | Unset = UNSET
    nested_virt: bool | Unset = UNSET
    ports: list[int] | Unset = UNSET
    team: None | str | Unset = UNSET
    ttl_policy: None | TtlPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )
        from ..models.auto_pause_policy_type_1 import (
            AutoPausePolicyType1,
        )
        from ..models.ttl_policy import TtlPolicy

        auto_pause_policy: dict[str, Any] | None | Unset
        if isinstance(self.auto_pause_policy, Unset):
            auto_pause_policy = UNSET
        elif isinstance(self.auto_pause_policy, AutoPausePolicyType0) or isinstance(
            self.auto_pause_policy, AutoPausePolicyType1
        ):
            auto_pause_policy = self.auto_pause_policy.to_dict()
        else:
            auto_pause_policy = self.auto_pause_policy

        cpus: int | None | Unset
        if isinstance(self.cpus, Unset):
            cpus = UNSET
        else:
            cpus = self.cpus

        disk_size_gb: int | None | Unset
        if isinstance(self.disk_size_gb, Unset):
            disk_size_gb = UNSET
        else:
            disk_size_gb = self.disk_size_gb

        image: None | str | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        initial_secrets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.initial_secrets, Unset):
            initial_secrets = []
            for initial_secrets_item_data in self.initial_secrets:
                initial_secrets_item = initial_secrets_item_data.to_dict()
                initial_secrets.append(initial_secrets_item)

        initial_tags: dict[str, Any] | Unset = UNSET
        if not isinstance(self.initial_tags, Unset):
            initial_tags = self.initial_tags.to_dict()

        memory_mb: int | None | Unset
        if isinstance(self.memory_mb, Unset):
            memory_mb = UNSET
        else:
            memory_mb = self.memory_mb

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        nested_virt = self.nested_virt

        ports: list[int] | Unset = UNSET
        if not isinstance(self.ports, Unset):
            ports = self.ports

        team: None | str | Unset
        if isinstance(self.team, Unset):
            team = UNSET
        else:
            team = self.team

        ttl_policy: dict[str, Any] | None | Unset
        if isinstance(self.ttl_policy, Unset):
            ttl_policy = UNSET
        elif isinstance(self.ttl_policy, TtlPolicy):
            ttl_policy = self.ttl_policy.to_dict()
        else:
            ttl_policy = self.ttl_policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_pause_policy is not UNSET:
            field_dict["auto_pause_policy"] = auto_pause_policy
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if disk_size_gb is not UNSET:
            field_dict["disk_size_gb"] = disk_size_gb
        if image is not UNSET:
            field_dict["image"] = image
        if initial_secrets is not UNSET:
            field_dict["initial_secrets"] = initial_secrets
        if initial_tags is not UNSET:
            field_dict["initial_tags"] = initial_tags
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if name is not UNSET:
            field_dict["name"] = name
        if nested_virt is not UNSET:
            field_dict["nested_virt"] = nested_virt
        if ports is not UNSET:
            field_dict["ports"] = ports
        if team is not UNSET:
            field_dict["team"] = team
        if ttl_policy is not UNSET:
            field_dict["ttl_policy"] = ttl_policy

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )
        from ..models.auto_pause_policy_type_1 import (
            AutoPausePolicyType1,
        )
        from ..models.create_vm_request_initial_tags import (
            CreateVmRequestInitialTags,
        )
        from ..models.secret_spec import SecretSpec
        from ..models.ttl_policy import TtlPolicy

        d = dict(src_dict)

        def _parse_auto_pause_policy(
            data: object,
        ) -> AutoPausePolicyType0 | AutoPausePolicyType1 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_auto_pause_policy_type_0 = (
                    AutoPausePolicyType0.from_dict(data)
                )

                return componentsschemas_auto_pause_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_auto_pause_policy_type_1 = (
                    AutoPausePolicyType1.from_dict(data)
                )

                return componentsschemas_auto_pause_policy_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                AutoPausePolicyType0 | AutoPausePolicyType1 | None | Unset, data
            )

        auto_pause_policy = _parse_auto_pause_policy(d.pop("auto_pause_policy", UNSET))

        def _parse_cpus(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cpus = _parse_cpus(d.pop("cpus", UNSET))

        def _parse_disk_size_gb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        disk_size_gb = _parse_disk_size_gb(d.pop("disk_size_gb", UNSET))

        def _parse_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        _initial_secrets = d.pop("initial_secrets", UNSET)
        initial_secrets: list[SecretSpec] | Unset = UNSET
        if _initial_secrets is not UNSET:
            initial_secrets = []
            for initial_secrets_item_data in _initial_secrets:
                initial_secrets_item = SecretSpec.from_dict(initial_secrets_item_data)

                initial_secrets.append(initial_secrets_item)

        _initial_tags = d.pop("initial_tags", UNSET)
        initial_tags: CreateVmRequestInitialTags | Unset
        if isinstance(_initial_tags, Unset):
            initial_tags = UNSET
        else:
            initial_tags = CreateVmRequestInitialTags.from_dict(_initial_tags)

        def _parse_memory_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        nested_virt = d.pop("nested_virt", UNSET)

        ports = cast(list[int], d.pop("ports", UNSET))

        def _parse_team(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        team = _parse_team(d.pop("team", UNSET))

        def _parse_ttl_policy(data: object) -> None | TtlPolicy | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ttl_policy_type_1 = TtlPolicy.from_dict(data)

                return ttl_policy_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TtlPolicy | Unset, data)

        ttl_policy = _parse_ttl_policy(d.pop("ttl_policy", UNSET))

        create_vm_request = cls(
            auto_pause_policy=auto_pause_policy,
            cpus=cpus,
            disk_size_gb=disk_size_gb,
            image=image,
            initial_secrets=initial_secrets,
            initial_tags=initial_tags,
            memory_mb=memory_mb,
            name=name,
            nested_virt=nested_virt,
            ports=ports,
            team=team,
            ttl_policy=ttl_policy,
        )

        create_vm_request.additional_properties = d
        return create_vm_request

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
