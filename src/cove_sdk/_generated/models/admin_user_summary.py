from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_quota import UserQuota


T = TypeVar("T", bound="AdminUserSummary")


@_attrs_define
class AdminUserSummary:
    """`GET /api/admin/users` list entry + `GET /api/admin/users/{username}` body.
    Mirrors `cove_service::ops::admin_vms::AdminUserSummary`
    field-for-field.

    Published as `AdminUserSummary` (the `Dto` suffix is a Rust-side
    artifact). This is the copy that gets `ToSchema`: the handler serializes
    THIS type, converting from the identically-named `cove_service` value via
    `user_to_wire` — see the NOTE on that duplicate.

        Attributes:
            created_at (str):
            last_seen_at (str):
            usage (UserQuota): Per-user quota usage + caps, four dimensions.

                Populated by `QuotaChecker::user_summary` (cove-service) for the profile
                page. v1 wire shape.

                The default value is "all zero" (no usage, no cap). Test fixtures, mock
                API impls, and `unwrap_or_else` fallbacks construct via `Default` to keep
                boilerplate down at the seven `ProfileSummary { … }` sites; the real
                values flow from cove-service.
            username (str):
            display_name (None | str | Unset):
    """

    created_at: str
    last_seen_at: str
    usage: UserQuota
    username: str
    display_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        last_seen_at = self.last_seen_at

        usage = self.usage.to_dict()

        username = self.username

        display_name: None | str | Unset
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "last_seen_at": last_seen_at,
                "usage": usage,
                "username": username,
            }
        )
        if display_name is not UNSET:
            field_dict["display_name"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.user_quota import UserQuota

        d = dict(src_dict)
        created_at = d.pop("created_at")

        last_seen_at = d.pop("last_seen_at")

        usage = UserQuota.from_dict(d.pop("usage"))

        username = d.pop("username")

        def _parse_display_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_name = _parse_display_name(d.pop("display_name", UNSET))

        admin_user_summary = cls(
            created_at=created_at,
            last_seen_at=last_seen_at,
            usage=usage,
            username=username,
            display_name=display_name,
        )

        admin_user_summary.additional_properties = d
        return admin_user_summary

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
