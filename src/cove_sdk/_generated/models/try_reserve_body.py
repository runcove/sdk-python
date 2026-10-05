from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.pending_action_type_0 import PendingActionType0
    from ..models.pending_action_type_1 import PendingActionType1
    from ..models.pending_action_type_2 import PendingActionType2
    from ..models.pending_action_type_3 import PendingActionType3
    from ..models.pending_action_type_4 import PendingActionType4
    from ..models.pending_action_type_5 import PendingActionType5
    from ..models.pending_action_type_6 import PendingActionType6


T = TypeVar("T", bound="TryReserveBody")


@_attrs_define
class TryReserveBody:
    """
    Attributes:
        action (PendingActionType0 | PendingActionType1 | PendingActionType2 | PendingActionType3 | PendingActionType4 |
            PendingActionType5 | PendingActionType6): Action that needs admission before it executes — the body of
            `POST /host/reservations`.

            Internally tagged on `type`. See the module doc for the rename
            behind `WakeFromCheckpoint` / `Wake`.
        flow_id (str):
    """

    action: (
        PendingActionType0
        | PendingActionType1
        | PendingActionType2
        | PendingActionType3
        | PendingActionType4
        | PendingActionType5
        | PendingActionType6
    )
    flow_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pending_action_type_0 import PendingActionType0
        from ..models.pending_action_type_1 import PendingActionType1
        from ..models.pending_action_type_2 import PendingActionType2
        from ..models.pending_action_type_3 import PendingActionType3
        from ..models.pending_action_type_4 import PendingActionType4
        from ..models.pending_action_type_5 import PendingActionType5

        action: dict[str, Any]
        if (
            isinstance(self.action, PendingActionType0)
            or isinstance(self.action, PendingActionType1)
            or isinstance(self.action, PendingActionType2)
            or isinstance(self.action, PendingActionType3)
            or isinstance(self.action, PendingActionType4)
            or isinstance(self.action, PendingActionType5)
        ):
            action = self.action.to_dict()
        else:
            action = self.action.to_dict()

        flow_id = self.flow_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "flow_id": flow_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.pending_action_type_0 import PendingActionType0
        from ..models.pending_action_type_1 import PendingActionType1
        from ..models.pending_action_type_2 import PendingActionType2
        from ..models.pending_action_type_3 import PendingActionType3
        from ..models.pending_action_type_4 import PendingActionType4
        from ..models.pending_action_type_5 import PendingActionType5
        from ..models.pending_action_type_6 import PendingActionType6

        d = dict(src_dict)

        def _parse_action(
            data: object,
        ) -> (
            PendingActionType0
            | PendingActionType1
            | PendingActionType2
            | PendingActionType3
            | PendingActionType4
            | PendingActionType5
            | PendingActionType6
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pending_action_type_0 = PendingActionType0.from_dict(
                    data
                )

                return componentsschemas_pending_action_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pending_action_type_1 = PendingActionType1.from_dict(
                    data
                )

                return componentsschemas_pending_action_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pending_action_type_2 = PendingActionType2.from_dict(
                    data
                )

                return componentsschemas_pending_action_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pending_action_type_3 = PendingActionType3.from_dict(
                    data
                )

                return componentsschemas_pending_action_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pending_action_type_4 = PendingActionType4.from_dict(
                    data
                )

                return componentsschemas_pending_action_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pending_action_type_5 = PendingActionType5.from_dict(
                    data
                )

                return componentsschemas_pending_action_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_pending_action_type_6 = PendingActionType6.from_dict(data)

            return componentsschemas_pending_action_type_6

        action = _parse_action(d.pop("action"))

        flow_id = d.pop("flow_id")

        try_reserve_body = cls(
            action=action,
            flow_id=flow_id,
        )

        try_reserve_body.additional_properties = d
        return try_reserve_body

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
