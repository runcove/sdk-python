from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode

T = TypeVar("T", bound="PortNotAllowedBody")


@_attrs_define
class PortNotAllowedBody:
    """422 body for [`ErrorCode::PortNotAllowed`].

    Attributes:
        allowed (list[int]):
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
    """

    allowed: list[int]
    code: ErrorCode
    message: str
    port: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed = self.allowed

        code = self.code.value

        message = self.message

        port = self.port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allowed": allowed,
                "code": code,
                "message": message,
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        allowed = cast(list[int], d.pop("allowed"))

        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        port = d.pop("port")

        port_not_allowed_body = cls(
            allowed=allowed,
            code=code,
            message=message,
            port=port,
        )

        port_not_allowed_body.additional_properties = d
        return port_not_allowed_body

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
