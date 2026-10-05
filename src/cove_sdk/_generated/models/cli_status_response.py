from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CliStatusResponse")


@_attrs_define
class CliStatusResponse:
    """GET /me/cli-status response body. Published as `CliStatusResponse`.

    Attributes:
        has_cli_ticket (bool):
        cli_install_url (None | str | Unset):
    """

    has_cli_ticket: bool
    cli_install_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_cli_ticket = self.has_cli_ticket

        cli_install_url: None | str | Unset
        if isinstance(self.cli_install_url, Unset):
            cli_install_url = UNSET
        else:
            cli_install_url = self.cli_install_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_cli_ticket": has_cli_ticket,
            }
        )
        if cli_install_url is not UNSET:
            field_dict["cli_install_url"] = cli_install_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        has_cli_ticket = d.pop("has_cli_ticket")

        def _parse_cli_install_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cli_install_url = _parse_cli_install_url(d.pop("cli_install_url", UNSET))

        cli_status_response = cls(
            has_cli_ticket=has_cli_ticket,
            cli_install_url=cli_install_url,
        )

        cli_status_response.additional_properties = d
        return cli_status_response

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
