from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.ttl_policy import TtlPolicy


T = TypeVar("T", bound="UpdateTtlPolicyRequest")


@_attrs_define
class UpdateTtlPolicyRequest:
    """POST /vms/{name}/ttl-policy request body.

    Attributes:
        policy (TtlPolicy): Per-VM TTL policy bundle. Both knobs default to "off" (`Never` / `None`);
            pool defaults and CLI flags merge into this on create.
    """

    policy: TtlPolicy
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy = self.policy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy": policy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ttl_policy import TtlPolicy

        d = dict(src_dict)
        policy = TtlPolicy.from_dict(d.pop("policy"))

        update_ttl_policy_request = cls(
            policy=policy,
        )

        update_ttl_policy_request.additional_properties = d
        return update_ttl_policy_request

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
