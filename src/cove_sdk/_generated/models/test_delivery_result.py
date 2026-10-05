from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDeliveryResult")


@_attrs_define
class TestDeliveryResult:
    """Result of POST /api/webhooks/{id}/test (synchronous test delivery).

    `state` is `"delivered"` for a 2xx receiver response and `"failed"` for
    every other response or outbound error. Test deliveries are one-shot: their
    minted `delivery_id` is never persisted to the durable outbox, and they do
    not update subscription retry or health state.

        Attributes:
            delivery_id (UUID):
            sig_header (str): Signature header that would be sent if the worker delivered this event.
            state (str): `"delivered" | "failed"` — see struct doc.
            latency_ms (int | None | Unset): Measured outbound latency for the one-shot delivery.
            note (None | str | Unset): Free-form delivery failure classification, absent on a successful response.
            status (int | None | Unset): Receiver HTTP status, if a response was received.
    """

    delivery_id: UUID
    sig_header: str
    state: str
    latency_ms: int | None | Unset = UNSET
    note: None | str | Unset = UNSET
    status: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delivery_id = str(self.delivery_id)

        sig_header = self.sig_header

        state = self.state

        latency_ms: int | None | Unset
        if isinstance(self.latency_ms, Unset):
            latency_ms = UNSET
        else:
            latency_ms = self.latency_ms

        note: None | str | Unset
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        status: int | None | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delivery_id": delivery_id,
                "sig_header": sig_header,
                "state": state,
            }
        )
        if latency_ms is not UNSET:
            field_dict["latency_ms"] = latency_ms
        if note is not UNSET:
            field_dict["note"] = note
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        delivery_id = UUID(d.pop("delivery_id"))

        sig_header = d.pop("sig_header")

        state = d.pop("state")

        def _parse_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms", UNSET))

        def _parse_note(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_status(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        test_delivery_result = cls(
            delivery_id=delivery_id,
            sig_header=sig_header,
            state=state,
            latency_ms=latency_ms,
            note=note,
            status=status,
        )

        test_delivery_result.additional_properties = d
        return test_delivery_result

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
