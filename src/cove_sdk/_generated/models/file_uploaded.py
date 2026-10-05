from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="FileUploaded")


@_attrs_define
class FileUploaded:
    """`PUT /vms/{name}/files` response body: the file as it was committed in the
    guest.

        Attributes:
            mode (int): The file's permission bits as a number (`420` is `0o644`).
            path (str): The absolute guest path the file was written to.
            sha256 (str): Lowercase hex SHA-256 of the bytes the server sent to the guest.
            size (int): Bytes written: always the request's `Content-Length`.
    """

    mode: int
    path: str
    sha256: str
    size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        path = self.path

        sha256 = self.sha256

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "path": path,
                "sha256": sha256,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        mode = d.pop("mode")

        path = d.pop("path")

        sha256 = d.pop("sha256")

        size = d.pop("size")

        file_uploaded = cls(
            mode=mode,
            path=path,
            sha256=sha256,
            size=size,
        )

        file_uploaded.additional_properties = d
        return file_uploaded

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
