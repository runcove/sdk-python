"""client.spotlight against a fake server, with a real temporary git repository (mirrored by
unasync): the apply exec's argv, the order the binding tags are written in, ``off``'s base-commit
guard and its no-binding answer, and a refused upload."""

from __future__ import annotations

import gzip
import io
import json
import tarfile
from pathlib import Path
from typing import Any

import httpx
import pytest
from mockapi import HEADERS
from spotlight_repo import git, make_repo

from cove_sdk import (
    SPOTLIGHT_DEFAULT_PROTECT,
    AsyncCoveClient,
    CoveError,
    FileTooLargeError,
    SpotlightOffResult,
    SpotlightOnResult,
    SpotlightStatus,
)
from cove_sdk._spotlight import APPLY_SCRIPT

SUMMARY = '{"files":7,"bytes":99}\n'


def _sse(event: str, data: str) -> str:
    return (
        f"event: {event}\n"
        + "".join(f"data: {line}\n" for line in data.split("\n"))
        + "\n"
    )


class Fake:
    """The routes spotlight calls. ``tags`` is the VM's tag map; ``apply`` answers the exec as
    ``(stdout, stderr, code)``; ``upload_status`` answers the file PUT."""

    def __init__(
        self,
        tags: dict[str, str] | None = None,
        apply: tuple[str, str, int] = (SUMMARY, "", 0),
        timed_out: bool | None = None,
        upload_status: int = 200,
    ) -> None:
        self.tags = dict(tags or {})
        self.apply = apply
        self.timed_out = timed_out
        self.upload_status = upload_status
        self.calls: list[tuple[str, str]] = []
        self.command: list[str] | None = None
        self.upload_path = ""
        self.upload_body = b""

    def handler(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        self.calls.append((request.method, path))
        if path.endswith("/tags") and request.method == "GET":
            rows = [
                {
                    "key": k,
                    "value": v,
                    "set_by": "alice",
                    "set_at": "2026-10-05T00:00:00Z",
                }
                for k, v in self.tags.items()
            ]
            return httpx.Response(200, json=rows, headers=HEADERS)
        if "/tags/" in path:
            key = path.rsplit("/tags/", 1)[1]
            if request.method == "PUT":
                self.tags[key] = json.loads(request.content)["value"]
            else:
                self.tags.pop(key, None)
            return httpx.Response(204, headers=HEADERS)
        if path.endswith("/files") and request.method == "PUT":
            if self.upload_status == 413:
                refusal = {
                    "code": "file_too_large",
                    "message": "file is larger than 100 MiB",
                }
                return httpx.Response(413, json=refusal, headers=HEADERS)
            self.upload_path = request.url.params["path"]
            self.upload_body = request.content
            body: dict[str, Any] = {
                "path": self.upload_path,
                "size": len(request.content),
                "mode": 0o644,
                "sha256": "0" * 64,
            }
            return httpx.Response(200, json=body, headers=HEADERS)
        if path.endswith("/exec"):
            self.command = json.loads(request.content)["command"]
            stdout, stderr, code = self.apply
            exit_frame: dict[str, Any] = {"code": code}
            if self.timed_out is not None:
                exit_frame["timed_out"] = self.timed_out
            text = (
                (_sse("stdout", stdout) if stdout else "")
                + (_sse("stderr", stderr) if stderr else "")
                + _sse("exit", json.dumps(exit_frame))
            )
            return httpx.Response(
                200,
                content=text.encode(),
                headers={**HEADERS, "content-type": "text/event-stream"},
            )
        return httpx.Response(
            599, json={"error": f"no route for {path}"}, headers=HEADERS
        )

    def client(self) -> AsyncCoveClient:
        return AsyncCoveClient(
            "https://h", token="cvk_t", transport=httpx.MockTransport(self.handler)
        )

    def tag_writes(self) -> list[str]:
        return [
            f"{m} {p.rsplit('/tags/', 1)[1]}" for m, p in self.calls if "/tags/" in p
        ]


async def test_component_spotlight_apply_argv_carries_values_as_arguments(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake()
    dest = "/srv/my app;$(touch /tmp/pwned)'\""
    protect = ["node_modules/", "$(id)", "a b/"]
    async with fake.client() as client:
        out = await client.spotlight.on("box", tree=repo, dest=dest, protect=protect)
    assert out == SpotlightOnResult(
        vm="box", dest=dest, base=git(repo, "rev-parse", "HEAD"), files=7, bytes=99
    )
    assert fake.command is not None
    sh, dash_c, script, zero, tgz, stage, sent_dest, *sent_protect = fake.command
    assert [sh, dash_c, zero] == ["sh", "-c", "sh"]
    assert script == APPLY_SCRIPT
    assert tgz == fake.upload_path
    assert tgz.startswith("/tmp/cove-spotlight-") and tgz.endswith(".tgz")
    assert (
        stage == f"{dest}.cove-stage-{tgz[len('/tmp/cove-spotlight-') : -len('.tgz')]}"
    )
    assert sent_dest == dest
    assert sent_protect == [*protect, ".git/"]
    # The upload is the worktree as a gzip tar.
    with tarfile.open(fileobj=io.BytesIO(gzip.decompress(fake.upload_body))) as tar:
        assert "untracked.txt" in tar.getnames()


async def test_component_spotlight_defaults_to_the_cli_protect_list(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake()
    async with fake.client() as client:
        await client.spotlight.on("box", tree=repo, dest="/srv/app/")
    assert fake.command is not None
    assert fake.command[6:] == ["/srv/app", *SPOTLIGHT_DEFAULT_PROTECT, ".git/"]


async def test_component_spotlight_first_bind_writes_the_tags_after_the_apply(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake()
    async with fake.client() as client:
        await client.spotlight.on("box", tree=repo, dest="/srv/app")
        status = await client.spotlight.status("box")
    exec_at = fake.calls.index(("POST", "/api/vms/box/exec"))
    first_tag = next(i for i, (_, p) in enumerate(fake.calls) if "/tags/" in p)
    assert exec_at < first_tag
    assert fake.tag_writes() == [
        "PUT spotlight.base",
        "PUT spotlight.dest",
        "PUT spotlight.source",
    ]
    head = git(repo, "rev-parse", "HEAD")
    assert status == SpotlightStatus(dest="/srv/app", base=head, source="main")


async def test_component_spotlight_a_switch_keeps_the_first_base(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    first = "f" * 40
    fake = Fake(
        tags={
            "spotlight.base": first,
            "spotlight.dest": "/srv/app",
            "spotlight.source": "old",
        }
    )
    async with fake.client() as client:
        out = await client.spotlight.on("box", tree=repo, dest="/srv/app")
    assert out.base == first
    assert fake.tag_writes() == ["PUT spotlight.dest", "PUT spotlight.source"]
    assert fake.tags["spotlight.base"] == first
    assert fake.tags["spotlight.source"] == "main"


async def test_component_spotlight_a_failed_apply_writes_no_tags(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake(apply=("", "tar: bad archive\n", 2))
    async with fake.client() as client:
        with pytest.raises(CoveError, match=r"exit 2.*tar: bad archive"):
            await client.spotlight.on("box", tree=repo, dest="/srv/app")
    assert fake.tag_writes() == []


async def test_component_spotlight_an_apply_killed_at_its_deadline_says_dest_may_be_half_mirrored(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake(apply=("", "", 124), timed_out=True)
    async with fake.client() as client:
        with pytest.raises(
            CoveError,
            match=r"box:/srv/app hit its 42 s deadline.*may be half-mirrored; run on again",
        ):
            await client.spotlight.on(
                "box", tree=repo, dest="/srv/app", timeout_secs=42
            )
    assert fake.tag_writes() == []


async def test_component_spotlight_a_tree_over_the_file_cap_is_file_too_large(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake(upload_status=413)
    async with fake.client() as client:
        with pytest.raises(FileTooLargeError):
            await client.spotlight.on("box", tree=repo, dest="/srv/app")
    assert fake.command is None
    assert fake.tag_writes() == []


async def test_component_spotlight_status_without_a_binding_is_none() -> None:
    fake = Fake(tags={"other": "x"})
    async with fake.client() as client:
        assert await client.spotlight.status("box") is None


async def test_component_spotlight_off_restores_the_base_and_deletes_the_tags(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    base = git(repo, "rev-parse", "HEAD")
    fake = Fake(
        tags={
            "spotlight.base": base,
            "spotlight.dest": "/srv/app",
            "spotlight.source": "feat",
        }
    )
    async with fake.client() as client:
        out = await client.spotlight.off("box", tree=repo)
    assert out == SpotlightOffResult(vm="box", dest="/srv/app", restored=base)
    assert fake.command is not None and fake.command[6] == "/srv/app"
    with tarfile.open(fileobj=io.BytesIO(gzip.decompress(fake.upload_body))) as tar:
        names = tar.getnames()
    assert "gone.txt" in names and "untracked.txt" not in names
    exec_at = fake.calls.index(("POST", "/api/vms/box/exec"))
    assert all(i > exec_at for i, (m, _) in enumerate(fake.calls) if m == "DELETE")
    assert fake.tag_writes() == [
        "DELETE spotlight.base",
        "DELETE spotlight.source",
        "DELETE spotlight.dest",
    ]
    assert fake.tags == {}


async def test_component_spotlight_off_with_a_missing_base_says_to_fetch(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    missing = "0123456789abcdef0123456789abcdef01234567"
    fake = Fake(tags={"spotlight.base": missing, "spotlight.dest": "/srv/app"})
    async with fake.client() as client:
        with pytest.raises(CoveError) as err:
            await client.spotlight.off("box", tree=repo)
    assert (
        str(err.value)
        == f"restore commit {missing} not present locally — run `git fetch`"
    )
    assert {m for m, _ in fake.calls} == {"GET"}


async def test_component_spotlight_refuses_option_shaped_protect_entries(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake()
    async with fake.client() as client:
        for protect in (["--delete"], ["-e sh"], ["a\nb"]):
            with pytest.raises(CoveError):
                await client.spotlight.on(
                    "box", tree=repo, dest="/srv/app", protect=protect
                )
            with pytest.raises(CoveError):
                await client.spotlight.off("box", tree=repo, protect=protect)
        for dest in ("-rf", "/", "/srv/../etc"):
            with pytest.raises(CoveError):
                await client.spotlight.on("box", tree=repo, dest=dest)
    assert fake.calls == []


async def test_component_spotlight_a_hostile_base_tag_is_refused_before_any_git_call() -> (
    None
):
    # The tree does not exist: a git call would fail with a git error, not this one.
    tree = "/nonexistent/cove-spotlight-tree"
    fake = Fake(tags={"spotlight.base": "--output=/x", "spotlight.dest": "/srv/app"})
    async with fake.client() as client:
        with pytest.raises(CoveError, match=r"spotlight\.base is not a commit id"):
            await client.spotlight.off("box", tree=tree)
        with pytest.raises(CoveError, match=r"spotlight\.base is not a commit id"):
            await client.spotlight.on("box", tree=tree, dest="/srv/app")
    assert {m for m, _ in fake.calls} == {"GET"}


async def test_component_spotlight_a_hostile_dest_tag_is_refused_before_off_applies(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake(
        tags={"spotlight.base": git(repo, "rev-parse", "HEAD"), "spotlight.dest": "-rf"}
    )
    async with fake.client() as client:
        with pytest.raises(CoveError, match="dest must be an absolute path"):
            await client.spotlight.off("box", tree=repo)
    assert {m for m, _ in fake.calls} == {"GET"}


async def test_component_spotlight_an_empty_base_tag_counts_as_no_base(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake(tags={"spotlight.base": ""})
    async with fake.client() as client:
        out = await client.spotlight.on("box", tree=repo, dest="/srv/app")
    assert out.base == git(repo, "rev-parse", "HEAD")
    assert fake.tag_writes() == [
        "PUT spotlight.base",
        "PUT spotlight.dest",
        "PUT spotlight.source",
    ]
    unbound = Fake(tags={"spotlight.base": "", "spotlight.dest": "/srv/app"})
    async with unbound.client() as client:
        assert await client.spotlight.off("box", tree=repo) is None


async def test_component_spotlight_off_with_no_binding_is_a_no_op(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    fake = Fake()
    async with fake.client() as client:
        assert await client.spotlight.off("box", tree=repo) is None
    assert [m for m, _ in fake.calls] == ["GET"]
