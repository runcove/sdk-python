from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditEntry")


@_attrs_define
class AuditEntry:
    """A single persisted audit log entry, as returned by the query API.

    Attributes:
        actor_kind (str):
        at (datetime.datetime):
        event_kind (str):
        event_payload (Any):
        id (int):
        actor_key_id (None | str | Unset):
        actor_reason (None | str | Unset):
        actor_source (None | str | Unset):
        actor_username (None | str | Unset):
        request_id (None | str | Unset):
        source_ip (None | str | Unset):
        sudo_auth_at (None | str | Unset): Sudo mode — the `created_at` of the CLI ticket mint that
            satisfied the sudo window (ISO8601 UTC string). `None` unless
            `sudo_satisfied` is `Some(true)`. Mirrors
            [`AuditContext::sudo_auth_at`] on the write side.
        sudo_satisfied (bool | None | Unset): Sudo mode — whether the caller's sudo window was satisfied at
            the gate for this sensitive op. `None` for non-sensitive ops and
            callers the gate did not evaluate (bearer/API-key callers are exempt;
            core-originated events carry no request scope). Mirrors
            [`AuditContext::sudo_satisfied`] on the write side.

            `#[serde(default)]` so a legacy daemon that omits the column (pre-migration
            018) deserializes to `None`.
        vm_id (None | str | Unset):
        vm_name (None | str | Unset):
    """

    actor_kind: str
    at: datetime.datetime
    event_kind: str
    event_payload: Any
    id: int
    actor_key_id: None | str | Unset = UNSET
    actor_reason: None | str | Unset = UNSET
    actor_source: None | str | Unset = UNSET
    actor_username: None | str | Unset = UNSET
    request_id: None | str | Unset = UNSET
    source_ip: None | str | Unset = UNSET
    sudo_auth_at: None | str | Unset = UNSET
    sudo_satisfied: bool | None | Unset = UNSET
    vm_id: None | str | Unset = UNSET
    vm_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actor_kind = self.actor_kind

        at = self.at.isoformat()

        event_kind = self.event_kind

        event_payload = self.event_payload

        id = self.id

        actor_key_id: None | str | Unset
        if isinstance(self.actor_key_id, Unset):
            actor_key_id = UNSET
        else:
            actor_key_id = self.actor_key_id

        actor_reason: None | str | Unset
        if isinstance(self.actor_reason, Unset):
            actor_reason = UNSET
        else:
            actor_reason = self.actor_reason

        actor_source: None | str | Unset
        if isinstance(self.actor_source, Unset):
            actor_source = UNSET
        else:
            actor_source = self.actor_source

        actor_username: None | str | Unset
        if isinstance(self.actor_username, Unset):
            actor_username = UNSET
        else:
            actor_username = self.actor_username

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        source_ip: None | str | Unset
        if isinstance(self.source_ip, Unset):
            source_ip = UNSET
        else:
            source_ip = self.source_ip

        sudo_auth_at: None | str | Unset
        if isinstance(self.sudo_auth_at, Unset):
            sudo_auth_at = UNSET
        else:
            sudo_auth_at = self.sudo_auth_at

        sudo_satisfied: bool | None | Unset
        if isinstance(self.sudo_satisfied, Unset):
            sudo_satisfied = UNSET
        else:
            sudo_satisfied = self.sudo_satisfied

        vm_id: None | str | Unset
        if isinstance(self.vm_id, Unset):
            vm_id = UNSET
        else:
            vm_id = self.vm_id

        vm_name: None | str | Unset
        if isinstance(self.vm_name, Unset):
            vm_name = UNSET
        else:
            vm_name = self.vm_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actor_kind": actor_kind,
                "at": at,
                "event_kind": event_kind,
                "event_payload": event_payload,
                "id": id,
            }
        )
        if actor_key_id is not UNSET:
            field_dict["actor_key_id"] = actor_key_id
        if actor_reason is not UNSET:
            field_dict["actor_reason"] = actor_reason
        if actor_source is not UNSET:
            field_dict["actor_source"] = actor_source
        if actor_username is not UNSET:
            field_dict["actor_username"] = actor_username
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if source_ip is not UNSET:
            field_dict["source_ip"] = source_ip
        if sudo_auth_at is not UNSET:
            field_dict["sudo_auth_at"] = sudo_auth_at
        if sudo_satisfied is not UNSET:
            field_dict["sudo_satisfied"] = sudo_satisfied
        if vm_id is not UNSET:
            field_dict["vm_id"] = vm_id
        if vm_name is not UNSET:
            field_dict["vm_name"] = vm_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        actor_kind = d.pop("actor_kind")

        at = datetime.datetime.fromisoformat(d.pop("at"))

        event_kind = d.pop("event_kind")

        event_payload = d.pop("event_payload")

        id = d.pop("id")

        def _parse_actor_key_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor_key_id = _parse_actor_key_id(d.pop("actor_key_id", UNSET))

        def _parse_actor_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor_reason = _parse_actor_reason(d.pop("actor_reason", UNSET))

        def _parse_actor_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor_source = _parse_actor_source(d.pop("actor_source", UNSET))

        def _parse_actor_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor_username = _parse_actor_username(d.pop("actor_username", UNSET))

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        def _parse_source_ip(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_ip = _parse_source_ip(d.pop("source_ip", UNSET))

        def _parse_sudo_auth_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sudo_auth_at = _parse_sudo_auth_at(d.pop("sudo_auth_at", UNSET))

        def _parse_sudo_satisfied(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        sudo_satisfied = _parse_sudo_satisfied(d.pop("sudo_satisfied", UNSET))

        def _parse_vm_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vm_id = _parse_vm_id(d.pop("vm_id", UNSET))

        def _parse_vm_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vm_name = _parse_vm_name(d.pop("vm_name", UNSET))

        audit_entry = cls(
            actor_kind=actor_kind,
            at=at,
            event_kind=event_kind,
            event_payload=event_payload,
            id=id,
            actor_key_id=actor_key_id,
            actor_reason=actor_reason,
            actor_source=actor_source,
            actor_username=actor_username,
            request_id=request_id,
            source_ip=source_ip,
            sudo_auth_at=sudo_auth_at,
            sudo_satisfied=sudo_satisfied,
            vm_id=vm_id,
            vm_name=vm_name,
        )

        audit_entry.additional_properties = d
        return audit_entry

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
