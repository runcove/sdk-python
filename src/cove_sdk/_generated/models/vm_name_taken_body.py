from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="VmNameTakenBody")


@_attrs_define
class VmNameTakenBody:
    """409 body for [`ErrorCode::VmNameTaken`]. `retry_after_secs` is additive
    (`skip_serializing_if = None`) so a legacy client that only reads
    `{code, message}` keeps working.

        Attributes:
            code (ErrorCode): A machine-readable error code from the REST API's `ApiError.code` field.

                **Not** the vocabulary of the 409 admission/quota body: `DenyReason` keys its
                discriminant on `code` too, and that is all the two share — its values
                (`ram_headroom_exceeded`, `user_vcpu_quota_exceeded`, …) are a separate closed
                catalogue and none of them appears here. This text is published in
                `sdk/openapi.yaml`, and an earlier version said the two "share the same wire
                vocabulary", which would lead a client author to type every `code` as this
                enum and be wrong on every 409.

                `snake_case`, `<subject>_<condition>`: the subject is
                the thing that went wrong, not the endpoint.
            message (str):
            name (str):
            retry_after_secs (int | None | Unset):
    """

    code: ErrorCode
    message: str
    name: str
    retry_after_secs: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        name = self.name

        retry_after_secs: int | None | Unset
        if isinstance(self.retry_after_secs, Unset):
            retry_after_secs = UNSET
        else:
            retry_after_secs = self.retry_after_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "name": name,
            }
        )
        if retry_after_secs is not UNSET:
            field_dict["retry_after_secs"] = retry_after_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        name = d.pop("name")

        def _parse_retry_after_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        retry_after_secs = _parse_retry_after_secs(d.pop("retry_after_secs", UNSET))

        vm_name_taken_body = cls(
            code=code,
            message=message,
            name=name,
            retry_after_secs=retry_after_secs,
        )

        vm_name_taken_body.additional_properties = d
        return vm_name_taken_body

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
