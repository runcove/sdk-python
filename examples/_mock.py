"""An in-process fake Cove server for the examples' ``--mock`` mode.

Pass ``transport=mock_transport()`` to ``CoveClient`` or ``AsyncCoveClient`` (a sync handler
serves both), served through ``httpx.MockTransport``. It serves just the routes the examples
call, and runs their guest commands against a tiny fake guest per VM: a dict of files, a few
programs (``cat``, ``curl`` to the guest's own web servers, ``git clone``, ``git -C <dir> add
-A``, ``git -C <dir> diff --cached --output=<file>``, ``make``, ``python3 -m unittest``,
``uname``, ``hostname``), and a small shell that runs ``sh -c`` or ``bash -lc`` scripts made of
``&&``-joined steps, or a script file one line per step, that it knows (``find``, ``test -r``,
``test -s``, ``printf``, ``echo``, ``mkdir``, ``cd``, ``exit``, ``sleep``, a web server started
in the background, and a stand-in for ``claude -p`` that needs ``ANTHROPIC_API_KEY`` in its
environment and knows one edit). A command it does not know fails, so a wrong path or command in
an example fails its ``--mock`` run. Secrets land where the real guest puts them: in a directory
under ``/run/cove/secrets/`` whose random name the fake guest picks once, as the guest agent does
when it starts, for the one command that injects them or when ``rotate`` pushes a file secret;
or, for ``exposure: env`` with ``target_unit: @login``, as an ``export`` line in
``/run/cove/login-env.sh``, which only a login shell (``bash -lc``) reads. A command whose argv
holds a stored secret's value is refused (400), so an example that puts a key on a command line
fails; the real server does not check this, so it is a test of the examples, not a guarantee of
the server. It also serves ``vms.files``
(upload, download, stat): an upload needs its directory to exist, as on the real server, so an
example makes it first with ``mkdir -p``. Also a template for stubbing the SDK in your own
tests: no network, no mocking framework.

Each VM has a state the routes move it through as the server does, and refuse from the states
the server refuses (409): a command or file transfer needs a running VM; a checkpoint or a clone
needs a running or paused one; a disk-only checkpoint wakes only a stopped VM and cannot be
cloned; a full one wakes only a hibernated VM. A checkpoint keeps a copy of the guest's files,
so waking from it or cloning it brings them back, and one a live clone was made from cannot be
deleted (409). Tags filter the VM list, ports must be in the
server's default allowed list, and a port's URL has the server's shape. It serves a VM's tags too
(the same tags the list filters on), and runs ``client.spotlight``'s apply script in effect: it
extracts the uploaded tarball and mirrors it onto the destination with delete semantics and the
protect entries the script was given, so a wrong destination or protect list fails the spotlight
example.
``sdk/typescript/examples/_mock.ts`` is the same fake for the TypeScript examples.
"""

from __future__ import annotations

import base64
import io
import json
import random
import re
import string
import tarfile
from dataclasses import dataclass, field
from typing import Any

import httpx

from cove_sdk import API_VERSION

VM_NAME = "demo-vm"

# Every response carries the server's API version; one that differs from the SDK's would raise a
# CoveApiVersionWarning.
_HEADERS = {"x-cove-api-version": str(API_VERSION)}

# The server's default ``[service.proxy] allowed_ports``, and its default primary port: the one
# with a portless URL.
_ALLOWED_PORTS = [80, 443, 3000, 3001, 5173, 8000, 8080, 9000]
_PRIMARY_PORT = 80
_AT = "2026-10-01T00:00:00Z"

# What ``git clone`` puts in the destination: a Makefile, and a small Python module whose
# lowercasing is missing, with its unit test.
_CLONED = {
    "Makefile": "build:\n\t@echo build done\ntest:\n\t@echo all tests passed\n",
    "index.html": "<h1>demo</h1>\n",
    "slugify.py": 'def slugify(title):\n    return "-".join(title.split())\n',
    "test_slugify.py": "import unittest\nfrom slugify import slugify\n",
}


@dataclass
class _Repo:
    """A git work tree in the fake guest: ``head`` is the files as cloned, ``index`` what ``git add
    -A`` last staged (None until then), both keyed by their path in the tree."""

    head: dict[str, str]
    index: dict[str, str] | None = None


@dataclass
class _Guest:
    """One fake guest: its file system (with each upload's raw bytes), the web servers running in it
    (port to directory), and its git work trees (by directory)."""

    files: dict[str, str] = field(default_factory=dict)
    dirs: set[str] = field(default_factory=lambda: {"/root", "/tmp"})
    serving: dict[int, str] = field(default_factory=dict)
    repos: dict[str, _Repo] = field(default_factory=dict)
    # Each uploaded file's raw bytes, beside its text in ``files`` (a tarball is not text).
    blobs: dict[str, bytes] = field(default_factory=dict)

    def copy(self, with_memory: bool) -> _Guest:
        """A copy, for a checkpoint. A disk-only one keeps no running server."""
        repos = {
            d: _Repo(dict(r.head), None if r.index is None else dict(r.index)) for d, r in self.repos.items()
        }
        return _Guest(
            dict(self.files), set(self.dirs), dict(self.serving) if with_memory else {}, repos, dict(self.blobs)
        )


@dataclass
class _Vm:
    guest: _Guest
    id: str
    state: str
    polls: int = 0
    tags: dict[str, str] = field(default_factory=dict)
    ports: list[int] = field(default_factory=list)
    auto_pause: Any = field(
        default_factory=lambda: {"type": "auto_pause", "idle_timeout_secs": 600}
    )
    ttl: dict[str, Any] | None = None
    # The checkpoint this VM was cloned from, if it is a clone.
    clone_of: _Checkpoint | None = None


@dataclass
class _Checkpoint:
    id: str
    vm: str
    vm_id: str
    disk_only: bool
    description: str | None
    guest: _Guest
    # The live VMs cloned from it. While there are any, it cannot be deleted.
    clones: int = 0


# One exec in the fake guest: (stdout, stderr, exit code, the deadline it ran past or None).
GuestResult = tuple[str, str, int, float | None]


def _ok(stdout: str = "", stderr: str = "") -> GuestResult:
    return stdout, stderr, 0, None


def _fail(stderr: str, code: int = 1) -> GuestResult:
    return "", stderr, code, None


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _add_dirs(dirs: set[str], directory: str) -> None:
    """Mark ``directory`` and every directory above it as existing."""
    while directory:
        dirs.add(directory)
        directory = directory.rpartition("/")[0]


def _is_protected(rel: str, protect: list[str]) -> bool:
    """Is ``rel`` (a path under the destination) kept by one of ``protect``, rsync protect patterns:
    a bare name matches at any depth, a trailing ``/`` matches a directory only, a leading ``/``
    anchors; everything below a match is kept too."""
    parts = rel.split("/")
    for entry in protect:
        dir_only, anchored = entry.endswith("/"), entry.startswith("/")
        pat = entry.strip("/").split("/")
        for end in range(len(pat), len(parts) + 1):
            if anchored and end != len(pat):
                break
            # A file is not a directory: a dir-only pattern matches only a component above it.
            if dir_only and end == len(parts):
                break
            if parts[end - len(pat) : end] == pat:
                return True
    return False


def _spotlight_apply(args: list[str], guest: _Guest) -> GuestResult:
    """``client.spotlight``'s apply script, ``sh -c SCRIPT sh TARBALL STAGE DEST [PROTECT...]``, in
    effect. A symlink lands as a file holding its target: the fake guest has no links."""
    files, dirs, blobs = guest.files, guest.dirs, guest.blobs
    tgz, stage, dest, *protect = args
    if not re.fullmatch(r"/.+", dest):
        return _fail(f"spotlight: dest must be an absolute path other than /, got: {dest}\n", 2)
    if "//" in dest or dest.endswith("/") or any(c in (".", "..") for c in dest.split("/")):
        return _fail(f"spotlight: dest must not end in / or hold an empty, . or .. component, got: {dest}\n", 2)
    if not stage.startswith(f"{dest}.cove-stage-"):
        return _fail(f"the fake guest expects the stage beside dest, got {stage}\n", 2)
    if tgz not in blobs:
        return _fail(f"tar: {tgz}: Cannot open: No such file or directory\n", 2)
    tree: dict[str, tuple[str, int]] = {}
    with tarfile.open(fileobj=io.BytesIO(blobs[tgz]), mode="r:gz") as tar:
        for member in tar:
            if member.isfile():
                data = tar.extractfile(member)
                assert data is not None
                tree[member.name] = (data.read().decode(errors="replace"), member.size)
            elif member.issym():
                tree[member.name] = (member.linkname, 0)
    for path in list(files):
        rel = path[len(dest) + 1 :]
        if path.startswith(f"{dest}/") and rel not in tree and not _is_protected(rel, protect):
            del files[path]
    # Protect only keeps paths from deletion: the tree's own files are all written.
    for rel, (text, _) in tree.items():
        files[f"{dest}/{rel}"] = text
        _add_dirs(dirs, f"{dest}/{rel}".rpartition("/")[0])
    del files[tgz], blobs[tgz]
    summary = {"files": len(tree), "bytes": sum(size for _, size in tree.values())}
    return _ok(json.dumps(summary, separators=(",", ":")) + "\n")


def _run_shell(
    script: str, args: list[str], guest: _Guest, deadline: float, env: dict[str, str] | None = None
) -> GuestResult:
    """``sh -c <script> <$0> <$1>...``, ``bash -lc`` (the same, in a login shell), or ``sh
    <file>``. Two scripts are too much for this shell (an awk program), so they are recognised by
    the files they read and write and computed here instead. ``deadline`` is the exec's
    ``timeout_secs``: a ``sleep`` past it times the command out. ``env`` is the environment the
    shell starts with: a login shell's holds what ``/run/cove/login-env.sh`` exports, a plain ``sh
    -c``'s nothing."""
    if script.startswith("# cove spotlight apply v2"):
        return _spotlight_apply(args, guest)
    env = env or {}
    files, dirs = guest.files, guest.dirs
    if "cat /root/in/*.csv" in script and "> /root/out/totals.csv" in script:
        totals: dict[str, int] = {}
        for path, text in files.items():
            if not re.fullmatch(r"/root/in/[^/]+\.csv", path):
                continue
            for row in filter(None, text.split("\n")):
                item, qty = row.split(",")
                totals[item] = totals.get(item, 0) + int(qty)
        files["/root/out/totals.csv"] = "".join(f"{k},{v}\n" for k, v in sorted(totals.items()))
        return _ok()
    if script.startswith('seq "$1" "$2" | awk'):
        count = sum(1 for n in range(int(args[0]), int(args[1]) + 1) if _is_prime(n))
        return _ok(f"{count}\n")

    variables: dict[str, str] = {}

    def word(w: str) -> str:
        quoted = re.fullmatch(r'"(.*)"', w) or re.fullmatch(r"'(.*)'", w)
        inner = quoted.group(1) if quoted else w
        if w.startswith("'"):
            return inner

        def sub(m: re.Match[str]) -> str:
            v = m.group(1)
            if v.isdigit():
                return args[int(v) - 1] if int(v) <= len(args) else ""
            return variables.get(v, env.get(v, ""))

        return re.sub(r"\$(\d|\w+)", sub, inner)

    stdout = ""
    cwd = "/root"
    # A script file runs one line per step; blank lines and comments are skipped.
    steps = script.split("\n") if "\n" in script else script.split(" && ")
    for step in (s.strip() for s in steps):
        if not step or step.startswith("#"):
            continue
        if m := re.fullmatch(r"(\w+)=\$\(find (\S+) -name (\S+) -type f \| head -n 1\)", step):
            name, directory, file = m.groups()
            hits = sorted(p for p in files if p.startswith(f"{directory}/") and p.endswith(f"/{file}"))
            variables[name] = hits[0] if hits else ""
        elif m := re.fullmatch(r"test -r (\S+)", step):
            if word(m.group(1)) not in files:
                return stdout, "", 1, None
        elif m := re.fullmatch(r"test -s (\S+)", step):
            if not files.get(word(m.group(1))):
                return stdout, "", 1, None
        elif step.startswith("mkdir -p "):
            _add_dirs(dirs, word(step[len("mkdir -p ") :]))
        elif m := re.fullmatch(r"printf %s (\S+) > (\S+)", step):
            files[word(m.group(2))] = word(m.group(1))
        elif m := re.fullmatch(r"echo (.+?)(?: \| tee (\S+))?", step):
            line = f"{word(m.group(1))}\n"
            if m.group(2):
                files[word(m.group(2))] = line
            stdout += line
        elif m := re.fullmatch(r"exit (\d+)", step):
            return stdout, "", int(m.group(1)), None
        elif m := re.fullmatch(r"sleep (\d+)", step):
            if int(m.group(1)) > deadline:
                return stdout, "", -1, deadline
        elif m := re.fullmatch(r"cd (\S+)", step):
            if word(m.group(1)) not in dirs:
                return stdout, f"sh: cd: {word(m.group(1))}: No such file or directory\n", 1, None
            cwd = word(m.group(1))
        elif m := re.fullmatch(r"claude -p (\S+) --permission-mode acceptEdits", step):
            out, err, code, _ = _fake_claude(word(m.group(1)), cwd, env, guest)
            stdout += out
            if code != 0:
                return stdout, err, code, None
        elif m := re.fullmatch(
            r"setsid -f python3 -m http\.server (\S+) --directory (\S+) > (\S+) 2>&1", step
        ):
            # Starts in the background and answers at once, as `setsid -f` does.
            guest.serving[int(word(m.group(1)))] = word(m.group(2))
            files[word(m.group(3))] = ""
        else:
            return stdout, f"sh: the fake guest cannot run: {step}\n", 127, None
    return _ok(stdout)


def _tree_of(files: dict[str, str], directory: str) -> dict[str, str]:
    """The files under ``directory``, keyed by their path below it."""
    prefix = f"{directory}/"
    return {p[len(prefix) :]: t for p, t in files.items() if p.startswith(prefix)}


def _unified_diff(old_tree: dict[str, str], new_tree: dict[str, str]) -> str:
    """``git diff`` between two trees, in git's format with the whole of each small file as context
    (git's own three lines of context cover these files whole), but without the ``index`` lines,
    which name blob hashes the fake does not compute."""

    def lines(text: str | None) -> list[str]:
        return [] if text is None else text.removesuffix("\n").split("\n")

    def span(n: int) -> str:
        return "0,0" if n == 0 else "1" if n == 1 else f"1,{n}"

    out = ""
    for path in sorted(set(old_tree) | set(new_tree)):
        a, b = old_tree.get(path), new_tree.get(path)
        if a == b:
            continue
        old, new = lines(a), lines(b)
        pre = 0
        while pre < len(old) and pre < len(new) and old[pre] == new[pre]:
            pre += 1
        suf = 0
        while suf < len(old) - pre and suf < len(new) - pre and old[-1 - suf] == new[-1 - suf]:
            suf += 1
        out += f"diff --git a/{path} b/{path}\n"
        if a is None:
            out += "new file mode 100644\n"
        if b is None:
            out += "deleted file mode 100644\n"
        out += f"--- {'/dev/null' if a is None else 'a/' + path}\n+++ {'/dev/null' if b is None else 'b/' + path}\n"
        out += f"@@ -{span(len(old))} +{span(len(new))} @@\n"
        out += "".join(f" {line}\n" for line in old[:pre])
        out += "".join(f"-{line}\n" for line in old[pre : len(old) - suf])
        out += "".join(f"+{line}\n" for line in new[pre : len(new) - suf])
        out += "".join(f" {line}\n" for line in old[len(old) - suf :])
    return out


# The test the fake coding agent adds.
_LOWERCASE_TEST = (
    "import unittest\nfrom slugify import slugify\n\n\nclass TestLowercase(unittest.TestCase):\n"
    '    def test_lowercases(self):\n        self.assertEqual(slugify("Hello World"), "hello-world")\n'
)

# Where the guest agent's ``@login`` env sink writes the exports every login shell sources.
_LOGIN_ENV = "/run/cove/login-env.sh"


def _fake_claude(prompt: str, cwd: str, env: dict[str, str], guest: _Guest) -> GuestResult:
    """``claude -p <prompt> --permission-mode acceptEdits``, run in ``cwd``. It needs
    ``ANTHROPIC_API_KEY`` in its environment, as the real one does, and knows one edit: asked to
    lowercase, it makes ``slugify()`` lowercase the title and adds a test for it. Any other prompt
    changes nothing."""
    if not env.get("ANTHROPIC_API_KEY"):
        return _fail("Invalid API key · Please run /login\n")
    source = guest.files.get(f"{cwd}/slugify.py")
    if not re.search("lowercase", prompt, re.IGNORECASE) or source is None:
        return _ok("Nothing in this repository matches the task, so I changed no files.\n")
    guest.files[f"{cwd}/slugify.py"] = source.replace("title.split()", "title.lower().split()")
    guest.files[f"{cwd}/test_lowercase.py"] = _LOWERCASE_TEST
    return _ok("slugify() now lowercases the title, and test_lowercase.py tests it.\n")


def _login_env(files: dict[str, str]) -> dict[str, str]:
    """What a login shell's profile exports: the ``export NAME='value'`` lines of the ``@login``
    env file."""
    env = {}
    for line in files.get(_LOGIN_ENV, "").split("\n"):
        if m := re.fullmatch(r"export (\w+)='(.*)'", line):
            env[m.group(1)] = m.group(2).replace("'\\''", "'")
    return env


def _run_in_guest(command: list[str], guest: _Guest, deadline: float) -> GuestResult:
    """One exec in the fake guest."""
    files, dirs = guest.files, guest.dirs
    program, rest = command[0], command[1:]
    if program == "sh" and rest[:1] == ["-c"]:
        return _run_shell(rest[1], rest[3:], guest, deadline)
    # A login shell reads the profile, which sources the `@login` env file if there is one.
    if program == "bash" and rest[:1] == ["-lc"]:
        return _run_shell(rest[1], rest[3:], guest, deadline, _login_env(files))
    if program == "sh" and len(rest) == 1:
        if rest[0] not in files:
            return _fail(f"sh: 0: cannot open {rest[0]}: No such file\n", 2)
        return _run_shell(f"{files[rest[0]]}\n", [], guest, deadline)
    if program == "curl":
        # `curl -fsS [--retry N --retry-delay N --retry-connrefused] -o /dev/null <url>`, against the guest's
        # own web servers.
        m = re.fullmatch(
            r"-fsS (?:--retry \d+ (?:--retry-delay \d+ )?--retry-connrefused )?-o /dev/null (\S+)", " ".join(rest)
        )
        if not m:
            return _fail(f"curl: the fake guest cannot run: curl {' '.join(rest)}\n", 2)
        url = re.fullmatch(r"http://127\.0\.0\.1:(\d+)/", m.group(1))
        served = guest.serving.get(int(url.group(1))) if url else None
        if served is None:
            return _fail(f"curl: (7) Failed to connect to {m.group(1)}\n", 7)
        if served not in dirs:
            return _fail("curl: (22) The requested URL returned error: 404\n", 22)
        return _ok()
    if program == "mkdir" and len(rest) == 2 and rest[0] == "-p":
        _add_dirs(dirs, rest[1])
        return _ok()
    if program == "cat":
        if rest[0] not in files:
            return _fail(f"cat: {rest[0]}: No such file or directory\n")
        return _ok(files[rest[0]])
    if program == "python3" and " ".join(rest).startswith("-m unittest discover -s "):
        directory = rest[4]
        if f"{directory}/test_slugify.py" not in files:
            return _fail("\nRan 0 tests\n\nNO TESTS RAN\n", 5)
        if ".lower()" in files.get(f"{directory}/slugify.py", ""):
            return _ok("", "..\nRan 2 tests\n\nOK\n")
        return _fail("F.\nFAIL: test_lowercases\nRan 2 tests\n\nFAILED (failures=1)\n")
    if program == "git" and rest[:1] == ["clone"]:
        _add_dirs(dirs, rest[-1])
        for file, text in _CLONED.items():
            files[f"{rest[-1]}/{file}"] = text
        guest.repos[rest[-1]] = _Repo(_tree_of(files, rest[-1]))
        return _ok("", f"Cloning into '{rest[-1]}'...\n")
    if program == "git" and rest[:1] == ["-C"] and len(rest) >= 2:
        # `git -C <dir> add -A` stages the whole tree; `git -C <dir> diff --cached --output=<file>`
        # writes what is staged against HEAD (nothing, before an add).
        directory, args = rest[1], " ".join(rest[2:])
        repo = guest.repos.get(directory)
        if repo is None:
            return _fail("fatal: not a git repository (or any of the parent directories): .git\n", 128)
        if args == "add -A":
            repo.index = _tree_of(files, directory)
            return _ok()
        if m := re.fullmatch(r"diff --cached --output=(\S+)", args):
            target = m.group(1)
            if (target.rpartition("/")[0] or "/") not in dirs:
                return _fail(f"fatal: could not open '{target}' for writing: No such file or directory\n", 128)
            files[target] = _unified_diff(repo.head, repo.head if repo.index is None else repo.index)
            return _ok()
        return _fail(f"git: the fake guest cannot run: git {' '.join(rest)}\n", 129)
    if program == "make" and len(rest) == 3 and rest[0] == "-C" and rest[2] in ("test", "build"):
        if f"{rest[1]}/Makefile" not in files:
            return _fail(f"make: *** {rest[1]}: No such file or directory.  Stop.\n", 2)
        return _ok("all tests passed\n" if rest[2] == "test" else "build done\n")
    if program == "uname":
        return _ok("Linux demo-vm 6.12.0 x86_64 GNU/Linux\n")
    if program == "hostname":
        return _ok(f"{VM_NAME}\n")
    return _fail(f"{program}: command not found in the fake guest\n", 127)


def _secrets_dir() -> str:
    """The guest agent's secrets directory: 16 random letters and digits, picked when it starts."""
    alphabet = string.ascii_lowercase + string.digits
    return "/run/cove/secrets/" + "".join(random.choice(alphabet) for _ in range(16))


def _sse(event: str, data: str) -> str:
    """One server-sent event. A chunk "a\\nb\\n" is three ``data:`` fields, the last one empty."""
    return f"event: {event}\n" + "".join(f"data: {line}\n" for line in data.split("\n")) + "\n"


def mock_transport() -> httpx.MockTransport:
    vms: dict[str, _Vm] = {}
    checkpoints: dict[str, _Checkpoint] = {}
    secrets: dict[str, tuple[str, str | None]] = {}  # name -> (value, setup tag)

    def leaked(command: list[str]) -> str | None:
        """A test of the examples, not the server's behaviour: a stored secret's value in a
        command's argv is refused, so an example that passes a key on the command line fails its
        --mock run."""
        for n, (value, _) in secrets.items():
            if value and any(value in arg for arg in command):
                return n
        return None
    secrets_root = _secrets_dir()
    created = 0
    ids = 0

    def next_id(prefix: str) -> str:
        nonlocal ids
        ids += 1
        return f"{prefix}-0000-7000-8000-{ids:012d}"

    def json_response(status: int, body: Any = None) -> httpx.Response:
        if body is None:
            return httpx.Response(status, headers=_HEADERS)
        return httpx.Response(status, json=body, headers=_HEADERS)

    def error(status: int, code: str, message: str) -> httpx.Response:
        return json_response(status, {"code": code, "message": message})

    def invalid_state(name: str, vm: _Vm, doing: str) -> httpx.Response:
        return error(409, "invalid_state_transition", f"{name} is {vm.state}: cannot {doing}")

    def stream(body: str) -> httpx.Response:
        return httpx.Response(
            200,
            content=body.encode(),
            headers={**_HEADERS, "content-type": "text/event-stream"},
        )

    def vm_detail(name: str, vm: _Vm) -> dict[str, object]:
        # The fields the contract requires of a VmDetail, plus the IP the examples print.
        return {
            "auto_pause_policy": vm.auto_pause,
            "created_at": _AT,
            "disk_size_gb": 10,
            "image": "fedora-43",
            "ip_address": "10.99.0.7",
            "mac_address": "02:00:00:00:00:01",
            "memory_mb": 2048,
            "name": name,
            "state": vm.state,
            "tags": vm.tags,
            "updated_at": _AT,
            "vcpus": 2,
            "vm_id": vm.id,
        }

    def checkpoint_body(c: _Checkpoint) -> dict[str, object]:
        return {
            "id": c.id,
            "vm_id": c.vm_id,
            "state": "available",
            "owner_username": "demo",
            "created_at": _AT,
            "completed_at": _AT,
            "description": c.description,
            "disk_only": c.disk_only,
            "vm_name_at_creation": c.vm,
        }

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal created
        method = request.method
        # A file upload's body is the file, not JSON.
        is_json = bool(request.content) and method != "PUT"
        body: dict[str, Any] = json.loads(request.content) if is_json else {}
        parts = request.url.path.split("/")
        collection = parts[2] if len(parts) > 2 else ""
        name = parts[3] if len(parts) > 3 else ""
        action = parts[4] if len(parts) > 4 else ""
        key = parts[5] if len(parts) > 5 else ""
        sub = parts[6] if len(parts) > 6 else ""
        if parts[1:2] != ["api"]:
            return error(404, "resource_not_found", "no mock route")

        if collection == "checkpoints" and method == "DELETE" and name:
            doomed = checkpoints.get(name)
            if doomed is None:
                return error(404, "vm_not_found", f"VM '{name}' not found")
            if doomed.clones > 0:
                return error(409, "checkpoint_conflict", f"checkpoint {name} has {doomed.clones} live clones")
            del checkpoints[name]
            return json_response(204)
        if collection != "vms":
            return error(404, "resource_not_found", "no mock route")

        if method == "POST" and name == "":
            created += 1
            new = body.get("name") or (VM_NAME if created == 1 else f"{VM_NAME}-{created}")
            if new in vms:
                return error(409, "vm_name_taken", f"{new} is taken")
            vm = _Vm(
                guest=_Guest(),
                id=next_id("0199a000"),
                state="creating",
                tags=dict(body.get("initial_tags") or {}),
                ttl=body.get("ttl_policy"),
            )
            if body.get("auto_pause_policy"):
                vm.auto_pause = body["auto_pause_policy"]
            vms[new] = vm
            return json_response(202, {"name": new, "vm_id": vm.id})
        if method == "GET" and name == "":
            # `?tag=key=value`, repeatable, all must match.
            wanted = [t.partition("=")[::2] for t in request.url.params.get_list("tag")]
            rows = [
                {"name": n, "state": v.state, "image": "fedora-43", "tags": v.tags}
                for n, v in sorted(vms.items())
                if all(v.tags.get(k) == val for k, val in wanted)
            ]
            return json_response(200, {"vms": rows, "next_cursor": None})

        vm_or_none = vms.get(name)
        if vm_or_none is None:
            return error(404, "vm_not_found", f"no VM named {name}")
        vm = vm_or_none
        guest = vm.guest
        running = vm.state == "running"

        if action == "files":
            if not running:
                return invalid_state(name, vm, "transfer files")
            path = request.url.params.get("path", "")
            if method == "PUT":
                directory = path.rpartition("/")[0] or "/"
                if directory not in guest.dirs:
                    return error(404, "file_not_found", f"{directory}: no such directory")
                guest.files[path] = request.content.decode(errors="replace")
                guest.blobs[path] = request.content
                return json_response(
                    200,
                    {"path": path, "size": len(request.content), "mode": 0o644, "sha256": "0" * 64},
                )
            if path not in guest.files:
                return error(404, "file_not_found", f"{path}: no such file")
            data = guest.files[path].encode()
            headers = {**_HEADERS, "content-length": str(len(data)), "x-cove-file-mode": "0644"}
            return httpx.Response(200, content=b"" if method == "HEAD" else data, headers=headers)
        if action == "tags":
            # The VM's own tags, the ones the list filters on and its detail shows.
            if method == "GET" and not key:
                rows = [{"key": k, "value": v, "set_by": "mock", "set_at": _AT} for k, v in sorted(vm.tags.items())]
                return json_response(200, rows)
            if method == "PUT":
                vm.tags[key] = json.loads(request.content)["value"]
            if method == "DELETE":
                vm.tags.pop(key, None)
            return json_response(204)
        if method == "GET" and action == "":
            # A new VM is creating for two polls, then running; a stopping VM is stopped by the next.
            vm.polls += 1
            if vm.state == "creating" and vm.polls > 2:
                vm.state = "running"
            seen = vm_detail(name, vm)
            if vm.state == "stopping":
                vm.state = "stopped"
            return json_response(200, seen)
        if method == "DELETE" and action == "":
            if vm.clone_of is not None:
                vm.clone_of.clones -= 1
            del vms[name]
            return json_response(202)
        if method == "GET" and action == "events":
            # The stream ends on `running`, so the VM is running by the time a reader acts on it.
            vm.state = "running"
            return stream(
                _sse("state", json.dumps({"state": "creating", "timestamp": _AT}))
                + _sse("progress", json.dumps({"stage": "booting", "message": "starting the guest"}))
                + _sse("state", json.dumps({"state": "running", "timestamp": _AT}))
            )
        if method == "POST" and action == "stop":
            if vm.state not in ("running", "paused"):
                return invalid_state(name, vm, "stop")
            vm.state = "stopping"
            guest.serving.clear()
            return json_response(202)
        if method == "POST" and action in ("checkpoints", "hibernate"):
            if vm.state not in ("running", "paused"):
                return invalid_state(name, vm, action.rstrip("s"))
            disk_only = action == "checkpoints" and body.get("disk_only") is True
            c = _Checkpoint(
                id=next_id("0199a001"),
                vm=name,
                vm_id=vm.id,
                disk_only=disk_only,
                description=body.get("description") if action == "checkpoints" else None,
                guest=guest.copy(not disk_only),
            )
            checkpoints[c.id] = c
            if action == "hibernate":
                vm.state = "hibernated"
                guest.serving.clear()
            return json_response(200, checkpoint_body(c))
        if method == "POST" and action == "wake":
            # A named checkpoint, or the VM's newest one.
            own = [c for c in checkpoints.values() if c.vm_id == vm.id]
            wanted_id = body.get("checkpoint_id")
            if wanted_id:
                # A checkpoint that does not exist is a 404; one that belongs to another VM is a
                # 409, as on the real server.
                named = checkpoints.get(wanted_id)
                if named is None:
                    return error(404, "wake_target_not_found", f"not found: {wanted_id}")
                if named.vm_id != vm.id:
                    return invalid_state(name, vm, "wake from a checkpoint of another VM")
                ckpt = named
            elif own:
                ckpt = own[-1]
            else:
                return error(409, "invalid_state_transition", f"no available checkpoint to wake {name} from")
            # A disk-only checkpoint replaces a stopped VM's disk and boots it; a full one wakes
            # a hibernated VM with its memory.
            if vm.state != ("stopped" if ckpt.disk_only else "hibernated"):
                return invalid_state(name, vm, "wake from that checkpoint")
            vm.guest = ckpt.guest.copy(not ckpt.disk_only)
            vm.state = "running"
            return json_response(204)
        if method == "POST" and action == "clone":
            if vm.state not in ("running", "paused"):
                return invalid_state(name, vm, "clone")
            target = body["new_vm_name"]
            if target in vms:
                return error(409, "invalid_state_transition", f"new VM name already taken: {target}")
            # A clone without a checkpoint id is made from an implicit checkpoint of the source now.
            if body.get("source_checkpoint_id"):
                c_or_none = checkpoints.get(body["source_checkpoint_id"])
                if c_or_none is None:
                    return error(404, "clone_source_not_found", f"not found: {body['source_checkpoint_id']}")
                if c_or_none.vm_id != vm.id:
                    return invalid_state(name, vm, "clone from a checkpoint of another VM")
                if c_or_none.disk_only:
                    return error(
                        409, "invalid_state_transition", "a disk-only checkpoint cannot be cloned; stop the VM and wake it from this checkpoint"
                    )
                source = c_or_none
            else:
                source = _Checkpoint(
                    id=next_id("0199a001"),
                    vm=name,
                    vm_id=vm.id,
                    disk_only=False,
                    description="pre_clone",
                    guest=guest.copy(True),
                )
                checkpoints[source.id] = source
            source.clones += 1
            copy = _Vm(
                guest=source.guest.copy(True), id=next_id("0199a000"), state="running", clone_of=source
            )
            vms[target] = copy
            return json_response(200, {"new_vm": vm_detail(target, copy), "fingerprints": []})
        if method == "POST" and action == "ports":
            port = body["port"]
            if port not in _ALLOWED_PORTS:
                return json_response(
                    422,
                    {
                        "code": "port_not_allowed",
                        "message": f"port {port} is not allowed",
                        "port": port,
                        "allowed": _ALLOWED_PORTS,
                    },
                )
            if port not in vm.ports:
                vm.ports.append(port)
            return json_response(201)
        if method == "GET" and action == "url":
            # The primary port's URL is portless; another port's is a subdomain of its own.
            ports = [
                {
                    "port": p,
                    "public": False,
                    "is_primary": p == _PRIMARY_PORT,
                    "url": f"https://{name}.cove.mock/" if p == _PRIMARY_PORT else f"https://{name}-{p}.cove.mock/",
                }
                for p in vm.ports
            ]
            return json_response(
                200, {"vm_name": name, "ssh_url": f"ssh://demo@cove.mock:2222/{name}", "ports": ports}
            )
        if method == "POST" and action == "access":
            if body.get("subject_type") not in ("user", "team") or body.get("role") not in ("user", "collaborator"):
                return error(400, "validation_failed", "subject_type is user or team, role is user or collaborator")
            return json_response(201, {"user_known": True})
        if method == "GET" and action == "expiry":
            ttl = vm.ttl or {}
            policy = {
                "max_lifetime_secs": ttl.get("max_lifetime_secs"),
                "on_stop": ttl.get("on_stop") or {"type": "never"},
            }
            # The fake's clock never moves, so the whole lifetime is left.
            return json_response(
                200,
                {"policy": policy, "max_life_expires_in_secs": policy["max_lifetime_secs"], "deletes_in_secs": None},
            )
        if method == "POST" and action == "secrets" and key and sub in ("", "rotate"):
            if body.get("exposure") == "env" and not body.get("target_unit"):
                return error(400, "validation_failed", "exposure env needs a target_unit")
            value = base64.b64decode(body["value_b64"]).decode()
            secrets[key] = (value, body.get("setup_tag"))
            # `set` stores the secret for the VM's next lifecycle event; `rotate` also pushes it
            # into the running guest now: a file under the secrets directory by default, an
            # `export` line in the `@login` env file for `exposure: env` with `target_unit: @login`.
            if sub == "":
                return json_response(204)
            if not running:
                return json_response(200, {"vm_count": 0, "unconfirmed": [], "skipped": [vm.id]})
            if body.get("exposure") == "env" and body.get("target_unit") == "@login":
                kept = [
                    line
                    for line in guest.files.get(_LOGIN_ENV, "").split("\n")
                    if line and not line.startswith(f"export {key}=")
                ]
                quoted = value.replace("'", "'\\''")
                guest.files[_LOGIN_ENV] = "\n".join([*kept, f"export {key}='{quoted}'"]) + "\n"
            elif (body.get("exposure") or "file") == "file":
                guest.files[f"{secrets_root}/{key}"] = value
            return json_response(200, {"vm_count": 1, "unconfirmed": [], "skipped": []})
        if method == "POST" and action == "exec-with-secrets":
            if not running:
                return invalid_state(name, vm, "run a command")
            if in_argv := leaked(body["command"]):
                return error(400, "validation_failed", f"mock: the value of secret {in_argv} is in the command's argv")
            # Inject the selected secrets, run the command, then wipe them, as the server does.
            selector = body["selector"]
            directory = secrets_root
            injected = [
                n
                for n, (_, tag) in secrets.items()
                if (tag == selector["tag"] if selector["kind"] == "setup_tag" else selector["kind"] == "all" or n in selector["names"])
            ]
            for n in injected:
                guest.files[f"{directory}/{n}"] = secrets[n][0]
            # The guest agent's deadline is `timeout_secs`, 30 s when it is left out; the secrets
            # are wiped either way.
            stdout, stderr, code, timed_out = _run_in_guest(
                body["command"], guest, 30 if body.get("timeout_secs") is None else body["timeout_secs"]
            )
            for n in injected:
                del guest.files[f"{directory}/{n}"]
            return json_response(
                200,
                {
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": code if timed_out is None else 124,
                    "timed_out": timed_out is not None,
                },
            )
        if method == "POST" and action == "exec":
            if not running:
                return invalid_state(name, vm, "run a command")
            if in_argv := leaked(body["command"]):
                return error(400, "validation_failed", f"mock: the value of secret {in_argv} is in the command's argv")
            # The guest agent's deadline is `timeout_secs`, 30 s when it is left out.
            stdout, stderr, code, timed_out = _run_in_guest(
                body["command"], guest, 30 if body.get("timeout_secs") is None else body["timeout_secs"]
            )
            # At the deadline the agent kills the command and the stream ends with exit 124, `timed_out`.
            end = (
                _sse("exit", json.dumps({"code": code, "timed_out": False}))
                if timed_out is None
                else _sse("exit", json.dumps({"code": 124, "timed_out": True}))
            )
            return stream(
                (_sse("stdout", stdout) if stdout else "")
                + (_sse("stderr", stderr) if stderr else "")
                + end
            )
        return error(404, "resource_not_found", f"no mock route for {method} {request.url.path}")

    return httpx.MockTransport(handler)
