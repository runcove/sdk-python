from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RotateWebhookSecretResponse")


@_attrs_define
class RotateWebhookSecretResponse:
    """Response of `POST /api/webhooks/{id}/rotate`
    (`handlers::webhooks::rotate_secret`). Not named in the outgoing
    hand-written spec (it was an inline object there) — named here per
    `crate::openapi`'s rule 3.

        Attributes:
            rotated_at (datetime.datetime):
            secret (str): The new `whsec_<64 hex>` signing secret. Shown exactly once — capture
                it now. During the configured grace window
                (`[webhooks] secret_rotation_grace_seconds`, default 24h) deliveries
                are dual-signed with both the old and new secret; after grace expires
                the old secret is dropped and only this one verifies.
    """

    rotated_at: datetime.datetime
    secret: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rotated_at = self.rotated_at.isoformat()

        secret = self.secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rotated_at": rotated_at,
                "secret": secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        rotated_at = datetime.datetime.fromisoformat(d.pop("rotated_at"))

        secret = d.pop("secret")

        rotate_webhook_secret_response = cls(
            rotated_at=rotated_at,
            secret=secret,
        )

        rotate_webhook_secret_response.additional_properties = d
        return rotate_webhook_secret_response

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
