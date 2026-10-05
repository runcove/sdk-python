#!/usr/bin/env python3
"""Running untrusted code per request: every request gets a fresh VM that runs one snippet and is
deleted straight after, so nothing one request does can reach the next. The handler uploads the
snippet, runs it under a deadline, and answers with its exit code and output. Three requests: one
succeeds, one fails, one runs past its deadline.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/code_execution.py
    python examples/code_execution.py --mock     # offline, against an in-process fake server

The snippets are shell scripts; one in Python or JavaScript runs the same way with its
interpreter in the VM's image.
"""

from __future__ import annotations

import os
import sys

from cove_sdk import CoveAPIError, CoveClient

SNIPPET = "/root/job/snippet.sh"
# The deadline on each snippet, in seconds.
DEADLINE_SECS = 5

REQUESTS = [
    "echo hello from a fresh VM\n",
    "echo checking the input\nexit 3\n",
    "echo starting a long job\nsleep 600\n",
]


def main() -> int:
    mock = "--mock" in sys.argv
    failed = False
    with make_client(mock) as client:
        for i, code in enumerate(REQUESTS, start=1):
            try:
                exit_code, timed_out, output = handle(client, code, mock)
            except CoveAPIError as err:
                print(f"request {i}: API error {err.status} {err.code}: {err.message}", file=sys.stderr)
                failed = True
                continue
            status = f"killed at its {DEADLINE_SECS} s deadline" if timed_out else f"exit {exit_code}"
            print(f"request {i}: {status}: {output}")
    return 1 if failed else 0


def handle(client: CoveClient, code: str, mock: bool) -> tuple[int, bool, str]:
    """Run one snippet in a VM of its own, and delete the VM whatever happens."""
    # The VM deletes itself when it stops, and in any case an hour after it was created: a
    # backstop if this process dies before its `finally`.
    name = client.vms.create(
        ttl_policy={"max_lifetime_secs": 3600, "on_stop": {"type": "immediate"}}
    ).name
    print(f"created {name}")
    try:
        client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)
        mkdir = client.vms.exec_collect(name, command=["mkdir", "-p", "/root/job"])
        if mkdir.exit_code != 0:
            raise RuntimeError(f"creating /root/job failed: {mkdir.stderr}")
        client.vms.files.upload(name, SNIPPET, code)
        # At the deadline the guest agent kills the command and everything that stayed in its
        # process group, and the call returns exit 124 with `timed_out` set and the output written
        # before then.
        run = client.vms.exec_collect(name, command=["sh", SNIPPET], timeout_secs=DEADLINE_SECS)
        return run.exit_code, run.timed_out, (run.stdout + run.stderr).strip()
    finally:
        client.vms.delete(name)
        print(f"deleted {name}")


def make_client(mock: bool) -> CoveClient:
    if mock:
        from _mock import mock_transport

        return CoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport())
    url, token = os.environ.get("COVE_URL"), os.environ.get("COVE_TOKEN")
    if not url or not token:
        sys.exit("set COVE_URL and COVE_TOKEN (a cvk_ API key), or run with --mock")
    return CoveClient(url, token=token, timeout=30.0)


if __name__ == "__main__":
    sys.exit(main())
