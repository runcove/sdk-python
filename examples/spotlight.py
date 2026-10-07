#!/usr/bin/env python3
"""Spotlight from a script: put a local git worktree onto a long-lived VM at a path, switch the VM
to another worktree, then turn it off to put the base tree back, all over the HTTP API (a file
upload plus one exec per switch). Nothing on the VM restarts, and what the VM installed itself
(node_modules/ here) survives every switch. The binding lives in the VM's tags, so
``cove tag ls <vm>`` shows it and ``off`` works from another process.

The repository is a throwaway one made here, with two branches checked out as two worktrees: your
own would be a checkout and a ``git worktree add`` beside it. Needs ``git`` on PATH.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/spotlight.py
    python examples/spotlight.py --mock     # offline, against an in-process fake server
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from cove_sdk import CoveAPIError, CoveClient

DEST = "/srv/app"


def main() -> int:
    mock = "--mock" in sys.argv
    # worktree A is the repository's own checkout of `main`; worktree B is branch `feature`.
    work = Path(tempfile.mkdtemp(prefix="cove-spotlight-"))
    worktree_a, worktree_b = work / "app", work / "app-feature"
    make_repo(worktree_a, worktree_b)
    with make_client(mock) as client:
        name = client.vms.create().name
        print(f"created {name}")

        def guest(*command: str) -> str:
            """Run ``command`` in the VM and return its output, stripped; raise if it fails."""
            run = client.vms.exec_collect(name, command=list(command))
            if run.exit_code != 0:
                raise RuntimeError(
                    f"{' '.join(command)} failed (exit {run.exit_code}): {run.stderr}"
                )
            return run.stdout.strip()

        try:
            client.vms.wait_for_state(
                name, "running", timeout=300, interval=0.01 if mock else 1.0
            )
            print(f"{name} is running")

            on = client.spotlight.on(name, tree=worktree_a, dest=DEST)
            print(f"spotlight on: main -> {name}:{on.dest} ({on.files} files)")
            print(f"app.txt: {guest('cat', f'{DEST}/app.txt')}")

            # What the VM builds for itself, here a stand-in for `npm install`. The default protect
            # list (node_modules/, target/, volumes/, .venv/, .env) keeps it through every switch.
            guest("mkdir", "-p", f"{DEST}/node_modules")
            client.vms.files.upload(name, f"{DEST}/node_modules/marker", "installed\n")

            client.spotlight.on(name, tree=worktree_b, dest=DEST)
            print("switched to feature")
            print(f"app.txt: {guest('cat', f'{DEST}/app.txt')}")
            print(f"node_modules/marker: {guest('cat', f'{DEST}/node_modules/marker')}")

            status = client.spotlight.status(name)
            assert status is not None
            print(f"status: {status.source} on {status.dest}")

            off = client.spotlight.off(name, tree=worktree_a)
            assert off is not None
            print(f"spotlight off: base tree restored on {off.dest}")
            print(f"app.txt after off: {guest('cat', f'{DEST}/app.txt')}")
            print(f"status: {client.spotlight.status(name) or 'nothing bound'}")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            client.vms.delete(name)
            print(f"deleted {name}")
            shutil.rmtree(work, ignore_errors=True)
    return 0


def make_repo(worktree_a: Path, worktree_b: Path) -> None:
    """A repository whose ``main`` and ``feature`` branches differ in app.txt, one worktree each."""

    def git(cwd: Path, *args: str) -> None:
        identity = ["-c", "user.name=example", "-c", "user.email=example@example.com"]
        subprocess.run(
            ["git", *identity, "-c", "commit.gpgsign=false", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
        )

    subprocess.run(["git", "init", "-q", "-b", "main", str(worktree_a)], check=True)
    (worktree_a / ".gitignore").write_text("node_modules/\n")
    (worktree_a / "app.txt").write_text("version: base\n")
    git(worktree_a, "add", "-A")
    git(worktree_a, "commit", "-q", "-m", "base")
    git(worktree_a, "worktree", "add", "-q", "-b", "feature", str(worktree_b))
    (worktree_b / "app.txt").write_text("version: feature\n")
    git(worktree_b, "commit", "-q", "-am", "feature")


def make_client(mock: bool) -> CoveClient:
    if mock:
        # The in-process fake server, imported only for --mock: a copy of this file needs no _mock.py.
        from _mock import mock_transport

        return CoveClient(
            "https://cove.mock", token="cvk_mock", transport=mock_transport()
        )
    url, token = os.environ.get("COVE_URL"), os.environ.get("COVE_TOKEN")
    if not url or not token:
        sys.exit("set COVE_URL and COVE_TOKEN (a cvk_ API key), or run with --mock")
    return CoveClient(url, token=token, timeout=120.0)


if __name__ == "__main__":
    sys.exit(main())
