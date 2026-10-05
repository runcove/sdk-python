from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoveMemberOutcome")


@_attrs_define
class RemoveMemberOutcome:
    """Fail-loud member-removal outcome (the share-revoke shape, generalized to teams).

    This is the ONE `RemoveMemberOutcome` that gets `ToSchema`. The
    server-side `cove_service::teams::RemoveMemberOutcome` is a stale
    duplicate — `handlers::teams::remove_team_member` hand-projects the
    service value into this exact shape via `serde_json::json!` rather than
    serializing the service type directly; see the NOTE on that duplicate.

        Attributes:
            removed (bool):
            unconfirmed_edges (list[str] | Unset):
            unconfirmed_sessions (list[str] | Unset):
    """

    removed: bool
    unconfirmed_edges: list[str] | Unset = UNSET
    unconfirmed_sessions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        removed = self.removed

        unconfirmed_edges: list[str] | Unset = UNSET
        if not isinstance(self.unconfirmed_edges, Unset):
            unconfirmed_edges = self.unconfirmed_edges

        unconfirmed_sessions: list[str] | Unset = UNSET
        if not isinstance(self.unconfirmed_sessions, Unset):
            unconfirmed_sessions = self.unconfirmed_sessions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "removed": removed,
            }
        )
        if unconfirmed_edges is not UNSET:
            field_dict["unconfirmed_edges"] = unconfirmed_edges
        if unconfirmed_sessions is not UNSET:
            field_dict["unconfirmed_sessions"] = unconfirmed_sessions

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        removed = d.pop("removed")

        unconfirmed_edges = cast(list[str], d.pop("unconfirmed_edges", UNSET))

        unconfirmed_sessions = cast(list[str], d.pop("unconfirmed_sessions", UNSET))

        remove_member_outcome = cls(
            removed=removed,
            unconfirmed_edges=unconfirmed_edges,
            unconfirmed_sessions=unconfirmed_sessions,
        )

        remove_member_outcome.additional_properties = d
        return remove_member_outcome

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
