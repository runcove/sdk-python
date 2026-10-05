"""client.teams round-trips (mirrored to the sync client by unasync)."""

import pytest
from mockapi import Api

from cove_sdk._async._transport import AsyncCoveTransport
from cove_sdk._async.resources.teams import Teams
from cove_sdk._generated.models import (
    RemoveMemberOutcome,
    TeamDeleteOutcome,
    TeamMemberEntry,
    TeamSummary,
)
from cove_sdk.auth import BearerAuth
from cove_sdk.errors import CoveError

TEAM = {
    "created_at": "2026-10-01T00:00:00Z",
    "created_by": "alice",
    "id": "t1",
    "member_count": 1,
    "name": "eng",
}


def _t(api: Api) -> AsyncCoveTransport:
    return AsyncCoveTransport(
        "https://h", auth=BearerAuth("cvk_t"), transport=api.transport()
    )


async def test_component_teams_round_trips() -> None:
    api = (
        Api()
        .on("GET", "/api/teams", (200, [TEAM]))
        .on("POST", "/api/teams", (201, TEAM))
        .on("DELETE", "/api/teams/eng", (200, {"revoked_vm_count": 2}))
        .on(
            "GET",
            "/api/teams/eng/members",
            (
                200,
                [
                    {
                        "added_at": "2026-10-01T00:00:00Z",
                        "added_by": "alice",
                        "username": "bob",
                    }
                ],
            ),
        )
        .on("POST", "/api/teams/eng/members", 201)
        .on("DELETE", "/api/teams/eng/members/bob", (200, {"removed": True}))
    )
    teams = Teams(_t(api))
    listed = await teams.list()
    assert isinstance(listed[0], TeamSummary) and listed[0].name == "eng"
    made = await teams.create("eng")
    assert (api.last.method, api.last_json()) == ("POST", {"name": "eng"})
    assert isinstance(made, TeamSummary) and made.id == "t1"
    gone = await teams.delete("eng")
    assert api.last.method == "DELETE"
    assert isinstance(gone, TeamDeleteOutcome) and gone.revoked_vm_count == 2
    members = await teams.members("eng")
    assert isinstance(members[0], TeamMemberEntry) and members[0].username == "bob"
    assert await teams.add_member("eng", "bob") is None
    assert (api.last.method, api.last.url.path, api.last_json()) == (
        "POST",
        "/api/teams/eng/members",
        {"username": "bob"},
    )
    out = await teams.remove_member("eng", "bob")
    assert (api.last.method, api.last.url.path) == (
        "DELETE",
        "/api/teams/eng/members/bob",
    )
    assert isinstance(out, RemoveMemberOutcome) and out.removed is True


async def test_component_teams_refuse_dot_segments() -> None:
    api = Api()
    teams = Teams(_t(api))
    with pytest.raises(CoveError):
        await teams.remove_member("eng", "..")
    with pytest.raises(CoveError):
        await teams.delete(".")
    with pytest.raises(CoveError):
        await teams.members("")
    with pytest.raises(CoveError):
        await teams.add_member("..", "bob")
    assert api.seen == []


async def test_component_teams_names_are_encoded_as_one_segment() -> None:
    api = Api().on("GET", "/api/teams/a%2Fb/members", (200, []))
    assert await Teams(_t(api)).members("a/b") == []
