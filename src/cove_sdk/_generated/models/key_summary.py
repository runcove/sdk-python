from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="KeySummary")


@_attrs_define
class KeySummary:
    """`GET /api/keys` list item and `GET /api/keys/{id}` response body.

    Does not include `raw_token` — use `POST /api/keys` response (`CreatedKey`)
    to retrieve the token; it is only returned once at creation time.

    This is the ONE `KeySummary` that gets `ToSchema`. The
    server-side `cove_service::ops::keys::KeySummary` is a stale duplicate —
    `handlers::keys::list_keys` builds THIS type (aliased `WireSummary`)
    field-by-field from the service value before serializing; see the NOTE
    on that duplicate.

        Attributes:
            created_at (datetime.datetime):
            id (str):
            key_prefix (str): Display fingerprint (first 12 chars of token); safe for logs and UI lists.
            label (str):
            scopes (list[str]):
            status (str): `"active"` | `"expired"` | `"revoked"`.
            admin_key (bool | None | Unset): `true` = an admin key (`cove key create --admin`): the only kind of key
                that may hold `admin`/`admin:*`, and it must expire within
                `[auth] admin_max_key_lifetime_days`. Absent from older peers.
            bound_member (None | str | Unset): A member-bound service key's bound member.
            bound_team (None | str | Unset): A team key's team, or a team-bound service key's bound team (name).
            expires_at (datetime.datetime | None | Unset):
            last_used_at (datetime.datetime | None | Unset):
            service (None | str | Unset): A service key's principal, `svc:<name>`. Absent for any other key and
                from older peers.
            subject_type (None | str | Unset): What the key belongs to: `"user"` | `"team"` | `"service"`. Absent
                from older peers.
    """

    created_at: datetime.datetime
    id: str
    key_prefix: str
    label: str
    scopes: list[str]
    status: str
    admin_key: bool | None | Unset = UNSET
    bound_member: None | str | Unset = UNSET
    bound_team: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    last_used_at: datetime.datetime | None | Unset = UNSET
    service: None | str | Unset = UNSET
    subject_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        key_prefix = self.key_prefix

        label = self.label

        scopes = self.scopes

        status = self.status

        admin_key: bool | None | Unset
        if isinstance(self.admin_key, Unset):
            admin_key = UNSET
        else:
            admin_key = self.admin_key

        bound_member: None | str | Unset
        if isinstance(self.bound_member, Unset):
            bound_member = UNSET
        else:
            bound_member = self.bound_member

        bound_team: None | str | Unset
        if isinstance(self.bound_team, Unset):
            bound_team = UNSET
        else:
            bound_team = self.bound_team

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        service: None | str | Unset
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        subject_type: None | str | Unset
        if isinstance(self.subject_type, Unset):
            subject_type = UNSET
        else:
            subject_type = self.subject_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "key_prefix": key_prefix,
                "label": label,
                "scopes": scopes,
                "status": status,
            }
        )
        if admin_key is not UNSET:
            field_dict["admin_key"] = admin_key
        if bound_member is not UNSET:
            field_dict["bound_member"] = bound_member
        if bound_team is not UNSET:
            field_dict["bound_team"] = bound_team
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if service is not UNSET:
            field_dict["service"] = service
        if subject_type is not UNSET:
            field_dict["subject_type"] = subject_type

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        key_prefix = d.pop("key_prefix")

        label = d.pop("label")

        scopes = cast(list[str], d.pop("scopes"))

        status = d.pop("status")

        def _parse_admin_key(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        admin_key = _parse_admin_key(d.pop("admin_key", UNSET))

        def _parse_bound_member(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bound_member = _parse_bound_member(d.pop("bound_member", UNSET))

        def _parse_bound_team(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bound_team = _parse_bound_team(d.pop("bound_team", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        def _parse_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_subject_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subject_type = _parse_subject_type(d.pop("subject_type", UNSET))

        key_summary = cls(
            created_at=created_at,
            id=id,
            key_prefix=key_prefix,
            label=label,
            scopes=scopes,
            status=status,
            admin_key=admin_key,
            bound_member=bound_member,
            bound_team=bound_team,
            expires_at=expires_at,
            last_used_at=last_used_at,
            service=service,
            subject_type=subject_type,
        )

        key_summary.additional_properties = d
        return key_summary

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
