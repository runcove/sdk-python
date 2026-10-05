from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="RevokeShareOutcome")


@_attrs_define
class RevokeShareOutcome:
    """Fail-loud revoke result. `unconfirmed_*` name every edge/session the
    synchronous sweep could not confirm dead; the reconciler retries them.

    This is the ONE `RevokeShareOutcome` that gets `ToSchema`. The
    server-side `cove_service::ops::share::RevokeShareOutcome` is a stale
    duplicate the `DELETE /vms/{name}/shares/{subject_type}/{subject_id}`
    handler does not serialize directly (it hand-projects the service value
    into this wire shape via `serde_json::json!`) — see the NOTE on that
    duplicate.

        Attributes:
            revoked (bool):
            unconfirmed_edges (list[str] | Unset):
            unconfirmed_sessions (list[str] | Unset):
    """

    revoked: bool
    unconfirmed_edges: list[str] | Unset = UNSET
    unconfirmed_sessions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        revoked = self.revoked

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
                "revoked": revoked,
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
        revoked = d.pop("revoked")

        unconfirmed_edges = cast(list[str], d.pop("unconfirmed_edges", UNSET))

        unconfirmed_sessions = cast(list[str], d.pop("unconfirmed_sessions", UNSET))

        revoke_share_outcome = cls(
            revoked=revoked,
            unconfirmed_edges=unconfirmed_edges,
            unconfirmed_sessions=unconfirmed_sessions,
        )

        revoke_share_outcome.additional_properties = d
        return revoke_share_outcome

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
