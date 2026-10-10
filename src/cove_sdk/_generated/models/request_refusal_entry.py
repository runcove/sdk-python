from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RequestRefusalEntry")


@_attrs_define
class RequestRefusalEntry:
    """One row of host-state `request_refusals`: how many requests the external
    listener refused on one route group for one reason, this daemon process.

        Attributes:
            reason (str): `address_denied` (403, the group's `allow`/`deny` list),
                `rate_limited_address` (429, the address's budget) or
                `rate_limited_credential` (429, the credential's budget).
            route_group (str): `mcp`, `oauth_token`, `oauth` or `api`.
            total (int): Refusals this process.
    """

    reason: str
    route_group: str
    total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        route_group = self.route_group

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
                "route_group": route_group,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        reason = d.pop("reason")

        route_group = d.pop("route_group")

        total = d.pop("total")

        request_refusal_entry = cls(
            reason=reason,
            route_group=route_group,
            total=total,
        )

        request_refusal_entry.additional_properties = d
        return request_refusal_entry

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
