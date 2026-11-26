# Changelog

All notable changes to `runcove-sdk` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versions 0.1.0 to 0.1.2 were released inside the Cove server releases `cove-server-v0.34.0`
to `cove-server-v0.34.2`. Later versions are released on their own, under `sdk-py-v<version>`
tags, and Cove server releases no longer carry the SDK.

## [Unreleased]

## [0.2.0] - 2026-11-24

### Fixed

- **`vms.clone` types a taken `new_vm_name` as `VmNameTakenBody`, the body `vms.create` answers, and `cove_sdk.types` exports `VmCloneConflictResponse`, the clone's 409 union.** The server now answers a taken clone name with `vm_name_taken` (it was `invalid_state_transition`), with `retry_after_secs` while the name is in its post-delete cooldown.
- `RotateSummary` carries `existed`, set by a secret delete: `False` when nothing was stored under that name in that scope (the wipe is still sent).
- **`vms.exec` and `vms.exec_collect` return output with carriage returns byte for byte.** The SDK asks for each chunk as a JSON string (`?encoding=json`) and decodes it when the response carries `x-cove-exec-encoding: json`; a carriage return used to come back as a newline. Against an older server, which ignores the parameter, the chunks are read raw, as before.
- `vms.wake`, `wake_vm` and the `checkpoints` module docs say waking a stopped VM with a disk-only checkpoint's id is the in-place disk rollback (they said there is none), and `CreateVmRequest.ports` names the key `[service.proxy].allowed_ports`.
- **The SDK toolchain venv builds on a host whose default `python3` is 3.15.** `scripts/sdk-python-env.sh` now builds it with `COVE_SDK_PYTHON` if set (used or refused with a clear error, never replaced), else `python3.14`, else `python3`, and treats a venv whose Python is a different major.minor from that choice as stale. Before, the locked `markupsafe` has no 3.15 wheel, so `scripts/sync-sdk-python.sh` failed there.

### Added

- **`client.admin.enable_user(username)` lets a person an offboarding shut out back in** (`POST /api/admin/users/{username}/enable`). Until then every request of theirs is refused with 403 `user_disabled` (the new `ErrorCode.USER_DISABLED`), and nothing that would hand them a credential is created. It returns the cleared shut-out (`EnableUserResponse`: `disabled_at`, `disabled_by`, `reason`) and, like `offboard_user`, refuses every API key with 401 `sudo_required`. `AdminUserSummary` gains `disabled_at` and `OffboardUserReport` gains `disabled`.

- **`client.keys.revoke_by_token(token)` revokes an API key by presenting it** (`POST /api/api-keys/revoke`): any key you hold, yours or one you found, no scope needed. Returns alike whether or not the key was live.

- **A clone request can set the clone's idle-pause policy, expiry policy and tags.** `CloneRequest` gains optional `auto_pause_policy`, `ttl_policy` and `tags`; a clone that leaves them out keeps its source's (its expiry clock starts when the clone is created). The clone endpoint's documented errors now include a bad tag (400), more than 50 tags (409, `too_many_tags`) and an out-of-bounds policy (422).
- **`vms.exec` takes `cwd`, `env`, `user` and `login`.** They set the working directory (relative to the account's home), add environment variables that win over the defaults, run the command as another account in the VM, or run it through that account's login shell. Arguments left as `None` are left out of the request, so a plain exec is unchanged. A VM whose guest agent is older refuses an exec that sets any of them.
- **`OffboardUserReport` gains `tickets_left_on_other_instances`**: how many Warpgate
  tickets in the person's name offboarding left on targets another Cove instance
  owns. A count, not a failed item.
- **`ErrorCode.SECRETS_RESTORING` is added.** It is the code of a `409` that says a rebooted VM's secrets are still being put back and the command was not run; run it again.
- **API version 8 (`API_VERSION`). `vms.exec` and `vms.exec_collect` refuse `stdin` against an older server.** With `stdin` set, opening the stream first reads the server's version (`GET /api/whoami`). Below `EXEC_STDIN_MIN_API_VERSION` (8, now exported), or when the server does not report a version, it raises `CoveError` ("this server (API 7) does not support exec stdin; upgrade the server to API 8 or later") and sends nothing, because an older server would run the command without its input. An exec without stdin is unchanged.
- **`VmDetail` gains an optional `permissions` list of strings** (`vm.view`, `vm.power`, `vm.snapshot`, ...), what the caller may do to the VM. It is plain strings, not an enum: a name a newer server adds reads like any other, so skip names you do not know. Absent from older servers.
- **`TrafficMonitorState` gains `WAKE_STOPPED`:** the server's traffic monitor attached, then its wake path stopped, so no paused VM can wake on traffic until the daemon restarts.
- **`ErrorCode.CHECKPOINT_NOT_FOUND` is added.** Reading or deleting a checkpoint that does not exist answers it, naming the checkpoint.
- **`Checkpoint` gains optional `orphaned_at` and `reclaim_at`:** when the checkpoint's VM was deleted, and when the server will delete the checkpoint on its own.
- **`HealthResponse` gains `wake_jump`**: `true` while the server's wake jump is on, so a plain `ssh` to a hibernated VM waits while it wakes; absent otherwise and from older servers.
- **`vms.rename(name, new_name=...)` renames a VM**, on both `CoveClient` and `AsyncCoveClient`. It posts to `POST /api/vms/{name}/rename` and returns the VM's detail under its new name; the VM keeps its id, disk and state. A taken `new_name` raises `ConflictError` with `code == "vm_name_taken"` and `retry_after_secs` set while the name is in its cooldown, a busy VM raises `ConflictError` with `code == "invalid_state_transition"`, and a VM that is missing or that the caller may not delete raises `NotFoundError`.
- **`ProxyUrlInfo` (the answer of `GET /api/vms/{name}/url`) has `web_url`, the address Cove's web app is served on; the VM's page there is `<web_url>/vms/<vm_name>`.** It is unset when the server has no web address configured.
- **`clone_vm` can answer 500 and parses it as `ApiError`.** When the new VM's guest agent answers its setup after the restore with a failure on every attempt, the message is `the clone could not finish its setup in the guest: ` followed by the agent's answer, escaped and cut to about 512 characters, with code `internal_error`. Do not retry it: the same source gives a guest that fails the same way. A guest agent that gives no answer in time is still 503.
- **VM summaries and details carry an optional `activity` field,** set to `"starting"` while a stopped VM's cold start is waiting for its guest agent. `state` is unchanged.
- **`VmDetail` has an optional `network_policy_needs_restart` field.** It is `True` for a running or paused Mac VM whose stored network policy needs a restart of the VM to take effect (restart it, then set the policy again), and unset otherwise.
- **The generated `update_image`** (`cove_sdk._generated.api.host.update_image`, `POST /api/images/update`) starts or joins a Mac's box update in local mode, and `LocalStatus.image_update` (`ImageUpdate`, `ImageUpdateState`, `TransferProgress`) reports it.
- **`create_failed_vm_kept` joins the error codes** (500: a create failed after its VM existed, and the VM was kept under a new name; the message names it).
- **Team admin fields** (API version 9): `ProfileSummary` gains `team_admin_of`, the teams whose keys the caller can manage as the team's admin; `TeamMemberEntry` gains `role` (`"admin"` or `"member"`); `RemoveMemberOutcome` gains `team_keys_minted`, the ids of the team keys the removed person minted, which keep working. An older server sends none of them. The answer to ending the team admin role, `TeamAdminRevokeResponse`, carries `team_keys_minted` too.
- **`CreateVmResponse` has an optional `warnings` list.** On a Mac it carries the warning that the Mac is short of free memory for the new VM; it is absent when there are none.
- **Secret listings expose each entry's `exposure`, `lifetime`, `target_unit`, `setup_tag` and `ttl_seconds`.** `SecretEntryDto` gains them as optional fields; values are never returned.
- **The error code `destructive_not_granted`.** The server answers it (403) when a credential granted everything except destructive operations asks for one, such as deleting a VM; no scope would help, only the person who approved the credential.
- **`ErrorCode.CLIENT_ADDRESS_DENIED` joins the error codes, and the host state returns `request_refusals`** (a list of `RequestRefusalEntry`: the external listener's refusals per route group and reason; unset on older daemons).
- **`admin.restore_vms` starts the VMs a host drain stopped.** It takes the VM ids (and optionally how many to start at once) and returns a result per VM from `POST /api/admin/restore-vms`. The route is for the host's Unix socket; every API key is refused with 401 `sudo_required`. `admin.drain_host`'s answer now carries `attempted_vms` and `hibernated`.
- **`ExecExit` has an optional `exact` field.** It is `False` on a base64 exec whose guest agent predates protocol 17, so the output is lossy text rather than the command's exact bytes, and is unset when the bytes are exact.
- **`ResizeResult` has an optional `warnings` list.** On a Mac it carries the warning that a memory grow leaves the Mac short of free memory; it is absent when there are none.
- **`vms.resize(..., restart=True)` and `ResizeResult.restart`.** The generated models carry the
  field, and `ResizeRestart` is new.
- **`vms.exec` and `vms.exec_collect` take `stdin`.** A `str` is sent as text (`stdin`), `bytes` as base64 (`stdin_b64`), written to the command's stdin, which is then closed. At most 1 MiB. A VM whose guest agent is older refuses it rather than run the command without it.
- **`LocalStatus.guest_ram_wired_mb`**: the whole Mac's wired memory now, in MB, which the guest RAM cap counts against; absent off a Mac.
- **`vms.resize(..., force=True)`.** The generated `ResizeRequest` carries `force`, which shrinks memory even below what the guest is using.
- **`vms.recover(name)` returns a `failed` VM to `stopped`** (`POST /api/vms/{name}/recover`, scope `vms:write`), on both `CoveClient` and `AsyncCoveClient`, so `vms.start(name)` can boot it again from its disk. A 409 says the VM is not failed, its hypervisor process may still be running, or its disk is missing.
- **`LocalStatus.low_disk_free_bytes`**: a Mac's free disk, present only while below 10 GiB.
- **The generated client carries the rename route.** `RenameVmRequest` and the `rename_vm` call (`POST /api/vms/{name}/rename`) are generated from the contract.
- **`RamCapacity.committed_mb`**: the memory a cove instance has committed to the VMs that hold guest RAM plus the reservations no such VM accounts for, to compare with `headroom_mb`. Optional: absent from a server that predates it. It covers one instance only: two instances on one host each budget the whole host. `reservation_mb` is documented as the in-flight reservations only.
- **`HealthResponse` gains `oci_refused`**: set, with the reason, while the server refuses every OCI image reference because it could not build its registry client; absent otherwise and from older servers.
- **`OffboardUserReport` gains `warpgate_admin_roles_error`**: set when offboarding
  kept the person's Warpgate user and they hold a Warpgate admin role (naming it), or
  their admin roles could not be listed. A failed item: a Warpgate admin must remove
  the admin role.
- **`AdminQuotaDefaultsResponse.derived_from_mac` and `LocalStatus.guest_ram_cap_mb`, both optional.** `derived_from_mac` is `True` when a Mac's host quota defaults are its own figures, `False` when they are not (a `[quota]` block overrides them, or the figures could not be read), and absent off a Mac or from an older server. `guest_ram_cap_mb` is the cap on the guest RAM a Mac's running VMs may hold, absent when the Mac's RAM could not be read. Both are `UNSET` when the server omits them.
- **`AdminHostStateResponse` carries an optional `agent_hot_patch`.** It says whether the daemon can hot-patch guests with its embedded agent; it is unset from a daemon that predates the field.
- **`origin_not_trusted` joins the error codes** (403: a browser request from an origin not in the server's `[api] trusted_origins`, when that server enforces the list).
- **`OffboardUserReport` gains the optional `left_behind`** (`OffboardLeftBehind`, `OffboardMintedKey`, `OffboardPortInvite`, `OffboardServiceVm`, `OffboardServiceWebhook`): what offboarding leaves in place for an administrator to handle.

### Changed

- **`vms.add_port` returns the port (`ProxyPortInfo`), whether it was new (201) or already published (200: idempotent), and `vms.remove_port` / `tags.delete` return `RemovalResponse` (`existed`).** Each returns `None` from a server older than API version 7. `API_VERSION` is 7.
- **`vms.list` and `vms.iter` take `tag` as one `key=value` string or a sequence of them, and send each as its own `tag` parameter; only VMs carrying every one are listed.** The generated `list_vms` now types `tag` as `list[str]`, as the contract declares it.
- **The set-expiry request (`UpdateTtlPolicyRequest`) takes `expires_in`, an expiry counted from now that keeps the VM's `on_stop`, as an alternative to `policy`, which is now optional.** Send exactly one; the server answers 422 otherwise. A new `ExpiresIn` model carries `secs` (3600 to 315360000, or null to remove the expiry). The operation now documents its 422, and the `TtlPolicy` and create and clone texts give the ten-year ceiling.
- **`admin.revoke_user_sessions` can fail with 503 `unavailable`** when the bastion kept one of the person's CLI sessions; those sessions stay valid and calling again retries only them. It used to answer success with them still valid. `keys.revoke`'s docs say an administrator can revoke anyone's key.
- **`ErrorCode` gains `DISK_ROLLBACK_NOT_NAMED` (`disk_rollback_not_named`)**: `vms.wake` with no `checkpoint_id`, on a stopped VM whose latest checkpoint is disk-only, is refused with this 409 and changes nothing, where the server used to roll the disk back. `vms.wake`'s docstring, the wake operation's and `WakeRequest.checkpoint_id`'s say so.
- **Every operation the API-key listener serves declares its `429` response.** The generated calls parse a 429 body as `ApiError` (code `rate_limited`, with a `Retry-After` header in seconds). The client still raises `RateLimitError` as before.
- **`ExecWithSecretsRequest` no longer carries `additional_properties`.** The server now
  refuses a field `exec-with-secrets` does not define (400 `validation_failed`, naming
  it), so the regenerated model drops the catch-all dict; pass only `command`,
  `selector` and `timeout_secs`.
- **A 409 from `create_vm` can also parse as `ApiError`, with `too_many_tags`, when `initial_tags` has too many entries.** The `initial_tags` and clone `tags` descriptions also give the server's rules, including that a non-empty set needs the `tags:write` permission (403 `scope_denied` without it).
- **The generated client knows the profile routes' 409.** `GET /api/me/keys`, `POST /api/me/keys`, `PATCH`/`DELETE /api/me/keys/{id}` and `DELETE /api/me/sessions/{id}` declare a 409 with a plain-text reason when the server has no bastion (local mode without Warpgate, or its embedded Warpgate turned off or not answering), so their generated functions list it as a response. `GET /api/me`'s description says it answers 200 there, with no gateway half and the quotas.
- **`vms.share` to a user who has never signed in to the server raises `CoveAPIError` with status 422 and code `user_never_signed_in`**, which `ErrorCode` now includes. `user_known` is now `False` only when a known user has no access-gateway account right now.
- **`rename_vm`'s 401 can be the sudo challenge.** Renaming a VM needs a recent sign-in, as deleting one does, so the generated call parses a 401 as `ApiError` or `SudoRequiredBody`, as `delete_vm` does.
- **`wake_vm`'s 409 can be a `DenyReason`.** The generated client now parses the admission denial a wake gets when the host has no room for the VM's memory, beside the existing `ApiError`.
- **`stream_vm_events`' description documents a progress event's optional `transfer`** (`done`, `total`, `bytes_per_sec`, `secs_left`), which a Mac's first-run image download and unpack send about once a second.
- **The 401 of the user-, team- and project-scoped secret set, import and rotate operations now parses as `ApiError | SudoRequiredBody`**: those writes now need a fresh login on the daemon socket and the bastion-fronted listener. API-key callers never receive the `sudo_required` body.
- **`vms.get` and `vms.wait_for_state` raise a create's own failure, not `NotFoundError`, after it fails.** For 5 minutes after your create of a name was accepted and then failed, `GET /api/vms/{name}` answers the failure's own status in place of the 404, marked `x-cove-create-failed: 1`: a refusal by admission or a quota raises `ConflictError` (409), a host with no room or a create that failed raises `ServerError` (503 or 500), and a name refused after the 202 raises `CoveAPIError` (400 `invalid_vm_name`). Code that caught `NotFoundError` to detect a failed create must catch these too; after the 5 minutes, or once a new create of the name is accepted, the name answers 404 again.
- **`stream_vm_events`' description documents `transfer.stalled_secs`**: how long a download has had no data, once that is several seconds.

### Docs

- **`VmDetail` documents each size field: the size the VM has now, the size it boots with, and the bounds a resize can move it between.**
- **`delete_vm` documents the admin 204.** `DELETE /api/vms/pool-…` by an administrator drains an unclaimed warm-pool standby and answers 204, next to the 204 for a purged failed row; anyone else still gets not found.
- **`connect_vm` and `connect_management` say a connect ticket expires 12 hours after the mint and that its expiry also ends the session it opened**, following the server's contract.
- **`client.spotlight` docs no longer say the CLI keeps a separate binding:** `cove spotlight` now reads and writes the same `spotlight.*` VM tags, so a binding made by the CLI or the SDK is seen by the other.
- **The README names the server's browser address `<cove-web-host>`, the placeholder the documentation portal on a Cove server fills in.** The SDK download URLs and the Warpgate-fronted listener use it; the `ssh -L` example names the machine `<server-host>`.
- **`exec_vm` documents when a command's output may be cut short**: a background process that still holds the output open two seconds after the command exits ends the output with a line saying so; redirect such a process's output to avoid the wait.
- **`vms.resize` and the `ResizeResult` model document what `partial` means**, following the server's contract: a memory shrink the guest could not give back, or, with `restart`, a grow after the restart's start that failed (`restart` is `"restarted"`); resize again without `restart` to retry the grow. The generated `resize_vm` docs also say this, that on a Mac a reboot is refused while no network owner serves, and to read the VM before sending a resize with `restart` again after a timeout or a proxy's 502 to 504.
- **`HostTelemetryPoint` and `RamCapacity` document their fields**, following the server's contract: where each memory figure comes from on Linux and on a Mac, what the VM-count and reservation fields count, and that `RamCapacity.mem_available_mb` (like the swap and PSI fields) reads 0 on a Mac.
- The VM name rule in the README and the create and clone request models now say a new VM's name may not be exactly `warpgate`, Warpgate's admin host, which the server refuses as `invalid_vm_name`.
- **`connect_vm` says a hibernated VM is woken before the ticket is minted**, with the permission the connect needs, that the wake can take from seconds to a few minutes, and that a failed wake answers 409 naming `cove wake`, following the server's contract.
- The VM name rule in the README, the `create_vm` / `clone_vm` docstrings and the `CreateVmRequest`, `CloneRequest` and `InvalidVmNameBody` models now say a new VM's name may not start with `pool-`, which the server reserves for VMs Cove keeps ready in advance and refuses as `invalid_vm_name`.
- **`connect_vm` and `connect_management` say an unspent connect ticket is deleted 5 minutes after the mint**, and that revoking access deletes the person's tickets and closes their sessions, following the server's contract.
- **`clone_vm` and `create_checkpoint` say that checkpointing a running VM kills a command still running in it through exec where its guest agent is socket-activated**, that a clone never has such a command, and that background processes carry on, following the server's contract.
- **The README says where `cove login` now keeps its ticket**: in the current context, `contexts/<name>/ticket` under the CLI's config directory, `<name>` being the line in `current-context` there.
- **`vms.resize` says retrying a failed grow with a resize without `restart` is off a Mac.** A Mac
  starts the VM at its new vCPU count and memory, so nothing grows after the start there.
- The `CheckpointState` docstrings on `Checkpoint` and `AdminCheckpointSummary` now say the administrator's checkpoint listing returns checkpoints in every state, and `AdminHostStateResponse.orphaned_checkpoint_count` counts orphaned checkpoints in any state.
- **`bulk_delete_vms` says a client disconnect does not cancel a bulk delete**: it runs to completion and is audited, a caller that stopped waiting finds the outcome in the audit log, and sending the request again starts a second batch, following the server's contract.
- **`connect_vm`, `wake_vm`, `start_vm` and `resume_vm` say a VM whose owner was offboarded is brought back only by an administrator**, and that anyone else gets 403 `user_disabled` with no `detail`, following the server's contract.
- **`AdminBulkVmTarget.result` and `bulk_delete_vms` document `already_being_deleted`**: a bulk delete leaves alone a VM another delete already owns, lists it with that result and does not count it in `attempted`, following the server's contract.

## [0.1.2] - 2026-10-06

### Fixed

- **The sdist carries only the package and its build inputs.** `pyproject.toml` now lists what the sdist holds (the sources, tests, examples, scripts, README, LICENSE, `pyproject.toml` and the generator and lock files), so a file added later never ships by default. The sdist of 0.1.1 also held repository agent files, and was not published to PyPI for that reason. The wheel is unchanged: it ships only `cove_sdk`.

## [0.1.1] - 2026-10-06

### Added

- **From this version on `runcove-sdk` is published on PyPI: `pip install runcove-sdk`.** 0.1.1 itself did not reach PyPI, as its sdist was refused (see 0.1.2). Each version on PyPI is the wheel and sdist of the signed Cove release, uploaded unchanged after their checksums and signature are verified, and PyPI records attestations for them.

### Changed

- **The package declares its README, so its PyPI page shows it.** The page of 0.1.0 is empty, and PyPI does not accept that version again.

### Docs

- **The README leads with `pip install runcove-sdk`.** Installing from your Cove server's `/public/sdk/` stays documented as the second path, for the SDK that exact server shipped with. While the SDK is 0.x, pin an exact version.
- **The API descriptions and the SDK's own sources no longer cite internal planning notes.** Each now gives the reason in words, or links the published external API page. Nothing about the API's behaviour or shape changes.

## [0.1.0] - 2026-10-05

### Added

- **First release**, inside the `cove-server-v0.34.0` release assets as `cove-sdk-python.whl` and `cove-sdk-python.tar.gz`.
