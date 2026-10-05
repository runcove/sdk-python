from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SecretSpec")


@_attrs_define
class SecretSpec:
    """Wire representation of a secret to inject at VM creation time.

    `exposure` and `lifetime` use the same string tags as `SetSecretRequest`
    on `POST /vms/{name}/secrets/{key}`:
    * `exposure`: `"file"` | `"fifo"` | `"env"`
    * `lifetime`: `"persistent"` | `"setup_only"` | `"ttl"`

    `target_unit` is required when `exposure == "env"`.
    `setup_tag` is optional when `lifetime == "setup_only"`.
    `ttl_seconds` is required when `lifetime == "ttl"`.

        Attributes:
            exposure (str): `"file"` | `"fifo"` | `"env"`.
            lifetime (str): `"persistent"` | `"setup_only"` | `"ttl"`.
            name (str):
            value_b64 (str): base64-encoded secret bytes (so non-UTF8 binary tokens survive JSON).
            setup_tag (None | str | Unset): Required only when `lifetime == "setup_only"` and a tag is present.
            target_unit (None | str | Unset): Required only when `exposure == "env"`. Skipped otherwise.
            ttl_seconds (int | None | Unset): Required only when `lifetime == "ttl"`.
    """

    exposure: str
    lifetime: str
    name: str
    value_b64: str
    setup_tag: None | str | Unset = UNSET
    target_unit: None | str | Unset = UNSET
    ttl_seconds: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exposure = self.exposure

        lifetime = self.lifetime

        name = self.name

        value_b64 = self.value_b64

        setup_tag: None | str | Unset
        if isinstance(self.setup_tag, Unset):
            setup_tag = UNSET
        else:
            setup_tag = self.setup_tag

        target_unit: None | str | Unset
        if isinstance(self.target_unit, Unset):
            target_unit = UNSET
        else:
            target_unit = self.target_unit

        ttl_seconds: int | None | Unset
        if isinstance(self.ttl_seconds, Unset):
            ttl_seconds = UNSET
        else:
            ttl_seconds = self.ttl_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exposure": exposure,
                "lifetime": lifetime,
                "name": name,
                "value_b64": value_b64,
            }
        )
        if setup_tag is not UNSET:
            field_dict["setup_tag"] = setup_tag
        if target_unit is not UNSET:
            field_dict["target_unit"] = target_unit
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        exposure = d.pop("exposure")

        lifetime = d.pop("lifetime")

        name = d.pop("name")

        value_b64 = d.pop("value_b64")

        def _parse_setup_tag(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        setup_tag = _parse_setup_tag(d.pop("setup_tag", UNSET))

        def _parse_target_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_unit = _parse_target_unit(d.pop("target_unit", UNSET))

        def _parse_ttl_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        ttl_seconds = _parse_ttl_seconds(d.pop("ttl_seconds", UNSET))

        secret_spec = cls(
            exposure=exposure,
            lifetime=lifetime,
            name=name,
            value_b64=value_b64,
            setup_tag=setup_tag,
            target_unit=target_unit,
            ttl_seconds=ttl_seconds,
        )

        secret_spec.additional_properties = d
        return secret_spec

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
