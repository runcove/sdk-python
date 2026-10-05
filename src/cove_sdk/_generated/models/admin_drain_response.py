from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.drain_target import DrainTarget


T = TypeVar("T", bound="AdminDrainResponse")


@_attrs_define
class AdminDrainResponse:
    """
    Attributes:
        attempted (int):
        budget_secs (int):
        failed (int):
        succeeded (int):
        targets (list[DrainTarget]):
        timed_out (int):
    """

    attempted: int
    budget_secs: int
    failed: int
    succeeded: int
    targets: list[DrainTarget]
    timed_out: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempted = self.attempted

        budget_secs = self.budget_secs

        failed = self.failed

        succeeded = self.succeeded

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        timed_out = self.timed_out

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempted": attempted,
                "budget_secs": budget_secs,
                "failed": failed,
                "succeeded": succeeded,
                "targets": targets,
                "timed_out": timed_out,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.drain_target import DrainTarget

        d = dict(src_dict)
        attempted = d.pop("attempted")

        budget_secs = d.pop("budget_secs")

        failed = d.pop("failed")

        succeeded = d.pop("succeeded")

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = DrainTarget.from_dict(targets_item_data)

            targets.append(targets_item)

        timed_out = d.pop("timed_out")

        admin_drain_response = cls(
            attempted=attempted,
            budget_secs=budget_secs,
            failed=failed,
            succeeded=succeeded,
            targets=targets,
            timed_out=timed_out,
        )

        admin_drain_response.additional_properties = d
        return admin_drain_response

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
