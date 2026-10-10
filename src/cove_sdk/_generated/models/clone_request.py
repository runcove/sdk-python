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
    from ..models.clone_request_tags_type_0 import CloneRequestTagsType0
    from ..models.ttl_policy import TtlPolicy


T = TypeVar("T", bound="CloneRequest")


@_attrs_define
class CloneRequest:
    """POST /vms/{source}/clone request body. The new VM's name is supplied by
    the caller; an optional `source_checkpoint_id` pins which checkpoint to
    reflink from. When omitted the service creates an implicit
    `pre_clone` checkpoint of the source first, then clones from it
    (the caller never has to take a checkpoint themselves).

    Mirrors `cove_service::api_types::CloneRequest`. The wire field name is
    `new_vm_name` (not `new_name`) to match the service mirror — drift here
    breaks the cross-crate roundtrip pinned by `unit_clone_request_*`.

        Attributes:
            new_vm_name (str): The clone's name, under the same rule as a created VM's: 3-30
                characters of lowercase ASCII letters, digits and hyphens, not starting
                or ending with a hyphen. Any other name is refused with 400
                `invalid_vm_name`.
            auto_pause_policy (AutoPausePolicyType0 | AutoPausePolicyType1 | None | Unset):
            source_checkpoint_id (None | str | Unset): Stringified UUID v7 of an existing checkpoint. Optional — when
                `None` the server creates an implicit `pre_clone` checkpoint of
                the source before cloning. The server parses the string into a
                `Uuid` and surfaces a 400 on bad syntax.
            tags (CloneRequestTagsType0 | None | Unset): Tags for the clone, replacing the source's. Omitted, the clone gets
                the source's tags; an empty object gives it none. Each entry obeys
                the same rules as setting a tag, and at most 50 are allowed; a bad
                one is refused with 400 before anything is cloned. A non-empty set
                needs `tags:write` as well as `vms:write` (403 `scope_denied`
                without it).
            ttl_policy (None | TtlPolicy | Unset):
    """

    new_vm_name: str
    auto_pause_policy: AutoPausePolicyType0 | AutoPausePolicyType1 | None | Unset = (
        UNSET
    )
    source_checkpoint_id: None | str | Unset = UNSET
    tags: CloneRequestTagsType0 | None | Unset = UNSET
    ttl_policy: None | TtlPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )
        from ..models.auto_pause_policy_type_1 import (
            AutoPausePolicyType1,
        )
        from ..models.clone_request_tags_type_0 import (
            CloneRequestTagsType0,
        )
        from ..models.ttl_policy import TtlPolicy

        new_vm_name = self.new_vm_name

        auto_pause_policy: dict[str, Any] | None | Unset
        if isinstance(self.auto_pause_policy, Unset):
            auto_pause_policy = UNSET
        elif isinstance(self.auto_pause_policy, AutoPausePolicyType0) or isinstance(
            self.auto_pause_policy, AutoPausePolicyType1
        ):
            auto_pause_policy = self.auto_pause_policy.to_dict()
        else:
            auto_pause_policy = self.auto_pause_policy

        source_checkpoint_id: None | str | Unset
        if isinstance(self.source_checkpoint_id, Unset):
            source_checkpoint_id = UNSET
        else:
            source_checkpoint_id = self.source_checkpoint_id

        tags: dict[str, Any] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, CloneRequestTagsType0):
            tags = self.tags.to_dict()
        else:
            tags = self.tags

        ttl_policy: dict[str, Any] | None | Unset
        if isinstance(self.ttl_policy, Unset):
            ttl_policy = UNSET
        elif isinstance(self.ttl_policy, TtlPolicy):
            ttl_policy = self.ttl_policy.to_dict()
        else:
            ttl_policy = self.ttl_policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_vm_name": new_vm_name,
            }
        )
        if auto_pause_policy is not UNSET:
            field_dict["auto_pause_policy"] = auto_pause_policy
        if source_checkpoint_id is not UNSET:
            field_dict["source_checkpoint_id"] = source_checkpoint_id
        if tags is not UNSET:
            field_dict["tags"] = tags
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
        from ..models.clone_request_tags_type_0 import (
            CloneRequestTagsType0,
        )
        from ..models.ttl_policy import TtlPolicy

        d = dict(src_dict)
        new_vm_name = d.pop("new_vm_name")

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

        def _parse_source_checkpoint_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_checkpoint_id = _parse_source_checkpoint_id(
            d.pop("source_checkpoint_id", UNSET)
        )

        def _parse_tags(data: object) -> CloneRequestTagsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tags_type_0 = CloneRequestTagsType0.from_dict(data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CloneRequestTagsType0 | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

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

        clone_request = cls(
            new_vm_name=new_vm_name,
            auto_pause_policy=auto_pause_policy,
            source_checkpoint_id=source_checkpoint_id,
            tags=tags,
            ttl_policy=ttl_policy,
        )

        clone_request.additional_properties = d
        return clone_request

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
