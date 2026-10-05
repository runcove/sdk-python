"""AsyncCoveTransport against httpx.MockTransport (mirrored to the sync transport by unasync)."""

import warnings
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from cove_sdk._async._transport import _RESPONSE, AsyncCoveTransport
from cove_sdk._generated.api.vms import delete_vm, get_vm
from cove_sdk._generated.models import VmDetail
from cove_sdk._meta import API_VERSION
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import (
    CoveApiVersionWarning,
    CoveConfigError,
    CoveConnectionError,
    CoveDecodeError,
    CoveError,
    CoveTimeoutError,
    NotFoundError,
    ServerError,
)

# the fields VmDetail requires (sdk/openapi.yaml), so the generated parser accepts it
VM = {
    "auto_pause_policy": {"type": "auto_pause", "idle_timeout_secs": 600},
    "created_at": "2026-10-01T00:00:00Z",
    "disk_size_gb": 10,
    "image": "fedora-43",
    "mac_address": "02:00:00:00:00:01",
    "memory_mb": 2048,
    "name": "x",
    "state": "running",
    "updated_at": "2026-10-01T00:00:00Z",
    "vcpus": 2,
    "vm_id": "0199a000-0000-7000-8000-000000000000",
}


def _ok(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"ok": True})


def _t(
    handler: Callable[[httpx.Request], httpx.Response],
    base_url: str = "https://h",
    **kw: Any,
) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        base_url,
        auth=BearerAuth("cvk_t"),
        transport=httpx.MockTransport(handler),
        **kw,
    )


async def test_component_query_drops_none_and_repeats_lists() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    t = _t(handler)
    await t.request("GET", "/api/x", params={"a": None, "b": [1, 2], "c": "z"})
    assert seen[0].url.query == b"b=1&b=2&c=z"
    await t.aclose()


async def test_component_trailing_slashes_are_stripped_from_base_url() -> None:
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        return httpx.Response(200, json={})

    t = _t(handler, base_url="https://h/prefix///")
    await t.request("GET", "/api/vms/x")
    assert seen == ["https://h/prefix/api/vms/x"]
    await t.aclose()


async def test_component_sdk_headers_win_over_client_and_call_headers() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=VM)

    t = _t(
        handler,
        headers={"Authorization": "client", "X-Custom": "kept", "accept": "x/client"},
    )
    await t.request(
        "GET",
        "/api/vms/x",
        headers={
            "authorization": "call",
            "Accept": "x/call",
            "X-Cove-Api-Version": "1",
        },
    )
    await t.call(get_vm, path={"name": "x"})
    for r in seen:
        assert r.headers["Authorization"] == "Bearer cvk_t"
        assert r.headers["Accept"] == "application/json"
        assert r.headers["X-Cove-Api-Version"] == str(API_VERSION)
        assert r.headers["X-Custom"] == "kept"
    assert len(seen) == 2
    await t.aclose()


async def test_component_redirect_is_never_followed() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(302, headers={"location": "https://elsewhere/api/vms/x"})

    t = _t(handler)
    assert t._http.follow_redirects is False
    with pytest.raises(CoveConnectionError, match="never redirects"):
        await t.call(get_vm, path={"name": "x"})
    with pytest.raises(CoveConnectionError, match="never redirects"):
        await t.request("GET", "/api/vms/x")
    assert len(seen) == 2 and all(r.url.host == "h" for r in seen)
    await t.aclose()


async def test_component_generated_call_maps_errors_by_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        name = request.url.path.rsplit("/", 1)[1]
        if name == "json404":
            return httpx.Response(
                404, json={"code": "resource_not_found", "message": "no vm"}
            )
        if name == "text404":
            return httpx.Response(
                404, text="not here", headers={"content-type": "text/plain"}
            )
        return httpx.Response(
            502, text="<html>bad gateway</html>", headers={"content-type": "text/html"}
        )

    t = _t(handler)
    with pytest.raises(NotFoundError) as e404:
        await t.call(get_vm, path={"name": "json404"})
    assert (e404.value.status, e404.value.code, e404.value.message) == (
        404,
        "resource_not_found",
        "no vm",
    )
    # a non-JSON body for a status the generated parser decodes as JSON never reaches the parser
    with pytest.raises(NotFoundError) as etext:
        await t.call(get_vm, path={"name": "text404"})
    assert (etext.value.code, etext.value.message) == (None, "not here")
    with pytest.raises(ServerError) as e502:
        await t.call(get_vm, path={"name": "html502"})
    assert e502.value.status == 502 and e502.value.message == "<html>bad gateway</html>"
    with pytest.raises(ServerError):
        await t.request("GET", "/api/vms/html502")
    await t.aclose()


async def test_component_success_returns_the_generated_model() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=VM)

    t = _t(handler)
    vm = await t.call(get_vm, path={"name": "x"})
    assert isinstance(vm, VmDetail) and vm.name == "x" and vm.memory_mb == 2048
    await t.aclose()


async def test_component_undecodable_success_body_is_a_decode_error() -> None:
    def missing_field(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    def html(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, text="<html>captive portal</html>", headers={"content-type": "text/html"}
        )

    for handler, needle in ((missing_field, "{}"), (html, "captive portal")):
        t = _t(handler)
        with pytest.raises(CoveDecodeError) as ei:
            await t.call(get_vm, path={"name": "x"})
        err = ei.value
        assert isinstance(err, CoveError) and err.status == 200
        assert needle in err.body
        assert "get_vm" in str(err) and needle not in str(err)
        assert err.__cause__ is not None
        await t.aclose()


async def test_component_no_response_stays_referenced_after_a_call() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=VM)

    t = _t(handler)
    assert _RESPONSE.get() is None
    await t.call(get_vm, path={"name": "x"})
    assert _RESPONSE.get() is None
    await t.request("GET", "/api/vms/x")
    assert _RESPONSE.get() is None
    async with t.stream("GET", "/api/vms/x"):
        pass
    assert _RESPONSE.get() is None
    with pytest.raises(CoveDecodeError):
        t2 = _t(lambda request: httpx.Response(200, json={}))
        await t2.call(get_vm, path={"name": "x"})
    assert _RESPONSE.get() is None
    await t.aclose()


async def test_component_bad_argument_is_not_a_decode_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"handler reached: {request.url}")

    t = _t(handler)
    with pytest.raises(TypeError) as ei:
        await t.call(get_vm, path={"name": "x"}, bogus=1)
    assert not isinstance(ei.value, CoveError)
    await t.aclose()


async def test_component_unmodelled_success_status_with_a_body_is_a_decode_error() -> None:
    # get_vm documents only 200; the generated parser returns None for a 201 it does not know
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json={"surprise": True})

    t = _t(handler)
    with pytest.raises(CoveDecodeError) as ei:
        await t.call(get_vm, path={"name": "x"})
    assert ei.value.status == 201 and "surprise" in ei.value.body
    assert "get_vm" in str(ei.value) and "201" in str(ei.value)
    await t.aclose()


async def test_component_documented_empty_success_still_returns_none() -> None:
    for status in (202, 204):
        t = _t(lambda request, status=status: httpx.Response(status))
        assert await t.call(delete_vm, path={"name": "x"}) is None
        await t.aclose()


async def test_component_transport_failures_are_cove_errors() -> None:
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    def slow(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    t = _t(refuse)
    with pytest.raises(CoveConnectionError) as ec:
        await t.call(get_vm, path={"name": "x"})
    assert not isinstance(ec.value, CoveTimeoutError)
    assert isinstance(ec.value.__cause__, httpx.ConnectError)
    assert str(ec.value).startswith("request to https://h failed: ")
    with pytest.raises(CoveConnectionError) as er:
        await t.request("GET", "/api/vms/x")
    assert str(er.value).startswith("request to https://h failed: ")
    await t.aclose()
    t = _t(slow)
    with pytest.raises(CoveTimeoutError):
        await t.call(get_vm, path={"name": "x"})
    with pytest.raises(CoveTimeoutError):
        await t.request("GET", "/api/vms/x")
    await t.aclose()


async def test_component_version_skew_warns_once_per_transport() -> None:
    def skewed(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json=VM, headers={"x-cove-api-version": str(API_VERSION + 1)}
        )

    def equal(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json=VM, headers={"x-cove-api-version": str(API_VERSION)}
        )

    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        t = _t(skewed)
        assert t.server_api_version is None
        await t.call(get_vm, path={"name": "x"})
        await t.request("GET", "/api/vms/x")
        assert t.server_api_version == API_VERSION + 1
        await t.aclose()
        skew = [w for w in rec if issubclass(w.category, CoveApiVersionWarning)]
        assert len(skew) == 1
        assert str(API_VERSION + 1) in str(skew[0].message)
        assert skew[0].filename.endswith("_transport.py")
        # a second transport is a second client: it warns again
        t2 = _t(skewed)
        await t2.request("GET", "/api/vms/x")
        await t2.aclose()
        assert (
            len([w for w in rec if issubclass(w.category, CoveApiVersionWarning)]) == 2
        )
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        t = _t(equal)
        await t.call(get_vm, path={"name": "x"})
        await t.request("GET", "/api/vms/x")
        assert t.server_api_version == API_VERSION
        await t.aclose()
    assert not [w for w in rec if issubclass(w.category, CoveApiVersionWarning)]


async def test_component_skew_warning_names_the_sdk_frame_not_a_caller_frame() -> None:
    # The warning is raised inside an httpx event hook, so no fixed stacklevel above 1 reaches the
    # user's code; a stacklevel of 2 or more would only name httpx internals.
    def skewed(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json=VM, headers={"x-cove-api-version": str(API_VERSION + 1)}
        )

    seen: list[dict[str, Any]] = []

    def spy(*args: Any, **kwargs: Any) -> None:
        seen.append(kwargs)

    t = _t(skewed)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(warnings, "warn", spy)
        await t.request("GET", "/api/vms/x")
    await t.aclose()
    assert len(seen) == 1 and "stacklevel" not in seen[0]


async def test_component_skew_is_recorded_from_error_responses_too() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            426,
            json={"code": "CLI_TOO_OLD", "message": "m", "min_cli_version": "9.9.9"},
            headers={"x-cove-api-version": str(API_VERSION + 1)},
        )

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        t = _t(handler)
        with pytest.raises(CoveError):
            await t.call(get_vm, path={"name": "x"})
        assert t.server_api_version == API_VERSION + 1
        await t.aclose()


async def test_component_unparsable_api_version_header_is_treated_as_absent() -> None:
    # Plain ASCII digits only, as TS parseApiVersion (^\d{1,9}$): anything else is no header
    # at all. A loop, not parametrize: the anyio marker is added after parametrization.
    # Raw bytes, so a non-ASCII digit reaches the transport as the server would send it.
    for header in ["+6", "6_0", "-1", "\u0666", "\uff16", "6.0", "", "1234567890"]:

        def handler(request: httpx.Request, header: str = header) -> httpx.Response:
            return httpx.Response(
                200, json=VM, headers=[(b"x-cove-api-version", header.encode())]
            )

        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always")
            t = _t(handler)
            await t.request("GET", "/api/vms/x")
            await t.aclose()
        assert t.server_api_version is None, header
        assert not [
            w for w in rec if issubclass(w.category, CoveApiVersionWarning)
        ], header


async def test_component_api_version_header_is_trimmed_before_parsing() -> None:
    # positive control for the test above: padding around plain digits still parses
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json=VM, headers={"x-cove-api-version": f" {API_VERSION} "}
        )

    t = _t(handler)
    await t.request("GET", "/api/vms/x")
    await t.aclose()
    assert t.server_api_version == API_VERSION


async def test_component_dot_segment_never_reaches_the_server() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"handler reached: {request.url}")

    t = _t(handler)
    for bad in ("..", ".", ""):
        with pytest.raises(CoveError):
            await t.call(get_vm, path={"name": bad})
    await t.aclose()


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "http://127.evil.example",
        "http://localhost.evil.example",
        "ftp://h",
        "not a url",
    ],
)
def test_component_insecure_base_url_is_refused(url: str) -> None:
    with pytest.raises(CoveConfigError):
        _t(_ok, base_url=url)


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost",
        "http://127.0.0.1:8080",
        "http://127.5.6.7",
        "http://[::1]",
        "https://example.com",
    ],
)
def test_component_loopback_or_https_base_url_is_allowed(url: str) -> None:
    _t(_ok, base_url=url)


def test_component_allow_insecure_http_lifts_the_rule() -> None:
    _t(_ok, base_url="http://example.com", allow_insecure_http=True)


async def test_component_timeouts_reach_the_request() -> None:
    seen: list[dict[str, float | None]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions["timeout"])
        return httpx.Response(200, json=VM)

    default = httpx.Timeout(connect=10.0, read=None, write=None, pool=None).as_dict()
    t = _t(handler)
    await t.call(get_vm, path={"name": "x"})
    await t.request("GET", "/api/vms/x")
    await t.call(get_vm, path={"name": "x"}, timeout=2.0)
    await t.request("GET", "/api/vms/x", timeout=3.0)
    await t.call(
        get_vm, path={"name": "x"}
    )  # the per-call value does not leak into the next call
    await t.aclose()
    assert seen == [
        default,
        default,
        httpx.Timeout(2.0).as_dict(),
        httpx.Timeout(3.0).as_dict(),
        default,
    ]
    seen.clear()
    t = _t(handler, timeout=5.0)
    await t.call(get_vm, path={"name": "x"})
    await t.request("GET", "/api/vms/x")
    await t.aclose()
    assert seen == [httpx.Timeout(5.0).as_dict()] * 2


async def test_component_empty_success_returns_none() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return httpx.Response(204)

    t = _t(handler)
    assert await t.call(delete_vm, path={"name": "x"}) is None
    await t.aclose()


async def test_component_stream_asks_for_event_stream_and_bounds_connect_only() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200, content=b"data: x\n\n", headers={"content-type": "text/event-stream"}
        )

    t = _t(handler)
    async with t.stream("POST", "/api/vms/x/exec", json={"command": ["true"]}) as resp:
        assert resp.status_code == 200
    async with t.stream("GET", "/api/events", timeout=30.0):
        pass
    await t.aclose()
    assert seen[0].headers["Accept"] == "text/event-stream"
    assert (
        seen[0].extensions["timeout"]
        == httpx.Timeout(connect=10.0, read=None, write=None, pool=None).as_dict()
    )
    assert (
        seen[1].extensions["timeout"]
        == httpx.Timeout(connect=10.0, read=30.0, write=None, pool=None).as_dict()
    )


async def test_component_stream_error_status_raises_typed_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"code": "resource_not_found", "message": "gone"}
        )

    t = _t(handler)
    with pytest.raises(NotFoundError):
        async with t.stream("GET", "/api/vms/x/console"):
            pass
    await t.aclose()
