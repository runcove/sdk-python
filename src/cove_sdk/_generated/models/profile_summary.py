from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_permissions_type_0 import SelfPermissionsType0
    from ..models.self_permissions_type_1 import SelfPermissionsType1
    from ..models.team_quota import TeamQuota
    from ..models.user_quota import UserQuota


T = TypeVar("T", bound="ProfileSummary")


@_attrs_define
class ProfileSummary:
    """Summary of the signed-in user's identity and capability flags.

    `quota` carries the user's current/max usage across the four quota
    dimensions (vCPU / RAM / VM count / disk). Backends that don't yet wire
    the QuotaChecker (mock APIs, `unwrap_or_else` fallback paths) construct
    via `UserQuota::default()` — all-zero, semantically "no data, no cap".

        Attributes:
            active_cli_ticket_count (int):
            key_count (int):
            keys_managed (bool):
            ldap_linked (bool):
            roles (list[str]):
            username (str):
            is_admin (bool | None | Unset): The server's admin checks' answer (`auth::is_admin`): `true` for a
                session of a user listed in `[auth] admins`, or for an admin key
                (`--admin`) of one; an admin's ordinary key, or one minted before admin
                keys existed, reads `false`. A key also needs the route's `admin:*` permission in
                `permissions.scopes`, so `true` alone does not mean an admin route
                admits it. Absent from older servers.
            permissions (None | SelfPermissionsType0 | SelfPermissionsType1 | Unset):
            quota (UserQuota | Unset): Per-user quota usage + caps, four dimensions.

                Populated by `QuotaChecker::user_summary` (cove-service) for the profile
                page. v1 wire shape.

                The default value is "all zero" (no usage, no cap). Test fixtures, mock
                API impls, and `unwrap_or_else` fallbacks construct via `Default` to keep
                boilerplate down at the seven `ProfileSummary { … }` sites; the real
                values flow from cove-service.
            team_quotas (list[TeamQuota] | Unset): Quota envelopes for every team the caller has a
                team-attributed VM under (NOT full team membership — see
                `CoveService::team_quotas_for_user`). Empty for users with no
                team-attributed VMs. `#[serde(default)]` so older clients
                deserializing an old cached response don't fail.
            user_id (None | str | Unset):
    """

    active_cli_ticket_count: int
    key_count: int
    keys_managed: bool
    ldap_linked: bool
    roles: list[str]
    username: str
    is_admin: bool | None | Unset = UNSET
    permissions: None | SelfPermissionsType0 | SelfPermissionsType1 | Unset = UNSET
    quota: UserQuota | Unset = UNSET
    team_quotas: list[TeamQuota] | Unset = UNSET
    user_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.self_permissions_type_0 import (
            SelfPermissionsType0,
        )
        from ..models.self_permissions_type_1 import (
            SelfPermissionsType1,
        )

        active_cli_ticket_count = self.active_cli_ticket_count

        key_count = self.key_count

        keys_managed = self.keys_managed

        ldap_linked = self.ldap_linked

        roles = self.roles

        username = self.username

        is_admin: bool | None | Unset
        if isinstance(self.is_admin, Unset):
            is_admin = UNSET
        else:
            is_admin = self.is_admin

        permissions: dict[str, Any] | None | Unset
        if isinstance(self.permissions, Unset):
            permissions = UNSET
        elif isinstance(self.permissions, SelfPermissionsType0) or isinstance(
            self.permissions, SelfPermissionsType1
        ):
            permissions = self.permissions.to_dict()
        else:
            permissions = self.permissions

        quota: dict[str, Any] | Unset = UNSET
        if not isinstance(self.quota, Unset):
            quota = self.quota.to_dict()

        team_quotas: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.team_quotas, Unset):
            team_quotas = []
            for team_quotas_item_data in self.team_quotas:
                team_quotas_item = team_quotas_item_data.to_dict()
                team_quotas.append(team_quotas_item)

        user_id: None | str | Unset
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_cli_ticket_count": active_cli_ticket_count,
                "key_count": key_count,
                "keys_managed": keys_managed,
                "ldap_linked": ldap_linked,
                "roles": roles,
                "username": username,
            }
        )
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if quota is not UNSET:
            field_dict["quota"] = quota
        if team_quotas is not UNSET:
            field_dict["team_quotas"] = team_quotas
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.self_permissions_type_0 import (
            SelfPermissionsType0,
        )
        from ..models.self_permissions_type_1 import (
            SelfPermissionsType1,
        )
        from ..models.team_quota import TeamQuota
        from ..models.user_quota import UserQuota

        d = dict(src_dict)
        active_cli_ticket_count = d.pop("active_cli_ticket_count")

        key_count = d.pop("key_count")

        keys_managed = d.pop("keys_managed")

        ldap_linked = d.pop("ldap_linked")

        roles = cast(list[str], d.pop("roles"))

        username = d.pop("username")

        def _parse_is_admin(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_admin = _parse_is_admin(d.pop("is_admin", UNSET))

        def _parse_permissions(
            data: object,
        ) -> None | SelfPermissionsType0 | SelfPermissionsType1 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_self_permissions_type_0 = (
                    SelfPermissionsType0.from_dict(data)
                )

                return componentsschemas_self_permissions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_self_permissions_type_1 = (
                    SelfPermissionsType1.from_dict(data)
                )

                return componentsschemas_self_permissions_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None | SelfPermissionsType0 | SelfPermissionsType1 | Unset, data
            )

        permissions = _parse_permissions(d.pop("permissions", UNSET))

        _quota = d.pop("quota", UNSET)
        quota: UserQuota | Unset
        if isinstance(_quota, Unset):
            quota = UNSET
        else:
            quota = UserQuota.from_dict(_quota)

        _team_quotas = d.pop("team_quotas", UNSET)
        team_quotas: list[TeamQuota] | Unset = UNSET
        if _team_quotas is not UNSET:
            team_quotas = []
            for team_quotas_item_data in _team_quotas:
                team_quotas_item = TeamQuota.from_dict(team_quotas_item_data)

                team_quotas.append(team_quotas_item)

        def _parse_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        profile_summary = cls(
            active_cli_ticket_count=active_cli_ticket_count,
            key_count=key_count,
            keys_managed=keys_managed,
            ldap_linked=ldap_linked,
            roles=roles,
            username=username,
            is_admin=is_admin,
            permissions=permissions,
            quota=quota,
            team_quotas=team_quotas,
            user_id=user_id,
        )

        profile_summary.additional_properties = d
        return profile_summary

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
