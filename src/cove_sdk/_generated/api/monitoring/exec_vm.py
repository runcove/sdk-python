from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.exec_request_dto import ExecRequestDto
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    body: ExecRequestDto,
    encoding: str | Unset = UNSET,
    x_cove_exec_encoding: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_cove_exec_encoding, Unset):
        headers["x-cove-exec-encoding"] = x_cove_exec_encoding

    params: dict[str, Any] = {}

    params["encoding"] = encoding

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/exec".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecRequestDto,
    encoding: str | Unset = UNSET,
    x_cove_exec_encoding: None | str | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Execute a command in the guest, streaming its output

     **`200 text/event-stream`, always.** SSE event types:
    - `stdout` / `stderr`: data is one output chunk: a line with its newline, or a piece of at most 64
    KiB of a longer line. Concatenate the chunks of each stream to rebuild its output. Bytes the command
    wrote that are not valid UTF-8 arrive as U+FFFD. **How the chunk is written depends on the caller.**
    A request that opts in with `?encoding=json` (or the `x-cove-exec-encoding: json` header) gets each
    chunk as a JSON string (`"one\\r\\n"`), and the response carries `x-cove-exec-encoding: json`:
    decode the string to get the chunk byte for byte, carriage returns included. The opt-in is that
    parameter or header alone, whatever `X-Cove-Api-Version` the request declares. Any other request
    (such as `curl`, or a client that predates the parameter) gets the raw chunk, as before, and no such
    header: SSE ends a data line at a carriage return, so in raw form a `\\r` in the output arrives as a
    line break.
    - `exit`: terminal, data `{"code": <int>, "timed_out": <bool>}` (schema `ExecExit`). `timed_out` is
    `true` when the command ran past `timeout_secs` (default 30): the guest SIGKILLs the command's whole
    process group — the command and everything it started that stayed in its group — and `code` is 124,
    as `timeout(1)` reports. A command that exits 124 on its own has `timed_out: false`.
    - `error`: terminal, data `{"error": "<message>"}`.
    - `paused`: terminal, data `{"reason": "...", "new_state": "..."}` — the VM left the running state
    mid-exec (elastic-pause reaper, manual pause, checkpoint, stop, ...), so the stream was cut with an
    explicit reason instead of hanging forever. `new_state` is the state the VM moved to, spelled as
    everywhere else in this API (`pausing`, `stopping`, ...). The command does not outlive the stream:
    the host closes its guest connection, and the guest kills the command's process group once the VM
    runs again.

    Exactly one of `exit` / `error` / `paused` ends the stream. The response carries `x-accel-buffering:
    no` so reverse proxies do not hold frames back, and sends an SSE keep-alive comment every 15 seconds
    — comfortably under the ~30 second idle-connection cutoff some network paths in front of this daemon
    enforce, so a long-running command should not see the stream cut by a quiet middlebox. A stream that
    ends early for any other reason kills the command the same way: the client disconnected, or the API
    key that opened it was revoked mid-run.

    **The command's environment.** It runs as root, or as `user`, with a login-like environment: `HOME`,
    `USER`, `LOGNAME` and `SHELL` of that account, the variables in the VM's `/etc/environment`, a
    `LANG`, and a `PATH` of the usual profile directories (mise's shims, `~/.local/bin`,
    `/usr/local/sbin`, `/usr/local/bin`, then the system directories). It starts in the account's home
    directory unless `cwd` says otherwise. No profile file runs unless `login` is `true`, which runs the
    command through the account's login shell. `env` is applied last, so it wins. The command runs at
    default priority (nice 0, default OOM score), not with the guest agent's own. `cwd`, `env`, `user`
    and `login` need a guest agent that speaks protocol 9 or later: on a VM whose agent is older the
    stream ends with an `error` event naming both versions. Cove updates an outdated agent when it
    connects to it, so a retry shortly after usually succeeds. A `cwd` that does not exist or an unknown
    `user` also ends the stream with an `error` event.

    **Stdin.** `stdin` (text) or `stdin_b64` (standard base64, for bytes) is written to the command's
    stdin, which is then closed, so a reader sees end of input: pipe a script into an interpreter
    (`["python3", "-"]`) or data into a command. At most 1 MiB (1048576 bytes, counted after decoding);
    a larger one, both fields at once or malformed base64 is refused with 400 before anything runs.
    Without either, stdin is empty (`/dev/null`). Stdin needs a guest agent that speaks protocol 10 or
    later: on an older one the stream ends with an `error` event naming both versions instead of running
    the command without its input. Interactive (streamed) stdin is not offered; for larger payloads
    write a file first.

    **The buffered, secrets-injected form has moved to `POST /api/vms/{name}/exec-with-secrets`
    (`execVmWithSecrets`).** Until the split, this one route answered with either an SSE stream or a
    JSON body depending on whether the request body carried a `selector` field — the exact shape that
    started this description-generation effort, because OpenAPI cannot say "the response shape depends
    on a request field" and a real generator run against it silently dropped the streaming mode.

    **REMOVED in API version 5: sending `selector` to this operation.** It was accepted for one
    deprecation window and is now refused with 400 `validation_failed` naming the `selector` field. Use
    `execVmWithSecrets` instead.

    The caller needs SSH access to the VM (`vm.ssh`): the owner, a sharee, or an administrator (an
    admin-listed user's session or admin key; their ordinary API key or connected app is not one, and
    gets the same 404 as a VM that does not exist). An exec by anyone other than the VM's owner is
    recorded in the audit log as `vm.exec.opened`; the command line is not recorded.

    Args:
        name (str):
        encoding (str | Unset):
        x_cove_exec_encoding (None | str | Unset):
        body (ExecRequestDto): POST /vms/{name}/exec request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
        encoding=encoding,
        x_cove_exec_encoding=x_cove_exec_encoding,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecRequestDto,
    encoding: str | Unset = UNSET,
    x_cove_exec_encoding: None | str | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Execute a command in the guest, streaming its output

     **`200 text/event-stream`, always.** SSE event types:
    - `stdout` / `stderr`: data is one output chunk: a line with its newline, or a piece of at most 64
    KiB of a longer line. Concatenate the chunks of each stream to rebuild its output. Bytes the command
    wrote that are not valid UTF-8 arrive as U+FFFD. **How the chunk is written depends on the caller.**
    A request that opts in with `?encoding=json` (or the `x-cove-exec-encoding: json` header) gets each
    chunk as a JSON string (`"one\\r\\n"`), and the response carries `x-cove-exec-encoding: json`:
    decode the string to get the chunk byte for byte, carriage returns included. The opt-in is that
    parameter or header alone, whatever `X-Cove-Api-Version` the request declares. Any other request
    (such as `curl`, or a client that predates the parameter) gets the raw chunk, as before, and no such
    header: SSE ends a data line at a carriage return, so in raw form a `\\r` in the output arrives as a
    line break.
    - `exit`: terminal, data `{"code": <int>, "timed_out": <bool>}` (schema `ExecExit`). `timed_out` is
    `true` when the command ran past `timeout_secs` (default 30): the guest SIGKILLs the command's whole
    process group — the command and everything it started that stayed in its group — and `code` is 124,
    as `timeout(1)` reports. A command that exits 124 on its own has `timed_out: false`.
    - `error`: terminal, data `{"error": "<message>"}`.
    - `paused`: terminal, data `{"reason": "...", "new_state": "..."}` — the VM left the running state
    mid-exec (elastic-pause reaper, manual pause, checkpoint, stop, ...), so the stream was cut with an
    explicit reason instead of hanging forever. `new_state` is the state the VM moved to, spelled as
    everywhere else in this API (`pausing`, `stopping`, ...). The command does not outlive the stream:
    the host closes its guest connection, and the guest kills the command's process group once the VM
    runs again.

    Exactly one of `exit` / `error` / `paused` ends the stream. The response carries `x-accel-buffering:
    no` so reverse proxies do not hold frames back, and sends an SSE keep-alive comment every 15 seconds
    — comfortably under the ~30 second idle-connection cutoff some network paths in front of this daemon
    enforce, so a long-running command should not see the stream cut by a quiet middlebox. A stream that
    ends early for any other reason kills the command the same way: the client disconnected, or the API
    key that opened it was revoked mid-run.

    **The command's environment.** It runs as root, or as `user`, with a login-like environment: `HOME`,
    `USER`, `LOGNAME` and `SHELL` of that account, the variables in the VM's `/etc/environment`, a
    `LANG`, and a `PATH` of the usual profile directories (mise's shims, `~/.local/bin`,
    `/usr/local/sbin`, `/usr/local/bin`, then the system directories). It starts in the account's home
    directory unless `cwd` says otherwise. No profile file runs unless `login` is `true`, which runs the
    command through the account's login shell. `env` is applied last, so it wins. The command runs at
    default priority (nice 0, default OOM score), not with the guest agent's own. `cwd`, `env`, `user`
    and `login` need a guest agent that speaks protocol 9 or later: on a VM whose agent is older the
    stream ends with an `error` event naming both versions. Cove updates an outdated agent when it
    connects to it, so a retry shortly after usually succeeds. A `cwd` that does not exist or an unknown
    `user` also ends the stream with an `error` event.

    **Stdin.** `stdin` (text) or `stdin_b64` (standard base64, for bytes) is written to the command's
    stdin, which is then closed, so a reader sees end of input: pipe a script into an interpreter
    (`["python3", "-"]`) or data into a command. At most 1 MiB (1048576 bytes, counted after decoding);
    a larger one, both fields at once or malformed base64 is refused with 400 before anything runs.
    Without either, stdin is empty (`/dev/null`). Stdin needs a guest agent that speaks protocol 10 or
    later: on an older one the stream ends with an `error` event naming both versions instead of running
    the command without its input. Interactive (streamed) stdin is not offered; for larger payloads
    write a file first.

    **The buffered, secrets-injected form has moved to `POST /api/vms/{name}/exec-with-secrets`
    (`execVmWithSecrets`).** Until the split, this one route answered with either an SSE stream or a
    JSON body depending on whether the request body carried a `selector` field — the exact shape that
    started this description-generation effort, because OpenAPI cannot say "the response shape depends
    on a request field" and a real generator run against it silently dropped the streaming mode.

    **REMOVED in API version 5: sending `selector` to this operation.** It was accepted for one
    deprecation window and is now refused with 400 `validation_failed` naming the `selector` field. Use
    `execVmWithSecrets` instead.

    The caller needs SSH access to the VM (`vm.ssh`): the owner, a sharee, or an administrator (an
    admin-listed user's session or admin key; their ordinary API key or connected app is not one, and
    gets the same 404 as a VM that does not exist). An exec by anyone other than the VM's owner is
    recorded in the audit log as `vm.exec.opened`; the command line is not recorded.

    Args:
        name (str):
        encoding (str | Unset):
        x_cove_exec_encoding (None | str | Unset):
        body (ExecRequestDto): POST /vms/{name}/exec request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
        encoding=encoding,
        x_cove_exec_encoding=x_cove_exec_encoding,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecRequestDto,
    encoding: str | Unset = UNSET,
    x_cove_exec_encoding: None | str | Unset = UNSET,
) -> Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]:
    """Execute a command in the guest, streaming its output

     **`200 text/event-stream`, always.** SSE event types:
    - `stdout` / `stderr`: data is one output chunk: a line with its newline, or a piece of at most 64
    KiB of a longer line. Concatenate the chunks of each stream to rebuild its output. Bytes the command
    wrote that are not valid UTF-8 arrive as U+FFFD. **How the chunk is written depends on the caller.**
    A request that opts in with `?encoding=json` (or the `x-cove-exec-encoding: json` header) gets each
    chunk as a JSON string (`"one\\r\\n"`), and the response carries `x-cove-exec-encoding: json`:
    decode the string to get the chunk byte for byte, carriage returns included. The opt-in is that
    parameter or header alone, whatever `X-Cove-Api-Version` the request declares. Any other request
    (such as `curl`, or a client that predates the parameter) gets the raw chunk, as before, and no such
    header: SSE ends a data line at a carriage return, so in raw form a `\\r` in the output arrives as a
    line break.
    - `exit`: terminal, data `{"code": <int>, "timed_out": <bool>}` (schema `ExecExit`). `timed_out` is
    `true` when the command ran past `timeout_secs` (default 30): the guest SIGKILLs the command's whole
    process group — the command and everything it started that stayed in its group — and `code` is 124,
    as `timeout(1)` reports. A command that exits 124 on its own has `timed_out: false`.
    - `error`: terminal, data `{"error": "<message>"}`.
    - `paused`: terminal, data `{"reason": "...", "new_state": "..."}` — the VM left the running state
    mid-exec (elastic-pause reaper, manual pause, checkpoint, stop, ...), so the stream was cut with an
    explicit reason instead of hanging forever. `new_state` is the state the VM moved to, spelled as
    everywhere else in this API (`pausing`, `stopping`, ...). The command does not outlive the stream:
    the host closes its guest connection, and the guest kills the command's process group once the VM
    runs again.

    Exactly one of `exit` / `error` / `paused` ends the stream. The response carries `x-accel-buffering:
    no` so reverse proxies do not hold frames back, and sends an SSE keep-alive comment every 15 seconds
    — comfortably under the ~30 second idle-connection cutoff some network paths in front of this daemon
    enforce, so a long-running command should not see the stream cut by a quiet middlebox. A stream that
    ends early for any other reason kills the command the same way: the client disconnected, or the API
    key that opened it was revoked mid-run.

    **The command's environment.** It runs as root, or as `user`, with a login-like environment: `HOME`,
    `USER`, `LOGNAME` and `SHELL` of that account, the variables in the VM's `/etc/environment`, a
    `LANG`, and a `PATH` of the usual profile directories (mise's shims, `~/.local/bin`,
    `/usr/local/sbin`, `/usr/local/bin`, then the system directories). It starts in the account's home
    directory unless `cwd` says otherwise. No profile file runs unless `login` is `true`, which runs the
    command through the account's login shell. `env` is applied last, so it wins. The command runs at
    default priority (nice 0, default OOM score), not with the guest agent's own. `cwd`, `env`, `user`
    and `login` need a guest agent that speaks protocol 9 or later: on a VM whose agent is older the
    stream ends with an `error` event naming both versions. Cove updates an outdated agent when it
    connects to it, so a retry shortly after usually succeeds. A `cwd` that does not exist or an unknown
    `user` also ends the stream with an `error` event.

    **Stdin.** `stdin` (text) or `stdin_b64` (standard base64, for bytes) is written to the command's
    stdin, which is then closed, so a reader sees end of input: pipe a script into an interpreter
    (`["python3", "-"]`) or data into a command. At most 1 MiB (1048576 bytes, counted after decoding);
    a larger one, both fields at once or malformed base64 is refused with 400 before anything runs.
    Without either, stdin is empty (`/dev/null`). Stdin needs a guest agent that speaks protocol 10 or
    later: on an older one the stream ends with an `error` event naming both versions instead of running
    the command without its input. Interactive (streamed) stdin is not offered; for larger payloads
    write a file first.

    **The buffered, secrets-injected form has moved to `POST /api/vms/{name}/exec-with-secrets`
    (`execVmWithSecrets`).** Until the split, this one route answered with either an SSE stream or a
    JSON body depending on whether the request body carried a `selector` field — the exact shape that
    started this description-generation effort, because OpenAPI cannot say "the response shape depends
    on a request field" and a real generator run against it silently dropped the streaming mode.

    **REMOVED in API version 5: sending `selector` to this operation.** It was accepted for one
    deprecation window and is now refused with 400 `validation_failed` naming the `selector` field. Use
    `execVmWithSecrets` instead.

    The caller needs SSH access to the VM (`vm.ssh`): the owner, a sharee, or an administrator (an
    admin-listed user's session or admin key; their ordinary API key or connected app is not one, and
    gets the same 404 as a VM that does not exist). An exec by anyone other than the VM's owner is
    recorded in the audit log as `vm.exec.opened`; the command line is not recorded.

    Args:
        name (str):
        encoding (str | Unset):
        x_cove_exec_encoding (None | str | Unset):
        body (ExecRequestDto): POST /vms/{name}/exec request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ScopeDeniedBody | str]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
        encoding=encoding,
        x_cove_exec_encoding=x_cove_exec_encoding,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecRequestDto,
    encoding: str | Unset = UNSET,
    x_cove_exec_encoding: None | str | Unset = UNSET,
) -> ApiError | CliTooOldBody | ScopeDeniedBody | str | None:
    """Execute a command in the guest, streaming its output

     **`200 text/event-stream`, always.** SSE event types:
    - `stdout` / `stderr`: data is one output chunk: a line with its newline, or a piece of at most 64
    KiB of a longer line. Concatenate the chunks of each stream to rebuild its output. Bytes the command
    wrote that are not valid UTF-8 arrive as U+FFFD. **How the chunk is written depends on the caller.**
    A request that opts in with `?encoding=json` (or the `x-cove-exec-encoding: json` header) gets each
    chunk as a JSON string (`"one\\r\\n"`), and the response carries `x-cove-exec-encoding: json`:
    decode the string to get the chunk byte for byte, carriage returns included. The opt-in is that
    parameter or header alone, whatever `X-Cove-Api-Version` the request declares. Any other request
    (such as `curl`, or a client that predates the parameter) gets the raw chunk, as before, and no such
    header: SSE ends a data line at a carriage return, so in raw form a `\\r` in the output arrives as a
    line break.
    - `exit`: terminal, data `{"code": <int>, "timed_out": <bool>}` (schema `ExecExit`). `timed_out` is
    `true` when the command ran past `timeout_secs` (default 30): the guest SIGKILLs the command's whole
    process group — the command and everything it started that stayed in its group — and `code` is 124,
    as `timeout(1)` reports. A command that exits 124 on its own has `timed_out: false`.
    - `error`: terminal, data `{"error": "<message>"}`.
    - `paused`: terminal, data `{"reason": "...", "new_state": "..."}` — the VM left the running state
    mid-exec (elastic-pause reaper, manual pause, checkpoint, stop, ...), so the stream was cut with an
    explicit reason instead of hanging forever. `new_state` is the state the VM moved to, spelled as
    everywhere else in this API (`pausing`, `stopping`, ...). The command does not outlive the stream:
    the host closes its guest connection, and the guest kills the command's process group once the VM
    runs again.

    Exactly one of `exit` / `error` / `paused` ends the stream. The response carries `x-accel-buffering:
    no` so reverse proxies do not hold frames back, and sends an SSE keep-alive comment every 15 seconds
    — comfortably under the ~30 second idle-connection cutoff some network paths in front of this daemon
    enforce, so a long-running command should not see the stream cut by a quiet middlebox. A stream that
    ends early for any other reason kills the command the same way: the client disconnected, or the API
    key that opened it was revoked mid-run.

    **The command's environment.** It runs as root, or as `user`, with a login-like environment: `HOME`,
    `USER`, `LOGNAME` and `SHELL` of that account, the variables in the VM's `/etc/environment`, a
    `LANG`, and a `PATH` of the usual profile directories (mise's shims, `~/.local/bin`,
    `/usr/local/sbin`, `/usr/local/bin`, then the system directories). It starts in the account's home
    directory unless `cwd` says otherwise. No profile file runs unless `login` is `true`, which runs the
    command through the account's login shell. `env` is applied last, so it wins. The command runs at
    default priority (nice 0, default OOM score), not with the guest agent's own. `cwd`, `env`, `user`
    and `login` need a guest agent that speaks protocol 9 or later: on a VM whose agent is older the
    stream ends with an `error` event naming both versions. Cove updates an outdated agent when it
    connects to it, so a retry shortly after usually succeeds. A `cwd` that does not exist or an unknown
    `user` also ends the stream with an `error` event.

    **Stdin.** `stdin` (text) or `stdin_b64` (standard base64, for bytes) is written to the command's
    stdin, which is then closed, so a reader sees end of input: pipe a script into an interpreter
    (`["python3", "-"]`) or data into a command. At most 1 MiB (1048576 bytes, counted after decoding);
    a larger one, both fields at once or malformed base64 is refused with 400 before anything runs.
    Without either, stdin is empty (`/dev/null`). Stdin needs a guest agent that speaks protocol 10 or
    later: on an older one the stream ends with an `error` event naming both versions instead of running
    the command without its input. Interactive (streamed) stdin is not offered; for larger payloads
    write a file first.

    **The buffered, secrets-injected form has moved to `POST /api/vms/{name}/exec-with-secrets`
    (`execVmWithSecrets`).** Until the split, this one route answered with either an SSE stream or a
    JSON body depending on whether the request body carried a `selector` field — the exact shape that
    started this description-generation effort, because OpenAPI cannot say "the response shape depends
    on a request field" and a real generator run against it silently dropped the streaming mode.

    **REMOVED in API version 5: sending `selector` to this operation.** It was accepted for one
    deprecation window and is now refused with 400 `validation_failed` naming the `selector` field. Use
    `execVmWithSecrets` instead.

    The caller needs SSH access to the VM (`vm.ssh`): the owner, a sharee, or an administrator (an
    admin-listed user's session or admin key; their ordinary API key or connected app is not one, and
    gets the same 404 as a VM that does not exist). An exec by anyone other than the VM's owner is
    recorded in the audit log as `vm.exec.opened`; the command line is not recorded.

    Args:
        name (str):
        encoding (str | Unset):
        x_cove_exec_encoding (None | str | Unset):
        body (ExecRequestDto): POST /vms/{name}/exec request body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ScopeDeniedBody | str
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
            encoding=encoding,
            x_cove_exec_encoding=x_cove_exec_encoding,
        )
    ).parsed
