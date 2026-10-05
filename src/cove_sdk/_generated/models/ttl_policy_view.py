from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ttl_policy import TtlPolicy


T = TypeVar("T", bound="TtlPolicyView")


@_attrs_define
class TtlPolicyView:
    """TTL policy + computed countdowns for a VM (a `GET /vms/{name}` sub-view).

    Attributes:
        policy (TtlPolicy): Per-VM TTL policy bundle. Both knobs default to "off" (`Never` / `None`);
            pool defaults and CLI flags merge into this on create.
        deletes_in_secs (int | None | Unset): Seconds until the delete-after-stop grace expires; `None` if not
            stopped or the knob is `Never`. May go briefly negative under clock skew.
        max_life_expires_in_secs (int | None | Unset): Seconds until the `max_lifetime_secs` cap expires; `None` if
            disabled.
    """

    policy: TtlPolicy
    deletes_in_secs: int | None | Unset = UNSET
    max_life_expires_in_secs: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy = self.policy.to_dict()

        deletes_in_secs: int | None | Unset
        if isinstance(self.deletes_in_secs, Unset):
            deletes_in_secs = UNSET
        else:
            deletes_in_secs = self.deletes_in_secs

        max_life_expires_in_secs: int | None | Unset
        if isinstance(self.max_life_expires_in_secs, Unset):
            max_life_expires_in_secs = UNSET
        else:
            max_life_expires_in_secs = self.max_life_expires_in_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy": policy,
            }
        )
        if deletes_in_secs is not UNSET:
            field_dict["deletes_in_secs"] = deletes_in_secs
        if max_life_expires_in_secs is not UNSET:
            field_dict["max_life_expires_in_secs"] = max_life_expires_in_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ttl_policy import TtlPolicy

        d = dict(src_dict)
        policy = TtlPolicy.from_dict(d.pop("policy"))

        def _parse_deletes_in_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        deletes_in_secs = _parse_deletes_in_secs(d.pop("deletes_in_secs", UNSET))

        def _parse_max_life_expires_in_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_life_expires_in_secs = _parse_max_life_expires_in_secs(
            d.pop("max_life_expires_in_secs", UNSET)
        )

        ttl_policy_view = cls(
            policy=policy,
            deletes_in_secs=deletes_in_secs,
            max_life_expires_in_secs=max_life_expires_in_secs,
        )

        ttl_policy_view.additional_properties = d
        return ttl_policy_view

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
