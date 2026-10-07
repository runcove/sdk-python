"""``client.spotlight``'s colour-neutral half: the tree it packs (from a real temporary git
repository), the protect and dest checks, and the guest apply script itself, run with /bin/sh on
this machine with rsync on PATH and without."""

from __future__ import annotations

import gzip
import io
import json
import os
import shutil
import subprocess
import tarfile
import time
from pathlib import Path

import pytest
from spotlight_repo import LONG, LONGER, git, make_repo

from cove_sdk import SPOTLIGHT_DEFAULT_PROTECT, CoveError
from cove_sdk._spotlight import (
    APPLY_SCRIPT,
    apply_command,
    check_base,
    check_dest,
    check_protect,
    pack_commit,
    pack_worktree,
    split_names,
    tag_value,
)


def members(tgz: bytes) -> dict[str, tarfile.TarInfo]:
    with tarfile.open(fileobj=io.BytesIO(tgz), mode="r:gz") as tar:
        return {m.name: m for m in tar}


def test_unit_spotlight_pack_keeps_untracked_and_drops_ignored_files(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    packed = pack_worktree(
        repo / "build"
    )  # any path inside the checkout packs the whole of it
    got = members(packed.tgz)
    assert sorted(got) == sorted(
        [".gitignore", LONG, LONGER, "link", "run.sh", "tracked.txt", "untracked.txt"]
    )
    assert got["run.sh"].mode == 0o755
    assert got["link"].issym() and got["link"].linkname == "tracked.txt"
    assert all(m.uid == 0 and m.gid == 0 for m in got.values())
    assert packed.files == 7
    assert packed.head == git(repo, "rev-parse", "HEAD")
    assert packed.source == "main"


def test_unit_spotlight_tar_extracts_with_gnu_tar(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    archive = tmp_path / "t.tgz"
    archive.write_bytes(pack_worktree(repo).tgz)
    out = tmp_path / "x"
    out.mkdir()
    # -p, as the guest script extracts: modes as packed, whatever the umask.
    subprocess.run(["tar", "-xpzf", str(archive), "-C", str(out)], check=True)
    assert (out / LONG).read_text() == f"content of {len(LONG)}\n"
    assert (out / LONGER).read_text() == f"content of {len(LONGER)}\n"
    assert (out / "run.sh").stat().st_mode & 0o777 == 0o755
    assert (out / "link").is_symlink() and os.readlink(out / "link") == "tracked.txt"
    assert not (out / "ignored.log").exists()


def test_unit_spotlight_detached_head_is_labelled_by_the_directory_name(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "wt-feature")
    git(repo, "checkout", "-q", "--detach")
    assert pack_worktree(repo).source == "wt-feature"


def test_unit_spotlight_pack_commit_is_the_committed_tree(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    packed = pack_commit(repo, git(repo, "rev-parse", "HEAD"))
    got = members(packed.tgz)
    assert sorted(got) == sorted(
        [".gitignore", LONG, LONGER, "gone.txt", "link", "run.sh", "tracked.txt"]
    )
    assert got["link"].issym()


def test_unit_spotlight_pack_commit_missing_says_to_fetch(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    missing = "0123456789abcdef0123456789abcdef01234567"
    with pytest.raises(CoveError) as err:
        pack_commit(repo, missing)
    assert (
        str(err.value)
        == f"restore commit {missing} not present locally — run `git fetch`"
    )


def test_unit_spotlight_checks_dest_and_protect() -> None:
    assert check_dest("/srv/app/") == "/srv/app"
    for bad in (
        "srv/app",
        "/",
        "///",
        "",
        "/a\nb",
        "/" + "a" * 300,
        "-rf",
        "/srv/../etc",
        "/srv/./app",
        "/a\x85b",
        "/a\x9fb",
    ):
        with pytest.raises(CoveError):
            check_dest(bad)
    assert SPOTLIGHT_DEFAULT_PROTECT == (
        "node_modules/",
        "target/",
        "volumes/",
        ".venv/",
        ".env",
    )
    assert check_protect(None) == [*SPOTLIGHT_DEFAULT_PROTECT, ".git/"]
    assert check_protect(["a/", ".git/"]) == ["a/", ".git/"]
    for bad_list in (
        "node_modules/",
        [""],
        ["a\0b"],
        ["--delete"],
        ["-e sh"],
        ["ok/", "-x"],
        ["a\nb"],
    ):
        with pytest.raises(CoveError):
            check_protect(bad_list)  # type: ignore[arg-type]


def test_unit_spotlight_a_hostile_base_is_refused_before_any_git_call() -> None:
    # The tree does not exist: a git call would fail with a git error, not this one.
    tree = "/nonexistent/cove-spotlight-tree"
    for base in ("--output=/x", "-rf", "HEAD", "abc", "A" * 40, "a" * 40 + " "):
        with pytest.raises(CoveError, match=r"spotlight\.base is not a commit id"):
            check_base(base)
        with pytest.raises(CoveError, match=r"spotlight\.base is not a commit id"):
            pack_commit(tree, base)
    assert check_base("a" * 40) == "a" * 40


def test_unit_spotlight_pack_commit_resolves_an_abbreviated_base(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    packed = pack_commit(repo, git(repo, "rev-parse", "HEAD")[:10])
    assert "gone.txt" in members(packed.tgz)


def test_unit_spotlight_refuses_a_file_name_that_is_not_utf8() -> None:
    assert split_names("a.txt\0é/b\0".encode()) == ["a.txt", "é/b"]
    with pytest.raises(CoveError, match="file name is not valid UTF-8"):
        split_names(b"ok\0f\xffo\0")


def test_unit_spotlight_a_long_label_is_cut_at_a_code_point() -> None:
    assert tag_value("a" * 254 + "😀😀") == "a" * 254
    assert tag_value("a" * 252 + "😀") == "a" * 252 + "😀"


def test_unit_spotlight_a_missing_tree_directory_is_named() -> None:
    tree = "/nonexistent/cove-spotlight-tree"
    with pytest.raises(CoveError) as err:
        pack_worktree(tree)
    assert (
        str(err.value)
        == f"git rev-parse failed: the tree directory {tree} does not exist"
    )


def test_unit_spotlight_apply_command_never_interpolates() -> None:
    dest = "/srv/my app;$(touch /tmp/pwned)'\""
    protect = ["node_modules/", "$(id)"]
    argv = apply_command("/tmp/t.tgz", dest + ".s", dest, protect)
    assert argv == [
        "sh",
        "-c",
        APPLY_SCRIPT,
        "sh",
        "/tmp/t.tgz",
        dest + ".s",
        dest,
        *protect,
    ]
    for value in (dest, *protect, "/tmp/t.tgz"):
        assert value not in APPLY_SCRIPT


# -- the apply script, run by /bin/sh on this machine --------------------------------------------


def path_without_rsync(at: Path) -> str:
    """A PATH directory with just the tools the fallback path needs, and no rsync."""
    at.mkdir()
    tools = (
        "sh",
        "tar",
        "gzip",
        "find",
        "cat",
        "wc",
        "rm",
        "rmdir",
        "mkdir",
        "cp",
        "printf",
        "echo",
    )
    for tool in tools:
        found = shutil.which(tool)
        if found:
            (at / tool).symlink_to(found)
    return str(at)


def tree_tgz() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for name, data, mode in (
            ("keep.txt", b"new\n", 0o644),
            ("bin/run", b"#!/bin/sh\n", 0o755),
            (".env", b"FROM_TREE=1\n", 0o644),
            # Names that read as options to rm, cp, tar or rsync if a path were ever unprefixed.
            ("-rf", b"plain\n", 0o644),
            ("--checksum", b"plain\n", 0o644),
            # Under a protected path: lands, as protect only stops deletion (as in the CLI).
            ("volumes/seed", b"tracked\n", 0o644),
        ):
            info = tarfile.TarInfo(name)
            info.size, info.mode = len(data), mode
            tar.addfile(info, io.BytesIO(data))
        link = tarfile.TarInfo("latest")
        link.type, link.linkname = tarfile.SYMTYPE, "keep.txt"
        tar.addfile(link)
    return gzip.compress(buf.getvalue())


@pytest.mark.parametrize("with_rsync", [True, False], ids=["rsync", "sh_fallback"])
def test_component_spotlight_apply_script_mirrors_with_delete_and_protect(
    tmp_path: Path, with_rsync: bool
) -> None:
    if with_rsync and not shutil.which("rsync"):
        pytest.skip("rsync is not installed here")
    dest = tmp_path / "app"
    for p, body in {
        "keep.txt": "old\n",
        "stale.txt": "stale\n",
        "olddir/x.txt": "old dir\n",
        "node_modules/x": "installed\n",
        # A .gitignore under a protected path: the fallback does not refuse for it.
        "node_modules/pkg/.gitignore": "*.tmp\n",
        "web/node_modules/y": "nested install\n",
        ".env": "SECRET=1\n",
        "sub/.env": "SECRET=2\n",
        "--delete": "stale, named like an option\n",
        "volumes/db": "VM-only data\n",
    }.items():
        (dest / p).parent.mkdir(parents=True, exist_ok=True)
        (dest / p).write_text(body)
    tgz = tmp_path / "t.tgz"
    tgz.write_bytes(tree_tgz())
    stage = f"{dest}.cove-stage-test"
    path = os.environ["PATH"] if with_rsync else path_without_rsync(tmp_path / "bin")
    run = subprocess.run(
        [
            "/bin/sh",
            "-c",
            APPLY_SCRIPT,
            "sh",
            str(tgz),
            stage,
            str(dest),
            "node_modules/",
            ".env",
            "volumes/",
        ],
        env={**os.environ, "PATH": path},
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert json.loads(run.stdout.strip().split("\n")[-1]) == {
        "files": 7,
        "bytes": 4 + 10 + 12 + 6 + 6 + 8,
    }
    # Option-shaped names land as plain files, and the stale one is deleted like any other.
    assert (dest / "-rf").read_text() == "plain\n"
    assert (dest / "--checksum").read_text() == "plain\n"
    assert not (dest / "--delete").exists()
    assert (dest / "keep.txt").read_text() == "new\n"
    assert (dest / "bin/run").stat().st_mode & 0o777 == 0o755
    assert os.readlink(dest / "latest") == "keep.txt"
    # Delete semantics: what the tree lacks is gone.
    assert not (dest / "stale.txt").exists()
    assert not (dest / "olddir").exists()
    # Protect: nothing the VM alone has under a protected path is deleted, at any depth, even in
    # a directory the tree also holds; a file the tree holds there is written.
    assert (dest / "node_modules/x").read_text() == "installed\n"
    assert (dest / "web/node_modules/y").read_text() == "nested install\n"
    assert (dest / ".env").read_text() == "FROM_TREE=1\n"
    assert (dest / "sub/.env").read_text() == "SECRET=2\n"
    assert (dest / "volumes/seed").read_text() == "tracked\n"
    assert (dest / "volumes/db").read_text() == "VM-only data\n"
    # The stage and the tarball are cleaned up.
    assert not Path(stage).exists() and not tgz.exists()


def test_component_spotlight_apply_script_refuses_dot_components_and_a_stray_stage(
    tmp_path: Path,
) -> None:
    work = str(tmp_path)
    dest = tmp_path / "app"
    dest.mkdir()
    (dest / "keep").write_text("kept\n")
    tgz = tmp_path / "t.tgz"
    tgz.write_bytes(gzip.compress(b"\0" * 1024))
    cases = [
        (f"{dest}/.", f"{dest}/..cove-stage-x"),
        ("/.", "/..cove-stage-x"),
        ("//", "//.cove-stage-x"),
        (f"{work}/../app", f"{work}/../app.cove-stage-x"),
        (f"{work}//app", f"{work}//app.cove-stage-x"),
        (str(dest), f"{work}/elsewhere.cove-stage-x"),
        (str(dest), f"{dest}.cove-stage-"),
        # A trailing slash would put the stage inside dest.
        (f"{dest}/", f"{dest}/.cove-stage-x"),
    ]
    for d, stage in cases:
        run = subprocess.run(
            ["/bin/sh", "-c", APPLY_SCRIPT, "sh", str(tgz), stage, d],
            capture_output=True,
            text=True,
            check=False,
        )
        assert run.returncode == 2, (d, stage, run.stdout + run.stderr)
        assert run.stderr.startswith(
            ("spotlight: dest must not end in /", "spotlight: stage must be")
        )
        assert not Path(stage).exists()
    # Nothing touched: dest, its file and the tarball are all still there.
    assert (dest / "keep").read_text() == "kept\n"
    assert tgz.exists()


def test_unit_spotlight_pack_commit_restores_the_recorded_commit_not_a_branch(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path / "repo")
    first = git(repo, "rev-parse", "HEAD")
    (repo / "tracked.txt").write_text("tracked v2\n")
    git(repo, "commit", "-q", "-am", "second")
    # A branch named like the recorded id's prefix, pointing at the other commit.
    git(repo, "branch", first[:10], "HEAD")
    tracked = members_data(pack_commit(repo, first[:10]).tgz, "tracked.txt")
    assert tracked == b"tracked v1\n"


def members_data(tgz: bytes, name: str) -> bytes:
    with tarfile.open(fileobj=io.BytesIO(tgz), mode="r:gz") as tar:
        f = tar.extractfile(name)
        assert f is not None
        return f.read()


# -- what dest's .gitignore keeps, and the debris of a killed run ---------------------------------


def write_tree(root: Path, files: dict[str, str]) -> None:
    for p, body in files.items():
        (root / p).parent.mkdir(parents=True, exist_ok=True)
        (root / p).write_text(body)


def snapshot(root: Path) -> dict[str, str]:
    """Every file under ``root``, as path to body, to compare a dest before and after."""
    return {
        str(p.relative_to(root)): p.read_text()
        for p in sorted(root.rglob("*"))
        if not p.is_dir()
    }


def tgz_of(files: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for name, body in files.items():
            data = body.encode()
            info = tarfile.TarInfo(name)
            info.size, info.mode = len(data), 0o644
            tar.addfile(info, io.BytesIO(data))
    return gzip.compress(buf.getvalue())


IGNORE = "dist/\n*.log\n.env.local\n"


def run_script(
    tgz: Path, stage: str, dest: Path, *protect: str, path: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/bin/sh", "-c", APPLY_SCRIPT, "sh", str(tgz), stage, str(dest), *protect],
        env={**os.environ, "PATH": path or os.environ["PATH"]},
        capture_output=True,
        text=True,
        check=False,
    )


def gitignored(
    tmp_path: Path, *, with_rsync: bool, gitignore: bool = True
) -> tuple[subprocess.CompletedProcess[str], Path, dict[str, str], str]:
    """A dest holding a .gitignore and the files it ignores, switched to a two-file tree."""
    dest = tmp_path / "app"
    write_tree(
        dest,
        {
            **({".gitignore": IGNORE} if gitignore else {}),
            "dist/bundle.js": "built on the box\n",
            "debug.log": "box log\n",
            ".env.local": "BOX=1\n",
            "stale.txt": "tracked once, gone from the tree\n",
        },
    )
    tgz = tmp_path / "t.tgz"
    tgz.write_bytes(tgz_of({".gitignore": IGNORE, "src.txt": "source\n"}))
    before = snapshot(dest)
    stage = f"{dest}.cove-stage-test"
    path = None if with_rsync else path_without_rsync(tmp_path / "bin")
    run = run_script(tgz, stage, dest, *check_protect(None), path=path)
    return run, dest, before, stage


def test_component_spotlight_apply_script_with_rsync_keeps_what_dest_gitignore_ignores(
    tmp_path: Path,
) -> None:
    if not shutil.which("rsync"):
        pytest.skip("rsync is not installed here")
    run, dest, _, _ = gitignored(tmp_path, with_rsync=True)
    assert run.returncode == 0, run.stdout + run.stderr
    # As the CLI's rsync does: the box's ignored files survive, the stale tracked-looking one goes.
    assert snapshot(dest) == {
        ".gitignore": IGNORE,
        "dist/bundle.js": "built on the box\n",
        "debug.log": "box log\n",
        ".env.local": "BOX=1\n",
        "src.txt": "source\n",
    }


def test_component_spotlight_apply_script_without_rsync_refuses_a_dest_with_a_gitignore(
    tmp_path: Path,
) -> None:
    run, dest, before, stage = gitignored(tmp_path, with_rsync=False)
    assert run.returncode == 3, run.stdout + run.stderr
    assert run.stderr.startswith("spotlight: rsync is not installed on the VM, and ")
    assert "holds ./.gitignore: " in run.stderr
    assert "Install rsync on the VM" in run.stderr
    assert snapshot(dest) == before
    assert not Path(stage).exists()


def test_component_spotlight_apply_script_without_rsync_and_no_gitignore_mirrors_as_before(
    tmp_path: Path,
) -> None:
    run, dest, _, _ = gitignored(tmp_path, with_rsync=False, gitignore=False)
    assert run.returncode == 0, run.stdout + run.stderr
    # Nothing tells the fallback what is ignored, so everything the tree lacks goes.
    assert snapshot(dest) == {".gitignore": IGNORE, "src.txt": "source\n"}


def test_component_spotlight_apply_script_with_rsync_never_deletes_dest_git_even_unprotected(
    tmp_path: Path,
) -> None:
    if not shutil.which("rsync"):
        pytest.skip("rsync is not installed here")
    dest = tmp_path / "app"
    write_tree(dest, {".git/HEAD": "ref: refs/heads/main\n", "stale.txt": "gone\n"})
    tgz = tmp_path / "t.tgz"
    tgz.write_bytes(tgz_of({}))
    # No protect entries at all: the CLI's own --exclude=.git/ is what keeps it.
    run = run_script(tgz, f"{dest}.cove-stage-x", dest)
    assert run.returncode == 0, run.stdout + run.stderr
    assert snapshot(dest) == {".git/HEAD": "ref: refs/heads/main\n"}


def test_component_spotlight_apply_script_clears_debris_of_a_run_killed_at_its_deadline(
    tmp_path: Path,
) -> None:
    dest = tmp_path / "app"
    write_tree(
        tmp_path,
        {
            "app/kept.txt": "x\n",
            "app.cove-stage-0123abcd/half/copied.txt": "debris\n",
            "app-other/kept.txt": "a neighbour\n",
            "cove-spotlight-old.tgz": "an old tarball\n",
            "cove-spotlight-fresh.tgz": "another run's tarball, in flight\n",
        },
    )
    hours_ago = time.time() - 2 * 3600
    os.utime(tmp_path / "cove-spotlight-old.tgz", (hours_ago, hours_ago))
    tgz = tmp_path / "cove-spotlight-cur.tgz"
    tgz.write_bytes(tgz_of({"kept.txt": "x\n"}))
    stage = f"{dest}.cove-stage-cur"
    run = run_script(tgz, stage, dest, ".git/")
    assert run.returncode == 0, run.stdout + run.stderr
    assert not (tmp_path / "app.cove-stage-0123abcd").exists()
    assert not (tmp_path / "cove-spotlight-old.tgz").exists()
    # A tarball under an hour old may be another run's, in flight: kept.
    assert (tmp_path / "cove-spotlight-fresh.tgz").exists()
    assert (tmp_path / "app-other/kept.txt").read_text() == "a neighbour\n"
    assert not Path(stage).exists() and not tgz.exists()
