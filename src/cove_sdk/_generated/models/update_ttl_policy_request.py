from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.expires_in import ExpiresIn
    from ..models.ttl_policy import TtlPolicy


T = TypeVar("T", bound="UpdateTtlPolicyRequest")


@_attrs_define
class UpdateTtlPolicyRequest:
    """POST /vms/{name}/expiry request body. Carries exactly one of `policy`
    (replace the whole policy) and `expires_in` (set only the expiry, counted
    from now). A server older than `expires_in` refuses a body without
    `policy` rather than misreading it.

        Attributes:
            expires_in (ExpiresIn | None | Unset):
            policy (None | TtlPolicy | Unset):
    """

    expires_in: ExpiresIn | None | Unset = UNSET
    policy: None | TtlPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.expires_in import ExpiresIn
        from ..models.ttl_policy import TtlPolicy

        expires_in: dict[str, Any] | None | Unset
        if isinstance(self.expires_in, Unset):
            expires_in = UNSET
        elif isinstance(self.expires_in, ExpiresIn):
            expires_in = self.expires_in.to_dict()
        else:
            expires_in = self.expires_in

        policy: dict[str, Any] | None | Unset
        if isinstance(self.policy, Unset):
            policy = UNSET
        elif isinstance(self.policy, TtlPolicy):
            policy = self.policy.to_dict()
        else:
            policy = self.policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.expires_in import ExpiresIn
        from ..models.ttl_policy import TtlPolicy

        d = dict(src_dict)

        def _parse_expires_in(data: object) -> ExpiresIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                expires_in_type_1 = ExpiresIn.from_dict(data)

                return expires_in_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExpiresIn | None | Unset, data)

        expires_in = _parse_expires_in(d.pop("expires_in", UNSET))

        def _parse_policy(data: object) -> None | TtlPolicy | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                policy_type_1 = TtlPolicy.from_dict(data)

                return policy_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TtlPolicy | Unset, data)

        policy = _parse_policy(d.pop("policy", UNSET))

        update_ttl_policy_request = cls(
            expires_in=expires_in,
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
