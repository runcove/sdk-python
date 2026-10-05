"""verify_webhook_signature against the server's known vector (cove-service webhooks/sign.rs)."""

from datetime import UTC, datetime, timedelta

import pytest

from cove_sdk import verify_webhook_signature

HEX = "7fc7064942271bda82b1f5ccf056e865c3ddfed4dd4b81a976722a6dc0d3acb6"
H = {
    "ce-id": "0192f000-0000-7000-8000-000000000001",
    "ce-time": "2026-05-09T12:34:56.789Z",
    "cove-signature": f"v1,{HEX}",
}
BODY = b'{"kind":"vm.created"}'
NOW = datetime(2026, 5, 9, 12, 35, tzinfo=UTC)
SECRET = "whsec_test_secret"


def test_unit_webhook_known_vector_verifies() -> None:
    assert verify_webhook_signature(secret=SECRET, headers=H, body=BODY, now=NOW)


def test_unit_webhook_rotation_accepts_any_entry_and_rejects_tamper() -> None:
    h = {**H, "cove-signature": f"v1,{'0' * 64} v1,{HEX}"}
    assert verify_webhook_signature(secret=SECRET, headers=h, body=BODY, now=NOW)
    assert not verify_webhook_signature(
        secret=SECRET, headers=H, body=BODY + b" ", now=NOW
    )


def test_unit_webhook_replay_window() -> None:
    late = datetime(2026, 5, 9, 12, 45, tzinfo=UTC)
    assert not verify_webhook_signature(secret=SECRET, headers=H, body=BODY, now=late)
    early = datetime(2026, 5, 9, 12, 25, tzinfo=UTC)  # clocks drift both ways
    assert not verify_webhook_signature(secret=SECRET, headers=H, body=BODY, now=early)
    assert verify_webhook_signature(
        secret=SECRET, headers=H, body=BODY, now=late, tolerance=3600
    )
    assert verify_webhook_signature(
        secret=SECRET, headers=H, body=BODY, now=late, tolerance=0
    )
    edge = datetime(2026, 5, 9, 12, 39, 56, 789000, tzinfo=UTC)
    assert verify_webhook_signature(secret=SECRET, headers=H, body=BODY, now=edge)
    assert not verify_webhook_signature(
        secret=SECRET, headers=H, body=BODY, now=edge + timedelta(milliseconds=1)
    )


def test_unit_webhook_default_now_is_the_wall_clock() -> None:
    # the vector's ce-time is long past, so the default replay window rejects it
    assert not verify_webhook_signature(secret=SECRET, headers=H, body=BODY)
    assert verify_webhook_signature(secret=SECRET, headers=H, body=BODY, tolerance=0)


def test_unit_webhook_headers_are_case_insensitive_and_body_may_be_text() -> None:
    h = {
        "CE-ID": H["ce-id"],
        "Ce-Time": H["ce-time"],
        "Cove-Signature": f"v1,{HEX.upper()}",
    }
    assert verify_webhook_signature(
        secret=SECRET, headers=h, body=BODY.decode(), now=NOW
    )


def test_unit_webhook_any_of_several_secrets() -> None:
    assert verify_webhook_signature(
        secret=["whsec_new", SECRET], headers=H, body=BODY, now=NOW
    )
    assert not verify_webhook_signature(
        secret=["whsec_new"], headers=H, body=BODY, now=NOW
    )


def test_unit_webhook_rejects_without_a_v1_entry_or_with_a_bad_time() -> None:
    assert not verify_webhook_signature(
        secret=SECRET, headers={**H, "cove-signature": f"v2,{HEX}"}, body=BODY, now=NOW
    )
    assert not verify_webhook_signature(
        secret=SECRET, headers={**H, "ce-time": "yesterday"}, body=BODY, now=NOW
    )


def test_unit_webhook_misconfiguration_raises() -> None:
    for secret in ("", [], [SECRET, ""]):
        with pytest.raises(ValueError, match="secret"):
            verify_webhook_signature(secret=secret, headers=H, body=BODY, now=NOW)
    for missing in ("ce-id", "ce-time", "cove-signature"):
        h = {k: v for k, v in H.items() if k != missing}
        with pytest.raises(ValueError, match="header"):
            verify_webhook_signature(secret=SECRET, headers=h, body=BODY, now=NOW)


def test_unit_webhook_non_ascii_signature_is_a_mismatch_not_an_error() -> None:
    h = {**H, "cove-signature": "v1,é" + HEX[1:]}
    assert not verify_webhook_signature(secret=SECRET, headers=h, body=BODY, now=NOW)


# The server's real ce-time shape: chrono's to_rfc3339(), nanoseconds and "+00:00"
# (cove-service webhooks/dispatcher.rs). Hex computed as sign.rs does: HMAC-SHA256 over
# "<ce-id>.<ce-time>.<body>" with the same secret and body as the vector above.
NANO_TIME = "2026-05-09T12:34:56.789123456+00:00"
NANO_HEX = "5018fbb5e8a79de1201715ca7f99e5c3bb2bbd7393b7635095eeb57d5f7e09ba"
NANO_H = {**H, "ce-time": NANO_TIME, "cove-signature": f"v1,{NANO_HEX}"}


def test_unit_webhook_server_rfc3339_nanosecond_time_verifies() -> None:
    assert verify_webhook_signature(secret=SECRET, headers=NANO_H, body=BODY, now=NOW)
    # the time is signed: the millisecond vector's hex does not verify this ce-time
    h = {**NANO_H, "cove-signature": f"v1,{HEX}"}
    assert not verify_webhook_signature(secret=SECRET, headers=h, body=BODY, now=NOW)
    late = datetime(2026, 5, 9, 12, 45, tzinfo=UTC)
    assert not verify_webhook_signature(
        secret=SECRET, headers=NANO_H, body=BODY, now=late
    )
