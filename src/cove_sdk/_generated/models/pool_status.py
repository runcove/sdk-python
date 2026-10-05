from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="PoolStatus")


@_attrs_define
class PoolStatus:
    """Pool entry within [`SystemStatusDto`].

    Attributes:
        count (int):
        image (str):
        consecutive_failures (int | Unset):
        degraded (bool | Unset): Refill circuit-breaker open for this image.
        retry_after_secs (int | None | Unset):
    """

    count: int
    image: str
    consecutive_failures: int | Unset = UNSET
    degraded: bool | Unset = UNSET
    retry_after_secs: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        image = self.image

        consecutive_failures = self.consecutive_failures

        degraded = self.degraded

        retry_after_secs: int | None | Unset
        if isinstance(self.retry_after_secs, Unset):
            retry_after_secs = UNSET
        else:
            retry_after_secs = self.retry_after_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "image": image,
            }
        )
        if consecutive_failures is not UNSET:
            field_dict["consecutive_failures"] = consecutive_failures
        if degraded is not UNSET:
            field_dict["degraded"] = degraded
        if retry_after_secs is not UNSET:
            field_dict["retry_after_secs"] = retry_after_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        count = d.pop("count")

        image = d.pop("image")

        consecutive_failures = d.pop("consecutive_failures", UNSET)

        degraded = d.pop("degraded", UNSET)

        def _parse_retry_after_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        retry_after_secs = _parse_retry_after_secs(d.pop("retry_after_secs", UNSET))

        pool_status = cls(
            count=count,
            image=image,
            consecutive_failures=consecutive_failures,
            degraded=degraded,
            retry_after_secs=retry_after_secs,
        )

        pool_status.additional_properties = d
        return pool_status

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
