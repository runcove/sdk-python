"""Auth strategies: the header each sets, SDK headers winning, redaction, exactly one credential."""

import pickle

import httpx
import pytest

from cove_sdk._meta import API_VERSION
from cove_sdk.auth import BearerAuth, CoveAuth, TicketAuth, resolve_auth
from cove_sdk.errors import CoveConfigError


def _flow(auth: CoveAuth, **extensions: object) -> httpx.Request:
    req = httpx.Request(
        "GET",
        "https://h/api/vms",
        headers={"Authorization": "caller", "Accept": "x/y", "X-Cove-Api-Version": "1"},
        extensions=extensions,
    )
    return next(auth.sync_auth_flow(req))


def test_unit_bearer_sets_header_and_wins_over_caller() -> None:
    r = _flow(BearerAuth("cvk_" + "a" * 43, api_version=5))
    assert r.headers["Authorization"] == "Bearer cvk_" + "a" * 43
    assert (
        r.headers["X-Cove-Api-Version"] == "5"
        and r.headers["Accept"] == "application/json"
    )


def test_unit_ticket_uses_the_warpgate_scheme() -> None:
    assert (
        _flow(TicketAuth("t1", api_version=5)).headers["Authorization"] == "Warpgate t1"
    )


def test_unit_api_version_defaults_to_the_contract_version() -> None:
    assert _flow(BearerAuth("cvk_x")).headers["X-Cove-Api-Version"] == str(API_VERSION)


def test_unit_stream_accept_comes_from_the_request_extension() -> None:
    r = _flow(BearerAuth("cvk_x"), cove_accept="text/event-stream")
    assert r.headers["Accept"] == "text/event-stream"


def test_unit_credentials_are_redacted_and_unpicklable() -> None:
    a = BearerAuth("cvk_secret", api_version=5)
    assert (
        "cvk_secret" not in repr(a)
        and "cvk_secret" not in str(a)
        and "redacted" in repr(a)
    )
    t = TicketAuth("tk_secret", api_version=5)
    assert "tk_secret" not in repr(t) and repr(t) == "TicketAuth(<redacted>)"
    with pytest.raises(TypeError):
        pickle.dumps(a)
    with pytest.raises(TypeError):
        pickle.dumps(t)


@pytest.mark.parametrize(
    "kw", [{}, {"token": "a", "ticket": "b"}, {"token": ""}, {"ticket": ""}]
)
def test_unit_exactly_one_credential(kw: dict[str, str]) -> None:
    with pytest.raises(CoveConfigError):
        resolve_auth(**kw, api_version=5)


def test_unit_resolve_auth_returns_the_one_supplied() -> None:
    custom = TicketAuth("t", api_version=5)
    assert resolve_auth(auth=custom, api_version=5) is custom
    with pytest.raises(CoveConfigError):
        resolve_auth(auth=custom, token="a", api_version=5)
    r = _flow(resolve_auth(token="cvk_y", api_version=5))
    assert r.headers["Authorization"] == "Bearer cvk_y"
