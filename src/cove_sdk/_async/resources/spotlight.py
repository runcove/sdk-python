"""``client.spotlight``: mirror a local git worktree onto a VM directory, switch it, and restore
the base tree, over the file and exec API.

The packing, the guest apply script and the checks live in ``cove_sdk._spotlight`` (colour-neutral,
blocking); this module sequences the calls and runs the blocking part in a worker thread on the
async client.
"""

from __future__ import annotations

import builtins
import os
from collections.abc import Sequence

from ..._colour import async_run_blocking
from ..._spotlight import (
    TAG_BASE,
    TAG_DEST,
    TAG_SOURCE,
    PackedTree,
    SpotlightOffResult,
    SpotlightOnResult,
    SpotlightStatus,
    apply_command,
    check_base,
    check_dest,
    check_protect,
    nonce,
    pack_commit,
    pack_worktree,
    parse_summary,
)
from ...errors import CoveError
from .._transport import CLIENT_DEFAULT, CallTimeout, _Default
from .tags import Tags
from .vms import Vms

DEFAULT_TIMEOUT_SECS = 300


class Spotlight:
    """``client.spotlight`` — put a local git worktree onto a long-lived VM at a path, switch it
    to another worktree, and restore the base tree with ``off``. Nothing on the VM is restarted.

    The transport is the HTTP API only: ``vms.files.upload`` of a gzip tar, then one ``exec`` of a
    fixed POSIX sh script that mirrors it onto ``dest`` with delete semantics (rsync when the image
    has it, else ``find``/``cp``). No SSH, and no rsync on your machine; ``git`` must be on PATH.

    The binding lives in the VM's tags (``spotlight.base``, ``spotlight.dest``,
    ``spotlight.source``), so any client can read it and ``off`` works from another process. The
    CLI's ``cove spotlight`` reads and writes the same tags, so each sees the other's binding.

    Scopes: ``tags:read`` and ``tags:write`` (the binding), ``files:write`` (the upload),
    ``vms:exec`` (the apply). Each switch sends the whole tree; one larger than the host's file limit raises
    ``FileTooLargeError`` (413 ``file_too_large``) before anything changes on the VM.
    """

    def __init__(self, vms: Vms, tags: Tags) -> None:
        self._vms = vms
        self._tags = tags

    async def on(
        self,
        name: str,
        *,
        tree: str | os.PathLike[str],
        dest: str,
        protect: Sequence[str] | None = None,
        timeout_secs: int | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> SpotlightOnResult:
        """Mirror ``tree``'s worktree onto ``dest`` in VM ``name``.

        Every path of ``dest`` the tree lacks is deleted, except what the ``protect`` entries match
        and everything below it (rsync protect patterns: a bare name matches at any depth, a
        trailing ``/`` matches a directory only, a leading ``/`` anchors at ``dest``; default
        :data:`~cove_sdk.SPOTLIGHT_DEFAULT_PROTECT`, the CLI's set). A file the tree holds under a
        protected path is still written, as with the CLI.
        The tree is the checkout's tracked files plus its untracked files git does not ignore.

        The first bind records the tree's HEAD as the base ``off`` restores; a later ``on`` (a
        switch to another worktree) keeps it. The tags are written only after the tree is in
        place, so a failed switch leaves the binding as it was. ``timeout_secs`` is the server's
        deadline on the apply command (default 300).
        """
        dest = check_dest(dest)
        protect_list = check_protect(protect)
        # The base tag comes back from the VM: a bound one is checked before any git call.
        bound = await self._binding(name, timeout)
        # An empty tag counts as no base, as in the TypeScript SDK.
        bound_base = bound.get(TAG_BASE) or None
        if bound_base is not None:
            check_base(bound_base)
        packed = await async_run_blocking(pack_worktree, tree)
        base = bound_base or packed.head
        files, size = await self._apply(
            name, dest, packed, protect_list, timeout_secs, timeout
        )
        if bound_base is None:
            await self._tags.set(name, TAG_BASE, base, timeout=timeout)
        await self._tags.set(name, TAG_DEST, dest, timeout=timeout)
        await self._tags.set(name, TAG_SOURCE, packed.source, timeout=timeout)
        return SpotlightOnResult(vm=name, dest=dest, base=base, files=files, bytes=size)

    async def off(
        self,
        name: str,
        *,
        tree: str | os.PathLike[str],
        protect: Sequence[str] | None = None,
        timeout_secs: int | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> SpotlightOffResult | None:
        """Restore the base commit onto the bound ``dest``, then delete the three tags.

        ``tree`` is a checkout of the same repository that holds the base commit; its tree is
        taken with ``git archive`` and applied as ``on`` applies a worktree. With no binding on
        the VM it does nothing and returns ``None``, as ``cove dev spotlight off`` does. A base
        commit missing from that repository raises ``CoveError`` ("run `git fetch`") before
        anything changes.
        """
        protect_list = check_protect(protect)
        bound = await self._binding(name, timeout)
        base = bound.get(TAG_BASE)
        dest = bound.get(TAG_DEST)
        if not base or not dest:
            return None
        # Both tags come back from the VM: check them before any git call or upload.
        check_base(base)
        check_dest(dest)
        packed = await async_run_blocking(pack_commit, tree, base)
        await self._apply(
            name, check_dest(dest), packed, protect_list, timeout_secs, timeout
        )
        # Base first, dest last: a failure part-way leaves no base, so ``off`` returns None, while
        # ``status`` still shows the dest and the next ``on`` records a fresh base.
        for key in (TAG_BASE, TAG_SOURCE, TAG_DEST):
            await self._tags.delete(name, key, timeout=timeout)
        return SpotlightOffResult(vm=name, dest=dest, restored=base)

    async def status(
        self, name: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> SpotlightStatus | None:
        """VM ``name``'s binding, from its tags, or ``None`` when nothing is bound. Scope
        ``tags:read``."""
        bound = await self._binding(name, timeout)
        dest = bound.get(TAG_DEST)
        if not dest:
            return None
        return SpotlightStatus(
            dest=dest, base=bound.get(TAG_BASE, ""), source=bound.get(TAG_SOURCE, "")
        )

    async def _binding(self, name: str, timeout: CallTimeout) -> dict[str, str]:
        tags = await self._tags.list_for_vm(name, timeout=timeout)
        return {t.key: t.value for t in tags if t.key.startswith("spotlight.")}

    async def _apply(
        self,
        name: str,
        dest: str,
        packed: PackedTree,
        protect: builtins.list[str],
        timeout_secs: int | None,
        timeout: CallTimeout,
    ) -> tuple[int, int]:
        """Upload the tarball and run the apply script; its ``(files, bytes)``, or ``CoveError``."""
        tag = nonce()
        tgz = f"/tmp/cove-spotlight-{tag}.tgz"
        stage = f"{dest}.cove-stage-{tag}"
        await self._vms.files.upload(name, tgz, packed.tgz, timeout=timeout)
        deadline = DEFAULT_TIMEOUT_SECS if timeout_secs is None else timeout_secs
        run = await self._vms.exec_collect(
            name,
            command=apply_command(tgz, stage, dest, protect),
            timeout_secs=deadline,
            # exec's timeout= is the idle bound between chunks; the client default is none.
            timeout=None if isinstance(timeout, _Default) else timeout,
        )
        if run.timed_out:
            raise CoveError(
                f"spotlight: applying the tree to {name}:{dest} hit its {deadline} s deadline and"
                f" was killed, so {dest} may be half-mirrored; run on again (with a larger"
                " timeout_secs if the tree is big)"
            )
        if run.exit_code != 0:
            raise CoveError(
                f"spotlight: applying the tree to {name}:{dest} failed"
                f" (exit {run.exit_code}): {run.stderr.strip()}"
            )
        return parse_summary(run.stdout)
