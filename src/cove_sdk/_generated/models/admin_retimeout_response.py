from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_retimeout_response_by_current_value import (
        AdminRetimeoutResponseByCurrentValue,
    )
    from ..models.admin_retimeout_vm import AdminRetimeoutVm


T = TypeVar("T", bound="AdminRetimeoutResponse")


@_attrs_define
class AdminRetimeoutResponse:
    """`POST /admin/auto-pause/retimeout` response body.

    `target_secs` is the resolved target (request value, or config default
    when absent). `total_auto_pause` is the count of rows that have an
    auto-pause policy at query time (regardless of filter).
    `by_current_value` groups every auto-pausing VM by its current
    `idle_timeout_secs` so operators can preview the spread before flipping.

        Attributes:
            by_current_value (AdminRetimeoutResponseByCurrentValue): `current_secs -> count`, as a JSON object whose keys
                are the
                seconds written as strings (a list of `[seconds, count]` pairs until
                API version 5). Ordered ascending by key.
            changed (list[AdminRetimeoutVm]):
            dry_run (bool):
            skipped_custom (list[AdminRetimeoutVm]):
            target_secs (int):
            total_auto_pause (int): Named `total_auto_suspend` until the 2026-07 terminology rename. The alias lets a
                current
                client read a response from a server one version behind; it cannot help
                the other direction, so a client older than this rename needs the
                version gate in `docs/cli-distribution.md` rather than a serde
                attribute.
            from_secs (int | None | Unset):
    """

    by_current_value: AdminRetimeoutResponseByCurrentValue
    changed: list[AdminRetimeoutVm]
    dry_run: bool
    skipped_custom: list[AdminRetimeoutVm]
    target_secs: int
    total_auto_pause: int
    from_secs: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        by_current_value = self.by_current_value.to_dict()

        changed = []
        for changed_item_data in self.changed:
            changed_item = changed_item_data.to_dict()
            changed.append(changed_item)

        dry_run = self.dry_run

        skipped_custom = []
        for skipped_custom_item_data in self.skipped_custom:
            skipped_custom_item = skipped_custom_item_data.to_dict()
            skipped_custom.append(skipped_custom_item)

        target_secs = self.target_secs

        total_auto_pause = self.total_auto_pause

        from_secs: int | None | Unset
        if isinstance(self.from_secs, Unset):
            from_secs = UNSET
        else:
            from_secs = self.from_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "by_current_value": by_current_value,
                "changed": changed,
                "dry_run": dry_run,
                "skipped_custom": skipped_custom,
                "target_secs": target_secs,
                "total_auto_pause": total_auto_pause,
            }
        )
        if from_secs is not UNSET:
            field_dict["from_secs"] = from_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.admin_retimeout_response_by_current_value import (
            AdminRetimeoutResponseByCurrentValue,
        )
        from ..models.admin_retimeout_vm import AdminRetimeoutVm

        d = dict(src_dict)
        by_current_value = AdminRetimeoutResponseByCurrentValue.from_dict(
            d.pop("by_current_value")
        )

        changed = []
        _changed = d.pop("changed")
        for changed_item_data in _changed:
            changed_item = AdminRetimeoutVm.from_dict(changed_item_data)

            changed.append(changed_item)

        dry_run = d.pop("dry_run")

        skipped_custom = []
        _skipped_custom = d.pop("skipped_custom")
        for skipped_custom_item_data in _skipped_custom:
            skipped_custom_item = AdminRetimeoutVm.from_dict(skipped_custom_item_data)

            skipped_custom.append(skipped_custom_item)

        target_secs = d.pop("target_secs")

        total_auto_pause = d.pop("total_auto_pause")

        def _parse_from_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        from_secs = _parse_from_secs(d.pop("from_secs", UNSET))

        admin_retimeout_response = cls(
            by_current_value=by_current_value,
            changed=changed,
            dry_run=dry_run,
            skipped_custom=skipped_custom,
            target_secs=target_secs,
            total_auto_pause=total_auto_pause,
            from_secs=from_secs,
        )

        admin_retimeout_response.additional_properties = d
        return admin_retimeout_response

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
