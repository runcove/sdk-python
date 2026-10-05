"""Signature verification for Cove lifecycle webhook deliveries (a port of the TypeScript SDK's
``webhook.ts``).

Cove signs every delivery with HMAC-SHA256 over ``<ce-id>.<ce-time>.<raw body>`` using the
subscription's ``whsec_...`` secret, and sends the lowercase hex digest as
``Cove-Signature: v1,<hex>``. During rotation grace the header carries two space-separated
``v1,<hex>`` entries: a delivery is authentic if any entry verifies against any secret given.
"""

from __future__ import annotations

import hashlib
import hmac
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime

DEFAULT_TOLERANCE_SECS = 300.0
"""The default replay window, in seconds."""


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def _within_window(ce_time: str, tolerance: float, now: datetime | None) -> bool:
    if tolerance <= 0:
        return True
    try:
        sent = datetime.fromisoformat(ce_time)
    except ValueError:
        return (
            False  # a malformed delivery is the sender's problem, not misconfiguration
        )
    if sent.tzinfo is None:
        sent = sent.replace(tzinfo=UTC)
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return abs((current - sent).total_seconds()) <= tolerance


def verify_webhook_signature(
    *,
    secret: str | Sequence[str],
    headers: Mapping[str, str],
    body: bytes | str,
    tolerance: float = DEFAULT_TOLERANCE_SECS,
    now: datetime | None = None,
) -> bool:
    """Whether a webhook delivery is authentic and inside the replay window.

    ``secret`` is the subscription's secret, or a list of them during rotation grace.
    ``headers`` are the request's (any mapping, looked up case-insensitively; ``ce-id``,
    ``ce-time`` and ``Cove-Signature`` are required). ``body`` is the raw body exactly as
    received -- never re-serialised JSON, whose key order or whitespace would differ.

    ``tolerance`` is the replay window in seconds: a delivery whose signed ``ce-time`` is further
    than that from ``now`` (default: the current time), in either direction, is rejected; ``0``
    accepts any age. The window bounds how long a captured delivery stays replayable; Cove
    retries, so the same ``ce-id`` can legitimately arrive more than once, and deduplicating on
    it remains the caller's job.

    Returns ``False`` for a forged, tampered, stale or malformed delivery. Raises ``ValueError``
    for misconfiguration -- an empty secret or a missing header -- so it fails loudly instead of
    rejecting every delivery. Digests are compared with :func:`hmac.compare_digest`.
    """
    secrets = [secret] if isinstance(secret, str) else list(secret)
    if not secrets or any(not s for s in secrets):
        raise ValueError("verify_webhook_signature: secret must be non-empty")
    ce_id = _header(headers, "ce-id")
    ce_time = _header(headers, "ce-time")
    signature = _header(headers, "cove-signature")
    if not ce_id or not ce_time or not signature:
        raise ValueError(
            "verify_webhook_signature: missing ce-id, ce-time or Cove-Signature header"
        )
    if not _within_window(ce_time, tolerance, now):
        return False
    candidates = [
        token[len("v1,") :].lower()
        for token in (t.strip() for t in signature.split(" "))
        if token.startswith("v1,")
    ]
    if not candidates:
        return False
    raw = body.encode() if isinstance(body, str) else body
    payload = f"{ce_id}.{ce_time}.".encode() + raw
    authentic = False
    for s in secrets:
        digest = hmac.new(s.encode(), payload, hashlib.sha256).hexdigest().encode()
        for candidate in candidates:
            # No early exit: every pair is compared, so timing does not show which matched.
            # Bytes, because compare_digest refuses a str holding non-ASCII (header input).
            if hmac.compare_digest(digest, candidate.encode()):
                authentic = True
    return authentic
