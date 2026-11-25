from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="PurgeUserRequest")


@_attrs_define
class PurgeUserRequest:
    """`POST /api/admin/users/{username}/purge` request body. An absent body
    means `{"dry_run": false}`; a body must carry `dry_run`. An unknown field
    is refused, so a misspelt `dry_run` can never run the real purge.

        Attributes:
            dry_run (bool): Report what the purge would delete and change nothing. Required in a
                body; only an absent body means `false`.
    """

    dry_run: bool

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dry_run": dry_run,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        dry_run = d.pop("dry_run")

        purge_user_request = cls(
            dry_run=dry_run,
        )

        return purge_user_request
