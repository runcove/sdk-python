from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SecretEntryDto")


@_attrs_define
class SecretEntryDto:
    """One row of a secret listing (`GET /vms/{name}/secrets`, and the user,
    team and project listings): the secret's name, how it reaches the VM and
    how long it lasts. Never its value, nor anything derived from it: values
    are never exposed via HTTP.

        Attributes:
            name (str):
            exposure (str | Unset): How the VM receives it: `file`, `fifo` or `env` (an environment
                variable of `target_unit`). Every current server sends it.
            lifetime (str | Unset): How long it lasts: `persistent`, `setup_only` (removed after setup,
                grouped by `setup_tag`) or `ttl` (removed after `ttl_seconds`). Every
                current server sends it.
            setup_tag (None | str | Unset): The tag a `setup_only` secret was set with. Omitted when it has none.
            target_unit (None | str | Unset): The systemd unit that receives an `env` secret. Omitted otherwise.
            ttl_seconds (int | None | Unset): Seconds a `ttl` secret lasts. Omitted otherwise.
    """

    name: str
    exposure: str | Unset = UNSET
    lifetime: str | Unset = UNSET
    setup_tag: None | str | Unset = UNSET
    target_unit: None | str | Unset = UNSET
    ttl_seconds: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        exposure = self.exposure

        lifetime = self.lifetime

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
                "name": name,
            }
        )
        if exposure is not UNSET:
            field_dict["exposure"] = exposure
        if lifetime is not UNSET:
            field_dict["lifetime"] = lifetime
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
        name = d.pop("name")

        exposure = d.pop("exposure", UNSET)

        lifetime = d.pop("lifetime", UNSET)

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

        secret_entry_dto = cls(
            name=name,
            exposure=exposure,
            lifetime=lifetime,
            setup_tag=setup_tag,
            target_unit=target_unit,
            ttl_seconds=ttl_seconds,
        )

        secret_entry_dto.additional_properties = d
        return secret_entry_dto

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
