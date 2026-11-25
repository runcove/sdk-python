from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.purged_rows import PurgedRows


T = TypeVar("T", bound="PurgeUserReport")


@_attrs_define
class PurgeUserReport:
    """`POST /api/admin/users/{username}/purge` response: the leftover rows of
    an offboarded person, deleted or (in a dry run) counted. The purge deletes
    records about the person and changes no record that belongs to someone
    else; `left_in_place` says what still names them.

        Attributes:
            deleted (list[PurgedRows]): Every table the purge deletes from, with the rows it deleted (or would
                delete); a table with none is listed with zero.
            dry_run (bool): True when nothing was deleted and this is only what would be.
            left_in_place (str): What the purge leaves in place and where the person's name remains: the
                audit log, their name as the actor on records that belong to other
                people or to teams, and the service keys that were bound to them. The
                same text on a dry run and a real run.
            username (str): The person, as Cove has them stored: the one spelling their rows carry
                (in the `users` table or any other that names a person), or else the
                shut-out record's.
    """

    deleted: list[PurgedRows]
    dry_run: bool
    left_in_place: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted = []
        for deleted_item_data in self.deleted:
            deleted_item = deleted_item_data.to_dict()
            deleted.append(deleted_item)

        dry_run = self.dry_run

        left_in_place = self.left_in_place

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deleted": deleted,
                "dry_run": dry_run,
                "left_in_place": left_in_place,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.purged_rows import PurgedRows

        d = dict(src_dict)
        deleted = []
        _deleted = d.pop("deleted")
        for deleted_item_data in _deleted:
            deleted_item = PurgedRows.from_dict(deleted_item_data)

            deleted.append(deleted_item)

        dry_run = d.pop("dry_run")

        left_in_place = d.pop("left_in_place")

        username = d.pop("username")

        purge_user_report = cls(
            deleted=deleted,
            dry_run=dry_run,
            left_in_place=left_in_place,
            username=username,
        )

        purge_user_report.additional_properties = d
        return purge_user_report

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
