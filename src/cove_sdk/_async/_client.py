"""The Cove client (async; mirrored to CoveClient by unasync).

The client owns the transport, the credential and the lifecycle; the API is reached through its
resource groups (``client.vms``, ``client.admin``, ...), one attribute per group.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import TracebackType
from typing import Self

import httpx

from ..auth import CoveAuth, resolve_auth
from ._transport import DEFAULT_TIMEOUT, AsyncCoveTransport, TimeoutArg
from .resources.admin import Admin
from .resources.audit import Audit
from .resources.checkpoints import Checkpoints
from .resources.events import Events
from .resources.host import Host
from .resources.keys import Keys
from .resources.meta import Meta
from .resources.policies import Policies
from .resources.secrets import Secrets
from .resources.tags import Tags
from .resources.teams import Teams
from .resources.vms import Vms
from .resources.webhooks import Webhooks


class AsyncCoveClient:
    """A client for one Cove deployment.

    Pass exactly one credential: ``token=`` (a ``cvk_`` service key, for the external bearer
    listener), ``ticket=`` (a Warpgate SSO ticket, for the Warpgate-fronted listener) or ``auth=`` (a
    :class:`~cove_sdk.auth.CoveAuth`). ``base_url`` must be https unless its host is loopback, or
    ``allow_insecure_http=True``. ``timeout`` defaults to a 10 s connect bound and no read deadline.

    Use it as a context manager, or call ``aclose()``, so the connection pool is released.

    Every resource method takes ``timeout=`` for that call; list methods return one page, and
    their ``iter*`` twins walk every page.
    """

    vms: Vms
    """VM lifecycle, ports and invites, monitoring, streamed ``exec`` and the console tail,
    ``exec_with_secrets``, ``wait_for_state``."""
    checkpoints: Checkpoints
    """Checkpoints, and hibernating a VM."""
    policies: Policies
    """Per-VM auto-pause and expiry."""
    host: Host
    """Host status, capacity, reservations, telemetry and images."""
    secrets: Secrets
    """Secrets bound to a VM, user, team or project: ``secrets.vm(name).list()``."""
    tags: Tags
    """VM tags and team attribution."""
    audit: Audit
    """The audit log."""
    keys: Keys
    """API keys."""
    webhooks: Webhooks
    """Webhook subscriptions and deliveries."""
    meta: Meta
    """Health, version and the caller's identity."""
    events: Events
    """Live lifecycle and VM event streams.

    Served on every listener, the bearer (API-key) one included. The server closes each stream
    after five minutes; the helpers reconnect on that clean close by default (``reconnect=False``
    opts out), and events between the close and the reconnect are lost. ``vm(name)`` ends for good
    after a ``state`` of ``deleted`` or an ``error`` (a failed create).
    """
    teams: Teams
    """Teams and their members."""
    admin: Admin
    """Administrator operations: the fleet, the host, projects, quotas, users, every VM and every
    checkpoint."""

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        ticket: str | None = None,
        auth: CoveAuth | None = None,
        timeout: TimeoutArg = DEFAULT_TIMEOUT,
        allow_insecure_http: bool = False,
        transport: httpx.AsyncBaseTransport | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self._transport = AsyncCoveTransport(
            base_url,
            auth=resolve_auth(token=token, ticket=ticket, auth=auth),
            timeout=timeout,
            allow_insecure_http=allow_insecure_http,
            transport=transport,
            headers=headers,
        )
        self.vms = Vms(self._transport)
        self.checkpoints = Checkpoints(self._transport)
        self.policies = Policies(self._transport)
        self.host = Host(self._transport)
        self.secrets = Secrets(self._transport)
        self.tags = Tags(self._transport)
        self.audit = Audit(self._transport)
        self.keys = Keys(self._transport)
        self.webhooks = Webhooks(self._transport)
        self.meta = Meta(self._transport)
        self.events = Events(self._transport)
        self.teams = Teams(self._transport)
        self.admin = Admin(self._transport)

    @property
    def base_url(self) -> str:
        return self._transport.base_url

    @property
    def server_api_version(self) -> int | None:
        """The ``x-cove-api-version`` of the latest response, or ``None`` before any."""
        return self._transport.server_api_version

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(base_url={self.base_url!r}, auth=<redacted>)"

    __str__ = __repr__
