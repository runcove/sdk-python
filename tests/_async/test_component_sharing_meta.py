"""VM sharing, meta.users() and meta.openapi() round-trips (mirrored to the sync client by unasync)."""

import pytest
from mockapi import Api

from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.meta import Meta
from cove_sdk._async.resources.vms import Vms
from cove_sdk._generated.models import (
    GrantShareOutcome,
    RevokeShareOutcome,
    SharedVmSummary,
    ShareEntry,
)
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError

SHARE = {
    "granted_at": "2026-10-01T00:00:00Z",
    "granted_by": "alice",
    "role": "collaborator",
    "subject_id": "eng",
    "subject_type": "team",
}


def _t(api: Api) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
    )


async def test_component_vms_sharing_round_trips() -> None:
    api = (
        Api()
        .on(
            "GET",
            "/api/vms/shared-with-me",
            (
                200,
                [
                    {
                        "image": "fedora-43",
                        "name": "w",
                        "owner": "bob",
                        "state": "running",
                    }
                ],
            ),
        )
        .on("GET", "/api/vms/v/access", (200, [SHARE]))
        .on("POST", "/api/vms/v/access", (201, {"user_known": False}))
        .on("DELETE", "/api/vms/v/access/team/eng", (200, {"revoked": True}))
    )
    vms = Vms(_t(api))
    shared = await vms.shared_with_me()
    assert isinstance(shared[0], SharedVmSummary)
    assert (shared[0].name, shared[0].owner) == ("w", "bob")
    access = await vms.access("v")
    assert isinstance(access[0], ShareEntry) and access[0].subject_id == "eng"
    granted = await vms.share(
        "v", subject_type="team", subject_id="eng", role="collaborator"
    )
    assert (api.last.method, api.last_json()) == (
        "POST",
        {"subject_type": "team", "subject_id": "eng", "role": "collaborator"},
    )
    assert isinstance(granted, GrantShareOutcome) and granted.user_known is False
    revoked = await vms.unshare("v", "team", "eng")
    assert (api.last.method, api.last.url.path) == (
        "DELETE",
        "/api/vms/v/access/team/eng",
    )
    assert isinstance(revoked, RevokeShareOutcome) and revoked.revoked is True


async def test_component_vms_unshare_guards_all_three_segments() -> None:
    api = Api()
    vms = Vms(_t(api))
    for args in (("..", "user", "bob"), ("v", ".", "bob"), ("v", "user", "..")):
        with pytest.raises(CoveError):
            await vms.unshare(*args)
    with pytest.raises(CoveError):
        await vms.access("..")
    with pytest.raises(CoveError):
        await vms.share("", subject_type="user", subject_id="bob", role="user")
    assert api.seen == []


async def test_component_vms_unshare_encodes_each_segment() -> None:
    api = Api().on("DELETE", "/api/vms/v/access/user/a%2Fb", (200, {"revoked": False}))
    out = await Vms(_t(api)).unshare("v", "user", "a/b")
    assert out.revoked is False


async def test_component_meta_users_and_openapi() -> None:
    doc = {
        "openapi": "3.1.0",
        "info": {"title": "cove", "version": "5"},
        "paths": {"/api/vms": {"get": {"operationId": "listVms"}}},
    }
    api = (
        Api()
        .on("GET", "/api/users", (200, ["alice", "bob"]))
        .on("GET", "/api/openapi.json", (200, doc))
    )
    meta = Meta(_t(api))
    assert await meta.users() == ["alice", "bob"]
    got = await meta.openapi()
    assert type(got) is dict
    assert got == doc
    assert got["paths"]["/api/vms"]["get"]["operationId"] == "listVms"
