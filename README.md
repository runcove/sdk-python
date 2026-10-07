# Python SDK (runcove-sdk)

Python SDK for the Cove REST API — the API of the `cove-server` daemon. Its models and
per-operation calls are generated from `sdk/openapi.yaml`, the canonical contract; the client on
top of them (transport, auth, streams, pagination, errors) is hand-written.

- Installed as `runcove-sdk`, imported as `cove_sdk` (`from cove_sdk import CoveClient`).
- Python >= 3.11. Runtime dependencies: `httpx`, `anyio`, `attrs`, `typing-extensions`.
- Two clients with the same surface: `CoveClient` (sync) and `AsyncCoveClient` (async). The sync
  client is generated from the async one, so a method has the same name and arguments in both.
- Resource groups follow the API's areas: `vms`, `checkpoints`, `policies`, `host`, `secrets`,
  `tags`, `audit`, `keys`, `webhooks`, `meta`, `events`, `teams`, `admin`, `spotlight`.
- Fully typed (`py.typed`); `mypy --strict` runs over the package and its examples.

> **0.x: no stability promise.** A rename removes the old name outright rather than keeping a
> deprecated alias. Pin an exact version (`runcove-sdk==<version>`) rather than a range.

## Install

Install the package from PyPI. The SDK is pre-1.0, so pin an exact version:

```sh
pip install "runcove-sdk==<version>"
```

To match a Cove server, take `<version>` from `https://<cove-host>/public/sdk/index.json`.

### From your Cove server

A Cove server can also serve an SDK version, the one its operator installed on it, under `/public/sdk/`,
on its Warpgate-fronted URL (the external bearer listener does not serve `/public/sdk`). Use this when
you want exactly the SDK version your server's operator chose. The routes are unauthenticated. Install from the
server's PEP 503 index, or straight from the wheel's URL:

```sh
pip install --index-url https://<cove-host>/public/sdk/simple/ \
    --extra-index-url https://pypi.org/simple "runcove-sdk==<version>"
pip install https://<cove-host>/public/sdk/<wheel>
```

`<version>` and `<wheel>` are the ones `https://<cove-host>/public/sdk/index.json` lists (`kind`
`wheel` and `sdist`, `package` `runcove-sdk`). A server with nothing staged in `[daemon.sdk_releases]
dir` answers `index.json` with an empty `artifacts` list: there is then nothing to install from it.

- **The extra index is required.** The server serves only `runcove-sdk`; its dependencies (`httpx`,
  `anyio`, `attrs`, `typing-extensions`) come from a normal index. The direct-URL form resolves
  them from your configured index the same way.
- **Pin the version.** With `--extra-index-url`, pip takes the highest `runcove-sdk` across both
  indexes, so an unpinned install takes whichever of the server's copy and PyPI's is newer. Pin
  `==<version>` to get the version your server serves. A pin picks the version, not the index the
  file comes from; only the direct wheel URL guarantees the server's own file.
- **Offline installs are not solved.** Neither form installs without reaching an index that
  carries the dependencies; mirror them yourself.
- pip checks each download against the `#sha256=` the index publishes for it.

### Inside a Cove VM, a release less than three days old is held back

The Cove golden images give pip an `uploaded-prior-to = P3D` cooldown. PyPI dates a release by its
upload, and the server's index dates a file by the time the server staged it, so a just-released
`runcove-sdk` is hidden from pip until it is three days old (pip prints "from versions: none").
Lift the cooldown for `runcove-sdk` alone (`--uploaded-prior-to P0D --no-deps`), then install its
dependencies under the cooldown. From PyPI:

```sh
pip install --uploaded-prior-to P0D --no-deps "runcove-sdk==<version>"
pip install "runcove-sdk==<version>"
```

From your server, either install the wheel by its URL, which the cooldown does not check for the SDK
itself and still applies to its PyPI dependencies, or lift the cooldown the same way:

```sh
# Either by the wheel's URL:
pip install https://<cove-host>/public/sdk/<wheel>
# or lift the cooldown for runcove-sdk alone, then install its dependencies under it:
pip install --uploaded-prior-to P0D --no-deps \
    --index-url https://<cove-host>/public/sdk/simple/ "runcove-sdk==<version>"
pip install --index-url https://<cove-host>/public/sdk/simple/ \
    --extra-index-url https://pypi.org/simple "runcove-sdk==<version>"
```

`P0D` applies to every package a command resolves, PyPI dependencies included, so it goes only
with `--no-deps`. The command after it finds that `runcove-sdk` already installed and resolves only
its PyPI dependencies, which keep the cooldown.

## Quickstart

```python
from cove_sdk import CoveClient

# The external bearer listener ([api] bind): loopback by default, so plain http is accepted.
with CoveClient("http://127.0.0.1:8090", token="cvk_...") as client:
    # One page per list call; iter() follows next_cursor for "all of them".
    for vm in client.vms.iter(state="running"):
        print(vm.name)

    # Create answers 202 and creation continues in the background: wait for it.
    # No image: the host's default golden image (a wrong name 404s with the valid aliases).
    name = client.vms.create().name
    vm = client.vms.wait_for_state(name, "running", timeout=300)

    result = client.vms.exec_collect(name, command=["uname", "-a"])
    print(result.exit_code, result.stdout, end="")

    client.vms.delete(name)
```

The async client is the same, awaited:

```python
import asyncio
from cove_sdk import AsyncCoveClient

async def main() -> None:
    async with AsyncCoveClient("http://127.0.0.1:8090", token="cvk_...") as client:
        name = (await client.vms.create()).name
        await client.vms.wait_for_state(name, "running", timeout=300)
        result = await client.vms.exec_collect(name, command=["hostname"])
        print(result.stdout, end="")
        await client.vms.delete(name)

asyncio.run(main())
```

Use a client as a context manager, or call `close()` / `aclose()`, so its connection pool is
released. Methods take keyword arguments and return the generated models (`cove_sdk.types`);
a request body can be given as keywords (`create(name="web", cpus=2)`) or as one model or
mapping. Each method's docstring names the API-key scope it needs (`vms:read`, `vms:write`,
`vms:exec`, ...).

VM names: `create()` without a `name` lets the server pick one. A name you choose must be 3-30
characters of lowercase ASCII letters, digits and hyphens, and must not start or end with a hyphen
(`web-1`, not `Web_1`, `ab` or `-web`); a clone's `new_vm_name` follows the same rule. Any other
name raises `CoveAPIError` with `status == 400` and `code == "invalid_vm_name"`, before anything is
created, and `err.body["name"]` echoes the refused name.

A `base_url` that is plain `http://` is refused with `CoveConfigError` unless its host is
loopback (`localhost`, `127.0.0.0/8`, `::1`), because the credential would travel in cleartext;
`allow_insecure_http=True` accepts it for another host. The SDK never follows a redirect: a 3xx
raises `CoveConnectionError`.

## Authentication — match the credential to the listener

A Cove deployment has two listeners, and each accepts one kind of credential. Pass exactly one of
`token=`, `ticket=` or `auth=`; zero or two raise `CoveConfigError`.

| Listener | Credential | Client argument |
|---|---|---|
| External bearer listener (`[api] bind`, `127.0.0.1:8090` by default) | a `cvk_` API key (`cove key create`) | `token="cvk_..."`, the shorthand for `auth=BearerAuth(...)` |
| Warpgate-fronted main listener (`https://<cove-host>`) | a Warpgate SSO ticket, the one `cove login` stores (`~/.config/cove/ticket` on Linux, `~/Library/Application Support/cove/ticket` on macOS; `$XDG_CONFIG_HOME/cove/ticket` when `XDG_CONFIG_HOME` is set) | `ticket=...`, the shorthand for `auth=TicketAuth(...)` |

A bearer key on the Warpgate-fronted listener is refused with 401; so is a ticket on the bearer
listener. From another machine, either forward the port
(`ssh -L 8090:127.0.0.1:8090 <cove-host>`, which needs a shell account on the host) and keep the
loopback URL, or point `base_url` at the `https://` address an operator has fronted the listener
with (see the external API page of the Cove docs). Use a bearer key for
automation: a ticket can hit Warpgate's interactive step-up (401 `sudo_required`) on a sensitive
operation, which a headless caller cannot satisfy. Five
administrator operations — drain, agent update, bulk stop, bulk delete and checkpoint delete —
refuse every API key with 401 `sudo_required`, an admin key included.

`CoveAuth` is the base class of both strategies, and an `httpx.Auth`: subclass it and override
the private `_authorization` hook to supply a credential another way. Credentials never print (`repr` shows `BearerAuth(<redacted>)`) and
never pickle.

## Streams

Streamed exec, the console tail and the event streams are Server-Sent Events. Each returns a
stream object to **use in a `with` block** (`async with` on the async client) and iterate:

```python
import sys

from cove_sdk import ExecError, ExecExit, ExecPaused, ExecStderr, ExecStdout

with client.vms.exec("my-vm", command=["ls", "-la"]) as stream:
    for event in stream:
        match event:
            case ExecStdout(data=data):
                sys.stdout.write(data)  # a raw chunk, its own newlines included
            case ExecStderr(data=data):
                sys.stderr.write(data)
            case ExecExit(code=code, timed_out=timed_out):
                # timed_out: killed at the timeout_secs deadline (30 s by default); code is then 124.
                print("exited with", code, "(timed out)" if timed_out else "")
            case ExecError(error=error):
                print("exec failed:", error)
            case ExecPaused(reason=reason, new_state=state):
                print("VM left running mid-exec:", reason, state)
```

- Nothing is sent until the block is entered, so a non-2xx raises there. Leaving the block — the
  end of the stream, a `break` or an exception — closes the response, which stops the server
  holding the stream open. Iterating a stream outside its block raises `CoveError`.
- `ExecStdout` / `ExecStderr` carry raw chunks, not lines: concatenate them verbatim. The stream
  ends after exactly one `ExecExit`, `ExecError` or `ExecPaused`.
- **`exec_collect`** is the common case: it runs the stream for you and returns
  `ExecResult(stdout, stderr, exit_code, timed_out)`, raising `CoveError` on `ExecError`,
  `ExecPaused`, or a stream that ends without a terminal event. A command killed at its deadline
  returns `exit_code` 124 with `timed_out` true rather than raising.
- `timeout_secs=` on `exec` is the deadline the *server* puts on the guest command; `timeout=` is
  this client's (see [Timeouts](#timeouts)).
- `exec_with_secrets` is not a stream: the server buffers the run and returns its output as JSON.
  Its `timeout_secs=` is the server's deadline on the command (30 s when omitted, at most 3600:
  the server refuses more with 400 `validation_failed`); a command still running then is killed
  with everything that stayed in its process group, and the result has `exit_code` 124 and
  `timed_out` true.
- `vms.stream_console(name)` yields raw console lines: `lines=` historical ones first (the
  server sends 20 when `lines` is not given), then the live tail, which never ends on its own,
  so leave the block to stop. It does not reconnect unless you pass `reconnect=True`.
- A single SSE line or event over 16 MiB closes the stream with a `CoveError`.

### Event streams and their gap

`client.events.lifecycle()`, `client.events.all_vms()` and `client.events.vm(name)` yield
`LifecycleEvent` / `VmEvent` items. The server closes every event stream after 300 seconds; these
streams reconnect on that clean close by default (`reconnect=False` opts out), at most once per
second, and stop on cancellation or any non-2xx.

`events.vm(name)` ends without reconnecting or raising after a `state` of `deleted` or an `error`
(a failed create): the server ends that stream there, since the name is free again and a later VM
under it is a different VM. Open `events.vm(name)` again to follow it.

**A reconnect does not resume.** The server does not honour `Last-Event-ID`, so the SDK sends none:
a reconnected stream starts from "now", and events between the close and the reconnect are lost.
When the server drops events because this reader fell behind, the stream yields
`StreamLagged(skipped)` instead. After either, re-read the state you need (`vms.list`, `vms.get`)
rather than trusting the stream to be complete.

**A state can repeat.** `all_vms()` and `vm(name)` also carry advisories about a VM whose state did
not change (a health degrade or recovery, creation progress, pause and clone details), so an item can
repeat the state the previous one carried for that VM. Treat the state as idempotent: act when it
changes, not on every item.

## Errors

Every error the SDK raises is a `CoveError`, with one exception: a request body that does not
match the generated types (an unknown top-level field, a missing required field, a bad enum value
such as an unknown selector `kind`) is refused before anything is sent, with a plain `TypeError`:

```
CoveError
├── CoveConfigError        bad client arguments (also a ValueError)
├── CoveConnectionError    unreachable server, transport failure, or a redirect
│   └── CoveTimeoutError   an httpx timeout, or wait_for_state's deadline
├── CoveDecodeError        a 2xx body the SDK could not decode (.status, .body)
├── DownloadTruncatedError a download shorter than its Content-Length (.expected_bytes, .received_bytes)
└── CoveAPIError           a non-2xx answer: .status, .code, .message, .body
    ├── AuthenticationError    401
    ├── PermissionDeniedError  403
    │   └── FilePathDeniedError    403 file_path_denied
    ├── NotFoundError          404
    │   └── VmFileNotFoundError    404 file_not_found
    ├── ConflictError          409: .deny, .retry_after_secs
    ├── PayloadTooLargeError   413
    │   └── FileTooLargeError      413 file_too_large
    ├── ValidationError        422, or 400 validation_failed
    │   └── FileNotRegularError    422 file_not_regular
    ├── UpgradeRequiredError   426 CLI_TOO_OLD: .server_api_version, .min_cli_version
    ├── RateLimitError         429 rate_limited: .retry_after_secs
    └── ServerError            5xx: .retry_after_secs
        └── UnavailableError       503 unavailable
```

`code` is the exact wire string from the server's error catalogue; the SDK defines none of its
own. `body` is the parsed JSON body, or the text when it is not JSON.

- **A request the server cannot decode is a `ValidationError` with status 400.** Malformed JSON,
  a field of the wrong type, an unknown enum value, or a query or path value of the wrong type
  answers 400 `validation_failed`, with the field in `body["field"]`; a well-formed value the
  server refuses is 422. Both raise `ValidationError`, so one `except ValidationError` covers them,
  and so does any other 400 `validation_failed` the server answers (a relative path on file
  transfer, for one).
  Any other 400 is a plain `CoveAPIError`.
- **404 may mean "not yours".** Cove answers most 403s as 404 so a caller cannot probe for what
  exists: a VM that exists but is not yours reads as a missing one.
- **409 with a `DenyReason`.** An admission or quota refusal (`vms.create`, `vms.start`,
  `vms.resize`, `host.reserve`, ...) sets `ConflictError.deny` to a `DenyReason(code, details)`,
  e.g. `ram_headroom_exceeded` with its numeric fields in `details`. A name still taken, or in its
  post-delete cooldown, is `code == "vm_name_taken"` with `retry_after_secs`.
- **503** with `feature_disabled` means the feature (secrets, webhooks) is off on that host, not
  that the server is down.
- **429 `rate_limited` means this source IP is over its request budget.** The bearer listener
  allows each source IP 30 requests per second by default (the operator sets it with
  `[api] rate_limit_per_ip`). The budget is per IP, not per key or per client, so every caller
  behind one NAT or tunnel shares it, and a program that fires many calls at once
  (`asyncio.gather`, a thread pool) runs through it fast. The SDK **never retries**: catch
  `RateLimitError`, wait `retry_after_secs` seconds (the response's `Retry-After`; `None` if the
  server sent none), and send the request again. Do this for cleanup too: a `vms.delete` in a
  `finally` that gets a 429 must be retried, or the VM keeps running. `ServerError` carries
  `retry_after_secs` as well, set only when a 5xx sent `Retry-After`.
- **503 `unavailable` "file transfer busy"** is the file-transfer API's per-person cap: one person
  (a user, across their sessions and personal keys, or a team key's team) may have 4 uploads or
  downloads, and 8 file stats, in flight on a host. One more is refused at once with no
  `Retry-After`; retry when one of your transfers finishes. It raises `UnavailableError` (see
  [File transfer](#file-transfer)).
- **426 is `UpgradeRequiredError`**: the server no longer speaks this SDK's API version. Install
  the SDK that matches it (see [Versions](#versions)).

```python
from cove_sdk import ConflictError, CoveAPIError, NotFoundError

try:
    client.vms.create(name="web-1")
except ConflictError as err:
    if err.deny is not None:
        print("refused:", err.deny.code, dict(err.deny.details))
    elif err.code == "vm_name_taken":
        print("name taken; retry in", err.retry_after_secs, "s")
    else:
        raise
```

Retrying a call the rate limit refused:

```python
import time

from cove_sdk import RateLimitError


def delete_with_retry(client, name: str, attempts: int = 5) -> None:
    for attempt in range(attempts):
        try:
            client.vms.delete(name)
            return
        except RateLimitError as err:
            if attempt == attempts - 1:
                raise
            time.sleep(err.retry_after_secs or 1)
```

## File transfer

`client.vms.files` moves single files in and out of a running VM (`GET`, `PUT` and `HEAD` on
`/api/vms/{name}/files`), with the same methods on both clients. The key needs `files:read` to stat
or download and `files:write` to upload; both are in a new key's default scopes. `files:write` is as
strong as `vms:exec`: a file written as root can run code. The caller also needs SSH access to the
VM. `path` is the file's absolute path in the guest.

```python
st = client.vms.files.stat("my-vm", "/etc/os-release")       # VmFileStat(size, mode, mtime)
data = client.vms.files.download_bytes("my-vm", "/var/log/app.log")

with client.vms.files.download("my-vm", "/var/log/app.log") as dl:   # a stream, for a big file
    print(dl.size, oct(dl.mode or 0))
    for chunk in dl:
        sink.write(chunk)

done = client.vms.files.upload("my-vm", "/root/run.sh", b"#!/bin/sh\necho hi\n", mode=0o755)
print(done.size, done.sha256)                                 # FileUploaded

with open("data.tar", "rb") as f:                             # a file object: read from its position
    client.vms.files.upload("my-vm", "/root/data.tar", f)

client.vms.files.upload("my-vm", "/root/out.bin", chunks(), size=total)   # an iterator needs size=
```

- **A short download is a failed download.** Once the server has sent `200` it cannot change the
  status, so a transfer that fails part-way ends the body early. The SDK checks the body against its
  `Content-Length` and raises `DownloadTruncatedError` rather than return fewer bytes as if they
  were the file.
- **An upload needs its size up front.** The server refuses a chunked body. Bytes (a `str` is sent
  as UTF-8) and a seekable file object have a known size; an iterator, or a file object that cannot
  seek, needs `size=`. A body that yields a different number of bytes raises `CoveError` before the
  server commits anything. The guest renames the file into place only once every byte has arrived,
  so a failed upload leaves the old file as it was. On the async client a file object is read in a
  worker thread, and an iterator may be sync or async.
- **Typed errors.** 413 `file_too_large` is `FileTooLargeError` (the message states the host's
  limit). 403 `file_path_denied` is `FilePathDeniedError`, for a deny-listed or pseudo-filesystem
  path; a key without the scope is a plain `PermissionDeniedError`. 404 `file_not_found` is
  `VmFileNotFoundError`, and a missing VM is a plain `NotFoundError`. 422 `file_not_regular` is
  `FileNotRegularError`: a directory, a device, or a symlink anywhere in the path, since symlinks
  are refused and never followed. 503 `unavailable` is `UnavailableError` (any endpoint's 503
  `unavailable`; here, the guest agent was lost or timed out, or it already has as many transfers
  open as it allows). Retry it. A `HEAD` error has
  no body; the server names its code in `X-Cove-Error-Code`, so `stat` raises the same class a
  download would. From a server without that header, the status alone picks: a 403 or a 404 there
  stays the plain class with `code` `None`.
- **Timeouts.** `download`'s `timeout=` bounds the idle time between chunks, as on the other
  streams; by default only the connect phase is bounded. The server ends a transfer that averages
  under 256 KiB/s (after 60 s at least).
- **Mode.** `mode=` is an int (`0o755`) or the octal string the server takes (`"0755"`), within
  `0o777`. Without one, the server keeps the replaced file's bits, or uses `0644` for a new file.

## Spotlight

`client.spotlight` puts a local git worktree onto a long-lived VM at a path, switches it to another
worktree, and puts the base tree back with `off`, without restarting anything on the VM. It is the
SDK's form of `cove dev spotlight`, over the HTTP API alone: no SSH, and no rsync on your machine;
`git` must be on `PATH`.

```python
on = client.spotlight.on("my-box", tree="./wt-feature", dest="/srv/app")
client.spotlight.on("my-box", tree="./wt-fix", dest="/srv/app")  # a switch
client.spotlight.status("my-box")  # SpotlightStatus(dest, base, source), or None
client.spotlight.off("my-box", tree=".")  # restores the base commit
```

- **What is sent.** The worktree's tracked files plus its untracked files git does not ignore
  (`git ls-files -co --exclude-standard`), as one gzip tar uploaded with `vms.files`, with modes and
  symlinks kept. Each switch sends the whole tree; one over the host's file limit raises
  `FileTooLargeError` before anything changes on the VM. The async client packs in a worker thread.
  The tree is read, tarred and gzipped in memory, so it suits source trees rather than large
  binaries, and the upload counts against the call's `timeout=`. A submodule's contents are not
  sent, so a switch deletes a submodule's files in `dest` unless a protect entry covers them.
- **How it lands.** One `exec` of a fixed sh script (every value is an argument) extracts the tar
  beside `dest` and mirrors it onto `dest` with delete semantics, with `rsync` when the image has
  it and `find`/`cp` otherwise. Nothing matching `protect=` (rsync protect patterns, as the CLI
  uses; default `SPOTLIGHT_DEFAULT_PROTECT`: the `node_modules`, `target`, `volumes` and `.venv`
  directories, and `.env`), nor anything below it, nor a `.git/`, is ever deleted, so what the VM built there
  survives a switch. A file the tree itself holds there is still written, as with the CLI.
  Wildcards in an entry behave as in rsync only within one path component (as in the defaults'
  plain names): on the fallback path a `*` can also match across a `/`. Files land owned by root
  (`root:root`), while the CLI's rsync writes them as the SSH user.
- **What `dest`'s `.gitignore` ignores is kept.** With rsync the script uses the CLI's filter rules
  in the CLI's order (`:- .gitignore`, then `--exclude=.git/`, then the protect rules): `.git/` is
  never touched, and a path a `.gitignore` in `dest` ignores (build output, `*.log`, `.env.local`) is
  not deleted. rsync reads the `.gitignore` files `dest` holds before the switch, so the first bind
  of a `dest` with none deletes ignored files, as the CLI's first sync does. As with the CLI, a
  file the tree holds that its own `.gitignore` ignores (a force-added one) is not written.
- **Without rsync on the VM** the script cannot read `.gitignore`, so when `dest` holds one outside
  a protected path it refuses (exit 3) before changing anything, and the `CoveError` says to
  install rsync on the VM. A protected path inside a directory the tree replaces with a file or
  symlink can make this fallback fail part-way, after its deletions. The first fallback apply
  writes the tree's own `.gitignore` into `dest`, so on an image without rsync every later `on`
  and `off` is refused (and `off` cannot clear the binding) until rsync is installed.
- **Deadline.** The apply runs under `timeout_secs=` (default 300). An apply killed at its deadline
  raises `CoveError` saying so: `dest` may be half-mirrored, so run `on` again. The next run
  removes the stage directory the killed one left beside `dest`, and spotlight tarballs over an
  hour old in `/tmp`.
- **Where the binding lives.** In the VM's tags: `spotlight.base` (the HEAD of the first bind,
  which `off` restores; a switch keeps it), `spotlight.dest` and `spotlight.source` (the branch).
  They are written only after a successful apply, show in `cove tag ls <vm>`, and let
  `off` run from another process. The CLI keeps its binding on the laptop, so the two do not see
  each other's yet. As with the CLI, `on` with a different `dest` re-points the binding but keeps
  the base, so `off` restores only the new `dest`, never the old one.
- **`off`** needs a checkout that holds the base commit (else `CoveError`: "run `git fetch`"),
  applies `git archive <base>` the same way, and deletes the tags. It restores the recorded commit
  by its id, never a branch or other ref. With nothing bound it returns
  `None`, as the CLI's `off` does.
- **Scopes:** `tags:read` and `tags:write` (the binding), `files:write` (the upload), `vms:exec`
  (the apply).

## Timeouts

By default a client bounds only the connect phase (10 s) and sets no deadline on the rest of a
call, as the TypeScript SDK does. `timeout=` on the client sets the default for every call, and
`timeout=` on a method overrides it for that call: a number of seconds, an `httpx.Timeout`, or
`None` for no timeout at all.

Streams are different. A stream bounds its connect phase only, whatever the client's default.
A `timeout=` passed to a stream method becomes httpx's read timeout, which httpx applies to every
read: it is an **idle bound between chunks**, not a deadline on the response headers. This
differs from the TypeScript SDK, whose stream deadline covers the headers only; httpx has no way to
lift a timeout once the headers arrive.

`vms.wait_for_state(name, states, timeout=..., interval=1.0)` takes a required `timeout`, in
seconds, for the whole wait; when it passes, `CoveTimeoutError` names the last state seen. A VM that
settles in a state you did not ask for (`failed`, say) is not an error there: polling continues to
the deadline.

## Cancellation

On the async client, cancel the task (or the anyio cancel scope) that awaits the call: the
cancellation propagates unwrapped, never as a `CoveError`, and an open stream closes its response
as its `async with` block exits. The sync client has no cancellation: httpx offers no cancel token
for a blocking call, so bound the call with `timeout=` instead.

## Versions

Every request declares the API version this SDK speaks (`X-Cove-Api-Version`, the package's
`API_VERSION`, generated from the contract), and every response carries the server's.
`client.server_api_version` is the last one the server sent (`None` before any).

- **The server speaks another version but still serves this one.** The call succeeds and the
  client emits one `CoveApiVersionWarning` (a `UserWarning`) per client through `warnings`. The SDK
  never refuses on skew and never configures `logging`. Filter or escalate it like any warning:

  ```python
  import warnings
  from cove_sdk import CoveApiVersionWarning

  warnings.filterwarnings("ignore", category=CoveApiVersionWarning)   # silence it
  warnings.filterwarnings("error", category=CoveApiVersionWarning)    # or fail on it
  ```

- **The server no longer speaks this SDK's version.** It answers 426 `CLI_TOO_OLD`, raised as
  `UpgradeRequiredError` with `server_api_version` and `min_cli_version` (the oldest cove-cli
  release that speaks the server's version — a CLI version, not an SDK one). Install the SDK
  listed in the server's `/public/sdk/index.json` on its Warpgate-fronted URL. Any other 426 stays
  a plain `CoveAPIError`.

## Pagination

List methods return one page and its `next_cursor`; a non-null `next_cursor` is the only sign
there is more. The `iter*` twins walk every page (`async for` on the async client), and a
`timeout=` applies to each page: `vms.iter`, `vms.iter_events_log`, `checkpoints.iter_for_vm`,
`checkpoints.iter_all`, `audit.iter`, `webhooks.iter_deliveries`, `admin.iter_vms`,
`admin.iter_checkpoints`.

## Secrets and webhooks

Secrets are scope-first: `client.secrets.vm(name)`, `.user(username)`, `.team(name)` or
`.project(project_id)`, then `list`, `set`, `unset`, `rotate` or `import_`. Values are write-only:
`list` returns names.

`verify_webhook_signature(secret=..., headers=..., body=...)` checks a webhook delivery's
`Cove-Signature` (HMAC-SHA256 over `<ce-id>.<ce-time>.<raw body>`, both entries during rotation
grace, a replay window on `ce-time`, constant-time compare). Pass the raw body exactly as
received, never re-serialised JSON.

## What is covered

Both clients have a method for every operation the external bearer listener serves, except the
operation in `tests/coverage_allowlist.py` that no method wraps yet: `listMyConnectedApps`.
`tests/test_unit_coverage.py` fails when an operation
is added to the contract without a method or an allowlist entry. Operations the bearer listener
does not serve have no method.

## Development

From the repository root:

```sh
./scripts/test-sdk-python.sh          # mypy --strict, build the wheel and sdist, run pytest on the installed wheel
./scripts/sync-sdk-python.sh --check  # the generated parts match sdk/openapi.yaml
./scripts/sync-sdk-python.sh          # regenerate them after a contract change
```

Both use the hash-locked toolchain venv (`scripts/sdk-python-env.sh install` builds it from
`sdk/python/requirements-dev.lock`). Never hand-edit `src/cove_sdk/_generated/`, `_meta.py`,
`types.py`, `src/cove_sdk/_sync/` or `tests/_sync/`: write the async code and tests, and the sync
ones are mirrored from them.

## Examples

`examples/create_exec_destroy.py` (sync) and `examples/create_exec_destroy_async.py` (async) walk
the whole flow — create, wait until running, streamed and buffered exec, delete in a `finally`:

```sh
COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/create_exec_destroy.py
python examples/create_exec_destroy.py --mock   # offline, against an in-process fake server
```

The key is read from `COVE_TOKEN` only: the examples take no `--token` flag, which would leak it
through `ps` and shell history. `--base-url` is an alternative to `COVE_URL`; `--image` (or
`COVE_IMAGE`) picks a golden image, and the host's default is used when it is omitted. The
`--mock` path
(`examples/_mock.py`, an `httpx.MockTransport`) doubles as a template for stubbing the SDK in your
own tests: pass `transport=` to either client. The suite runs both examples under `--mock`
(`tests/test_component_examples.py`).

Twelve worked use cases sit beside them. Each is the same program as its twin in the TypeScript
SDK's examples (same steps, same order, same output), and the documentation portal shows each
pair side by side under Use cases:

| File | What it does |
|---|---|
| `agent_sandbox.py` | An agent's sandbox: write code into a VM, run its tests, fix it, run them again |
| `ci_runner.py` | A CI runner: clone, set up with a setup-only secret (`exec_with_secrets`, `setup_tag`), test, stop at the first failure |
| `file_processing.py` | Send input files into a throwaway VM, process them there, read the result back |
| `event_driven.py` | Follow a new VM's event stream and provision it the moment it runs |
| `fan_out.py` | Split a job over three VMs at once with `AsyncCoveClient`, then combine the results |
| `pet_vm.py` | A long-lived VM that pauses when idle: disk-only checkpoint, roll back a broken change, hibernate, wake |
| `code_execution.py` | One fresh VM per request: upload a snippet, run it under a deadline, delete the VM |
| `preview.py` | A VM per pull request, tagged with its number: start the app, publish its port, delete by tag |
| `parallel_tries.py` | Prepare one VM, checkpoint it, clone a VM per candidate fix with `AsyncCoveClient`, keep the first that passes |
| `repro_box.py` | A VM with a lifetime cap to reproduce a bug: checkpoint the failure, give a colleague access |
| `coding_agent.py` | A fresh VM per task for Claude Code: the key as a secret, clone, run the agent, download the diff |
| `spotlight.py` | Put a git worktree onto a VM, switch it to another, then restore the base (`client.spotlight`) |

Each runs offline with `--mock` (the suite runs every one and checks what it prints), or against a
host with `COVE_URL` and `COVE_TOKEN`; the comment at the top of a file lists anything else it needs.

## License

Licensed under the Apache License, Version 2.0. The full text is in `LICENSE`.
