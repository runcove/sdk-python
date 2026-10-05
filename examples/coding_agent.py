#!/usr/bin/env python3
"""A coding agent per task: every task gets a fresh VM, where Claude Code clones the repository,
makes the change unattended, and hands back a diff. The VM is deleted when the task ends, whatever
happened. Two tasks: one the agent carries out, one it finds nothing to change for.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... \\
      AGENT_REPO_URL=https://example.com/your/repo.git ANTHROPIC_API_KEY=... \\
      python examples/coding_agent.py
    python examples/coding_agent.py --mock     # offline, against an in-process fake server

Needs git, bash and the `claude` CLI in the VM's image (Cove's -loaded images have them), and
secrets turned on for the host (a host with them off answers 503 `feature_disabled`).
"""

from __future__ import annotations

import base64
import os
import re
import sys
from dataclasses import dataclass

from cove_sdk import CoveAPIError, CoveClient, CoveError

REPO = "/root/work"
DIFF = "/root/task.diff"
# The deadline asked for one agent run, in seconds. Today the host ends every streamed exec after
# 300 seconds whatever is asked for here, so a run that needs longer comes back as "did not
# finish" (see below).
AGENT_DEADLINE_SECS = 1800


@dataclass
class Task:
    id: str
    prompt: str


@dataclass
class Outcome:
    diff: str | None
    failure: str | None = None


TASKS = [
    Task("lowercase-slugs", "Make slugify() lowercase the title, and add a unit test for it."),
    Task("contributing-typo", "Fix the typo in CONTRIBUTING.md."),
]


def main() -> int:
    mock = "--mock" in sys.argv
    repo_url = "https://example.com/demo.git" if mock else env("AGENT_REPO_URL")
    api_key = "sk-ant-mock-not-a-real-key" if mock else env("ANTHROPIC_API_KEY")
    failed = False
    with make_client(mock) as client:
        for task in TASKS:
            try:
                report(task, run_task(client, task, repo_url, api_key, mock))
            except CoveAPIError as err:
                print(f"task {task.id}: API error {err.status} {err.code}: {err.message}", file=sys.stderr)
                failed = True
    return 1 if failed else 0


def run_task(client: CoveClient, task: Task, repo_url: str, api_key: str, mock: bool) -> Outcome:
    """Run one task in a VM of its own, and delete the VM whatever happens."""
    # The tag names the task, so `cove ls --tag task=<id>` finds its VM. The VM deletes itself when
    # it stops, and in any case two hours after it was created: a backstop if this process dies
    # before its `finally`.
    name = client.vms.create(
        initial_tags={"task": task.id},
        ttl_policy={"max_lifetime_secs": 7200, "on_stop": {"type": "immediate"}},
    ).name
    print(f"created {name} for task {task.id}")
    try:
        client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)

        # The key goes in as a secret, never on a command line: an environment variable that the
        # guest exports in its login shells, kept in memory and deleted with the VM. `rotate` puts
        # it into the running VM now; `set` would wait for the VM's next start.
        delivery = client.secrets.vm(name).rotate(
            "ANTHROPIC_API_KEY",
            value_b64=base64.b64encode(api_key.encode()).decode(),
            exposure="env",
            target_unit="@login",
        )
        # The summary says how many VMs the key reached. Without it the agent would run keyless.
        if delivery.vm_count != 1:
            return Outcome(None, "the API key was not delivered to the VM")

        clone = client.vms.exec_collect(
            name, command=["git", "clone", "--depth", "1", repo_url, REPO], timeout_secs=300
        )
        if clone.exit_code != 0:
            return Outcome(None, f"git clone failed: {clone.stderr.strip()}")

        # `bash -l` is a login shell, so the key is in the agent's environment. acceptEdits lets it
        # edit files without asking; the task text is an argument, not part of the script.
        try:
            run = client.vms.exec_collect(
                name,
                command=[
                    "bash",
                    "-lc",
                    'cd "$1" && claude -p "$2" --permission-mode acceptEdits',
                    "agent",
                    REPO,
                    task.prompt,
                ],
                timeout_secs=AGENT_DEADLINE_SECS,
            )
        except CoveAPIError:
            raise
        except CoveError as err:
            # The host ends the stream after 300 seconds, whatever the deadline, and the call then
            # fails. The agent may still be running in the VM: the diff is not taken, and the VM is
            # deleted below.
            return Outcome(None, f"the agent did not finish: {err}")
        print(f"agent: {(run.stdout + run.stderr).strip()}")
        if run.exit_code != 0:
            return Outcome(None, f"the agent failed (exit {run.exit_code})")

        # Stage everything, so files the agent created count too, and write the diff to a file.
        for command in (
            ["git", "-C", REPO, "add", "-A"],
            ["git", "-C", REPO, "diff", "--cached", f"--output={DIFF}"],
        ):
            step = client.vms.exec_collect(name, command=command)
            if step.exit_code != 0:
                return Outcome(None, f"{' '.join(command[3:])} failed: {step.stderr.strip()}")
        return Outcome(client.vms.files.download_bytes(name, DIFF).decode())
    finally:
        client.vms.delete(name)
        print(f"deleted {name}")


def report(task: Task, outcome: Outcome) -> None:
    """A short summary: the files the diff changes, and its first changed lines."""
    if outcome.failure:
        print(f"task {task.id}: {outcome.failure}")
        return
    diff = outcome.diff or ""
    files = re.findall(r"^diff --git a/\S+ b/(\S+)$", diff, re.MULTILINE)
    if not files:
        print(f"task {task.id}: no changes")
        return
    print(f"task {task.id}: {len(files)} file{'' if len(files) == 1 else 's'} changed: {', '.join(files)}")
    changed = [l for l in diff.split("\n") if re.match(r"[-+]", l) and not re.match(r"(---|\+\+\+) ", l)]
    for line in changed[:4]:
        print(f"  {line}")


def env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        sys.exit(f"set {key} (see the top of this file), or run with --mock")
    return value


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
