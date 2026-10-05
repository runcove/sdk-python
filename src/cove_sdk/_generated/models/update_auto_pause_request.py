from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.auto_pause_policy_type_0 import AutoPausePolicyType0
    from ..models.auto_pause_policy_type_1 import AutoPausePolicyType1


T = TypeVar("T", bound="UpdateAutoPauseRequest")


@_attrs_define
class UpdateAutoPauseRequest:
    """POST /vms/{name}/auto-pause request body (was
    `/vms/{name}/suspend-policy`, and was named `UpdateSuspendPolicyRequest`).

        Attributes:
            policy (AutoPausePolicyType0 | AutoPausePolicyType1): What Cove does with a VM that has gone idle.

                `AutoPause` pauses the VM after `idle_timeout_secs` without traffic:
                scheduling stops, memory stays resident, and the VM resumes instantly on
                the next packet. `AlwaysOn` leaves it running.
    """

    policy: AutoPausePolicyType0 | AutoPausePolicyType1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )

        policy: dict[str, Any]
        if isinstance(self.policy, AutoPausePolicyType0):
            policy = self.policy.to_dict()
        else:
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
        from ..models.auto_pause_policy_type_0 import (
            AutoPausePolicyType0,
        )
        from ..models.auto_pause_policy_type_1 import (
            AutoPausePolicyType1,
        )

        d = dict(src_dict)

        def _parse_policy(data: object) -> AutoPausePolicyType0 | AutoPausePolicyType1:
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

        policy = _parse_policy(d.pop("policy"))

        update_auto_pause_request = cls(
            policy=policy,
        )

        update_auto_pause_request.additional_properties = d
        return update_auto_pause_request

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
