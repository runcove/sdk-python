from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode

T = TypeVar("T", bound="CliTooOldBody")


@_attrs_define
class CliTooOldBody:
    """426 body for [`cove_types::ErrorCode::CliTooOld`]. `min_cli_version` is
    additive to `ApiError`'s shape (not modeled there — no other code needs
    it), so this gets its own small typed struct rather than an untyped
    `json!`, matching the pattern `handlers::PortNotAllowedBody` and friends
    set for the other "ApiError plus extra fields" bodies.

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
            min_cli_version (str): The oldest cove-cli release that speaks this server's API version.
                Not a field on `ApiError`, which is why this body exists at all — a
                CLI that has just been refused needs to know what to upgrade TO.
    """

    code: ErrorCode
    message: str
    min_cli_version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        min_cli_version = self.min_cli_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "min_cli_version": min_cli_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        min_cli_version = d.pop("min_cli_version")

        cli_too_old_body = cls(
            code=code,
            message=message,
            min_cli_version=min_cli_version,
        )

        cli_too_old_body.additional_properties = d
        return cli_too_old_body

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
