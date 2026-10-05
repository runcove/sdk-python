#!/usr/bin/env python3
"""A CI runner: one fresh VM per run. Clone the repository, install with a registry token the VM
holds only during setup, run the tests, and report the first step that fails. The VM is tagged
with the run's id, so ``cove ls`` shows which run it belongs to.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... \\
      CI_REPO_URL=https://example.com/your/repo.git REGISTRY_TOKEN=... CI_RUN_ID=42 \\
      python examples/ci_runner.py
    python examples/ci_runner.py --mock     # offline, against an in-process fake server

Needs git and make in the VM's image, and secrets turned on for the host (a host with them off
answers 503 ``feature_disabled``).
"""

from __future__ import annotations

import base64
import os
import sys
from dataclasses import dataclass

from cove_sdk import CoveAPIError, CoveClient, ExecExit, ExecStderr, ExecStdout


@dataclass
class Step:
    name: str
    command: list[str]
    secrets_tag: str | None = None


def pipeline(repo_url: str) -> list[Step]:
    """``setup`` runs with the secrets tagged "setup", which the VM wipes as soon as the step
    ends; the other steps never see them. Replace the commands with your project's."""
    return [
        Step("checkout", ["git", "clone", "--depth", "1", repo_url, "/root/src"]),
        Step(
            "setup",
            # The guest agent keeps secrets in a directory under /run/cove/secrets whose random
            # name it picks when it starts (a new one after every boot, wake or clone), so look
            # the file up by name rather than guess its path.
            [
                "sh",
                "-c",
                'f=$(find /run/cove/secrets -name REGISTRY_TOKEN -type f | head -n 1) && test -r "$f"'
                " && echo registry token available to setup",
            ],
            secrets_tag="setup",
        ),
        Step("test", ["make", "-C", "/root/src", "test"]),
    ]


def main() -> int:
    mock = "--mock" in sys.argv
    repo_url = "https://example.com/demo.git" if mock else env("CI_REPO_URL")
    registry_token = "mock-registry-token" if mock else env("REGISTRY_TOKEN")
    run_id = os.environ.get("CI_RUN_ID", "local")

    with make_client(mock) as client:
        name = client.vms.create(initial_tags={"ci_run": run_id}).name
        print(f"created {name} for run {run_id}")
        failed: str | None = None
        try:
            client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)

            # Stored on the VM, but delivered only to a command run with its tag (below).
            client.secrets.vm(name).set(
                "REGISTRY_TOKEN",
                value_b64=base64.b64encode(registry_token.encode()).decode(),
                lifetime="setup_only",
                setup_tag="setup",
            )

            for step in pipeline(repo_url):
                if step.secrets_tag:
                    # Buffered: the server runs the command with the tagged secrets, then wipes
                    # them. The whole step is one HTTP request, so the client's 30 s default would
                    # cut a long install short: give this call its own 30-minute deadline.
                    out = client.vms.exec_with_secrets(
                        name,
                        command=step.command,
                        selector={"kind": "setup_tag", "tag": step.secrets_tag},
                        timeout=1800.0,
                    )
                    sys.stdout.write(out.stdout)
                    sys.stderr.write(out.stderr)
                    exit_code = out.exit_code
                else:
                    # Streamed: output chunks arrive raw, newlines included, so write them as they are.
                    exit_code = -1
                    with client.vms.exec(name, command=step.command, timeout_secs=1800) as stream:
                        for event in stream:
                            if isinstance(event, ExecStdout):
                                sys.stdout.write(event.data)
                            elif isinstance(event, ExecStderr):
                                sys.stderr.write(event.data)
                            elif isinstance(event, ExecExit):
                                exit_code = event.code
                            else:  # ExecError or ExecPaused
                                print(f"step {step.name} did not finish: {event}", file=sys.stderr)
                if exit_code != 0:
                    print(f"step {step.name}: failed (exit {exit_code})")
                    failed = step.name
                    break
                print(f"step {step.name}: ok")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            failed = "the runner"
        finally:
            client.vms.delete(name)
            print(f"ci: failed at {failed}" if failed else "ci: passed")
            print(f"deleted {name}")
    return 1 if failed else 0


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
