"""What the caller's credential may do, read from ``meta.me()`` (colour-neutral; both clients use it).

``GET /api/me`` reports ``permissions`` as a union tagged on ``kind``: ``{"kind": "key", "scopes":
[...]}`` for an API key, whose list is complete (exactly what it was minted with, the only list the
bearer gate reads), and ``{"kind": "session"}`` for an SSH, web or local session, which has no scope
list. ``is_admin`` is the admin checks' answer. :func:`has_scope` implements that
``/api/me`` contract (the server's profile handler): an admin permission needs ``is_admin``, and bare
``admin`` covers every ``admin:*`` permission.
"""

from __future__ import annotations

from ._generated.models import (
    ProfileSummary,
    SelfPermissionsType0,
    SelfPermissionsType1,
)
from ._generated.types import Unset
from .errors import CoveError


def _is_admin_scope(scope: str) -> bool:
    return scope == "admin" or scope.startswith("admin:")


def has_scope(me: ProfileSummary, scope: str) -> bool:
    """Whether the credential that fetched ``me`` (``client.meta.me()``) holds ``scope``.

    - An API key holds exactly the list it was minted with. A permission is held when it is on the
      list or, for an ``admin:...`` permission, when bare ``admin`` is (the back-compat superset).
      Nothing else implies anything: ``vms:write`` does not give ``vms:read``, and
      ``admin:quotas:read`` does not give ``admin:quotas:write``.
    - A session has no scope list, so it is not restricted by one: the answer is ``True`` (but see
      the next point).
    - An ``admin`` or ``admin:...`` permission also needs the server's admin check, which
      ``me.is_admin`` reports: an ordinary key that lists ``admin`` (one not minted as an admin key)
      passes no admin check, and a session of a user outside ``[auth] admins`` holds no admin
      permission. For those the answer is ``False`` unless ``me.is_admin`` is ``True``.

    It says nothing about whether a particular VM is reachable: that is decided per VM, and a VM you
    cannot see answers 404.

    Raises :class:`~cove_sdk.errors.CoveError` rather than guessing when ``me`` carries no
    ``permissions`` (a server older than the field), or carries them in a shape this SDK does not
    recognise (a newer server: upgrade the SDK).
    """
    permissions = me.permissions
    if permissions is None or isinstance(permissions, Unset):
        raise CoveError(
            "this server's /api/me does not report permissions; has_scope cannot answer"
        )
    if not isinstance(permissions, (SelfPermissionsType0, SelfPermissionsType1)):
        # the generated parser leaves a shape it does not recognise (a newer kind) as raw data
        raise CoveError(
            "this server's /api/me reports permissions in an unrecognised shape, likely "
            "newer than this SDK; has_scope cannot answer: upgrade the SDK"
        )
    if _is_admin_scope(scope) and me.is_admin is not True:
        return False
    if isinstance(permissions, SelfPermissionsType1):
        return True
    return scope in permissions.scopes or (
        scope.startswith("admin:") and "admin" in permissions.scopes
    )
