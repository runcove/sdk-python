from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ReplayWebhookDeliveryResponse")


@_attrs_define
class ReplayWebhookDeliveryResponse:
    """Response of `POST /api/webhooks/{id}/deliveries/{delivery_id}/replay`
    (`handlers::webhook_deliveries::replay_delivery`). Not named in the
    outgoing hand-written spec (it was an inline object there) — named here
    per `crate::openapi`'s rule 3.

        Attributes:
            new_delivery_id (UUID): Freshly-minted id of the replayed delivery row. The replay keeps the
                original `ce_id` (so the receiver's idempotency key is stable) but gets
                its own `delivery_id`.
    """

    new_delivery_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_delivery_id = str(self.new_delivery_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_delivery_id": new_delivery_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        new_delivery_id = UUID(d.pop("new_delivery_id"))

        replay_webhook_delivery_response = cls(
            new_delivery_id=new_delivery_id,
        )

        replay_webhook_delivery_response.additional_properties = d
        return replay_webhook_delivery_response

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
