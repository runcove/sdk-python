"""``client.webhooks``: lifecycle webhook subscriptions and their deliveries.

Verify a delivery you receive with :func:`cove_sdk.verify_webhook_signature`.
"""

from __future__ import annotations

import builtins
import uuid
from collections.abc import AsyncIterator, Mapping
from typing import Any, cast

from ..._args import build_body, opt
from ..._generated.api.webhooks import (
    create_webhook,
    delete_webhook,
    disable_webhook,
    enable_webhook,
    get_webhook,
    get_webhook_delivery,
    list_webhook_deliveries,
    list_webhooks,
    replay_webhook_delivery,
    rotate_webhook_secret,
    test_webhook,
    update_webhook,
)
from ..._generated.models import (
    ReplayWebhookDeliveryResponse,
    RotateWebhookSecretResponse,
    TestDeliveryResult,
    WebhookCreateInput,
    WebhookDelivery,
    WebhookDeliveryPage,
    WebhookSubscription,
    WebhookUpdateInput,
)
from ..._operations import operation
from .._pagination import paginate
from .._transport import CLIENT_DEFAULT, AsyncCoveTransport, CallTimeout

Id = str | uuid.UUID


class Webhooks:
    """``client.webhooks`` — subscriptions (by id) and their delivery log."""

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("listWebhooks")
    async def list(
        self,
        *,
        scope: str | None = None,
        vm_id: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> builtins.list[WebhookSubscription]:
        """The caller's subscriptions, optionally by ``scope`` or ``vm_id``. Scope ``admin``."""
        subs = await self._t.call(
            list_webhooks, scope=opt(scope), vm_id=opt(vm_id), timeout=timeout
        )
        return cast(builtins.list[WebhookSubscription], subs)

    @operation("createWebhook")
    async def create(
        self,
        body: WebhookCreateInput | Mapping[str, Any] | None = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> WebhookSubscription:
        """Subscribe ``url`` to ``events`` in ``scope`` (``WebhookCreateInput``'s fields). Scope ``admin``.

        The response's ``secret`` is the signing secret, shown this once: capture it then. The
        returned model's repr prints that secret, so do not log the return value.
        """
        req = build_body(WebhookCreateInput, body, fields)
        sub = await self._t.call(create_webhook, body=req, timeout=timeout)
        return cast(WebhookSubscription, sub)

    @operation("getWebhook")
    async def get(
        self, id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> WebhookSubscription:
        """One subscription. Scope ``admin``."""
        sub = await self._t.call(get_webhook, path={"id": str(id)}, timeout=timeout)
        return cast(WebhookSubscription, sub)

    @operation("updateWebhook")
    async def update(
        self,
        id: Id,
        body: WebhookUpdateInput | Mapping[str, Any] | None = None,
        *,
        timeout: CallTimeout = CLIENT_DEFAULT,
        **fields: Any,
    ) -> WebhookSubscription:
        """Change a subscription (``WebhookUpdateInput``'s fields; only those given). Scope ``admin``."""
        req = build_body(WebhookUpdateInput, body, fields)
        sub = await self._t.call(
            update_webhook, path={"id": str(id)}, body=req, timeout=timeout
        )
        return cast(WebhookSubscription, sub)

    @operation("deleteWebhook")
    async def delete(self, id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT) -> None:
        """Delete a subscription. Scope ``admin``."""
        await self._t.call(delete_webhook, path={"id": str(id)}, timeout=timeout)

    @operation("rotateWebhookSecret")
    async def rotate_secret(
        self, id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> RotateWebhookSecretResponse:
        """A new signing secret, shown this once; the old one verifies during the grace period. Scope ``admin``.

        The returned model's repr prints the new secret, so do not log the return value.
        """
        result = await self._t.call(
            rotate_webhook_secret, path={"id": str(id)}, timeout=timeout
        )
        return cast(RotateWebhookSecretResponse, result)

    @operation("testWebhook")
    async def test(
        self, id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> TestDeliveryResult:
        """Send a test delivery now. Scope ``admin``."""
        result = await self._t.call(test_webhook, path={"id": str(id)}, timeout=timeout)
        return cast(TestDeliveryResult, result)

    @operation("disableWebhook")
    async def disable(
        self, id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> WebhookSubscription:
        """Stop deliveries to a subscription. Scope ``admin``."""
        sub = await self._t.call(disable_webhook, path={"id": str(id)}, timeout=timeout)
        return cast(WebhookSubscription, sub)

    @operation("enableWebhook")
    async def enable(
        self, id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> WebhookSubscription:
        """Resume deliveries to a subscription. Scope ``admin``."""
        sub = await self._t.call(enable_webhook, path={"id": str(id)}, timeout=timeout)
        return cast(WebhookSubscription, sub)

    @operation("listWebhookDeliveries")
    async def list_deliveries(
        self,
        id: Id,
        *,
        state: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> WebhookDeliveryPage:
        """One page of a subscription's deliveries, optionally by ``state``. Scope ``admin``."""
        page = await self._t.call(
            list_webhook_deliveries,
            path={"id": str(id)},
            state=opt(state),
            limit=opt(limit),
            cursor=opt(cursor),
            timeout=timeout,
        )
        return cast(WebhookDeliveryPage, page)

    async def iter_deliveries(
        self,
        id: Id,
        *,
        state: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> AsyncIterator[WebhookDelivery]:
        """Every delivery of a subscription, following ``next_cursor``."""

        async def fetch(c: str | None) -> WebhookDeliveryPage:
            return await self.list_deliveries(
                id, state=state, limit=limit, cursor=c, timeout=timeout
            )

        async for delivery in paginate(fetch, "deliveries", cursor=cursor):
            yield delivery

    @operation("getWebhookDelivery")
    async def get_delivery(
        self, id: Id, delivery_id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> WebhookDelivery:
        """One delivery of a subscription. Scope ``admin``."""
        delivery = await self._t.call(
            get_webhook_delivery,
            path={"id": str(id), "delivery_id": str(delivery_id)},
            timeout=timeout,
        )
        return cast(WebhookDelivery, delivery)

    @operation("replayWebhookDelivery")
    async def replay_delivery(
        self, id: Id, delivery_id: Id, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> ReplayWebhookDeliveryResponse:
        """Deliver a past event again, as a new delivery. Scope ``admin``."""
        result = await self._t.call(
            replay_webhook_delivery,
            path={"id": str(id), "delivery_id": str(delivery_id)},
            timeout=timeout,
        )
        return cast(ReplayWebhookDeliveryResponse, result)
