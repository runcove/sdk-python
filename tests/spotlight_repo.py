"""A temporary git repository for the spotlight tests (colour-neutral; shared by the unit tests and
both clients' component tests)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

# A path over 100 bytes the ustar prefix field could carry, and one over 255 that needs pax.
LONG = f"{'d' * 60}/{'e' * 60}/long-file.txt"
LONGER = f"{'x' * 120}/{'y' * 120}/{'z' * 120}.txt"

GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.com",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def git(cwd: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *args],
        cwd=cwd,
        # A hook's GIT_DIR and friends would point git at the real repository, so drop every GIT_ variable.
        env={**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}, **GIT_ENV},
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def make_repo(root: Path) -> Path:
    """A repository with one commit and a worktree holding every kind of path the packer sorts."""
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    (root / ".gitignore").write_text("ignored.log\nbuild/\n")
    (root / "tracked.txt").write_text("tracked v1\n")
    (root / "run.sh").write_text("#!/bin/sh\necho hi\n")
    (root / "run.sh").chmod(0o755)
    (root / "gone.txt").write_text("deleted after the commit\n")
    (root / "link").symlink_to("tracked.txt")
    for p in (LONG, LONGER):
        (root / p).parent.mkdir(parents=True, exist_ok=True)
        (root / p).write_text(f"content of {len(p)}\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    (root / "untracked.txt").write_text("not yet added\n")
    (root / "ignored.log").write_text("ignored\n")
    (root / "build").mkdir()
    (root / "build" / "out.bin").write_text("ignored dir\n")
    (root / "gone.txt").unlink()
    return root
