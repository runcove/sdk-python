#!/usr/bin/env python3
"""Event-driven provisioning: instead of polling a new VM until it runs, follow its event
stream, which reports each creation stage as it happens, and provision the VM the moment the
stream says it is running. A failed creation arrives on the same stream as an ``error`` event, or
as state ``failed``; a stream that ends on ``deleted`` has no VM to provision.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/event_driven.py
    python examples/event_driven.py --mock     # offline, against an in-process fake server
"""

from __future__ import annotations

import os
import sys
from time import monotonic

from cove_sdk import CoveAPIError, CoveClient, VmEvent

# What to run once the VM is up.
PROVISION = "echo 'provisioned by an event handler' | tee /etc/motd"


def main() -> int:
    mock = "--mock" in sys.argv
    with make_client(mock) as client:
        name = client.vms.create().name
        print(f"created {name}")
        provisioned = False
        try:
            # The stream sends the VM's current state first on every connect, so nothing is
            # missed between `create` and here. Give up after five minutes: the stream's
            # `timeout` bounds only the wait between two events, so check a deadline too.
            deadline = monotonic() + 300
            with client.events.vm(name, timeout=300) as stream:
                for event in stream:
                    if monotonic() > deadline:
                        raise TimeoutError(f"{name} was not running after 300 s")
                    if not isinstance(event, VmEvent):
                        # StreamLagged: the server dropped events for a slow reader. A handler
                        # that must not miss one re-reads `vms.get`.
                        continue
                    if event.kind == "progress":
                        print(f"event: progress {event.data['stage']}")
                    elif event.kind == "error":
                        raise RuntimeError(
                            f"creating {name} failed at {event.data['stage']}: {event.data['message']}"
                        )
                    elif event.kind == "state":
                        print(f"event: state {event.data['state']}")
                        if event.data["state"] == "failed":
                            raise RuntimeError(f"creating {name} failed: the VM is in state failed")
                        if event.data["state"] == "deleted":
                            break  # The stream ends here; the check below reports it.
                        if event.data["state"] != "running":
                            continue
                        print(f"{name} is running, provisioning it")
                        run = client.vms.exec_collect(name, command=["sh", "-c", PROVISION, "provision"])
                        sys.stdout.write(run.stdout)
                        provisioned = True
                        break  # Leaving the block closes the stream.
            if not provisioned:
                raise RuntimeError(f"{name} was never provisioned: the event stream ended first")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            client.vms.delete(name)
            print(f"deleted {name}")
    return 0


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
