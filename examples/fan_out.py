#!/usr/bin/env python3
"""Multi-VM fan-out: split one job into shards, run each shard on its own VM at the same time,
and combine the results. The job here counts the primes in 1..30000 with awk; a test suite split
by file, or a batch split by input, has the same shape. Uses the async client.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/fan_out.py
    python examples/fan_out.py --mock     # offline, against an in-process fake server

Each VM counts against your quota.
"""

from __future__ import annotations

import asyncio
import os
import sys

from cove_sdk import AsyncCoveClient, CoveAPIError

SHARDS = [(1, 10000), (10001, 20000), (20001, 30000)]

# Counts the primes in $1..$2 by trial division.
COUNT_PRIMES = """seq "$1" "$2" | awk '{ n = $1; if (n < 2) next; p = 1
  for (i = 2; i * i <= n; i++) if (n % i == 0) { p = 0; break }
  c += p } END { print c + 0 }'"""


async def main() -> int:
    mock = "--mock" in sys.argv
    async with make_client(mock) as client:
        # Create every VM at once. Keep the ones that were created even if another failed, so
        # the `finally` below deletes them all.
        created = await asyncio.gather(
            *(client.vms.create() for _ in SHARDS), return_exceptions=True
        )
        names = [c.name for c in created if not isinstance(c, BaseException)]
        try:
            for c in created:
                if isinstance(c, BaseException):
                    raise c
            print(f"created {len(names)} VMs")

            interval = 0.01 if mock else 1.0
            await asyncio.gather(
                *(client.vms.wait_for_state(n, "running", timeout=300, interval=interval) for n in names)
            )
            print(f"all {len(names)} running")

            # One shard per VM, all at once; results come back in shard order.
            async def run_shard(i: int, start: int, end: int) -> int:
                run = await client.vms.exec_collect(
                    names[i],
                    command=["sh", "-c", COUNT_PRIMES, "count-primes", str(start), str(end)],
                    timeout_secs=600,
                )
                if run.exit_code != 0:
                    raise RuntimeError(f"shard {i + 1} failed (exit {run.exit_code}): {run.stderr}")
                return int(run.stdout.strip())

            counts = await asyncio.gather(
                *(run_shard(i, start, end) for i, (start, end) in enumerate(SHARDS))
            )
            for i, count in enumerate(counts):
                print(f"shard {i + 1}: {count} primes in {SHARDS[i][0]}..{SHARDS[i][1]}")
            print(f"total: {sum(counts)} primes in {SHARDS[0][0]}..{SHARDS[-1][1]}")
        except CoveAPIError as err:
            # A create over your quota is refused here as a 409 that names the reason.
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            # Delete every VM that was created, even when one of the deletes fails.
            deleted = await asyncio.gather(
                *(client.vms.delete(n) for n in names), return_exceptions=True
            )
            ok = sum(1 for d in deleted if not isinstance(d, BaseException))
            print(f"deleted {ok} VMs")
    return 0


def make_client(mock: bool) -> AsyncCoveClient:
    if mock:
        from _mock import mock_transport

        return AsyncCoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport())
    url, token = os.environ.get("COVE_URL"), os.environ.get("COVE_TOKEN")
    if not url or not token:
        sys.exit("set COVE_URL and COVE_TOKEN (a cvk_ API key), or run with --mock")
    return AsyncCoveClient(url, token=token, timeout=30.0)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
