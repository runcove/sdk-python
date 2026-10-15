from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.restore_vm_result_dto import RestoreVmResultDto


T = TypeVar("T", bound="RestoreVmsResponse")


@_attrs_define
class RestoreVmsResponse:
    """
    Attributes:
        concurrency (int): Starts allowed in flight at once, after clamping.
        failed (int):
        requested (int): Distinct VM ids the request named.
        results (list[RestoreVmResultDto]): One row per distinct id, in the order named.
        skipped (int): Gone, in the pool, already up, not stopped, or owner disabled.
        started (int):
    """

    concurrency: int
    failed: int
    requested: int
    results: list[RestoreVmResultDto]
    skipped: int
    started: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        concurrency = self.concurrency

        failed = self.failed

        requested = self.requested

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        skipped = self.skipped

        started = self.started

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "concurrency": concurrency,
                "failed": failed,
                "requested": requested,
                "results": results,
                "skipped": skipped,
                "started": started,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.restore_vm_result_dto import RestoreVmResultDto

        d = dict(src_dict)
        concurrency = d.pop("concurrency")

        failed = d.pop("failed")

        requested = d.pop("requested")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = RestoreVmResultDto.from_dict(results_item_data)

            results.append(results_item)

        skipped = d.pop("skipped")

        started = d.pop("started")

        restore_vms_response = cls(
            concurrency=concurrency,
            failed=failed,
            requested=requested,
            results=results,
            skipped=skipped,
            started=started,
        )

        restore_vms_response.additional_properties = d
        return restore_vms_response

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
