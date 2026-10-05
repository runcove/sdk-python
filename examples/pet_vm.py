#!/usr/bin/env python3
"""A personal pet VM: one long-lived box you keep. It pauses itself when idle, and before a risky
change you take a disk-only checkpoint, so a change that breaks it is undone by rolling the disk
back. The "upgrade" here is scripted to break the config file; the program notices, rolls back,
then hibernates the VM and wakes it again.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/pet_vm.py
    python examples/pet_vm.py --mock     # offline, against an in-process fake server

A real pet is kept. This program deletes the VM and its checkpoints at the end, so a demo run
leaves nothing behind.
"""

from __future__ import annotations

import os
import sys

from cove_sdk import CoveAPIError, CoveClient

NAME = "my-pet"
CONFIG = "/root/app/config.toml"
IDLE_SECS = 3600


def main() -> int:
    mock = "--mock" in sys.argv
    interval = 0.01 if mock else 1.0
    with make_client(mock) as client:
        # Pause the VM after an hour without traffic: its memory is kept, and it resumes where
        # it was.
        client.vms.create(
            name=NAME, auto_pause_policy={"type": "auto_pause", "idle_timeout_secs": IDLE_SECS}
        )
        print(f"created {NAME}, pausing after {IDLE_SECS // 60} minutes idle")
        checkpoints: list[str] = []
        try:
            client.vms.wait_for_state(NAME, "running", timeout=300, interval=interval)
            print(f"{NAME} is running")

            write_file(client, CONFIG, "version = 1\n")
            print(f"config: {read_config(client)}")

            # Disk only: cheaper than a full checkpoint, and enough to undo a change on disk.
            # Rolling back to it boots the VM fresh, so programs that were running start again.
            before = client.checkpoints.create(NAME, disk_only=True, description="before upgrade")
            checkpoints.append(before.id)
            print("checkpoint taken: before upgrade (disk only)")

            # The risky change, and the check that it worked. This "upgrade" empties the config.
            sh(client, f'printf %s "$1" > {CONFIG}', "")
            if sh(client, f"test -s {CONFIG}") != 0:
                print("upgrade broke the config, rolling back")
                # A disk-only checkpoint restores onto a stopped VM: its disk is replaced and it
                # boots.
                client.vms.stop(NAME)
                client.vms.wait_for_state(NAME, "stopped", timeout=300, interval=interval)
                client.vms.wake(NAME, checkpoint_id=before.id)
                client.vms.wait_for_state(NAME, "running", timeout=300, interval=interval)
                print(f"rolled back, config: {read_config(client)}")

            # Hibernate: the memory goes to disk and the VM holds no RAM until it is woken.
            hibernation = client.checkpoints.hibernate(NAME)
            checkpoints.append(hibernation.id)
            print(f"{NAME} is hibernated")
            # No checkpoint id: wake from the newest, the one hibernating just took.
            client.vms.wake(NAME)
            client.vms.wait_for_state(NAME, "running", timeout=300, interval=interval)
            print(f"woke {NAME}, config: {read_config(client)}")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            # A real pet stays. Checkpoints outlive their VM, so delete them too.
            client.vms.delete(NAME)
            for checkpoint_id in checkpoints:
                client.checkpoints.delete(checkpoint_id)
            print(f"deleted {NAME} and {len(checkpoints)} checkpoints")
    return 0


def sh(client: CoveClient, script: str, *args: str) -> int:
    """Run a shell script in the VM, with ``args`` as $1...; return its exit code."""
    run = client.vms.exec_collect(NAME, command=["sh", "-c", script, "sh", *args], timeout_secs=60)
    return run.exit_code


def read_config(client: CoveClient) -> str:
    run = client.vms.exec_collect(NAME, command=["cat", CONFIG])
    if run.exit_code != 0:
        raise RuntimeError(f"reading {CONFIG} failed: {run.stderr}")
    return run.stdout.strip()


def write_file(client: CoveClient, path: str, content: str) -> None:
    """Write ``content`` to ``path`` with ``vms.files.upload``, after making its directory."""
    mkdir = client.vms.exec_collect(NAME, command=["mkdir", "-p", path.rpartition("/")[0] or "/"])
    if mkdir.exit_code != 0:
        raise RuntimeError(f"creating the directory for {path} failed: {mkdir.stderr}")
    client.vms.files.upload(NAME, path, content)


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
