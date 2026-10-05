from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateKeyRequest")


@_attrs_define
class CreateKeyRequest:
    """`POST /api/keys` request body.

    This is the ONE `CreateKeyRequest` that gets `ToSchema`. The
    server-side `cove_service::ops::keys::CreateKeyRequest` is a stale
    duplicate — `handlers::keys::create_key` deserializes THIS type (aliased
    `WireCKR`) and converts it to the service type itself; see the NOTE on
    that duplicate.

        Attributes:
            label (str):
            admin_key (bool | None | Unset): `true` = an admin key (`cove key create --admin`): the only kind of key
                that may hold `admin`/`admin:*`, and it must expire within
                `[auth] admin_max_key_lifetime_days`. Only an administrator on a
                signed-in session may set it: any API key caller, admin key or not,
                gets 403 (an admin key can still mint ordinary keys). Absent from
                older peers.
            expires_in_secs (int | None | Unset): Omit (or send `null`) for a key that never expires (subject to the
                `cove.toml` `[auth]` `max_key_lifetime_days` cap). From an API key
                that expires, omitting it gives the new key the calling key's own
                expiry, and a longer one is refused (422).
            member (None | str | Unset): With `service`: bind the key to this one member (its VMs are charged
                to and controlled by them). Refused without `service`.
            scopes (list[str] | None | Unset): Omit (or send `null`) for the default set (`vms:read`, `vms:write`,
                `vms:exec`, `files:read`, `files:write`, `checkpoints:write`,
                `tags:read`, `tags:write`). An empty
                array is refused (422).
            service (None | str | Unset): Set to `<name>` to mint a service key `svc:<name>` (admin only; expiry
                required; never `keys:manage`, `access:write`, `admin` or `admin:*`). Exactly one of
                `team` or `member` must then name its binding. Absent from older peers.
            team (None | str | Unset): Set to a team name to mint a team-subject key, gated on
                team-manage (admin in v1) and requiring an expiry. Omit for a personal
                key.
    """

    label: str
    admin_key: bool | None | Unset = UNSET
    expires_in_secs: int | None | Unset = UNSET
    member: None | str | Unset = UNSET
    scopes: list[str] | None | Unset = UNSET
    service: None | str | Unset = UNSET
    team: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        admin_key: bool | None | Unset
        if isinstance(self.admin_key, Unset):
            admin_key = UNSET
        else:
            admin_key = self.admin_key

        expires_in_secs: int | None | Unset
        if isinstance(self.expires_in_secs, Unset):
            expires_in_secs = UNSET
        else:
            expires_in_secs = self.expires_in_secs

        member: None | str | Unset
        if isinstance(self.member, Unset):
            member = UNSET
        else:
            member = self.member

        scopes: list[str] | None | Unset
        if isinstance(self.scopes, Unset):
            scopes = UNSET
        elif isinstance(self.scopes, list):
            scopes = self.scopes

        else:
            scopes = self.scopes

        service: None | str | Unset
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        team: None | str | Unset
        if isinstance(self.team, Unset):
            team = UNSET
        else:
            team = self.team

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
            }
        )
        if admin_key is not UNSET:
            field_dict["admin_key"] = admin_key
        if expires_in_secs is not UNSET:
            field_dict["expires_in_secs"] = expires_in_secs
        if member is not UNSET:
            field_dict["member"] = member
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if service is not UNSET:
            field_dict["service"] = service
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        label = d.pop("label")

        def _parse_admin_key(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        admin_key = _parse_admin_key(d.pop("admin_key", UNSET))

        def _parse_expires_in_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        expires_in_secs = _parse_expires_in_secs(d.pop("expires_in_secs", UNSET))

        def _parse_member(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        member = _parse_member(d.pop("member", UNSET))

        def _parse_scopes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scopes_type_0 = cast(list[str], data)

                return scopes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        scopes = _parse_scopes(d.pop("scopes", UNSET))

        def _parse_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_team(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        team = _parse_team(d.pop("team", UNSET))

        create_key_request = cls(
            label=label,
            admin_key=admin_key,
            expires_in_secs=expires_in_secs,
            member=member,
            scopes=scopes,
            service=service,
            team=team,
        )

        create_key_request.additional_properties = d
        return create_key_request

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
