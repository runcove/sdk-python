#!/usr/bin/env python3
"""Hello VM (async): create a VM, wait for it to boot, run a command, delete it.

Against a real host, on the external bearer listener, with a ``cvk_`` API key:

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/create_exec_destroy_async.py

``--base-url`` also sets the URL. The key is read from ``COVE_TOKEN`` only: a command-line flag would
leak it through ``ps`` and shell history. ``--image`` (or ``COVE_IMAGE``) picks a golden image
(omitted: the host's default). Without a host, against an in-process fake server:

    python examples/create_exec_destroy_async.py --mock

The sync twin is ``create_exec_destroy.py``; the calls are the same, awaited.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys

from cove_sdk import (
    AsyncCoveClient,
    CoveAPIError,
    CoveError,
    ExecExit,
    ExecStderr,
    ExecStdout,
)


def make_client(args: argparse.Namespace) -> AsyncCoveClient:
    if args.mock:
        from _mock import mock_transport

        return AsyncCoveClient(
            "https://cove.mock", token="cvk_mock", transport=mock_transport()
        )
    token = os.environ.get("COVE_TOKEN")
    if not args.base_url or not token:
        sys.exit("set COVE_URL (or pass --base-url) and COVE_TOKEN, or run with --mock")
    # timeout bounds each plain request; a stream bounds only its connect phase by default.
    return AsyncCoveClient(args.base_url, token=token, timeout=30.0)


async def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] if __doc__ else None
    )
    parser.add_argument("--base-url", default=os.environ.get("COVE_URL"))
    parser.add_argument("--image", default=os.environ.get("COVE_IMAGE"))
    parser.add_argument(
        "--mock", action="store_true", help="run against an in-process fake server"
    )
    args = parser.parse_args()

    async with make_client(args) as client:
        # 1. Create: the server answers 202 and creation continues in the background.
        # No image: the host's default golden image.
        name = (
            await client.vms.create(**({"image": args.image} if args.image else {}))
        ).name
        print(f"created {name}")
        try:
            # 2. Wait for it to boot: CoveTimeoutError after 300 s, naming the last state seen.
            vm = await client.vms.wait_for_state(
                name, "running", timeout=300, interval=0.05 if args.mock else 1.0
            )
            print(f"{name} is {vm.state} at {vm.ip_address}")

            # 3. Streamed exec. Use the stream in a with block: leaving it closes the response.
            # Output events are raw chunks with their own newlines: write them verbatim.
            async with client.vms.exec(name, command=["uname", "-a"]) as stream:
                async for event in stream:
                    if isinstance(event, ExecStdout):
                        sys.stdout.write(event.data)
                    elif isinstance(event, ExecStderr):
                        sys.stderr.write(event.data)
                    elif isinstance(event, ExecExit):
                        print(f"exit code {event.code}")
                    else:  # ExecError or ExecPaused: the stream ends here
                        print(f"exec did not finish: {event}", file=sys.stderr)

            # Or buffered, when you only want the result.
            result = await client.vms.exec_collect(name, command=["hostname"])
            print(f"hostname: {result.stdout.strip()} (exit code {result.exit_code})")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            # 4. Delete, whatever happened above (202: deletion continues in the background).
            try:
                await client.vms.delete(name)
                print(f"deleted {name}")
            except CoveError as err:  # do not mask the error that got us here
                print(f"could not delete {name}: {err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
