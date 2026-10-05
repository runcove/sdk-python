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
    from ..models.admin_bulk_vm_target import AdminBulkVmTarget


T = TypeVar("T", bound="AdminBulkVmResponse")


@_attrs_define
class AdminBulkVmResponse:
    """`POST /admin/vms/stop-bulk` / `delete-bulk` response body. `targets` is
    sorted by `vm_name` for deterministic CLI output. `attempted` is the
    count the call acted on (stoppable subset for stop; full set for delete);
    in `dry_run` the full target set is reported with `result: "skipped"`.

        Attributes:
            attempted (int):
            dry_run (bool):
            failed (int):
            scope (AdminBulkScopeType0 | AdminBulkScopeType1 | AdminBulkScopeType2): Scope for a fleet-scoped admin bulk op
                (`cove admin stop|delete --all|--user`
                or the `/admin/users` web page's checkbox multi-select).

                `--all` operates on every assigned (and, with `include_pool`, pooled) VM
                across all users; `--user <name>` drains one user's VMs without dropping
                their tenancy; `Vms` targets an arbitrary hand-picked
                set by name — the web bulk-select's only scope, never CLI-constructed
                today. Serialized as `{"type":"all"}` / `{"type":"user","username":"…"}` /
                `{"type":"vms","vm_names":["…"]}`.
            succeeded (int):
            targets (list[AdminBulkVmTarget]):
            include_pool (bool | Unset):
    """

    attempted: int
    dry_run: bool
    failed: int
    scope: AdminBulkScopeType0 | AdminBulkScopeType1 | AdminBulkScopeType2
    succeeded: int
    targets: list[AdminBulkVmTarget]
    include_pool: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.admin_bulk_scope_type_0 import (
            AdminBulkScopeType0,
        )
        from ..models.admin_bulk_scope_type_1 import (
            AdminBulkScopeType1,
        )

        attempted = self.attempted

        dry_run = self.dry_run

        failed = self.failed

        scope: dict[str, Any]
        if isinstance(self.scope, AdminBulkScopeType0) or isinstance(
            self.scope, AdminBulkScopeType1
        ):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()

        succeeded = self.succeeded

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        include_pool = self.include_pool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempted": attempted,
                "dry_run": dry_run,
                "failed": failed,
                "scope": scope,
                "succeeded": succeeded,
                "targets": targets,
            }
        )
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
        from ..models.admin_bulk_vm_target import AdminBulkVmTarget

        d = dict(src_dict)
        attempted = d.pop("attempted")

        dry_run = d.pop("dry_run")

        failed = d.pop("failed")

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

        succeeded = d.pop("succeeded")

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = AdminBulkVmTarget.from_dict(targets_item_data)

            targets.append(targets_item)

        include_pool = d.pop("include_pool", UNSET)

        admin_bulk_vm_response = cls(
            attempted=attempted,
            dry_run=dry_run,
            failed=failed,
            scope=scope,
            succeeded=succeeded,
            targets=targets,
            include_pool=include_pool,
        )

        admin_bulk_vm_response.additional_properties = d
        return admin_bulk_vm_response

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
