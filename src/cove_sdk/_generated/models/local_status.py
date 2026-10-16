from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_update import ImageUpdate
    from ..models.shadowing_route import ShadowingRoute


T = TypeVar("T", bound="LocalStatus")


@_attrs_define
class LocalStatus:
    """What a Mac's local daemon runs beside its VMs, within the system status.
    On a Mac `ch_processes` counts the VM helpers (one
    `cove __vz-helper` per running or paused VM), and there are no TAP
    devices or warm pool.

        Attributes:
            bastion_ssh_port (int | None | Unset): The embedded Warpgate's SSH port on `127.0.0.1` when it serves.
            bastion_unavailable (None | str | Unset): Why the embedded Warpgate isn't serving; absent when it is.
            guest_ram_cap_mb (int | None | Unset): The cap on the guest RAM running VMs may hold, in MB: `[capacity]
                mac_max_guest_ram_fraction` of this Mac's RAM, which create and start
                are admitted against (VZ wires guest memory). Absent when the Mac's
                RAM couldn't be read at daemon start.
            image_update (ImageUpdate | None | Unset):
            network_owner_gateway (None | str | Unset): The network owner's gateway when it answers its control socket;
                absent when it doesn't.
            shadowing_routes (list[ShadowingRoute] | Unset): Another program's routes that take some of the VM subnet away
                from
                vmnet's interface, as the daemon last found them (after its startup
                pass, then every 30 s). Empty when there are none, and from older
                daemons.
    """

    bastion_ssh_port: int | None | Unset = UNSET
    bastion_unavailable: None | str | Unset = UNSET
    guest_ram_cap_mb: int | None | Unset = UNSET
    image_update: ImageUpdate | None | Unset = UNSET
    network_owner_gateway: None | str | Unset = UNSET
    shadowing_routes: list[ShadowingRoute] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.image_update import ImageUpdate

        bastion_ssh_port: int | None | Unset
        if isinstance(self.bastion_ssh_port, Unset):
            bastion_ssh_port = UNSET
        else:
            bastion_ssh_port = self.bastion_ssh_port

        bastion_unavailable: None | str | Unset
        if isinstance(self.bastion_unavailable, Unset):
            bastion_unavailable = UNSET
        else:
            bastion_unavailable = self.bastion_unavailable

        guest_ram_cap_mb: int | None | Unset
        if isinstance(self.guest_ram_cap_mb, Unset):
            guest_ram_cap_mb = UNSET
        else:
            guest_ram_cap_mb = self.guest_ram_cap_mb

        image_update: dict[str, Any] | None | Unset
        if isinstance(self.image_update, Unset):
            image_update = UNSET
        elif isinstance(self.image_update, ImageUpdate):
            image_update = self.image_update.to_dict()
        else:
            image_update = self.image_update

        network_owner_gateway: None | str | Unset
        if isinstance(self.network_owner_gateway, Unset):
            network_owner_gateway = UNSET
        else:
            network_owner_gateway = self.network_owner_gateway

        shadowing_routes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.shadowing_routes, Unset):
            shadowing_routes = []
            for shadowing_routes_item_data in self.shadowing_routes:
                shadowing_routes_item = shadowing_routes_item_data.to_dict()
                shadowing_routes.append(shadowing_routes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bastion_ssh_port is not UNSET:
            field_dict["bastion_ssh_port"] = bastion_ssh_port
        if bastion_unavailable is not UNSET:
            field_dict["bastion_unavailable"] = bastion_unavailable
        if guest_ram_cap_mb is not UNSET:
            field_dict["guest_ram_cap_mb"] = guest_ram_cap_mb
        if image_update is not UNSET:
            field_dict["image_update"] = image_update
        if network_owner_gateway is not UNSET:
            field_dict["network_owner_gateway"] = network_owner_gateway
        if shadowing_routes is not UNSET:
            field_dict["shadowing_routes"] = shadowing_routes

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.image_update import ImageUpdate
        from ..models.shadowing_route import ShadowingRoute

        d = dict(src_dict)

        def _parse_bastion_ssh_port(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        bastion_ssh_port = _parse_bastion_ssh_port(d.pop("bastion_ssh_port", UNSET))

        def _parse_bastion_unavailable(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bastion_unavailable = _parse_bastion_unavailable(
            d.pop("bastion_unavailable", UNSET)
        )

        def _parse_guest_ram_cap_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        guest_ram_cap_mb = _parse_guest_ram_cap_mb(d.pop("guest_ram_cap_mb", UNSET))

        def _parse_image_update(data: object) -> ImageUpdate | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                image_update_type_1 = ImageUpdate.from_dict(data)

                return image_update_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ImageUpdate | None | Unset, data)

        image_update = _parse_image_update(d.pop("image_update", UNSET))

        def _parse_network_owner_gateway(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        network_owner_gateway = _parse_network_owner_gateway(
            d.pop("network_owner_gateway", UNSET)
        )

        _shadowing_routes = d.pop("shadowing_routes", UNSET)
        shadowing_routes: list[ShadowingRoute] | Unset = UNSET
        if _shadowing_routes is not UNSET:
            shadowing_routes = []
            for shadowing_routes_item_data in _shadowing_routes:
                shadowing_routes_item = ShadowingRoute.from_dict(
                    shadowing_routes_item_data
                )

                shadowing_routes.append(shadowing_routes_item)

        local_status = cls(
            bastion_ssh_port=bastion_ssh_port,
            bastion_unavailable=bastion_unavailable,
            guest_ram_cap_mb=guest_ram_cap_mb,
            image_update=image_update,
            network_owner_gateway=network_owner_gateway,
            shadowing_routes=shadowing_routes,
        )

        local_status.additional_properties = d
        return local_status

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
