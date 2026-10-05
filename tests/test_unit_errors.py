"""raise_for: status -> class, code/message fallbacks, CLI_TOO_OLD, 3xx, and the DenyReason walk."""

import enum
import importlib
import json
import pathlib
import re
import typing

import attrs
import pytest

import cove_sdk._generated.models as generated_models
from cove_sdk import errors as E
from cove_sdk._meta import API_VERSION


def _raise(
    status: int,
    body: object,
    ctype: str = "application/json",
    headers: dict[str, str] | None = None,
) -> E.CoveError:
    raw = body if isinstance(body, bytes) else json.dumps(body).encode()
    h = {"content-type": ctype, **(headers or {})}
    with pytest.raises(E.CoveError) as ei:
        E.raise_for(status, h, raw)
    return ei.value


@pytest.mark.parametrize(
    "status,cls",
    [
        (401, E.AuthenticationError),
        (403, E.PermissionDeniedError),
        (404, E.NotFoundError),
        (409, E.ConflictError),
        (422, E.ValidationError),
        (429, E.RateLimitError),
        (500, E.ServerError),
        (503, E.ServerError),
        (418, E.CoveAPIError),
    ],
)
def test_unit_status_maps_to_class(status: int, cls: type[E.CoveAPIError]) -> None:
    e = _raise(status, {"code": "x", "message": "m"})
    assert type(e) is cls
    assert isinstance(e, E.CoveAPIError)
    assert e.status == status and e.code == "x" and e.message == "m"
    assert e.body == {"code": "x", "message": "m"}


@pytest.mark.parametrize(
    "status,code,cls",
    [
        # A request the server cannot decode (cove-server's `extract` module).
        (400, "validation_failed", E.ValidationError),
        # A well-formed value the server refuses.
        (422, "validation_failed", E.ValidationError),
        (422, "invalid_selector", E.ValidationError),
        # Any other 400 keeps the base class.
        (400, "invalid_vm_name", E.CoveAPIError),
        (400, "bad_request", E.CoveAPIError),
        # A code maps to its class only on its own status.
        (500, "validation_failed", E.ServerError),
    ],
)
def test_unit_validation_failed_400_is_a_validation_error(
    status: int, code: str, cls: type[E.CoveAPIError]
) -> None:
    body = {"code": code, "message": "cpus: invalid type", "field": "cpus"}
    e = _raise(status, body)
    assert type(e) is cls
    assert (e.status, e.code, e.body) == (status, code, body)


def test_unit_code_and_message_fallbacks() -> None:
    e = _raise(400, {"error": "bad"})
    assert isinstance(e, E.CoveAPIError)
    assert (e.code, e.message) == ("bad", "bad")
    e = _raise(404, b"plain words", "text/plain")
    assert isinstance(e, E.CoveAPIError)
    assert (e.code, e.message, e.body) == (None, "plain words", "plain words")
    # a body with only a code reports the code as its message (sdk/typescript/src/errors.ts)
    e = _raise(403, {"code": "sudo_required", "reauth_window_secs": 60})
    assert isinstance(e, E.CoveAPIError)
    assert (e.code, e.message) == ("sudo_required", "sudo_required")
    e = _raise(500, b"")
    assert isinstance(e, E.CoveAPIError)
    assert (e.code, e.message, e.body) == (None, "request failed", None)


def test_unit_426_cli_too_old_is_upgrade_required() -> None:
    e = _raise(
        426,
        {"code": "CLI_TOO_OLD", "message": "m", "min_cli_version": "0.23.0"},
        headers={"x-cove-api-version": "5"},
    )
    assert isinstance(e, E.UpgradeRequiredError)
    assert (e.code, e.server_api_version, e.min_cli_version) == (
        "CLI_TOO_OLD",
        5,
        "0.23.0",
    )
    assert "/public/sdk/" in str(e) and "http" not in str(e)  # never embeds base_url
    # the server's text is for the CLI; the SDK user gets the SDK's own message, naming both
    # API versions, and the server's text stays reachable on .body
    assert "cove update" not in str(e)
    assert f"API version {API_VERSION}" in str(e) and "(server version 5)" in str(e)
    assert isinstance(e.body, dict) and e.body["message"] == "m"


def test_unit_426_names_no_server_version_when_the_header_is_absent() -> None:
    server_text = "Your CLI is too old. Minimum API version: 5. Run `cove update` to upgrade."
    e = _raise(426, {"code": "CLI_TOO_OLD", "message": server_text})
    assert isinstance(e, E.UpgradeRequiredError) and e.server_api_version is None
    assert "cove update" not in str(e) and "server version" not in str(e)
    assert f"API version {API_VERSION};" in str(e)
    assert isinstance(e.body, dict) and e.body["message"] == server_text


@pytest.mark.parametrize("header", ["+5", "5_0", "-1", "\u0665", "\uff15", "1234567890"])
def test_unit_426_unparsable_api_version_header_is_absent(header: str) -> None:
    e = _raise(
        426,
        {"code": "CLI_TOO_OLD", "message": "m"},
        headers={"x-cove-api-version": header},
    )
    assert isinstance(e, E.UpgradeRequiredError) and e.server_api_version is None
    assert "server version" not in str(e)


def test_unit_other_426_stays_generic() -> None:
    e = _raise(426, {"code": "something_else"})
    assert type(e) is E.CoveAPIError


def test_unit_3xx_is_a_connection_error() -> None:
    e = _raise(302, b"", headers={"location": "https://elsewhere"})
    assert isinstance(e, E.CoveConnectionError) and "never redirects" in str(e)
    assert "https://elsewhere" in str(e)


def test_unit_vm_name_taken_has_no_deny_but_retry_after() -> None:
    e = _raise(409, {"code": "vm_name_taken", "message": "m", "retry_after_secs": 3})
    assert isinstance(e, E.ConflictError)
    assert e.deny is None and e.retry_after_secs == 3


_RATE_LIMITED = {"code": "rate_limited", "message": "too many requests"}


@pytest.mark.parametrize(
    "header,expected",
    [
        ("7", 7),
        (" 12 ", 12),
        ("0", 0),
        (None, None),
        ("", None),
        ("soon", None),
        ("-1", None),
        ("+5", None),
        ("1.5", None),
        ("Wed, 21 Oct 2026 07:28:00 GMT", None),
    ],
)
def test_unit_429_retry_after_secs_from_header(
    header: str | None, expected: int | None
) -> None:
    headers = {} if header is None else {"Retry-After": header}
    e = _raise(429, _RATE_LIMITED, headers=headers)
    assert isinstance(e, E.RateLimitError)
    assert e.code == "rate_limited"
    assert e.retry_after_secs == expected


def test_unit_503_retry_after_secs_from_header() -> None:
    e = _raise(503, {"code": "unavailable", "message": "m"}, headers={"retry-after": "3"})
    assert isinstance(e, E.ServerError)
    assert isinstance(e, E.UnavailableError)
    assert e.retry_after_secs == 3
    e = _raise(503, {"code": "unavailable", "message": "m"})
    assert isinstance(e, E.ServerError)
    assert e.retry_after_secs is None


def test_unit_names_do_not_shadow_builtins() -> None:
    assert not {"ConnectionError", "PermissionError", "TimeoutError"} & set(E.__all__)
    # positive control: __all__ is the real list, not empty
    assert {"CoveError", "ConflictError", "DenyReason", "raise_for"} <= set(E.__all__)


def test_unit_config_error_is_a_value_error() -> None:
    assert issubclass(E.CoveConfigError, ValueError) and issubclass(
        E.CoveConfigError, E.CoveError
    )
    assert issubclass(E.CoveTimeoutError, E.CoveConnectionError)


def _sample(tp: object) -> object:
    if tp is int:
        return 7
    if tp is float:
        return 1.5
    if tp is str:
        return "s"
    if tp is bool:
        return True
    raise AssertionError(f"no sample value for field type {tp!r}; extend _sample")


def test_unit_every_deny_reason_branch_parses() -> None:
    models_dir = pathlib.Path(generated_models.__file__).parent
    branch_files = sorted(
        p.stem
        for p in models_dir.glob("deny_reason_type_*.py")
        if re.fullmatch(r"deny_reason_type_\d+", p.stem)
    )
    walked = 0
    for stem in branch_files:
        mod = importlib.import_module(f"cove_sdk._generated.models.{stem}")
        cls_name = "DenyReasonType" + stem.rsplit("_", 1)[1]
        cls = getattr(mod, cls_name)
        hints = typing.get_type_hints(cls)
        kwargs: dict[str, object] = {}
        code_value = None
        for f in attrs.fields(cls):
            if not f.init:
                continue
            tp = hints[f.name]
            if f.name == "code":
                assert isinstance(tp, type) and issubclass(tp, enum.Enum)
                members = list(tp)
                assert len(members) == 1, f"{cls_name}.code has {len(members)} values"
                kwargs["code"] = members[0]
                code_value = members[0].value
            else:
                kwargs[f.name] = _sample(tp)
        # to_dict() gives the wire names (max_ -> max), so the body is what the server sends
        body = cls(**kwargs).to_dict()
        e = _raise(409, body)
        assert isinstance(e, E.ConflictError), cls_name
        assert e.deny is not None, (
            f"{cls_name} ({code_value}) did not parse as a DenyReason"
        )
        assert e.deny.code == code_value
        assert set(e.deny.details) == set(body) - {"code"}, cls_name
        assert all(e.deny.details[k] == body[k] for k in e.deny.details)
        with pytest.raises(TypeError):
            e.deny.details["x"] = 1  # type: ignore[index]
        walked += 1
    print(f"deny_reason branches walked: {walked}")
    # 17 on this contract; a walk that finds none fails
    assert walked == len(branch_files) and walked >= 17
