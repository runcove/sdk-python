from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode

T = TypeVar("T", bound="InvalidVmNameBody")


@_attrs_define
class InvalidVmNameBody:
    """400 body for [`ErrorCode::InvalidVmName`]: the name asked for the new VM is
    one cove refuses.

    A name must be 3-30 characters of lowercase ASCII letters, digits and
    hyphens, and must not start or end with a hyphen; a name held by a
    bastion target this server may not take over is refused too. `message`
    says which rule the name broke, `field` is always `"name"`, and `name`
    echoes the rejected name so a caller that submitted several can tell which
    one failed.

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
            field (str): The request field that held the name. Always `"name"`, as on a
                `validation_failed` body scoped to one field.
            message (str):
            name (str): The rejected name, exactly as submitted.
    """

    code: ErrorCode
    field: str
    message: str
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        field = self.field

        message = self.message

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "field": field,
                "message": message,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        field = d.pop("field")

        message = d.pop("message")

        name = d.pop("name")

        invalid_vm_name_body = cls(
            code=code,
            field=field,
            message=message,
            name=name,
        )

        invalid_vm_name_body.additional_properties = d
        return invalid_vm_name_body

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
