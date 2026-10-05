from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.idle_kind_type_0 import IdleKindType0
    from ..models.idle_kind_type_1 import IdleKindType1
    from ..models.idle_kind_type_2 import IdleKindType2
    from ..models.idle_kind_type_3 import IdleKindType3


T = TypeVar("T", bound="IdleState")


@_attrs_define
class IdleState:
    """GET /vms/{name}/idle-state response body.

    Attributes:
        kind (IdleKindType0 | IdleKindType1 | IdleKindType2 | IdleKindType3):
        timeout_secs (int | None | Unset): Current configured timeout in seconds. `None` when policy is AlwaysOn.
    """

    kind: IdleKindType0 | IdleKindType1 | IdleKindType2 | IdleKindType3
    timeout_secs: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.idle_kind_type_0 import IdleKindType0
        from ..models.idle_kind_type_1 import IdleKindType1
        from ..models.idle_kind_type_2 import IdleKindType2

        kind: dict[str, Any]
        if (
            isinstance(self.kind, IdleKindType0)
            or isinstance(self.kind, IdleKindType1)
            or isinstance(self.kind, IdleKindType2)
        ):
            kind = self.kind.to_dict()
        else:
            kind = self.kind.to_dict()

        timeout_secs: int | None | Unset
        if isinstance(self.timeout_secs, Unset):
            timeout_secs = UNSET
        else:
            timeout_secs = self.timeout_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if timeout_secs is not UNSET:
            field_dict["timeout_secs"] = timeout_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.idle_kind_type_0 import IdleKindType0
        from ..models.idle_kind_type_1 import IdleKindType1
        from ..models.idle_kind_type_2 import IdleKindType2
        from ..models.idle_kind_type_3 import IdleKindType3

        d = dict(src_dict)

        def _parse_kind(
            data: object,
        ) -> IdleKindType0 | IdleKindType1 | IdleKindType2 | IdleKindType3:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_idle_kind_type_0 = IdleKindType0.from_dict(data)

                return componentsschemas_idle_kind_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_idle_kind_type_1 = IdleKindType1.from_dict(data)

                return componentsschemas_idle_kind_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_idle_kind_type_2 = IdleKindType2.from_dict(data)

                return componentsschemas_idle_kind_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_idle_kind_type_3 = IdleKindType3.from_dict(data)

            return componentsschemas_idle_kind_type_3

        kind = _parse_kind(d.pop("kind"))

        def _parse_timeout_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timeout_secs = _parse_timeout_secs(d.pop("timeout_secs", UNSET))

        idle_state = cls(
            kind=kind,
            timeout_secs=timeout_secs,
        )

        idle_state.additional_properties = d
        return idle_state

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
