from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offboard_minted_key import OffboardMintedKey
    from ..models.offboard_port_invite import OffboardPortInvite
    from ..models.offboard_service_vm import OffboardServiceVm
    from ..models.offboard_service_webhook import OffboardServiceWebhook


T = TypeVar("T", bound="OffboardLeftBehind")


@_attrs_define
class OffboardLeftBehind:
    """What offboarding leaves in place because it is not the person's own, and
    an administrator must look at: offboarding reports it and never ends it.

        Attributes:
            in_auth_admins (bool): The person is listed in `[auth] admins` (names compared regardless of
                case). Offboarding cannot change the config: take them out and
                restart Cove.
            minted_keys (list[OffboardMintedKey]): Team and service keys the person minted (or rotated) that still
                work, read from the `keys.issued` and `keys.team_created` audit rows
                written in their name. The audit log is the only record of who minted
                a key, so a key whose row was pruned from it is not listed. A team or service key belongs to its team or
                service, not to the person, so offboarding leaves it active; they
                saw its token when they minted it. Rotate or revoke each one. The
                service keys bound to the person themselves are not listed here:
                offboarding revokes those (`service_keys`).
            port_invites (list[OffboardPortInvite]): Port invites the person made on VMs that are not theirs, from the
                `vm.invite.created` audit rows written in their name, less those a
                `vm.invite.revoked` row ended and less those offboarding revoked
                itself (its ticket sweep deletes every ticket whose invite row names
                the person). Only an invite offboarding could NOT revoke is listed:
                its ticket delete failed, the ticket listing failed, or Warpgate was
                not asked. An invite is a ticket in the VM owner's name, with no use
                limit: the person saw its URL and it works until it expires. The
                audit log does not record an invite's expiry, so one listed may
                already have expired: `cove share invites <vm>` shows the live ones.
            service_vms (list[OffboardServiceVm]): The live VMs owned by the services bound to the person (`svc:<name>`
                of each of their member bindings, ended or not). Offboarding revokes
                those services' keys but leaves their VMs as they are, running or
                not: reassign, stop or delete them.
            service_webhooks (list[OffboardServiceWebhook]): The active webhook subscriptions owned by the services bound to
                the
                person. They still deliver to the endpoint they were created with:
                disable or delete them.
            error (None | str | Unset): Why the lists above could not be read, when they could not: they may
                then be incomplete. A failed item; run the offboarding again.
    """

    in_auth_admins: bool
    minted_keys: list[OffboardMintedKey]
    port_invites: list[OffboardPortInvite]
    service_vms: list[OffboardServiceVm]
    service_webhooks: list[OffboardServiceWebhook]
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        in_auth_admins = self.in_auth_admins

        minted_keys = []
        for minted_keys_item_data in self.minted_keys:
            minted_keys_item = minted_keys_item_data.to_dict()
            minted_keys.append(minted_keys_item)

        port_invites = []
        for port_invites_item_data in self.port_invites:
            port_invites_item = port_invites_item_data.to_dict()
            port_invites.append(port_invites_item)

        service_vms = []
        for service_vms_item_data in self.service_vms:
            service_vms_item = service_vms_item_data.to_dict()
            service_vms.append(service_vms_item)

        service_webhooks = []
        for service_webhooks_item_data in self.service_webhooks:
            service_webhooks_item = service_webhooks_item_data.to_dict()
            service_webhooks.append(service_webhooks_item)

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "in_auth_admins": in_auth_admins,
                "minted_keys": minted_keys,
                "port_invites": port_invites,
                "service_vms": service_vms,
                "service_webhooks": service_webhooks,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.offboard_minted_key import OffboardMintedKey
        from ..models.offboard_port_invite import OffboardPortInvite
        from ..models.offboard_service_vm import OffboardServiceVm
        from ..models.offboard_service_webhook import (
            OffboardServiceWebhook,
        )

        d = dict(src_dict)
        in_auth_admins = d.pop("in_auth_admins")

        minted_keys = []
        _minted_keys = d.pop("minted_keys")
        for minted_keys_item_data in _minted_keys:
            minted_keys_item = OffboardMintedKey.from_dict(minted_keys_item_data)

            minted_keys.append(minted_keys_item)

        port_invites = []
        _port_invites = d.pop("port_invites")
        for port_invites_item_data in _port_invites:
            port_invites_item = OffboardPortInvite.from_dict(port_invites_item_data)

            port_invites.append(port_invites_item)

        service_vms = []
        _service_vms = d.pop("service_vms")
        for service_vms_item_data in _service_vms:
            service_vms_item = OffboardServiceVm.from_dict(service_vms_item_data)

            service_vms.append(service_vms_item)

        service_webhooks = []
        _service_webhooks = d.pop("service_webhooks")
        for service_webhooks_item_data in _service_webhooks:
            service_webhooks_item = OffboardServiceWebhook.from_dict(
                service_webhooks_item_data
            )

            service_webhooks.append(service_webhooks_item)

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        offboard_left_behind = cls(
            in_auth_admins=in_auth_admins,
            minted_keys=minted_keys,
            port_invites=port_invites,
            service_vms=service_vms,
            service_webhooks=service_webhooks,
            error=error,
        )

        offboard_left_behind.additional_properties = d
        return offboard_left_behind

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
