from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransferProgress")


@_attrs_define
class TransferProgress:
    """How far a long creation stage has got, in bytes. Sent again about once a
    second while the stage runs.

        Attributes:
            done (int): Bytes done so far.
            bytes_per_sec (int | None | Unset): The recent rate, once there is one to measure.
            secs_left (int | None | Unset): Seconds left at that rate, when both the total and the rate are known.
            stalled_secs (int | None | Unset): Present only while the transfer is stalled (no data for several
                seconds): the seconds since the last byte arrived. The rate and time
                left are absent then.
            total (int | None | Unset): The stage's size in bytes, when known (a download without a
                `Content-Length` has none).
    """

    done: int
    bytes_per_sec: int | None | Unset = UNSET
    secs_left: int | None | Unset = UNSET
    stalled_secs: int | None | Unset = UNSET
    total: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        done = self.done

        bytes_per_sec: int | None | Unset
        if isinstance(self.bytes_per_sec, Unset):
            bytes_per_sec = UNSET
        else:
            bytes_per_sec = self.bytes_per_sec

        secs_left: int | None | Unset
        if isinstance(self.secs_left, Unset):
            secs_left = UNSET
        else:
            secs_left = self.secs_left

        stalled_secs: int | None | Unset
        if isinstance(self.stalled_secs, Unset):
            stalled_secs = UNSET
        else:
            stalled_secs = self.stalled_secs

        total: int | None | Unset
        if isinstance(self.total, Unset):
            total = UNSET
        else:
            total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "done": done,
            }
        )
        if bytes_per_sec is not UNSET:
            field_dict["bytes_per_sec"] = bytes_per_sec
        if secs_left is not UNSET:
            field_dict["secs_left"] = secs_left
        if stalled_secs is not UNSET:
            field_dict["stalled_secs"] = stalled_secs
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        done = d.pop("done")

        def _parse_bytes_per_sec(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        bytes_per_sec = _parse_bytes_per_sec(d.pop("bytes_per_sec", UNSET))

        def _parse_secs_left(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        secs_left = _parse_secs_left(d.pop("secs_left", UNSET))

        def _parse_stalled_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        stalled_secs = _parse_stalled_secs(d.pop("stalled_secs", UNSET))

        def _parse_total(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total = _parse_total(d.pop("total", UNSET))

        transfer_progress = cls(
            done=done,
            bytes_per_sec=bytes_per_sec,
            secs_left=secs_left,
            stalled_secs=stalled_secs,
            total=total,
        )

        transfer_progress.additional_properties = d
        return transfer_progress

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
