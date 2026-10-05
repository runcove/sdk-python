from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_bulk_scope_type_0 import AdminBulkScopeType0
    from ..models.admin_bulk_scope_type_1 import AdminBulkScopeType1
    from ..models.admin_bulk_scope_type_2 import AdminBulkScopeType2


T = TypeVar("T", bound="AdminBulkVmRequest")


@_attrs_define
class AdminBulkVmRequest:
    """`POST /admin/vms/stop-bulk` / `POST /admin/vms/delete-bulk` request body.

    `scope` selects the target set. `dry_run` lists targets without acting.
    `include_pool` is only meaningful with `AdminBulkScope::All` — pool VMs
    have no owner so `User` never touches them (the server rejects the combo).

        Attributes:
            scope (AdminBulkScopeType0 | AdminBulkScopeType1 | AdminBulkScopeType2): Scope for a fleet-scoped admin bulk op
                (`cove admin stop|delete --all|--user`
                or the `/admin/users` web page's checkbox multi-select).

                `--all` operates on every assigned (and, with `include_pool`, pooled) VM
                across all users; `--user <name>` drains one user's VMs without dropping
                their tenancy; `Vms` targets an arbitrary hand-picked
                set by name — the web bulk-select's only scope, never CLI-constructed
                today. Serialized as `{"type":"all"}` / `{"type":"user","username":"…"}` /
                `{"type":"vms","vm_names":["…"]}`.
            dry_run (bool | Unset):
            include_pool (bool | Unset):
    """

    scope: AdminBulkScopeType0 | AdminBulkScopeType1 | AdminBulkScopeType2
    dry_run: bool | Unset = UNSET
    include_pool: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.admin_bulk_scope_type_0 import (
            AdminBulkScopeType0,
        )
        from ..models.admin_bulk_scope_type_1 import (
            AdminBulkScopeType1,
        )

        scope: dict[str, Any]
        if isinstance(self.scope, AdminBulkScopeType0) or isinstance(
            self.scope, AdminBulkScopeType1
        ):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()

        dry_run = self.dry_run

        include_pool = self.include_pool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if include_pool is not UNSET:
            field_dict["include_pool"] = include_pool

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.admin_bulk_scope_type_0 import (
            AdminBulkScopeType0,
        )
        from ..models.admin_bulk_scope_type_1 import (
            AdminBulkScopeType1,
        )
        from ..models.admin_bulk_scope_type_2 import (
            AdminBulkScopeType2,
        )

        d = dict(src_dict)

        def _parse_scope(
            data: object,
        ) -> AdminBulkScopeType0 | AdminBulkScopeType1 | AdminBulkScopeType2:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_admin_bulk_scope_type_0 = (
                    AdminBulkScopeType0.from_dict(data)
                )

                return componentsschemas_admin_bulk_scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_admin_bulk_scope_type_1 = (
                    AdminBulkScopeType1.from_dict(data)
                )

                return componentsschemas_admin_bulk_scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_admin_bulk_scope_type_2 = AdminBulkScopeType2.from_dict(
                data
            )

            return componentsschemas_admin_bulk_scope_type_2

        scope = _parse_scope(d.pop("scope"))

        dry_run = d.pop("dry_run", UNSET)

        include_pool = d.pop("include_pool", UNSET)

        admin_bulk_vm_request = cls(
            scope=scope,
            dry_run=dry_run,
            include_pool=include_pool,
        )

        admin_bulk_vm_request.additional_properties = d
        return admin_bulk_vm_request

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
