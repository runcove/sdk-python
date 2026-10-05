#!/usr/bin/env python3
"""Trying several fixes from one prepared VM: set up a VM once (check out the code, build it),
checkpoint it, and clone one VM per candidate fix from that checkpoint, so every try starts from
the same prepared state without repeating the setup. Each clone applies its fix and runs the
tests; the first fix that passes is kept and the other clones deleted. The candidates here are
three fixed versions of one function; an agent would write them. Uses the async client.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... \\
      TRIES_REPO_URL=https://example.com/your/repo.git python examples/parallel_tries.py
    python examples/parallel_tries.py --mock     # offline, against an in-process fake server

Needs git, make and python3 in the VM's image. Each clone counts against your quota.
"""

from __future__ import annotations

import asyncio
import os
import sys

from cove_sdk import AsyncCoveClient, CoveAPIError
from cove_sdk.types import CloneResponse

SRC = "/root/src"
# The candidate fixes for slugify.py, which the tests in the repository check.
FIXES = [
    'def slugify(title):\n    return "-".join(title.split(" "))\n',
    'def slugify(title):\n    return "-".join(title.lower().split())\n',
    'def slugify(title):\n    return "-".join(w.lower() for w in title.split())\n',
]


async def main() -> int:
    mock = "--mock" in sys.argv
    repo_url = "https://example.com/demo.git" if mock else env("TRIES_REPO_URL")
    interval = 0.01 if mock else 1.0
    async with make_client(mock) as client:
        base = (await client.vms.create()).name
        print(f"created {base}")
        tries: list[str] = []
        failed = False
        try:
            await client.vms.wait_for_state(base, "running", timeout=300, interval=interval)
            await run(client, base, ["git", "clone", "--depth", "1", repo_url, SRC])
            await run(client, base, ["make", "-C", SRC, "build"])
            print(f"{base} is prepared")

            # A full checkpoint (memory too): a disk-only one cannot be cloned.
            prepared = await client.checkpoints.create(base, description="prepared")
            print("checkpoint taken: prepared")

            # One clone per fix, requested together. The host makes the clones of one VM one at
            # a time, and one can take about 45 s, so each call gets 300 s rather than the
            # client's 30 s; each clone is a copy, not a fresh setup.
            names = [f"{base}-try-{i}" for i in range(1, len(FIXES) + 1)]
            cloned = await asyncio.gather(
                *(
                    client.vms.clone(
                        base, new_vm_name=n, source_checkpoint_id=prepared.id, timeout=300
                    )
                    for n in names
                ),
                return_exceptions=True,
            )
            tries += [c.new_vm.name for c in cloned if isinstance(c, CloneResponse)]
            for c in cloned:
                if isinstance(c, BaseException):
                    raise c
            print(f"cloned {len(tries)} VMs from the checkpoint")

            # Every clone tries its fix at the same time; results come back in fix order.
            async def try_fix(vm: str, fix: str) -> int:
                await client.vms.files.upload(vm, f"{SRC}/slugify.py", fix)
                test = await client.vms.exec_collect(
                    vm, command=["python3", "-m", "unittest", "discover", "-s", SRC], timeout_secs=600
                )
                return test.exit_code

            exits = await asyncio.gather(*(try_fix(vm, fix) for vm, fix in zip(tries, FIXES)))
            for i, code in enumerate(exits):
                result = "passed" if code == 0 else f"failed (exit {code})"
                print(f"fix {i + 1} on {tries[i]}: tests {result}")
            if 0 not in exits:
                print("no fix passed")
                failed = True
            else:
                winner = exits.index(0)
                print(f"keeping fix {winner + 1}, on {tries[winner]}")
                # Delete the clones that lost, now.
                for i, vm in enumerate(tries):
                    if i == winner:
                        continue
                    await client.vms.delete(vm)
                    print(f"deleted {vm}")
                tries[:] = [tries[winner]]
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            failed = True
        finally:
            # A real run keeps the winner (and the base, to try again). This one deletes both, so
            # a demo run leaves nothing behind but the checkpoint; `cove checkpoint rm` removes it.
            for vm in [*tries, base]:
                await client.vms.delete(vm)
                print(f"deleted {vm}")
    return 1 if failed else 0


async def run(client: AsyncCoveClient, vm: str, command: list[str]) -> None:
    """Run a command in the VM and fail if it fails."""
    out = await client.vms.exec_collect(vm, command=command, timeout_secs=1800)
    if out.exit_code != 0:
        raise RuntimeError(f"{' '.join(command)} failed (exit {out.exit_code}): {out.stderr}")


def make_client(mock: bool) -> AsyncCoveClient:
    if mock:
        from _mock import mock_transport

        return AsyncCoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport())
    return AsyncCoveClient(env("COVE_URL"), token=env("COVE_TOKEN"), timeout=30.0)


def env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        sys.exit(f"set {key} (see the top of this file), or run with --mock")
    return value


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
