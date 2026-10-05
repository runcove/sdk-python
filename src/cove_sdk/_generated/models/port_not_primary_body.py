from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode

T = TypeVar("T", bound="PortNotPrimaryBody")


@_attrs_define
class PortNotPrimaryBody:
    """422 body for [`ErrorCode::PortNotPrimary`].

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
        port (int):
        primary_port (int):
    """

    code: ErrorCode
    message: str
    port: int
    primary_port: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        port = self.port

        primary_port = self.primary_port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "port": port,
                "primary_port": primary_port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        port = d.pop("port")

        primary_port = d.pop("primary_port")

        port_not_primary_body = cls(
            code=code,
            message=message,
            port=port,
            primary_port=primary_port,
        )

        port_not_primary_body.additional_properties = d
        return port_not_primary_body

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
