from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="GrantShareOutcome")


@_attrs_define
class GrantShareOutcome:
    """Grant result. A user grant must name someone who has signed in to this
    Cove server at least once; a never-seen username is refused (422
    `user_never_signed_in`) rather than answered here. `user_known` is `false`
    when that person has no account at the access gateway right now (it was
    deleted, say). The grant still succeeds (role assigned to targets); access
    applies when they next sign in. Callers surface a note when it is false.

    This is the ONE `GrantShareOutcome` that gets `ToSchema`. The
    server-side `cove_service::ops::share::GrantShareOutcome` is a stale
    duplicate the `POST /vms/{name}/shares` handler does not serialize
    directly — see the NOTE on that duplicate.

        Attributes:
            user_known (bool):
    """

    user_known: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_known = self.user_known

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_known": user_known,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        user_known = d.pop("user_known")

        grant_share_outcome = cls(
            user_known=user_known,
        )

        grant_share_outcome.additional_properties = d
        return grant_share_outcome

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
