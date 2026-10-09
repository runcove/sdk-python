from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offboard_api_key import OffboardApiKey
    from ..models.offboard_cli_session import OffboardCliSession
    from ..models.offboard_connected_app import OffboardConnectedApp
    from ..models.offboard_left_behind import OffboardLeftBehind
    from ..models.offboard_secret import OffboardSecret
    from ..models.offboard_service_key import OffboardServiceKey
    from ..models.offboard_session import OffboardSession
    from ..models.offboard_share import OffboardShare
    from ..models.offboard_ssh_key import OffboardSshKey
    from ..models.offboard_team import OffboardTeam
    from ..models.offboard_ticket import OffboardTicket
    from ..models.offboard_vm import OffboardVm
    from ..models.offboard_warpgate_role import OffboardWarpgateRole
    from ..models.offboard_warpgate_user import OffboardWarpgateUser
    from ..models.offboard_webhook import OffboardWebhook


T = TypeVar("T", bound="OffboardUserReport")


@_attrs_define
class OffboardUserReport:
    """`POST /api/admin/users/{username}/offboard` response body: everything
    offboarding ended, or would end when `dry_run` is true. The credential
    lists (`cli_sessions_revoked` through `webhooks_disabled`) were changed in
    one transaction; Warpgate SSH keys, tickets and sessions, teams, secrets
    and VMs are handled one by one afterwards and each carries its own
    result, so one failure never hides the others.

        Attributes:
            api_keys_revoked (list[OffboardApiKey]): The user's personal and admin API keys, revoked.
            cli_sessions_failed (list[OffboardCliSession]): CLI sessions Warpgate could not delete: they still work. Each is
                a
                failed item; a re-run retries them. Empty in a dry run.
            cli_sessions_revoked (int): CLI sessions (tickets) revoked.
            connected_apps_revoked (list[OffboardConnectedApp]): The user's connected apps, revoked.
            dry_run (bool): True when nothing was changed and this is only what would happen.
            secrets_deleted (list[OffboardSecret]): The user's own (user-scope) secrets, deleted, one result each.
            secrets_kept (str): Why secrets outside the user's own scope stay.
            service_keys (list[OffboardServiceKey]): Service keys bound to the user: binding ended, keys revoked.
            sessions_closed (list[OffboardSession]): The user's live Warpgate sessions on every target, closed after the
                tickets are deleted, one result each. Keys, tickets and sessions are
                handled again until a pass finds none left (at most three passes),
                and every pass is reported here. Empty when Cove runs without
                Warpgate.
            shares_withdrawn (list[OffboardShare]): Direct shares to the user withdrawn, on any VM.
            ssh_keys_deleted (list[OffboardSshKey]): The user's SSH public keys at Warpgate, deleted after the Warpgate
                user, one result each (deleting the user normally takes them with
                it, so this is usually empty). Empty when Cove runs without Warpgate.
            teams_left (list[OffboardTeam]): The teams the user was removed from, one result each.
            tickets_deleted (list[OffboardTicket]): The Warpgate tickets in the user's name, and every port invite the
                user minted on any VM (on a VM someone else owns it is a ticket in
                the owner's name; its `vm.invite.created` audit row names the user),
                deleted after the keys, one result each. Empty when Cove runs without
                Warpgate.
            username (str): Whose account this is.
            vms_stopped (list[OffboardVm]): The VMs the user owns, one result each.
            webhooks_disabled (list[OffboardWebhook]): The user's webhook subscriptions, disabled (`owner-offboarded`).
            disabled (bool | Unset): True when the person is now shut out of Cove (in a dry run: would
                be): every request they make, and anything that would hand them a
                credential or a way in, is refused with 403 `user_disabled` until an
                administrator enables them again (`POST
                /api/admin/users/{username}/enable`). False from a server that
                predates this.
            left_behind (None | OffboardLeftBehind | Unset):
            second_sweep_error (None | str | Unset): Set when the credential sweep that runs again after the Warpgate
                sessions are closed failed: anything a still-open session created in
                between may still be live, so run the offboarding again. A failed
                item. Never set in a dry run.
            warpgate_role (None | OffboardWarpgateRole | Unset):
            warpgate_user (None | OffboardWarpgateUser | Unset):
    """

    api_keys_revoked: list[OffboardApiKey]
    cli_sessions_failed: list[OffboardCliSession]
    cli_sessions_revoked: int
    connected_apps_revoked: list[OffboardConnectedApp]
    dry_run: bool
    secrets_deleted: list[OffboardSecret]
    secrets_kept: str
    service_keys: list[OffboardServiceKey]
    sessions_closed: list[OffboardSession]
    shares_withdrawn: list[OffboardShare]
    ssh_keys_deleted: list[OffboardSshKey]
    teams_left: list[OffboardTeam]
    tickets_deleted: list[OffboardTicket]
    username: str
    vms_stopped: list[OffboardVm]
    webhooks_disabled: list[OffboardWebhook]
    disabled: bool | Unset = UNSET
    left_behind: None | OffboardLeftBehind | Unset = UNSET
    second_sweep_error: None | str | Unset = UNSET
    warpgate_role: None | OffboardWarpgateRole | Unset = UNSET
    warpgate_user: None | OffboardWarpgateUser | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.offboard_left_behind import OffboardLeftBehind
        from ..models.offboard_warpgate_role import OffboardWarpgateRole
        from ..models.offboard_warpgate_user import OffboardWarpgateUser

        api_keys_revoked = []
        for api_keys_revoked_item_data in self.api_keys_revoked:
            api_keys_revoked_item = api_keys_revoked_item_data.to_dict()
            api_keys_revoked.append(api_keys_revoked_item)

        cli_sessions_failed = []
        for cli_sessions_failed_item_data in self.cli_sessions_failed:
            cli_sessions_failed_item = cli_sessions_failed_item_data.to_dict()
            cli_sessions_failed.append(cli_sessions_failed_item)

        cli_sessions_revoked = self.cli_sessions_revoked

        connected_apps_revoked = []
        for connected_apps_revoked_item_data in self.connected_apps_revoked:
            connected_apps_revoked_item = connected_apps_revoked_item_data.to_dict()
            connected_apps_revoked.append(connected_apps_revoked_item)

        dry_run = self.dry_run

        secrets_deleted = []
        for secrets_deleted_item_data in self.secrets_deleted:
            secrets_deleted_item = secrets_deleted_item_data.to_dict()
            secrets_deleted.append(secrets_deleted_item)

        secrets_kept = self.secrets_kept

        service_keys = []
        for service_keys_item_data in self.service_keys:
            service_keys_item = service_keys_item_data.to_dict()
            service_keys.append(service_keys_item)

        sessions_closed = []
        for sessions_closed_item_data in self.sessions_closed:
            sessions_closed_item = sessions_closed_item_data.to_dict()
            sessions_closed.append(sessions_closed_item)

        shares_withdrawn = []
        for shares_withdrawn_item_data in self.shares_withdrawn:
            shares_withdrawn_item = shares_withdrawn_item_data.to_dict()
            shares_withdrawn.append(shares_withdrawn_item)

        ssh_keys_deleted = []
        for ssh_keys_deleted_item_data in self.ssh_keys_deleted:
            ssh_keys_deleted_item = ssh_keys_deleted_item_data.to_dict()
            ssh_keys_deleted.append(ssh_keys_deleted_item)

        teams_left = []
        for teams_left_item_data in self.teams_left:
            teams_left_item = teams_left_item_data.to_dict()
            teams_left.append(teams_left_item)

        tickets_deleted = []
        for tickets_deleted_item_data in self.tickets_deleted:
            tickets_deleted_item = tickets_deleted_item_data.to_dict()
            tickets_deleted.append(tickets_deleted_item)

        username = self.username

        vms_stopped = []
        for vms_stopped_item_data in self.vms_stopped:
            vms_stopped_item = vms_stopped_item_data.to_dict()
            vms_stopped.append(vms_stopped_item)

        webhooks_disabled = []
        for webhooks_disabled_item_data in self.webhooks_disabled:
            webhooks_disabled_item = webhooks_disabled_item_data.to_dict()
            webhooks_disabled.append(webhooks_disabled_item)

        disabled = self.disabled

        left_behind: dict[str, Any] | None | Unset
        if isinstance(self.left_behind, Unset):
            left_behind = UNSET
        elif isinstance(self.left_behind, OffboardLeftBehind):
            left_behind = self.left_behind.to_dict()
        else:
            left_behind = self.left_behind

        second_sweep_error: None | str | Unset
        if isinstance(self.second_sweep_error, Unset):
            second_sweep_error = UNSET
        else:
            second_sweep_error = self.second_sweep_error

        warpgate_role: dict[str, Any] | None | Unset
        if isinstance(self.warpgate_role, Unset):
            warpgate_role = UNSET
        elif isinstance(self.warpgate_role, OffboardWarpgateRole):
            warpgate_role = self.warpgate_role.to_dict()
        else:
            warpgate_role = self.warpgate_role

        warpgate_user: dict[str, Any] | None | Unset
        if isinstance(self.warpgate_user, Unset):
            warpgate_user = UNSET
        elif isinstance(self.warpgate_user, OffboardWarpgateUser):
            warpgate_user = self.warpgate_user.to_dict()
        else:
            warpgate_user = self.warpgate_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_keys_revoked": api_keys_revoked,
                "cli_sessions_failed": cli_sessions_failed,
                "cli_sessions_revoked": cli_sessions_revoked,
                "connected_apps_revoked": connected_apps_revoked,
                "dry_run": dry_run,
                "secrets_deleted": secrets_deleted,
                "secrets_kept": secrets_kept,
                "service_keys": service_keys,
                "sessions_closed": sessions_closed,
                "shares_withdrawn": shares_withdrawn,
                "ssh_keys_deleted": ssh_keys_deleted,
                "teams_left": teams_left,
                "tickets_deleted": tickets_deleted,
                "username": username,
                "vms_stopped": vms_stopped,
                "webhooks_disabled": webhooks_disabled,
            }
        )
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if left_behind is not UNSET:
            field_dict["left_behind"] = left_behind
        if second_sweep_error is not UNSET:
            field_dict["second_sweep_error"] = second_sweep_error
        if warpgate_role is not UNSET:
            field_dict["warpgate_role"] = warpgate_role
        if warpgate_user is not UNSET:
            field_dict["warpgate_user"] = warpgate_user

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.offboard_api_key import OffboardApiKey
        from ..models.offboard_cli_session import OffboardCliSession
        from ..models.offboard_connected_app import (
            OffboardConnectedApp,
        )
        from ..models.offboard_left_behind import OffboardLeftBehind
        from ..models.offboard_secret import OffboardSecret
        from ..models.offboard_service_key import OffboardServiceKey
        from ..models.offboard_session import OffboardSession
        from ..models.offboard_share import OffboardShare
        from ..models.offboard_ssh_key import OffboardSshKey
        from ..models.offboard_team import OffboardTeam
        from ..models.offboard_ticket import OffboardTicket
        from ..models.offboard_vm import OffboardVm
        from ..models.offboard_warpgate_role import (
            OffboardWarpgateRole,
        )
        from ..models.offboard_warpgate_user import (
            OffboardWarpgateUser,
        )
        from ..models.offboard_webhook import OffboardWebhook

        d = dict(src_dict)
        api_keys_revoked = []
        _api_keys_revoked = d.pop("api_keys_revoked")
        for api_keys_revoked_item_data in _api_keys_revoked:
            api_keys_revoked_item = OffboardApiKey.from_dict(api_keys_revoked_item_data)

            api_keys_revoked.append(api_keys_revoked_item)

        cli_sessions_failed = []
        _cli_sessions_failed = d.pop("cli_sessions_failed")
        for cli_sessions_failed_item_data in _cli_sessions_failed:
            cli_sessions_failed_item = OffboardCliSession.from_dict(
                cli_sessions_failed_item_data
            )

            cli_sessions_failed.append(cli_sessions_failed_item)

        cli_sessions_revoked = d.pop("cli_sessions_revoked")

        connected_apps_revoked = []
        _connected_apps_revoked = d.pop("connected_apps_revoked")
        for connected_apps_revoked_item_data in _connected_apps_revoked:
            connected_apps_revoked_item = OffboardConnectedApp.from_dict(
                connected_apps_revoked_item_data
            )

            connected_apps_revoked.append(connected_apps_revoked_item)

        dry_run = d.pop("dry_run")

        secrets_deleted = []
        _secrets_deleted = d.pop("secrets_deleted")
        for secrets_deleted_item_data in _secrets_deleted:
            secrets_deleted_item = OffboardSecret.from_dict(secrets_deleted_item_data)

            secrets_deleted.append(secrets_deleted_item)

        secrets_kept = d.pop("secrets_kept")

        service_keys = []
        _service_keys = d.pop("service_keys")
        for service_keys_item_data in _service_keys:
            service_keys_item = OffboardServiceKey.from_dict(service_keys_item_data)

            service_keys.append(service_keys_item)

        sessions_closed = []
        _sessions_closed = d.pop("sessions_closed")
        for sessions_closed_item_data in _sessions_closed:
            sessions_closed_item = OffboardSession.from_dict(sessions_closed_item_data)

            sessions_closed.append(sessions_closed_item)

        shares_withdrawn = []
        _shares_withdrawn = d.pop("shares_withdrawn")
        for shares_withdrawn_item_data in _shares_withdrawn:
            shares_withdrawn_item = OffboardShare.from_dict(shares_withdrawn_item_data)

            shares_withdrawn.append(shares_withdrawn_item)

        ssh_keys_deleted = []
        _ssh_keys_deleted = d.pop("ssh_keys_deleted")
        for ssh_keys_deleted_item_data in _ssh_keys_deleted:
            ssh_keys_deleted_item = OffboardSshKey.from_dict(ssh_keys_deleted_item_data)

            ssh_keys_deleted.append(ssh_keys_deleted_item)

        teams_left = []
        _teams_left = d.pop("teams_left")
        for teams_left_item_data in _teams_left:
            teams_left_item = OffboardTeam.from_dict(teams_left_item_data)

            teams_left.append(teams_left_item)

        tickets_deleted = []
        _tickets_deleted = d.pop("tickets_deleted")
        for tickets_deleted_item_data in _tickets_deleted:
            tickets_deleted_item = OffboardTicket.from_dict(tickets_deleted_item_data)

            tickets_deleted.append(tickets_deleted_item)

        username = d.pop("username")

        vms_stopped = []
        _vms_stopped = d.pop("vms_stopped")
        for vms_stopped_item_data in _vms_stopped:
            vms_stopped_item = OffboardVm.from_dict(vms_stopped_item_data)

            vms_stopped.append(vms_stopped_item)

        webhooks_disabled = []
        _webhooks_disabled = d.pop("webhooks_disabled")
        for webhooks_disabled_item_data in _webhooks_disabled:
            webhooks_disabled_item = OffboardWebhook.from_dict(
                webhooks_disabled_item_data
            )

            webhooks_disabled.append(webhooks_disabled_item)

        disabled = d.pop("disabled", UNSET)

        def _parse_left_behind(data: object) -> None | OffboardLeftBehind | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                left_behind_type_1 = OffboardLeftBehind.from_dict(data)

                return left_behind_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OffboardLeftBehind | Unset, data)

        left_behind = _parse_left_behind(d.pop("left_behind", UNSET))

        def _parse_second_sweep_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        second_sweep_error = _parse_second_sweep_error(
            d.pop("second_sweep_error", UNSET)
        )

        def _parse_warpgate_role(data: object) -> None | OffboardWarpgateRole | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                warpgate_role_type_1 = OffboardWarpgateRole.from_dict(data)

                return warpgate_role_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OffboardWarpgateRole | Unset, data)

        warpgate_role = _parse_warpgate_role(d.pop("warpgate_role", UNSET))

        def _parse_warpgate_user(data: object) -> None | OffboardWarpgateUser | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                warpgate_user_type_1 = OffboardWarpgateUser.from_dict(data)

                return warpgate_user_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OffboardWarpgateUser | Unset, data)

        warpgate_user = _parse_warpgate_user(d.pop("warpgate_user", UNSET))

        offboard_user_report = cls(
            api_keys_revoked=api_keys_revoked,
            cli_sessions_failed=cli_sessions_failed,
            cli_sessions_revoked=cli_sessions_revoked,
            connected_apps_revoked=connected_apps_revoked,
            dry_run=dry_run,
            secrets_deleted=secrets_deleted,
            secrets_kept=secrets_kept,
            service_keys=service_keys,
            sessions_closed=sessions_closed,
            shares_withdrawn=shares_withdrawn,
            ssh_keys_deleted=ssh_keys_deleted,
            teams_left=teams_left,
            tickets_deleted=tickets_deleted,
            username=username,
            vms_stopped=vms_stopped,
            webhooks_disabled=webhooks_disabled,
            disabled=disabled,
            left_behind=left_behind,
            second_sweep_error=second_sweep_error,
            warpgate_role=warpgate_role,
            warpgate_user=warpgate_user,
        )

        offboard_user_report.additional_properties = d
        return offboard_user_report

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
