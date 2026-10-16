from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.image_update_state import ImageUpdateState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_progress import TransferProgress


T = TypeVar("T", bound="ImageUpdate")


@_attrs_define
class ImageUpdate:
    """A Mac's box against the one the daemon would fetch now (the config's
    `[image] mac_box_url`, else the build's): `local.image_update` in the
    system status, and the answer to `POST /api/images/update`. Box updates
    are never automatic: `cove images update` (or the web UI's button)
    starts one.

        Attributes:
            image (str): The image the box provides (`ubuntu-2404-arm64`).
            state (ImageUpdateState): Where a Mac's box stands (`ImageUpdate.state`).
            available_version (None | str | Unset): The version an update would install, when it is not the installed
                box or that can't be told (`unknown` when its file name carries
                none).
            error (None | str | Unset): Why the last update failed, until another starts. The installed box
                is unchanged by a failure.
            installed_version (None | str | Unset): The installed box's version (from its file name); absent for a box
                unpacked before cove recorded it.
            message (None | str | Unset):
            stage (None | str | Unset): While updating: the stage (`DownloadingImage`, `VerifyingImage`,
                `UnpackingImage`, `OptimisingImage`, `SwitchingImage`), what it is
                doing, and how far it has got, as a create's progress event carries
                them.
            transfer (None | TransferProgress | Unset):
    """

    image: str
    state: ImageUpdateState
    available_version: None | str | Unset = UNSET
    error: None | str | Unset = UNSET
    installed_version: None | str | Unset = UNSET
    message: None | str | Unset = UNSET
    stage: None | str | Unset = UNSET
    transfer: None | TransferProgress | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.transfer_progress import TransferProgress

        image = self.image

        state = self.state.value

        available_version: None | str | Unset
        if isinstance(self.available_version, Unset):
            available_version = UNSET
        else:
            available_version = self.available_version

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        installed_version: None | str | Unset
        if isinstance(self.installed_version, Unset):
            installed_version = UNSET
        else:
            installed_version = self.installed_version

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        stage: None | str | Unset
        if isinstance(self.stage, Unset):
            stage = UNSET
        else:
            stage = self.stage

        transfer: dict[str, Any] | None | Unset
        if isinstance(self.transfer, Unset):
            transfer = UNSET
        elif isinstance(self.transfer, TransferProgress):
            transfer = self.transfer.to_dict()
        else:
            transfer = self.transfer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "state": state,
            }
        )
        if available_version is not UNSET:
            field_dict["available_version"] = available_version
        if error is not UNSET:
            field_dict["error"] = error
        if installed_version is not UNSET:
            field_dict["installed_version"] = installed_version
        if message is not UNSET:
            field_dict["message"] = message
        if stage is not UNSET:
            field_dict["stage"] = stage
        if transfer is not UNSET:
            field_dict["transfer"] = transfer

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.transfer_progress import TransferProgress

        d = dict(src_dict)
        image = d.pop("image")

        state = ImageUpdateState(d.pop("state"))

        def _parse_available_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        available_version = _parse_available_version(d.pop("available_version", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_installed_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        installed_version = _parse_installed_version(d.pop("installed_version", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_stage(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        stage = _parse_stage(d.pop("stage", UNSET))

        def _parse_transfer(data: object) -> None | TransferProgress | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                transfer_type_1 = TransferProgress.from_dict(data)

                return transfer_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TransferProgress | Unset, data)

        transfer = _parse_transfer(d.pop("transfer", UNSET))

        image_update = cls(
            image=image,
            state=state,
            available_version=available_version,
            error=error,
            installed_version=installed_version,
            message=message,
            stage=stage,
            transfer=transfer,
        )

        image_update.additional_properties = d
        return image_update

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
