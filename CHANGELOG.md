# Changelog

All notable changes to `runcove-sdk` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versions 0.1.0 to 0.1.2 were released inside the Cove server releases `cove-server-v0.34.0`
to `cove-server-v0.34.2`. Later versions are released on their own, under `sdk-py-v<version>`
tags, and Cove server releases no longer carry the SDK.

## [Unreleased]

### Added

- **`client.keys.revoke_by_token(token)` revokes an API key by presenting it** (`POST /api/api-keys/revoke`): any key you hold, yours or one you found, no scope needed. Returns alike whether or not the key was live.

- **A clone request can set the clone's idle-pause policy, expiry policy and tags.** `CloneRequest` gains optional `auto_pause_policy`, `ttl_policy` and `tags`; a clone that leaves them out keeps its source's (its expiry clock starts when the clone is created). The clone endpoint's documented errors now include a bad tag (400), more than 50 tags (409, `too_many_tags`) and an out-of-bounds policy (422).
- **`vms.exec` takes `cwd`, `env`, `user` and `login`.** They set the working directory (relative to the account's home), add environment variables that win over the defaults, run the command as another account in the VM, or run it through that account's login shell. Arguments left as `None` are left out of the request, so a plain exec is unchanged. A VM whose guest agent is older refuses an exec that sets any of them.

### Changed

- **`vms.list` and `vms.iter` take `tag` as one `key=value` string or a sequence of them, and send each as its own `tag` parameter; only VMs carrying every one are listed.** The generated `list_vms` now types `tag` as `list[str]`, as the contract declares it.
- **The set-expiry request (`UpdateTtlPolicyRequest`) takes `expires_in`, an expiry counted from now that keeps the VM's `on_stop`, as an alternative to `policy`, which is now optional.** Send exactly one; the server answers 422 otherwise. A new `ExpiresIn` model carries `secs` (3600 to 315360000, or null to remove the expiry). The operation now documents its 422, and the `TtlPolicy` and create and clone texts give the ten-year ceiling.
- **`admin.revoke_user_sessions` can fail with 503 `unavailable`** when the bastion kept one of the person's CLI sessions; those sessions stay valid and calling again retries only them. It used to answer success with them still valid. `keys.revoke`'s docs say an administrator can revoke anyone's key.
- **`ErrorCode` gains `DISK_ROLLBACK_NOT_NAMED` (`disk_rollback_not_named`)**: `vms.wake` with no `checkpoint_id`, on a stopped VM whose latest checkpoint is disk-only, is refused with this 409 and changes nothing, where the server used to roll the disk back. `vms.wake`'s docstring, the wake operation's and `WakeRequest.checkpoint_id`'s say so.
- **Every operation the API-key listener serves declares its `429` response.** The generated calls parse a 429 body as `ApiError` (code `rate_limited`, with a `Retry-After` header in seconds). The client still raises `RateLimitError` as before.

### Docs

- **`VmDetail` documents each size field: the size the VM has now, the size it boots with, and the bounds a resize can move it between.**

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
