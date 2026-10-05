from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.webhook_delivery import WebhookDelivery


T = TypeVar("T", bound="WebhookDeliveryPage")


@_attrs_define
class WebhookDeliveryPage:
    """Page of [`WebhookDelivery`] rows with an opaque cursor for the next page.
    Returned by `GET /api/webhooks/{id}/deliveries`
    (`handlers::webhook_deliveries::list_deliveries`).

        Attributes:
            deliveries (list[WebhookDelivery]):
            next_cursor (None | str): Opaque pagination cursor. `null` once the last page has been returned —
                always present, never omitted (`crate`-wide page convention, see
                `cove_types::page`). When set, also echoed in a
                `Link: <...>; rel="next"` response header.
    """

    deliveries: list[WebhookDelivery]
    next_cursor: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deliveries = []
        for deliveries_item_data in self.deliveries:
            deliveries_item = deliveries_item_data.to_dict()
            deliveries.append(deliveries_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deliveries": deliveries,
                "next_cursor": next_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.webhook_delivery import WebhookDelivery

        d = dict(src_dict)
        deliveries = []
        _deliveries = d.pop("deliveries")
        for deliveries_item_data in _deliveries:
            deliveries_item = WebhookDelivery.from_dict(deliveries_item_data)

            deliveries.append(deliveries_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        webhook_delivery_page = cls(
            deliveries=deliveries,
            next_cursor=next_cursor,
        )

        webhook_delivery_page.additional_properties = d
        return webhook_delivery_page

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
