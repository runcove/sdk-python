from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inject_selector_type_0 import InjectSelectorType0
    from ..models.inject_selector_type_1 import InjectSelectorType1
    from ..models.inject_selector_type_2 import InjectSelectorType2


T = TypeVar("T", bound="ExecWithSecretsRequest")


@_attrs_define
class ExecWithSecretsRequest:
    """POST /vms/{name}/exec-with-secrets request body.

    The buffered, secrets-injected form of exec, split out of `/exec` because
    one route cannot answer with both an SSE stream and a JSON body in any
    describable way. `selector` is REQUIRED here — it is what the operation is
    for — where on `ExecRequestDto` it is the optional field that used to switch
    `/exec` between its two response shapes.

    `timeout_secs` bounds the command as it does on `ExecRequestDto`: past it
    the guest kills the command's process group and the response is exit 124
    with `timed_out`. The `setup_tag` wipe still runs afterwards.

    A field this operation does not define is refused with 400
    `validation_failed` naming it, not ignored: a caller that sends an option
    it lacks (a typo, or an exec option added after this one) would otherwise
    get the command run without it.

        Attributes:
            command (list[str]): argv, first element is the program. Must not be empty.
            selector (InjectSelectorType0 | InjectSelectorType1 | InjectSelectorType2): Which secrets a single
                `exec_with_inject` invocation should push to
                the guest before running the command.

                Defined in cove-service rather than cove-api-client because the
                service crate doesn't take a wire-types dependency for this one
                enum — and the public surface is stable enough that re-defining it
                in the wire crate later is a safe additive change.

                The values:
                * `All` — every secret currently attached to the VM (the default
                  `cove exec --inject` shape).
                * `Subset(names)` — caller-curated allowlist: only the named secrets
                  are injected.
                * `SetupTag(tag)` — `Lifetime::SetupOnly { tag }` rows only;
                  wiped post-exec (host + guest) so secrets vanish after the setup
                  phase regardless of the command's exit status.
            timeout_secs (int | None | Unset): Seconds the command may run (default 30, at most 3600; a larger
                value is refused with 400 `validation_failed`). Past it the guest
                kills the command's whole process group and the result is
                `exit_code` 124 with `timed_out: true`.
    """

    command: list[str]
    selector: InjectSelectorType0 | InjectSelectorType1 | InjectSelectorType2
    timeout_secs: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.inject_selector_type_0 import InjectSelectorType0
        from ..models.inject_selector_type_1 import InjectSelectorType1

        command = self.command

        selector: dict[str, Any]
        if isinstance(self.selector, InjectSelectorType0) or isinstance(
            self.selector, InjectSelectorType1
        ):
            selector = self.selector.to_dict()
        else:
            selector = self.selector.to_dict()

        timeout_secs: int | None | Unset
        if isinstance(self.timeout_secs, Unset):
            timeout_secs = UNSET
        else:
            timeout_secs = self.timeout_secs

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "command": command,
                "selector": selector,
            }
        )
        if timeout_secs is not UNSET:
            field_dict["timeout_secs"] = timeout_secs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inject_selector_type_0 import InjectSelectorType0
        from ..models.inject_selector_type_1 import InjectSelectorType1
        from ..models.inject_selector_type_2 import InjectSelectorType2

        d = dict(src_dict)
        command = cast(list[str], d.pop("command"))

        def _parse_selector(
            data: object,
        ) -> InjectSelectorType0 | InjectSelectorType1 | InjectSelectorType2:
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
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_inject_selector_type_2 = InjectSelectorType2.from_dict(
                data
            )

            return componentsschemas_inject_selector_type_2

        selector = _parse_selector(d.pop("selector"))

        def _parse_timeout_secs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timeout_secs = _parse_timeout_secs(d.pop("timeout_secs", UNSET))

        exec_with_secrets_request = cls(
            command=command,
            selector=selector,
            timeout_secs=timeout_secs,
        )

        return exec_with_secrets_request
