from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delete_after_stop_type_0 import DeleteAfterStopType0
    from ..models.delete_after_stop_type_1 import DeleteAfterStopType1
    from ..models.delete_after_stop_type_2 import DeleteAfterStopType2


T = TypeVar("T", bound="TtlPolicy")


@_attrs_define
class TtlPolicy:
    """Per-VM TTL policy bundle. Both knobs default to "off" (`Never` / `None`);
    pool defaults and CLI flags merge into this on create.

        Attributes:
            max_lifetime_secs (int | None | Unset): Wall-clock cap counted from the VM's creation, or its claim for a VM
                Cove had ready in advance (default: `None`). Service-layer validation
                enforces 3600 (one hour) to 315360000 (ten years) when `Some`.
            on_stop (DeleteAfterStopType0 | DeleteAfterStopType1 | DeleteAfterStopType2 | Unset): Wire/in-memory
                representation of the "delete after VM enters Stopped" knob.
                Persisted by core as a single `INTEGER` (`vms.delete_after_stop_secs`) using
                the Daytona-style sentinel: `-1` = Never, `0` = Immediate, `N > 0` = grace
                seconds (see `cove_core::vm::DeleteAfterStopExt`).
    """

    max_lifetime_secs: int | None | Unset = UNSET
    on_stop: (
        DeleteAfterStopType0 | DeleteAfterStopType1 | DeleteAfterStopType2 | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.delete_after_stop_type_0 import (
            DeleteAfterStopType0,
        )
        from ..models.delete_after_stop_type_1 import (
            DeleteAfterStopType1,
        )

        max_lifetime_secs: int | None | Unset
        if isinstance(self.max_lifetime_secs, Unset):
            max_lifetime_secs = UNSET
        else:
            max_lifetime_secs = self.max_lifetime_secs

        on_stop: dict[str, Any] | Unset
        if isinstance(self.on_stop, Unset):
            on_stop = UNSET
        elif isinstance(self.on_stop, DeleteAfterStopType0) or isinstance(
            self.on_stop, DeleteAfterStopType1
        ):
            on_stop = self.on_stop.to_dict()
        else:
            on_stop = self.on_stop.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_lifetime_secs is not UNSET:
            field_dict["max_lifetime_secs"] = max_lifetime_secs
        if on_stop is not UNSET:
            field_dict["on_stop"] = on_stop

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delete_after_stop_type_0 import (
            DeleteAfterStopType0,
        )
        from ..models.delete_after_stop_type_1 import (
            DeleteAfterStopType1,
        )
        from ..models.delete_after_stop_type_2 import (
            DeleteAfterStopType2,
        )

        d = dict(src_dict)

        def _parse_max_lifetime_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_lifetime_secs = _parse_max_lifetime_secs(d.pop("max_lifetime_secs", UNSET))

        def _parse_on_stop(
            data: object,
        ) -> DeleteAfterStopType0 | DeleteAfterStopType1 | DeleteAfterStopType2 | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_delete_after_stop_type_0 = (
                    DeleteAfterStopType0.from_dict(data)
                )

                return componentsschemas_delete_after_stop_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_delete_after_stop_type_1 = (
                    DeleteAfterStopType1.from_dict(data)
                )

                return componentsschemas_delete_after_stop_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_delete_after_stop_type_2 = DeleteAfterStopType2.from_dict(
                data
            )

            return componentsschemas_delete_after_stop_type_2

        on_stop = _parse_on_stop(d.pop("on_stop", UNSET))

        ttl_policy = cls(
            max_lifetime_secs=max_lifetime_secs,
            on_stop=on_stop,
        )

        ttl_policy.additional_properties = d
        return ttl_policy

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
