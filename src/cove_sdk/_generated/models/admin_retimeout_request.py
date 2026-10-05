from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminRetimeoutRequest")


@_attrs_define
class AdminRetimeoutRequest:
    """`POST /admin/auto-pause/retimeout` request body. Filters and target for
    the bulk-rewrite of the idle timeout across every existing auto-pausing VM.

    * `from_secs` — when `Some(F)`, only flip rows whose current
      `idle_timeout_secs == F`. When `None`, flip every auto-pausing row
      whose current value differs from the resolved target.
    * `to_secs` — when `Some(T)`, target value. When `None`, the server uses
      `[auto_pause] default_idle_timeout_secs` from `cove.toml`.
    * `dry_run` — when `true`, the response describes the change set without
      mutating any rows.

        Attributes:
            dry_run (bool | Unset):
            from_secs (int | None | Unset):
            to_secs (int | None | Unset):
    """

    dry_run: bool | Unset = UNSET
    from_secs: int | None | Unset = UNSET
    to_secs: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        from_secs: int | None | Unset
        if isinstance(self.from_secs, Unset):
            from_secs = UNSET
        else:
            from_secs = self.from_secs

        to_secs: int | None | Unset
        if isinstance(self.to_secs, Unset):
            to_secs = UNSET
        else:
            to_secs = self.to_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if from_secs is not UNSET:
            field_dict["from_secs"] = from_secs
        if to_secs is not UNSET:
            field_dict["to_secs"] = to_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        dry_run = d.pop("dry_run", UNSET)

        def _parse_from_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        from_secs = _parse_from_secs(d.pop("from_secs", UNSET))

        def _parse_to_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        to_secs = _parse_to_secs(d.pop("to_secs", UNSET))

        admin_retimeout_request = cls(
            dry_run=dry_run,
            from_secs=from_secs,
            to_secs=to_secs,
        )

        admin_retimeout_request.additional_properties = d
        return admin_retimeout_request

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
