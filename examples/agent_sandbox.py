#!/usr/bin/env python3
"""An agent's sandbox: write code into a fresh VM, run its tests, read the failure, fix the
code and run the tests again. The "agent" here is scripted (two fixed versions of one file); a
real one would ask a model for the next version. Needs python3 in the VM's image.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/agent_sandbox.py
    python examples/agent_sandbox.py --mock     # offline, against an in-process fake server
"""

from __future__ import annotations

import os
import sys

from cove_sdk import CoveAPIError, CoveClient

WORKDIR = "/root/work"

# The agent's two attempts at the code under test, and the test it must pass.
FIRST_TRY = 'def slugify(title):\n    return "-".join(title.split())\n'
SECOND_TRY = 'def slugify(title):\n    return "-".join(title.lower().split())\n'
TEST = """import unittest
from slugify import slugify

class SlugifyTest(unittest.TestCase):
    def test_joins_words(self):
        self.assertEqual(slugify("hello  world"), "hello-world")

    def test_lowercases(self):
        self.assertEqual(slugify("Hello World"), "hello-world")
"""


def main() -> int:
    mock = "--mock" in sys.argv
    with make_client(mock) as client:
        # Create (202: creation goes on in the background), then wait until the VM runs.
        name = client.vms.create().name
        print(f"created {name}")
        try:
            client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)
            print(f"{name} is running")

            write_file(client, name, f"{WORKDIR}/test_slugify.py", TEST)
            passed = False
            for attempt, code in enumerate([FIRST_TRY, SECOND_TRY], start=1):
                write_file(client, name, f"{WORKDIR}/slugify.py", code)
                # timeout_secs is the server's deadline on the command in the guest.
                run = client.vms.exec_collect(
                    name,
                    command=["python3", "-m", "unittest", "discover", "-s", WORKDIR],
                    timeout_secs=120,
                )
                if run.exit_code == 0:
                    print(f"attempt {attempt}: tests passed")
                    passed = True
                    break
                # unittest reports on stderr; its last line is the verdict the agent reads.
                print(f"attempt {attempt}: tests failed (exit {run.exit_code})")
                print(f"  {(run.stderr.strip().splitlines() or ['(no output)'])[-1]}")
            if not passed:
                print("the tests still fail after the last attempt", file=sys.stderr)
                return 1
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            # Delete whatever happened above (202: deletion goes on in the background).
            client.vms.delete(name)
            print(f"deleted {name}")
    return 0


def write_file(client: CoveClient, vm: str, path: str, content: str) -> None:
    """Write ``content`` to ``path`` in the guest with ``vms.files.upload``.

    The server needs the directory to exist, so make it first. Any size and binary content work:
    pass ``bytes``, a binary file object, or an iterable of chunks (with ``size``) instead of a
    string.
    """
    directory = path.rpartition("/")[0] or "/"
    mkdir = client.vms.exec_collect(vm, command=["mkdir", "-p", directory])
    if mkdir.exit_code != 0:
        raise RuntimeError(f"creating the directory for {path} failed: {mkdir.stderr}")
    client.vms.files.upload(vm, path, content)


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
