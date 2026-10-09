#!/usr/bin/env python3
"""A throwaway box to reproduce a bug: create a VM that deletes itself after a day, tagged with
the bug report it is for, run the reproduction there, checkpoint it while it shows the failure,
and give a colleague access so they can look at the same box.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... REPORT=4521 COLLEAGUE=alice \\
      python examples/repro_box.py
    python examples/repro_box.py --mock     # offline, against an in-process fake server

The box would normally stay until its colleague is done, or until it expires; this program
deletes it and its checkpoint at the end, so a demo run leaves nothing behind.
"""

from __future__ import annotations

import os
import sys

from cove_sdk import CoveAPIError, CoveClient

# The reproduction from the report: here, a script that shows the failure and exits non-zero.
REPRO = """echo importing 3 rows
echo expected 3 rows, found 2
exit 1
"""
DAY_SECS = 24 * 3600


def main() -> int:
    mock = "--mock" in sys.argv
    report = "4521" if mock else env("REPORT")
    colleague = "alice" if mock else env("COLLEAGUE")
    with make_client(mock) as client:
        # The VM is deleted a day after it was created, whatever state it is in.
        name = client.vms.create(
            name=f"repro-{report}",
            initial_tags={"report": report},
            ttl_policy={"max_lifetime_secs": DAY_SECS},
        ).name
        print(f"created {name} for report {report}")
        checkpoint: str | None = None
        try:
            client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)
            left = client.policies.get_expiry(name).max_life_expires_in_secs
            hours = round(left / 3600) if isinstance(left, int) else 0
            print(f"{name} deletes itself in {hours} hours")

            mkdir = client.vms.exec_collect(name, command=["mkdir", "-p", "/root/repro"])
            if mkdir.exit_code != 0:
                raise RuntimeError(f"creating /root/repro failed: {mkdir.stderr}")
            client.vms.files.upload(name, "/root/repro/repro.sh", REPRO)
            run = client.vms.exec_collect(name, command=["sh", "/root/repro/repro.sh"], timeout_secs=600)
            print(run.stdout, end="")
            if run.exit_code == 0:
                print("the bug did not reproduce")
            else:
                print(f"reproduced: exit {run.exit_code}")
                # The failing state, kept: you can clone a fresh box from it even after this one
                # changed.
                saved = client.checkpoints.create(name, description=f"report {report}: failing")
                checkpoint = saved.id
                print("checkpoint taken: failing state")

                # Role "user" can connect and look; "collaborator" can also stop, start, resize
                # and checkpoint the VM.
                grant = client.vms.share(
                    name, subject_type="user", subject_id=colleague, role="collaborator"
                )
                print(f"gave {colleague} access{'' if grant.user_known else ' (when they next sign in)'}")
                print(f"{colleague} connects with: cove ssh {name}")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            client.vms.delete(name)
            if checkpoint:
                client.checkpoints.delete(checkpoint)
            print(f"deleted {name}")
    return 0


def make_client(mock: bool) -> CoveClient:
    if mock:
        from _mock import mock_transport

        return CoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport())
    return CoveClient(env("COVE_URL"), token=env("COVE_TOKEN"), timeout=30.0)


def env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        sys.exit(f"set {key} (see the top of this file), or run with --mock")
    return value


if __name__ == "__main__":
    sys.exit(main())
