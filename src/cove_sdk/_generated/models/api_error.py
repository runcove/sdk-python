from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_code import ErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiError")


@_attrs_define
class ApiError:
    """Standard API error envelope.

    `code` is [`ErrorCode`], not `String` — an unlisted code is a compile
    error, not a runtime string a reviewer has to catch. `field`
    absorbs what the retired `ValidationFailedBody` carried: when `code` is
    [`ErrorCode::ValidationFailed`] and the failure is scoped to one request
    field, `field` names it (`"label"`, `"cursor"`, `"value_b64"`, …); `None`
    for whole-body or cross-field failures, and for every other code.

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
            detail (None | str | Unset):
            field (None | str | Unset):
    """

    code: ErrorCode
    message: str
    detail: None | str | Unset = UNSET
    field: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        detail: None | str | Unset
        if isinstance(self.detail, Unset):
            detail = UNSET
        else:
            detail = self.detail

        field: None | str | Unset
        if isinstance(self.field, Unset):
            field = UNSET
        else:
            field = self.field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if detail is not UNSET:
            field_dict["detail"] = detail
        if field is not UNSET:
            field_dict["field"] = field

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        def _parse_detail(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        detail = _parse_detail(d.pop("detail", UNSET))

        def _parse_field(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        field = _parse_field(d.pop("field", UNSET))

        api_error = cls(
            code=code,
            message=message,
            detail=detail,
            field=field,
        )

        api_error.additional_properties = d
        return api_error

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
