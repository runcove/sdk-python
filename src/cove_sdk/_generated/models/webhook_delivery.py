from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.delivery_state import DeliveryState
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookDelivery")


@_attrs_define
class WebhookDelivery:
    """Wire shape of a delivery row, as hand-built by
    `handlers::webhook_deliveries::delivery_to_json` from a [`Delivery`] —
    everything that struct has except `event_payload` (see its doc comment).

        Attributes:
            attempt (int):
            ce_id (UUID): Event identity (UUID v7). Preserved across replays — sent as `ce-id` header.
            ce_time (str): ISO-8601 wall-clock of the original event; immutable across retries.
            created_at (datetime.datetime):
            delivery_id (UUID): Internal row identity (UUID v7). Fresh UUID on every replay.
            event_kind (str):
            retry_at (int): Unix timestamp (seconds) when the next attempt is due.
            state (DeliveryState): Delivery state as stored in `webhook_outbox.state`.
            subscription_id (UUID):
            claimed_at (int | None | Unset):
            delivered_at (datetime.datetime | None | Unset):
            last_error (None | str | Unset):
            last_status (int | None | Unset):
            replayed_from (None | Unset | UUID): `delivery_id` of the row this is a replay of; `None` for a first delivery.
            vm_id (None | Unset | UUID):
    """

    attempt: int
    ce_id: UUID
    ce_time: str
    created_at: datetime.datetime
    delivery_id: UUID
    event_kind: str
    retry_at: int
    state: DeliveryState
    subscription_id: UUID
    claimed_at: int | None | Unset = UNSET
    delivered_at: datetime.datetime | None | Unset = UNSET
    last_error: None | str | Unset = UNSET
    last_status: int | None | Unset = UNSET
    replayed_from: None | Unset | UUID = UNSET
    vm_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        ce_id = str(self.ce_id)

        ce_time = self.ce_time

        created_at = self.created_at.isoformat()

        delivery_id = str(self.delivery_id)

        event_kind = self.event_kind

        retry_at = self.retry_at

        state = self.state.value

        subscription_id = str(self.subscription_id)

        claimed_at: int | None | Unset
        if isinstance(self.claimed_at, Unset):
            claimed_at = UNSET
        else:
            claimed_at = self.claimed_at

        delivered_at: None | str | Unset
        if isinstance(self.delivered_at, Unset):
            delivered_at = UNSET
        elif isinstance(self.delivered_at, datetime.datetime):
            delivered_at = self.delivered_at.isoformat()
        else:
            delivered_at = self.delivered_at

        last_error: None | str | Unset
        if isinstance(self.last_error, Unset):
            last_error = UNSET
        else:
            last_error = self.last_error

        last_status: int | None | Unset
        if isinstance(self.last_status, Unset):
            last_status = UNSET
        else:
            last_status = self.last_status

        replayed_from: None | str | Unset
        if isinstance(self.replayed_from, Unset):
            replayed_from = UNSET
        elif isinstance(self.replayed_from, UUID):
            replayed_from = str(self.replayed_from)
        else:
            replayed_from = self.replayed_from

        vm_id: None | str | Unset
        if isinstance(self.vm_id, Unset):
            vm_id = UNSET
        elif isinstance(self.vm_id, UUID):
            vm_id = str(self.vm_id)
        else:
            vm_id = self.vm_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempt": attempt,
                "ce_id": ce_id,
                "ce_time": ce_time,
                "created_at": created_at,
                "delivery_id": delivery_id,
                "event_kind": event_kind,
                "retry_at": retry_at,
                "state": state,
                "subscription_id": subscription_id,
            }
        )
        if claimed_at is not UNSET:
            field_dict["claimed_at"] = claimed_at
        if delivered_at is not UNSET:
            field_dict["delivered_at"] = delivered_at
        if last_error is not UNSET:
            field_dict["last_error"] = last_error
        if last_status is not UNSET:
            field_dict["last_status"] = last_status
        if replayed_from is not UNSET:
            field_dict["replayed_from"] = replayed_from
        if vm_id is not UNSET:
            field_dict["vm_id"] = vm_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        attempt = d.pop("attempt")

        ce_id = UUID(d.pop("ce_id"))

        ce_time = d.pop("ce_time")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        delivery_id = UUID(d.pop("delivery_id"))

        event_kind = d.pop("event_kind")

        retry_at = d.pop("retry_at")

        state = DeliveryState(d.pop("state"))

        subscription_id = UUID(d.pop("subscription_id"))

        def _parse_claimed_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        claimed_at = _parse_claimed_at(d.pop("claimed_at", UNSET))

        def _parse_delivered_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                delivered_at_type_0 = datetime.datetime.fromisoformat(data)

                return delivered_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        delivered_at = _parse_delivered_at(d.pop("delivered_at", UNSET))

        def _parse_last_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_error = _parse_last_error(d.pop("last_error", UNSET))

        def _parse_last_status(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        last_status = _parse_last_status(d.pop("last_status", UNSET))

        def _parse_replayed_from(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                replayed_from_type_0 = UUID(data)

                return replayed_from_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        replayed_from = _parse_replayed_from(d.pop("replayed_from", UNSET))

        def _parse_vm_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                vm_id_type_0 = UUID(data)

                return vm_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        vm_id = _parse_vm_id(d.pop("vm_id", UNSET))

        webhook_delivery = cls(
            attempt=attempt,
            ce_id=ce_id,
            ce_time=ce_time,
            created_at=created_at,
            delivery_id=delivery_id,
            event_kind=event_kind,
            retry_at=retry_at,
            state=state,
            subscription_id=subscription_id,
            claimed_at=claimed_at,
            delivered_at=delivered_at,
            last_error=last_error,
            last_status=last_status,
            replayed_from=replayed_from,
            vm_id=vm_id,
        )

        webhook_delivery.additional_properties = d
        return webhook_delivery

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
