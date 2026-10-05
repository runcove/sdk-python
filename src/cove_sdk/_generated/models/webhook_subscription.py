from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tag_filter import TagFilter
    from ..models.webhook_scope import WebhookScope


T = TypeVar("T", bound="WebhookSubscription")


@_attrs_define
class WebhookSubscription:
    """Wire shape of a subscription, returned by every subscription endpoint
    except rotate (`POST/GET/PUT/DELETE /api/webhooks[/{id}]`, `.../disable`,
    `.../enable`). Field-for-field what `handlers::webhooks::sub_to_json`
    builds from a [`Subscription`] — kept here, next to the domain type it
    mirrors, so a field added to one and not the other is easy to spot.

        Attributes:
            consec_fail_count (int):
            created_at (datetime.datetime):
            events (list[str]): Sorted event-kind strings the subscription matches (exact-match
                dispatch, e.g. `"vm.stopped"`). `keys.*` kinds are rejected at creation.
            id (UUID): UUID v7, internal row identity.
            owner_username (str):
            scope (WebhookScope): Wire shape of [`Subscription`]`.scope`, as hand-built by
                `handlers::webhooks::sub_to_json` (`SubscriptionScope`'s own derive can't
                produce this — see that type's doc comment).
            url (str): Canonical webhook target URL.
            allowed_subnets (None | str | Unset): CSV of allowed CIDR overrides for the SSRF guard (`None` = global
                default).
            description (None | str | Unset):
            disabled_at (datetime.datetime | None | Unset):
            disabled_reason (None | str | Unset):
            last_failure_at (datetime.datetime | None | Unset):
            last_success_at (datetime.datetime | None | Unset):
            secret (None | str | Unset): The `whsec_<64 hex>` HMAC signing secret. `null` on every response
                this schema describes — it is populated only in the **create**
                response (`POST /api/webhooks`), which does not reuse this schema for
                that reason (see its own `responses(...)` in `handlers::webhooks`).
                Rotation returns a fresh secret too, but via the separate
                `RotateWebhookSecretResponse` shape below, never this one. There is no
                way to retrieve a previously-issued secret again after either moment
                passes — capture it then.
            tag_filter (None | TagFilter | Unset):
    """

    consec_fail_count: int
    created_at: datetime.datetime
    events: list[str]
    id: UUID
    owner_username: str
    scope: WebhookScope
    url: str
    allowed_subnets: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    disabled_at: datetime.datetime | None | Unset = UNSET
    disabled_reason: None | str | Unset = UNSET
    last_failure_at: datetime.datetime | None | Unset = UNSET
    last_success_at: datetime.datetime | None | Unset = UNSET
    secret: None | str | Unset = UNSET
    tag_filter: None | TagFilter | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.tag_filter import TagFilter

        consec_fail_count = self.consec_fail_count

        created_at = self.created_at.isoformat()

        events = self.events

        id = str(self.id)

        owner_username = self.owner_username

        scope = self.scope.to_dict()

        url = self.url

        allowed_subnets: None | str | Unset
        if isinstance(self.allowed_subnets, Unset):
            allowed_subnets = UNSET
        else:
            allowed_subnets = self.allowed_subnets

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        disabled_at: None | str | Unset
        if isinstance(self.disabled_at, Unset):
            disabled_at = UNSET
        elif isinstance(self.disabled_at, datetime.datetime):
            disabled_at = self.disabled_at.isoformat()
        else:
            disabled_at = self.disabled_at

        disabled_reason: None | str | Unset
        if isinstance(self.disabled_reason, Unset):
            disabled_reason = UNSET
        else:
            disabled_reason = self.disabled_reason

        last_failure_at: None | str | Unset
        if isinstance(self.last_failure_at, Unset):
            last_failure_at = UNSET
        elif isinstance(self.last_failure_at, datetime.datetime):
            last_failure_at = self.last_failure_at.isoformat()
        else:
            last_failure_at = self.last_failure_at

        last_success_at: None | str | Unset
        if isinstance(self.last_success_at, Unset):
            last_success_at = UNSET
        elif isinstance(self.last_success_at, datetime.datetime):
            last_success_at = self.last_success_at.isoformat()
        else:
            last_success_at = self.last_success_at

        secret: None | str | Unset
        if isinstance(self.secret, Unset):
            secret = UNSET
        else:
            secret = self.secret

        tag_filter: dict[str, Any] | None | Unset
        if isinstance(self.tag_filter, Unset):
            tag_filter = UNSET
        elif isinstance(self.tag_filter, TagFilter):
            tag_filter = self.tag_filter.to_dict()
        else:
            tag_filter = self.tag_filter

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "consec_fail_count": consec_fail_count,
                "created_at": created_at,
                "events": events,
                "id": id,
                "owner_username": owner_username,
                "scope": scope,
                "url": url,
            }
        )
        if allowed_subnets is not UNSET:
            field_dict["allowed_subnets"] = allowed_subnets
        if description is not UNSET:
            field_dict["description"] = description
        if disabled_at is not UNSET:
            field_dict["disabled_at"] = disabled_at
        if disabled_reason is not UNSET:
            field_dict["disabled_reason"] = disabled_reason
        if last_failure_at is not UNSET:
            field_dict["last_failure_at"] = last_failure_at
        if last_success_at is not UNSET:
            field_dict["last_success_at"] = last_success_at
        if secret is not UNSET:
            field_dict["secret"] = secret
        if tag_filter is not UNSET:
            field_dict["tag_filter"] = tag_filter

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.tag_filter import TagFilter
        from ..models.webhook_scope import WebhookScope

        d = dict(src_dict)
        consec_fail_count = d.pop("consec_fail_count")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        events = cast(list[str], d.pop("events"))

        id = UUID(d.pop("id"))

        owner_username = d.pop("owner_username")

        scope = WebhookScope.from_dict(d.pop("scope"))

        url = d.pop("url")

        def _parse_allowed_subnets(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        allowed_subnets = _parse_allowed_subnets(d.pop("allowed_subnets", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_disabled_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                disabled_at_type_0 = datetime.datetime.fromisoformat(data)

                return disabled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        disabled_at = _parse_disabled_at(d.pop("disabled_at", UNSET))

        def _parse_disabled_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        disabled_reason = _parse_disabled_reason(d.pop("disabled_reason", UNSET))

        def _parse_last_failure_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_failure_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_failure_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_failure_at = _parse_last_failure_at(d.pop("last_failure_at", UNSET))

        def _parse_last_success_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_success_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_success_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_success_at = _parse_last_success_at(d.pop("last_success_at", UNSET))

        def _parse_secret(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        secret = _parse_secret(d.pop("secret", UNSET))

        def _parse_tag_filter(data: object) -> None | TagFilter | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tag_filter_type_1 = TagFilter.from_dict(data)

                return tag_filter_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TagFilter | Unset, data)

        tag_filter = _parse_tag_filter(d.pop("tag_filter", UNSET))

        webhook_subscription = cls(
            consec_fail_count=consec_fail_count,
            created_at=created_at,
            events=events,
            id=id,
            owner_username=owner_username,
            scope=scope,
            url=url,
            allowed_subnets=allowed_subnets,
            description=description,
            disabled_at=disabled_at,
            disabled_reason=disabled_reason,
            last_failure_at=last_failure_at,
            last_success_at=last_success_at,
            secret=secret,
            tag_filter=tag_filter,
        )

        webhook_subscription.additional_properties = d
        return webhook_subscription

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
