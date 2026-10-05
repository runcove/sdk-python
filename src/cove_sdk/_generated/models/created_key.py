from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatedKey")


@_attrs_define
class CreatedKey:
    """`POST /api/keys` response body.

    Contains the raw token exactly once — it is never returned again.

    This is the ONE `CreatedKey` that gets `ToSchema`. The
    server-side `cove_service::ops::keys::CreatedKey` is a stale duplicate —
    `handlers::keys::create_key`/`rotate_key` build THIS type (aliased
    `WireCreated`) field-by-field from the service value before serializing;
    see the NOTE on that duplicate.

        Attributes:
            created_at (datetime.datetime):
            id (str):
            label (str):
            raw_token (str): Show-once raw token; never returned again after this response.
            scopes (list[str]):
            admin_key (bool | None | Unset): `true` = an admin key (`cove key create --admin`): the only kind of key
                that may hold `admin`/`admin:*`, and it must expire within
                `[auth] admin_max_key_lifetime_days`. Absent from older peers.
            expires_at (datetime.datetime | None | Unset):
    """

    created_at: datetime.datetime
    id: str
    label: str
    raw_token: str
    scopes: list[str]
    admin_key: bool | None | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        label = self.label

        raw_token = self.raw_token

        scopes = self.scopes

        admin_key: bool | None | Unset
        if isinstance(self.admin_key, Unset):
            admin_key = UNSET
        else:
            admin_key = self.admin_key

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "label": label,
                "raw_token": raw_token,
                "scopes": scopes,
            }
        )
        if admin_key is not UNSET:
            field_dict["admin_key"] = admin_key
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        id = d.pop("id")

        label = d.pop("label")

        raw_token = d.pop("raw_token")

        scopes = cast(list[str], d.pop("scopes"))

        def _parse_admin_key(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        admin_key = _parse_admin_key(d.pop("admin_key", UNSET))

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

        created_key = cls(
            created_at=created_at,
            id=id,
            label=label,
            raw_token=raw_token,
            scopes=scopes,
            admin_key=admin_key,
            expires_at=expires_at,
        )

        created_key.additional_properties = d
        return created_key

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
