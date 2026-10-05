from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="BroadcastLagEntry")


@_attrs_define
class BroadcastLagEntry:
    """One row of the admin payload: the (channel, consumer) label, the
    process-lifetime total dropped events, and the size of the most recent
    lag burst.

        Attributes:
            channel (str):
            consumer (str):
            last_skipped (int): `n` from the most recent `Lagged(n)` for this consumer.
            total_skipped (int): Process-lifetime total events dropped to this consumer (sum of every
                `Lagged(n).n`).
    """

    channel: str
    consumer: str
    last_skipped: int
    total_skipped: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel = self.channel

        consumer = self.consumer

        last_skipped = self.last_skipped

        total_skipped = self.total_skipped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel": channel,
                "consumer": consumer,
                "last_skipped": last_skipped,
                "total_skipped": total_skipped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        channel = d.pop("channel")

        consumer = d.pop("consumer")

        last_skipped = d.pop("last_skipped")

        total_skipped = d.pop("total_skipped")

        broadcast_lag_entry = cls(
            channel=channel,
            consumer=consumer,
            last_skipped=last_skipped,
            total_skipped=total_skipped,
        )

        broadcast_lag_entry.additional_properties = d
        return broadcast_lag_entry

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
