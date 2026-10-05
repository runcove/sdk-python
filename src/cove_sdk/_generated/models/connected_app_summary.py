from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.connected_app_access import ConnectedAppAccess
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectedAppSummary")


@_attrs_define
class ConnectedAppSummary:
    """`GET /api/me/connected-apps` item: one MCP client the caller signed in to
    Cove through (for example claude.ai), still live.

        Attributes:
            access (ConnectedAppAccess): The access level a user chose on the consent page.
            client_id (str): The client's metadata-document URL — its identity. Its host is what to
                show first: `client_name` is chosen by the client itself.
            client_name (str):
            created_at (datetime.datetime):
            expires_at (datetime.datetime): When the app lapses; signing in again creates a new one.
            id (str): The app id (`app_…`); the audit log's `actor_key_id` for its actions.
            last_used_at (datetime.datetime | None | Unset):
    """

    access: ConnectedAppAccess
    client_id: str
    client_name: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    id: str
    last_used_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access = self.access.value

        client_id = self.client_id

        client_name = self.client_name

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        id = self.id

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access": access,
                "client_id": client_id,
                "client_name": client_name,
                "created_at": created_at,
                "expires_at": expires_at,
                "id": id,
            }
        )
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        access = ConnectedAppAccess(d.pop("access"))

        client_id = d.pop("client_id")

        client_name = d.pop("client_name")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        id = d.pop("id")

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

        connected_app_summary = cls(
            access=access,
            client_id=client_id,
            client_name=client_name,
            created_at=created_at,
            expires_at=expires_at,
            id=id,
            last_used_at=last_used_at,
        )

        connected_app_summary.additional_properties = d
        return connected_app_summary

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
