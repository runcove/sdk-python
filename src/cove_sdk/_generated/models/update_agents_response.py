from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.agent_update_result import AgentUpdateResult


T = TypeVar("T", bound="UpdateAgentsResponse")


@_attrs_define
class UpdateAgentsResponse:
    """
    Attributes:
        failed (int):
        results (list[AgentUpdateResult]):
        updated (int):
    """

    failed: int
    results: list[AgentUpdateResult]
    updated: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failed = self.failed

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        updated = self.updated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failed": failed,
                "results": results,
                "updated": updated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.agent_update_result import AgentUpdateResult

        d = dict(src_dict)
        failed = d.pop("failed")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = AgentUpdateResult.from_dict(results_item_data)

            results.append(results_item)

        updated = d.pop("updated")

        update_agents_response = cls(
            failed=failed,
            results=results,
            updated=updated,
        )

        update_agents_response.additional_properties = d
        return update_agents_response

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
