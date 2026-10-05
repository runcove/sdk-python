from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode

T = TypeVar("T", bound="SudoRequiredBody")


@_attrs_define
class SudoRequiredBody:
    """401 body for [`cove_types::ErrorCode::SudoRequired`]. `reauth_window_secs`
    names how long a fresh sudo re-auth lasts. `message` was added later — like
    `ScopeDeniedBody`, this used to be `{code, reauth_window_secs}` with no
    `message` at all.

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
            reauth_window_secs (int):
    """

    code: ErrorCode
    message: str
    reauth_window_secs: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        reauth_window_secs = self.reauth_window_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "reauth_window_secs": reauth_window_secs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        reauth_window_secs = d.pop("reauth_window_secs")

        sudo_required_body = cls(
            code=code,
            message=message,
            reauth_window_secs=reauth_window_secs,
        )

        sudo_required_body.additional_properties = d
        return sudo_required_body

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
