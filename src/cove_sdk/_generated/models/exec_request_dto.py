from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.exec_request_dto_env_type_0 import ExecRequestDtoEnvType0
    from ..models.inject_selector_type_0 import InjectSelectorType0
    from ..models.inject_selector_type_1 import InjectSelectorType1
    from ..models.inject_selector_type_2 import InjectSelectorType2


T = TypeVar("T", bound="ExecRequestDto")


@_attrs_define
class ExecRequestDto:
    """POST /vms/{name}/exec request body.

    Attributes:
        command (list[str]):
        cwd (None | str | Unset): Working directory for the command. A relative path resolves against
            the home directory of the account it runs as. Default: that home
            directory (`/root`).
        env (ExecRequestDtoEnvType0 | None | Unset): Extra environment variables, set last so they win over the defaults
            (`PATH` included). At most 128, each name at most 256 bytes with no
            `=`; names and values must not contain NUL.
        login (bool | None | Unset): Run the command through the account's login shell (`<shell> -l -c`),
            so its profile files apply (for example tools a profile script adds
            to `PATH`). Default `false`: the command gets a login-like
            environment without any profile file being run.
        selector (InjectSelectorType0 | InjectSelectorType1 | InjectSelectorType2 | None | Unset):
        timeout_secs (int | None | Unset): Seconds the command may run (default 30). Past it the guest kills the
            command's whole process group and the stream ends with `exit`
            `{"code": 124, "timed_out": true}`.
        user (None | str | Unset): Account to run the command as, by name in the VM's `/etc/passwd`.
            Default: root.
    """

    command: list[str]
    cwd: None | str | Unset = UNSET
    env: ExecRequestDtoEnvType0 | None | Unset = UNSET
    login: bool | None | Unset = UNSET
    selector: (
        InjectSelectorType0 | InjectSelectorType1 | InjectSelectorType2 | None | Unset
    ) = UNSET
    timeout_secs: int | None | Unset = UNSET
    user: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.exec_request_dto_env_type_0 import (
            ExecRequestDtoEnvType0,
        )
        from ..models.inject_selector_type_0 import InjectSelectorType0
        from ..models.inject_selector_type_1 import InjectSelectorType1
        from ..models.inject_selector_type_2 import InjectSelectorType2

        command = self.command

        cwd: None | str | Unset
        if isinstance(self.cwd, Unset):
            cwd = UNSET
        else:
            cwd = self.cwd

        env: dict[str, Any] | None | Unset
        if isinstance(self.env, Unset):
            env = UNSET
        elif isinstance(self.env, ExecRequestDtoEnvType0):
            env = self.env.to_dict()
        else:
            env = self.env

        login: bool | None | Unset
        if isinstance(self.login, Unset):
            login = UNSET
        else:
            login = self.login

        selector: dict[str, Any] | None | Unset
        if isinstance(self.selector, Unset):
            selector = UNSET
        elif (
            isinstance(self.selector, InjectSelectorType0)
            or isinstance(self.selector, InjectSelectorType1)
            or isinstance(self.selector, InjectSelectorType2)
        ):
            selector = self.selector.to_dict()
        else:
            selector = self.selector

        timeout_secs: int | None | Unset
        if isinstance(self.timeout_secs, Unset):
            timeout_secs = UNSET
        else:
            timeout_secs = self.timeout_secs

        user: None | str | Unset
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command": command,
            }
        )
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if env is not UNSET:
            field_dict["env"] = env
        if login is not UNSET:
            field_dict["login"] = login
        if selector is not UNSET:
            field_dict["selector"] = selector
        if timeout_secs is not UNSET:
            field_dict["timeout_secs"] = timeout_secs
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.exec_request_dto_env_type_0 import (
            ExecRequestDtoEnvType0,
        )
        from ..models.inject_selector_type_0 import InjectSelectorType0
        from ..models.inject_selector_type_1 import InjectSelectorType1
        from ..models.inject_selector_type_2 import InjectSelectorType2

        d = dict(src_dict)
        command = cast(list[str], d.pop("command"))

        def _parse_cwd(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cwd = _parse_cwd(d.pop("cwd", UNSET))

        def _parse_env(data: object) -> ExecRequestDtoEnvType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                env_type_0 = ExecRequestDtoEnvType0.from_dict(data)

                return env_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExecRequestDtoEnvType0 | None | Unset, data)

        env = _parse_env(d.pop("env", UNSET))

        def _parse_login(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        login = _parse_login(d.pop("login", UNSET))

        def _parse_selector(
            data: object,
        ) -> (
            InjectSelectorType0
            | InjectSelectorType1
            | InjectSelectorType2
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_inject_selector_type_0 = (
                    InjectSelectorType0.from_dict(data)
                )

                return componentsschemas_inject_selector_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_inject_selector_type_1 = (
                    InjectSelectorType1.from_dict(data)
                )

                return componentsschemas_inject_selector_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_inject_selector_type_2 = (
                    InjectSelectorType2.from_dict(data)
                )

                return componentsschemas_inject_selector_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                InjectSelectorType0
                | InjectSelectorType1
                | InjectSelectorType2
                | None
                | Unset,
                data,
            )

        selector = _parse_selector(d.pop("selector", UNSET))

        def _parse_timeout_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timeout_secs = _parse_timeout_secs(d.pop("timeout_secs", UNSET))

        def _parse_user(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user = _parse_user(d.pop("user", UNSET))

        exec_request_dto = cls(
            command=command,
            cwd=cwd,
            env=env,
            login=login,
            selector=selector,
            timeout_secs=timeout_secs,
            user=user,
        )

        exec_request_dto.additional_properties = d
        return exec_request_dto

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
