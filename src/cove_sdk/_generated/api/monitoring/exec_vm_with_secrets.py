from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.exec_output_dto import ExecOutputDto
from ...models.exec_with_secrets_request import ExecWithSecretsRequest
from ...models.scope_denied_body import ScopeDeniedBody
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: ExecWithSecretsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/exec-with-secrets".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody | None:
    if response.status_code == 200:
        response_200 = ExecOutputDto.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody]:
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
    body: ExecWithSecretsRequest,
) -> Response[ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody]:
    """Execute a command in the guest with its secrets injected

     Pushes the selected secrets into the guest, runs the command to completion, then (for the
    `setup_tag` selector) wipes them again — win or lose — before returning `{stdout, stderr, exit_code,
    timed_out}` as a single `200 application/json` body. Nothing streams: use `execVm` for that. This is
    the wire form of `cove exec --inject` / `--setup=`. Each of `stdout` and `stderr` keeps at most 6
    MiB of output; longer output is cut short and ends with the line `[cove-agent: output truncated, the
    exec result keeps 6 MiB]`.

    Gated by `[secrets] enabled` on the host and answers 503 `feature_disabled` when secrets injection
    is off, which is the default — a host whose pool snapshots predate the v4 cove-agent protocol cannot
    inject at all.

    `selector` is required, and picks what gets injected:
    - `{"kind": "all"}` — every secret attached to the VM.
    - `{"kind": "subset", "names": [...]}` — a caller-curated allowlist.
    - `{"kind": "setup_tag", "tag": "..."}` — only `setup-only` secrets carrying that tag, wiped from
    host and guest after the command finishes whatever its exit status.

    A field the request does not define is refused with 400 `validation_failed` naming it, rather than
    ignored; `stdin` and `stdin_b64` (which `execVm` takes) are refused with `stdin is not supported
    with secrets`.

    `timeout_secs` (optional, default 30, at most 3600) bounds the command, as on `execVm`; a larger
    value is refused with 400 `validation_failed` and `field: "timeout_secs"`, because other changes to
    the VM's secrets wait until the run finishes. Past it the guest kills the command's whole process
    group with SIGKILL and the body reports `exit_code: 124` and `timed_out: true`, with the output
    written before then; the `setup_tag` wipe still runs. A command that exits 124 on its own has
    `timed_out: false`.

    **This operation is new.** A server that predates the split has never heard of this path and answers
    404, not a graceful degrade — there is no version-specific routing. It has been served since API
    version 4, and a server at API version 5 or later refuses a client older than version 5, so a
    version 5 client can always rely on it.

    The caller needs SSH access to the VM (`vm.ssh`) as well as `vm.secrets`. An exec by anyone other
    than the VM's owner is recorded in the audit log as `vm.exec.opened`.

    Args:
        name (str):
        body (ExecWithSecretsRequest): POST /vms/{name}/exec-with-secrets request body.

            The buffered, secrets-injected form of exec, split out of `/exec` because
            one route cannot answer with both an SSE stream and a JSON body in any
            describable way. `selector` is REQUIRED here — it is what the operation is
            for — where on `ExecRequestDto` it is the optional field that used to switch
            `/exec` between its two response shapes.

            `timeout_secs` bounds the command as it does on `ExecRequestDto`: past it
            the guest kills the command's process group and the response is exit 124
            with `timed_out`. The `setup_tag` wipe still runs afterwards.

            A field this operation does not define is refused with 400
            `validation_failed` naming it, not ignored: a caller that sends an option
            it lacks (a typo, or an exec option added after this one) would otherwise
            get the command run without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecWithSecretsRequest,
) -> ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody | None:
    """Execute a command in the guest with its secrets injected

     Pushes the selected secrets into the guest, runs the command to completion, then (for the
    `setup_tag` selector) wipes them again — win or lose — before returning `{stdout, stderr, exit_code,
    timed_out}` as a single `200 application/json` body. Nothing streams: use `execVm` for that. This is
    the wire form of `cove exec --inject` / `--setup=`. Each of `stdout` and `stderr` keeps at most 6
    MiB of output; longer output is cut short and ends with the line `[cove-agent: output truncated, the
    exec result keeps 6 MiB]`.

    Gated by `[secrets] enabled` on the host and answers 503 `feature_disabled` when secrets injection
    is off, which is the default — a host whose pool snapshots predate the v4 cove-agent protocol cannot
    inject at all.

    `selector` is required, and picks what gets injected:
    - `{"kind": "all"}` — every secret attached to the VM.
    - `{"kind": "subset", "names": [...]}` — a caller-curated allowlist.
    - `{"kind": "setup_tag", "tag": "..."}` — only `setup-only` secrets carrying that tag, wiped from
    host and guest after the command finishes whatever its exit status.

    A field the request does not define is refused with 400 `validation_failed` naming it, rather than
    ignored; `stdin` and `stdin_b64` (which `execVm` takes) are refused with `stdin is not supported
    with secrets`.

    `timeout_secs` (optional, default 30, at most 3600) bounds the command, as on `execVm`; a larger
    value is refused with 400 `validation_failed` and `field: "timeout_secs"`, because other changes to
    the VM's secrets wait until the run finishes. Past it the guest kills the command's whole process
    group with SIGKILL and the body reports `exit_code: 124` and `timed_out: true`, with the output
    written before then; the `setup_tag` wipe still runs. A command that exits 124 on its own has
    `timed_out: false`.

    **This operation is new.** A server that predates the split has never heard of this path and answers
    404, not a graceful degrade — there is no version-specific routing. It has been served since API
    version 4, and a server at API version 5 or later refuses a client older than version 5, so a
    version 5 client can always rely on it.

    The caller needs SSH access to the VM (`vm.ssh`) as well as `vm.secrets`. An exec by anyone other
    than the VM's owner is recorded in the audit log as `vm.exec.opened`.

    Args:
        name (str):
        body (ExecWithSecretsRequest): POST /vms/{name}/exec-with-secrets request body.

            The buffered, secrets-injected form of exec, split out of `/exec` because
            one route cannot answer with both an SSE stream and a JSON body in any
            describable way. `selector` is REQUIRED here — it is what the operation is
            for — where on `ExecRequestDto` it is the optional field that used to switch
            `/exec` between its two response shapes.

            `timeout_secs` bounds the command as it does on `ExecRequestDto`: past it
            the guest kills the command's process group and the response is exit 124
            with `timed_out`. The `setup_tag` wipe still runs afterwards.

            A field this operation does not define is refused with 400
            `validation_failed` naming it, not ignored: a caller that sends an option
            it lacks (a typo, or an exec option added after this one) would otherwise
            get the command run without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecWithSecretsRequest,
) -> Response[ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody]:
    """Execute a command in the guest with its secrets injected

     Pushes the selected secrets into the guest, runs the command to completion, then (for the
    `setup_tag` selector) wipes them again — win or lose — before returning `{stdout, stderr, exit_code,
    timed_out}` as a single `200 application/json` body. Nothing streams: use `execVm` for that. This is
    the wire form of `cove exec --inject` / `--setup=`. Each of `stdout` and `stderr` keeps at most 6
    MiB of output; longer output is cut short and ends with the line `[cove-agent: output truncated, the
    exec result keeps 6 MiB]`.

    Gated by `[secrets] enabled` on the host and answers 503 `feature_disabled` when secrets injection
    is off, which is the default — a host whose pool snapshots predate the v4 cove-agent protocol cannot
    inject at all.

    `selector` is required, and picks what gets injected:
    - `{"kind": "all"}` — every secret attached to the VM.
    - `{"kind": "subset", "names": [...]}` — a caller-curated allowlist.
    - `{"kind": "setup_tag", "tag": "..."}` — only `setup-only` secrets carrying that tag, wiped from
    host and guest after the command finishes whatever its exit status.

    A field the request does not define is refused with 400 `validation_failed` naming it, rather than
    ignored; `stdin` and `stdin_b64` (which `execVm` takes) are refused with `stdin is not supported
    with secrets`.

    `timeout_secs` (optional, default 30, at most 3600) bounds the command, as on `execVm`; a larger
    value is refused with 400 `validation_failed` and `field: "timeout_secs"`, because other changes to
    the VM's secrets wait until the run finishes. Past it the guest kills the command's whole process
    group with SIGKILL and the body reports `exit_code: 124` and `timed_out: true`, with the output
    written before then; the `setup_tag` wipe still runs. A command that exits 124 on its own has
    `timed_out: false`.

    **This operation is new.** A server that predates the split has never heard of this path and answers
    404, not a graceful degrade — there is no version-specific routing. It has been served since API
    version 4, and a server at API version 5 or later refuses a client older than version 5, so a
    version 5 client can always rely on it.

    The caller needs SSH access to the VM (`vm.ssh`) as well as `vm.secrets`. An exec by anyone other
    than the VM's owner is recorded in the audit log as `vm.exec.opened`.

    Args:
        name (str):
        body (ExecWithSecretsRequest): POST /vms/{name}/exec-with-secrets request body.

            The buffered, secrets-injected form of exec, split out of `/exec` because
            one route cannot answer with both an SSE stream and a JSON body in any
            describable way. `selector` is REQUIRED here — it is what the operation is
            for — where on `ExecRequestDto` it is the optional field that used to switch
            `/exec` between its two response shapes.

            `timeout_secs` bounds the command as it does on `ExecRequestDto`: past it
            the guest kills the command's process group and the response is exit 124
            with `timed_out`. The `setup_tag` wipe still runs afterwards.

            A field this operation does not define is refused with 400
            `validation_failed` naming it, not ignored: a caller that sends an option
            it lacks (a typo, or an exec option added after this one) would otherwise
            get the command run without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecWithSecretsRequest,
) -> ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody | None:
    """Execute a command in the guest with its secrets injected

     Pushes the selected secrets into the guest, runs the command to completion, then (for the
    `setup_tag` selector) wipes them again — win or lose — before returning `{stdout, stderr, exit_code,
    timed_out}` as a single `200 application/json` body. Nothing streams: use `execVm` for that. This is
    the wire form of `cove exec --inject` / `--setup=`. Each of `stdout` and `stderr` keeps at most 6
    MiB of output; longer output is cut short and ends with the line `[cove-agent: output truncated, the
    exec result keeps 6 MiB]`.

    Gated by `[secrets] enabled` on the host and answers 503 `feature_disabled` when secrets injection
    is off, which is the default — a host whose pool snapshots predate the v4 cove-agent protocol cannot
    inject at all.

    `selector` is required, and picks what gets injected:
    - `{"kind": "all"}` — every secret attached to the VM.
    - `{"kind": "subset", "names": [...]}` — a caller-curated allowlist.
    - `{"kind": "setup_tag", "tag": "..."}` — only `setup-only` secrets carrying that tag, wiped from
    host and guest after the command finishes whatever its exit status.

    A field the request does not define is refused with 400 `validation_failed` naming it, rather than
    ignored; `stdin` and `stdin_b64` (which `execVm` takes) are refused with `stdin is not supported
    with secrets`.

    `timeout_secs` (optional, default 30, at most 3600) bounds the command, as on `execVm`; a larger
    value is refused with 400 `validation_failed` and `field: "timeout_secs"`, because other changes to
    the VM's secrets wait until the run finishes. Past it the guest kills the command's whole process
    group with SIGKILL and the body reports `exit_code: 124` and `timed_out: true`, with the output
    written before then; the `setup_tag` wipe still runs. A command that exits 124 on its own has
    `timed_out: false`.

    **This operation is new.** A server that predates the split has never heard of this path and answers
    404, not a graceful degrade — there is no version-specific routing. It has been served since API
    version 4, and a server at API version 5 or later refuses a client older than version 5, so a
    version 5 client can always rely on it.

    The caller needs SSH access to the VM (`vm.ssh`) as well as `vm.secrets`. An exec by anyone other
    than the VM's owner is recorded in the audit log as `vm.exec.opened`.

    Args:
        name (str):
        body (ExecWithSecretsRequest): POST /vms/{name}/exec-with-secrets request body.

            The buffered, secrets-injected form of exec, split out of `/exec` because
            one route cannot answer with both an SSE stream and a JSON body in any
            describable way. `selector` is REQUIRED here — it is what the operation is
            for — where on `ExecRequestDto` it is the optional field that used to switch
            `/exec` between its two response shapes.

            `timeout_secs` bounds the command as it does on `ExecRequestDto`: past it
            the guest kills the command's process group and the response is exit 124
            with `timed_out`. The `setup_tag` wipe still runs afterwards.

            A field this operation does not define is refused with 400
            `validation_failed` naming it, not ignored: a caller that sends an option
            it lacks (a typo, or an exec option added after this one) would otherwise
            get the command run without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | ExecOutputDto | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
