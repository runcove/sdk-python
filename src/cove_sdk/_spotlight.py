"""``client.spotlight``'s colour-neutral half: packing a git tree, the guest apply script, the
binding's tag names and the checks on what a caller passes (the resource itself is in
``_async/resources/spotlight.py``, mirrored to the sync client).

Everything here is blocking (git subprocesses and file reads); the async client runs it in a
worker thread.
"""

from __future__ import annotations

import io
import json
import os
import re
import secrets
import stat
import subprocess
import tarfile
from collections.abc import Sequence
from dataclasses import dataclass

from .errors import CoveError

DEFAULT_PROTECT: tuple[str, ...] = (
    "node_modules/",
    "target/",
    "volumes/",
    ".venv/",
    ".env",
)
"""The paths a switch never deletes from ``dest`` unless the caller passes its own list: the same
set as ``cove dev spotlight``. A file the tree itself holds under one is still written, as with
the CLI; what only the VM has there survives."""

TAG_BASE = "spotlight.base"
"""The commit ``off`` restores: the tree's HEAD at the first bind. Set only when absent."""
TAG_DEST = "spotlight.dest"
"""The directory in the VM the tree is mirrored onto."""
TAG_SOURCE = "spotlight.source"
"""What is bound: the tree's branch, or its directory name when HEAD is detached."""

# The guest side of a switch, run as ``sh -c SCRIPT sh TARBALL STAGE DEST [PROTECT...]``. Every
# value travels as an argument, never inside the script text. The TypeScript SDK carries the same
# text (``SPOTLIGHT_APPLY_SCRIPT``), and its test suite holds the two equal.
APPLY_SCRIPT = r"""
# cove spotlight apply v2: sh -c SCRIPT sh TARBALL STAGE DEST [PROTECT...]
# Extracts TARBALL into STAGE, mirrors STAGE onto DEST with delete semantics (every path of DEST
# the tree lacks is removed), except that a path matching a PROTECT entry is never deleted (rsync
# protect rules, as the CLI uses: a bare name matches at any depth, a trailing / matches
# directories only, a leading / anchors at DEST); a file the tree holds is still written there.
# With rsync it also keeps what DEST's own .gitignore files ignore, and never touches .git/, as
# the CLI does (the same filter rules, in the same order). Without rsync it cannot read
# .gitignore, so it refuses (exit 3, before changing anything) when DEST holds one outside a
# protected path. It removes the stage dirs an earlier, killed run left beside DEST, and tarballs
# of this name in TARBALL's directory older than an hour. It then removes STAGE and TARBALL and
# prints {"files":N,"bytes":N}. Every value is a quoted positional parameter; every path reaching a
# command is absolute or starts with ./, and rm, rmdir, mkdir, cp and rsync get -- before their
# operands, so no value can be read as an option.
set -eu
tgz=$1 stage=$2 dest=$3
shift 3
case $dest in /?*) ;; *) echo "spotlight: dest must be an absolute path other than /, got: $dest" >&2; exit 2 ;; esac
case $dest in //*|*//*|*/|*/.|*/..|*/./*|*/../*) echo "spotlight: dest must not end in / or hold an empty, . or .. component, got: $dest" >&2; exit 2 ;; esac
case $stage in "$dest".cove-stage-?*) ;; *) echo "spotlight: stage must be $dest.cove-stage-<suffix>, got: $stage" >&2; exit 2 ;; esac
case $tgz in /?*) ;; *) echo "spotlight: tarball must be an absolute path, got: $tgz" >&2; exit 2 ;; esac
trap 'rm -rf -- "$stage"; rm -f -- "$tgz"' EXIT
n=$#
if command -v rsync >/dev/null 2>&1; then
  rsync=1
  # A protect rule for the entry, and one for everything below it: rsync otherwise deletes
  # untracked files inside a protected directory the tree also holds.
  for p do set -- "$@" "--filter=P $p" "--filter=P ${p%/}/**"; done
else
  rsync=
  # A find expression for "not protected, nor below a protected path".
  for p do
    case $p in /*) base=./${p#/} ;; *) base=*/$p ;; esac
    case $base in */) base=${base%/} dir=1 ;; *) dir= ;; esac
    set -- "$@" -o -path "$base/*"
    if [ -n "$dir" ]; then set -- "$@" -o \( -path "$base" -type d \); else set -- "$@" -o -path "$base"; fi
  done
fi
shift "$n"
if [ -z "$rsync" ] && [ $# -gt 0 ]; then shift; set -- ! \( "$@" \); fi
if [ -z "$rsync" ] && [ -d "$dest" ]; then
  ignore=$(cd "$dest" && find . ! -path . "$@" -name .gitignore -print)
  if [ -n "$ignore" ]; then
    nl='
'
    echo "spotlight: rsync is not installed on the VM, and $dest holds ${ignore%%"$nl"*}: without rsync a switch would delete the files it ignores. Install rsync on the VM and run again; nothing was changed." >&2
    exit 3
  fi
fi
# Two `on` calls onto the same DEST at once are not supported: the sweep removes the other run's stage, and the last tag write wins.
# Debris of an earlier run killed at its deadline (its EXIT trap never ran).
for old in "$dest".cove-stage-*; do
  if [ "$old" != "$stage" ] && { [ -e "$old" ] || [ -L "$old" ]; }; then rm -rf -- "$old"; fi
done
for old in "${tgz%/*}"/cove-spotlight-*.tgz; do
  if [ "$old" != "$tgz" ] && [ -f "$old" ] && [ -n "$(find "$old" -prune -mmin +60 2>/dev/null)" ]; then rm -f -- "$old"; fi
done
rm -rf -- "$stage"
mkdir -p -- "$stage" "$dest"
tar -xpzf "$tgz" -C "$stage"
# Everything in the stage lands in DEST, so these count what the switch writes.
files=0
for n in $(find "$stage" ! -type d -exec sh -c 'echo "$#"' sh {} +); do files=$((files + n)); done
bytes=$(find "$stage" -type f -exec cat -- {} + | wc -c)
if [ -n "$rsync" ]; then
  rsync -a --checksum --delete "--filter=:- .gitignore" --exclude=.git/ "$@" -- "$stage/" "$dest/"
else
  # The delete pass: every path of DEST, deepest first, except protected ones and what lies
  # below them; STALE removes each the stage lacks (or holds as another kind of file).
  STALE='stage=$1; shift
for p do
  s=$stage/${p#./}
  if [ -d "$p" ] && [ ! -L "$p" ]; then
    if [ -d "$s" ] && [ ! -L "$s" ]; then continue; fi
    rmdir -- "$p" 2>/dev/null || :
  else
    if [ -f "$p" ] && [ ! -L "$p" ] && [ -f "$s" ] && [ ! -L "$s" ]; then continue; fi
    rm -f -- "$p"
  fi
done'
  (cd "$dest" && find . -depth ! -path . "$@" -exec sh -c "$STALE" sh "$stage" {} +)
  cp -a -- "$stage/." "$dest/"
fi
printf '{"files":%d,"bytes":%d}\n' "$files" "$((bytes + 0))"
"""
APPLY_SCRIPT = APPLY_SCRIPT.strip("\n")

# Variables that would point git at another repository than the one ``tree`` is in.
_GIT_ROUTING_ENV = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE",
)


@dataclass(frozen=True)
class SpotlightOnResult:
    """The outcome of ``spotlight.on``."""

    vm: str
    dest: str
    base: str
    """The commit ``off`` restores."""
    files: int
    """Regular files and symlinks sent."""
    bytes: int
    """Bytes of regular-file content sent (before compression)."""


@dataclass(frozen=True)
class SpotlightOffResult:
    """The outcome of ``spotlight.off``."""

    vm: str
    dest: str
    restored: str
    """The base commit now on ``dest``."""


@dataclass(frozen=True)
class SpotlightStatus:
    """A VM's binding, read from its tags."""

    dest: str
    base: str
    source: str


@dataclass(frozen=True)
class PackedTree:
    """A tree as a gzip tar, with its counts; ``head`` and ``source`` are set for a worktree."""

    tgz: bytes
    files: int
    bytes: int
    head: str = ""
    source: str = ""


def _git(cwd: str | os.PathLike[str], *args: str) -> bytes:
    """``git args`` in ``cwd`` (an argument list, no shell); its stdout, or ``CoveError``."""
    env = {k: v for k, v in os.environ.items() if k not in _GIT_ROUTING_ENV}
    try:
        done = subprocess.run(
            ["git", *args], cwd=cwd, env=env, capture_output=True, check=False
        )
    except FileNotFoundError as err:
        # A missing cwd or a missing git: say which.
        if not os.path.isdir(cwd):
            raise CoveError(
                f"git {args[0]} failed: the tree directory {os.fspath(cwd)} does not exist"
            ) from err
        raise CoveError(
            f"git {args[0]} failed: git is not installed or not on PATH"
        ) from err
    except OSError as err:
        raise CoveError(f"git {args[0]} in {cwd} failed: {err}") from err
    if done.returncode != 0:
        detail = (
            done.stderr.decode(errors="replace").strip() or f"exit {done.returncode}"
        )
        raise CoveError(f"git {args[0]} in {cwd} failed: {detail}")
    return done.stdout


_FULL_SHA = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


def check_base(sha: str) -> str:
    """Refuse a base commit that is not a hex object name before it goes near git: the
    ``spotlight.base`` tag comes back from the VM, so it is untrusted, and a value such as
    ``--output=/x`` would otherwise reach ``git archive`` as an option."""
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{7,64}", sha):
        raise CoveError(
            f"spotlight.base is not a commit id (7 to 64 lowercase hex digits): {sha!r}"
        )
    return sha


def _text(out: bytes) -> str:
    return out.decode(errors="replace").strip()


def top_level(tree: str | os.PathLike[str]) -> str:
    """The top of the checkout ``tree`` is in."""
    return _text(_git(tree, "rev-parse", "--show-toplevel"))


def _info(name: str, mode: int, mtime: float) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.mode = mode & 0o7777
    info.mtime = int(mtime)
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    return info


def _pack(add: list[tuple[tarfile.TarInfo, bytes | None]]) -> tuple[bytes, int, int]:
    """The entries as a gzip tar (pax format: a long path goes in a pax header), and the counts."""
    buf = io.BytesIO()
    total = 0
    with tarfile.open(
        fileobj=buf, mode="w:gz", format=tarfile.PAX_FORMAT, compresslevel=6
    ) as tar:
        for info, data in add:
            if data is None:
                tar.addfile(info)
            else:
                info.size = len(data)
                total += len(data)
                tar.addfile(info, io.BytesIO(data))
    return buf.getvalue(), len(add), total


def pack_worktree(tree: str | os.PathLike[str]) -> PackedTree:
    """The worktree of the checkout ``tree`` is in, as a gzip tar.

    The files are ``git ls-files -co --exclude-standard -z``: tracked files plus untracked ones git
    does not ignore. A listed path that is gone from disk, or is a directory (a submodule), is left
    out. Files keep their permission bits and mtime; symlinks stay symlinks.
    """
    root = top_level(tree)
    head = _text(_git(root, "rev-parse", "--verify", "HEAD"))
    if not _FULL_SHA.fullmatch(head):
        raise CoveError(f"git rev-parse HEAD answered {head!r}, not a commit id")
    branch = _text(_git(root, "rev-parse", "--abbrev-ref", "HEAD"))
    source = os.path.basename(root) if branch == "HEAD" else branch
    # The listing is read here and never put on a command line: each name only reaches lstat/open.
    listed = _git(root, "ls-files", "-co", "--exclude-standard", "-z", "--")
    entries: list[tuple[tarfile.TarInfo, bytes | None]] = []
    for path in sorted(set(split_names(listed))):
        full = os.path.join(root, path)
        try:
            st = os.lstat(full)
        except (FileNotFoundError, NotADirectoryError):
            # Tracked, but deleted in the worktree (or a parent turned into a file); anything
            # else is real.
            continue
        if stat.S_ISLNK(st.st_mode):
            info = _info(path, 0o777, st.st_mtime)
            info.type = tarfile.SYMTYPE
            info.linkname = os.readlink(full)
            entries.append((info, None))
        elif stat.S_ISREG(st.st_mode):
            with open(full, "rb") as f:
                entries.append((_info(path, st.st_mode, st.st_mtime), f.read()))
    tgz, files, size = _pack(entries)
    return PackedTree(tgz, files, size, head=head, source=tag_value(source))


def split_names(listed: bytes) -> list[str]:
    """The NUL-separated names of ``git ls-files -z``. A name that is not valid UTF-8 is refused
    rather than packed under a name the guest would not recognise, as the TypeScript SDK does."""
    names = []
    for raw in listed.split(b"\0"):
        if not raw:
            continue
        try:
            names.append(raw.decode())
        except UnicodeDecodeError:
            shown = raw.decode(errors="replace")
            raise CoveError(
                f"spotlight cannot send {shown!r}: its file name is not valid UTF-8; rename it"
                " or ignore it in .gitignore"
            ) from None
    return names


def pack_commit(tree: str | os.PathLike[str], sha: str) -> PackedTree:
    """The tree of commit ``sha`` (``git archive``) from the checkout ``tree`` is in, as a gzip
    tar. A commit missing from that repository raises ``CoveError`` saying to fetch it.

    ``sha`` must pass :func:`check_base`, before any git call. It is resolved as an object id only
    (``git rev-parse --disambiguate``), never as a ref, so a branch that happens to be named like
    an abbreviated id cannot move what ``off`` restores; exactly one commit must match."""
    check_base(sha)
    root = top_level(tree)
    full = _resolve_commit(root, sha)
    archive = _git(root, "archive", "--format=tar", full)
    entries: list[tuple[tarfile.TarInfo, bytes | None]] = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar:
            if member.issym():
                info = _info(member.name, 0o777, member.mtime)
                info.type = tarfile.SYMTYPE
                info.linkname = member.linkname
                entries.append((info, None))
            elif member.isfile():
                f = tar.extractfile(member)
                assert f is not None
                entries.append(
                    (_info(member.name, member.mode, member.mtime), f.read())
                )
            elif not member.isdir():
                raise CoveError(
                    f"tar entry {member.name} is neither a file, a symlink nor a directory"
                )
    tgz, files, size = _pack(entries)
    return PackedTree(tgz, files, size)


def _resolve_commit(root: str, sha: str) -> str:
    """The one commit whose id starts with ``sha``, or ``CoveError``."""
    listed = _text(_git(root, "rev-parse", f"--disambiguate={sha}")).split("\n")
    commits = [
        c
        for c in listed
        if _FULL_SHA.fullmatch(c) and _text(_git(root, "cat-file", "-t", c)) == "commit"
    ]
    if not commits:
        raise CoveError(f"restore commit {sha} not present locally — run `git fetch`")
    if len(commits) > 1:
        raise CoveError(f"restore commit {sha} is ambiguous: {', '.join(commits)}")
    return commits[0]


def check_dest(dest: str) -> str:
    """``dest`` without trailing slashes; refused unless absolute (so it can never start with
    ``-``), not ``/``, free of ``.`` and ``..`` components and control characters, and a valid tag
    value."""
    if not isinstance(dest, str) or not dest.startswith("/") or dest.startswith("-"):
        raise CoveError(f"spotlight dest must be an absolute path, got {dest!r}")
    trimmed = dest.rstrip("/")
    if not trimmed:
        raise CoveError("spotlight dest cannot be /")
    if any(c in (".", "..") for c in trimmed.split("/")):
        raise CoveError(f"spotlight dest cannot hold . or .. components, got {dest!r}")
    # C0, DEL and C1 (U+0080-U+009F): the server refuses all of them in a tag value.
    if any(ord(c) < 0x20 or 0x7F <= ord(c) <= 0x9F for c in trimmed):
        raise CoveError("spotlight dest cannot hold control characters")
    if len(trimmed.encode()) > 256:
        raise CoveError("spotlight dest is longer than a tag value's 256 bytes")
    return trimmed


def check_protect(protect: Sequence[str] | None) -> list[str]:
    """The protect list to send: ``protect`` or :data:`DEFAULT_PROTECT`, plus ``.git/``.

    An entry starting with ``-``, or holding a NUL or a line break, is refused: each reaches rsync
    only inside one ``--filter=P <entry>`` argument, and find only as a ``-path`` operand, but an
    option-shaped pattern is never what a caller means."""
    if isinstance(protect, str):
        raise CoveError("spotlight protect is a list of patterns, not one string")
    items = list(DEFAULT_PROTECT if protect is None else protect)
    for p in items:
        if (
            not isinstance(p, str)
            or not p
            or p.startswith("-")
            or any(c in p for c in "\0\n\r")
        ):
            raise CoveError(
                "a spotlight protect entry must be a non-empty pattern, not starting with - and"
                f" without NUL or line breaks, got {p!r}"
            )
    # The checkout's own .git is never part of the tree, and a switch never deletes one in dest.
    if ".git/" not in items:
        items.append(".git/")
    return items


def tag_value(label: str) -> str:
    """``label`` cut to a tag value's 256 UTF-8 bytes."""
    return label.encode()[:256].decode(errors="ignore")


def apply_command(tgz: str, stage: str, dest: str, protect: Sequence[str]) -> list[str]:
    """The apply exec's argv. Every value is its own argument; the script text is fixed."""
    return ["sh", "-c", APPLY_SCRIPT, "sh", tgz, stage, dest, *protect]


def nonce() -> str:
    """16 random hex digits for the tarball and stage names."""
    return secrets.token_hex(8)


def parse_summary(stdout: str) -> tuple[int, int]:
    """The ``(files, bytes)`` of the apply script's last line, or ``CoveError``."""
    lines = stdout.strip().split("\n")
    try:
        summary = json.loads(lines[-1])
        files, size = summary["files"], summary["bytes"]
    except (ValueError, KeyError, TypeError):
        raise CoveError(
            f"spotlight: the apply script printed no summary: {stdout!r}"
        ) from None
    if not isinstance(files, int) or not isinstance(size, int):
        raise CoveError(f"spotlight: the apply script printed no summary: {stdout!r}")
    return files, size
