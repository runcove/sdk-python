"""The runnable examples under examples/ complete their whole flow offline, under ``--mock``.

The worked use cases print the same lines as their TypeScript twins
(sdk/typescript/tests/examples.test.mjs holds those to the same list).

Each runs in a subprocess with this interpreter and environment, so it imports the same cove_sdk
the suite does (the installed wheel under scripts/test-sdk-python.sh). ``-W error`` turns any
warning, a ``CoveApiVersionWarning`` from a fake server out of step with the SDK included, into a
failure.
"""

import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
from spotlight_repo import git, make_repo

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


# Each use case's script and the lines its --mock run must print, in this order.
USE_CASES = {
    "agent_sandbox.py": [
        "created demo-vm",
        "demo-vm is running",
        "attempt 1: tests failed (exit 1)",
        "attempt 2: tests passed",
        "deleted demo-vm",
    ],
    "ci_runner.py": [
        "created demo-vm for run local",
        "step checkout: ok",
        "registry token available to setup",
        "step setup: ok",
        "step test: ok",
        "ci: passed",
        "deleted demo-vm",
    ],
    "file_processing.py": [
        "uploaded 2 files to /root/in",
        "apples,12",
        "pears,5",
        "deleted demo-vm",
    ],
    "event_driven.py": [
        "event: state creating",
        "event: progress booting",
        "event: state running",
        "demo-vm is running, provisioning it",
        "provisioned by an event handler",
        "deleted demo-vm",
    ],
    "fan_out.py": [
        "created 3 VMs",
        "all 3 running",
        "shard 1: 1229 primes in 1..10000",
        "shard 2: 1033 primes in 10001..20000",
        "shard 3: 983 primes in 20001..30000",
        "total: 3245 primes in 1..30000",
        "deleted 3 VMs",
    ],
    "pet_vm.py": [
        "created my-pet, pausing after 60 minutes idle",
        "my-pet is running",
        "config: version = 1",
        "checkpoint taken: before upgrade (disk only)",
        "upgrade broke the config, rolling back",
        "rolled back, config: version = 1",
        "my-pet is hibernated",
        "woke my-pet, config: version = 1",
        "deleted my-pet and 2 checkpoints",
    ],
    "code_execution.py": [
        "created demo-vm",
        "deleted demo-vm",
        "request 1: exit 0: hello from a fresh VM",
        "created demo-vm-2",
        "deleted demo-vm-2",
        "request 2: exit 3: checking the input",
        "created demo-vm-3",
        "deleted demo-vm-3",
        "request 3: killed at its 5 s deadline: starting a long job",
    ],
    "preview.py": [
        "created pr-123",
        "app is up on port 8080",
        "preview for pull request 123: https://pr-123-8080.cove.mock/",
        "deleted pr-123",
    ],
    "parallel_tries.py": [
        "created demo-vm",
        "demo-vm is prepared",
        "checkpoint taken: prepared",
        "cloned 3 VMs from the checkpoint",
        "fix 1 on demo-vm-try-1: tests failed (exit 1)",
        "fix 2 on demo-vm-try-2: tests passed",
        "fix 3 on demo-vm-try-3: tests passed",
        "keeping fix 2, on demo-vm-try-2",
        "deleted demo-vm-try-1",
        "deleted demo-vm-try-3",
        "deleted demo-vm-try-2",
        "deleted demo-vm",
    ],
    "repro_box.py": [
        "created repro-4521 for report 4521",
        "repro-4521 deletes itself in 24 hours",
        "importing 3 rows",
        "expected 3 rows, found 2",
        "reproduced: exit 1",
        "checkpoint taken: failing state",
        "gave alice access",
        "alice connects with: cove ssh repro-4521",
        "deleted repro-4521",
    ],
    "coding_agent.py": [
        "created demo-vm for task lowercase-slugs",
        "agent: slugify() now lowercases the title, and test_lowercase.py tests it.",
        "deleted demo-vm",
        "task lowercase-slugs: 2 files changed: slugify.py, test_lowercase.py",
        "  -    return \"-\".join(title.split())",
        "  +    return \"-\".join(title.lower().split())",
        "  +import unittest",
        "  +from slugify import slugify",
        "created demo-vm-2 for task contributing-typo",
        "agent: Nothing in this repository matches the task, so I changed no files.",
        "deleted demo-vm-2",
        "task contributing-typo: no changes",
    ],
    "spotlight.py": [
        "created demo-vm",
        "demo-vm is running",
        "spotlight on: main -> demo-vm:/srv/app (2 files)",
        "app.txt: version: base",
        "switched to feature",
        "app.txt: version: feature",
        "node_modules/marker: installed",
        "status: feature on /srv/app",
        "spotlight off: base tree restored on /srv/app",
        "app.txt after off: version: base",
        "status: nothing bound",
        "deleted demo-vm",
    ],
}


def run_mock(script: str) -> subprocess.CompletedProcess[str]:
    path = EXAMPLES / script
    assert path.is_file(), f"missing example {path}"
    # A credential in the caller's environment must not matter under --mock.
    # Nor may a hook's GIT_DIR and friends, which would point the examples' git at the real repository.
    env = {k: v for k, v in os.environ.items() if not k.startswith(("COVE_", "GIT_"))}
    return subprocess.run(
        [sys.executable, "-W", "error", str(path), "--mock"],
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        check=False,
    )


@pytest.mark.parametrize(
    "script", ["create_exec_destroy.py", "create_exec_destroy_async.py"]
)
def test_component_example_runs_offline_under_mock(script: str) -> None:
    proc = run_mock(script)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "exit code 0" in proc.stdout, proc.stdout
    assert "deleted" in proc.stdout, proc.stdout


@pytest.mark.parametrize("script", sorted(USE_CASES))
def test_component_use_case_runs_offline_under_mock(script: str) -> None:
    proc = run_mock(script)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    printed = proc.stdout.split("\n")
    for line in USE_CASES[script]:
        assert line in printed, f"{script} did not print {line!r}:\n{proc.stdout}"
    at = [printed.index(line) for line in USE_CASES[script]]
    assert at == sorted(at), f"{script} printed its steps out of order:\n{proc.stdout}"


def test_unit_every_use_case_is_run_under_mock() -> None:
    scripts = {
        p.name
        for p in EXAMPLES.glob("*.py")
        if not p.name.startswith("_") and not p.name.startswith("create_exec_destroy")
    }
    assert scripts == set(USE_CASES)


def test_component_fake_server_refuses_to_delete_a_checkpoint_a_live_clone_was_made_from() -> None:
    sys.path.insert(0, str(EXAMPLES))
    try:
        from _mock import mock_transport
    finally:
        sys.path.remove(str(EXAMPLES))
    from cove_sdk import CoveAPIError, CoveClient

    with CoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport()) as client:
        client.vms.create(name="src-vm")
        client.vms.wait_for_state("src-vm", "running", timeout=5, interval=0.001)
        ckpt = client.checkpoints.create("src-vm")
        client.vms.clone("src-vm", new_vm_name="copy-vm", source_checkpoint_id=ckpt.id)
        # As the server: 409 while the clone lives, then deletable once it is gone.
        with pytest.raises(CoveAPIError) as refused:
            client.checkpoints.delete(ckpt.id)
        assert (refused.value.status, refused.value.code) == (409, "checkpoint_conflict")
        client.vms.delete("copy-vm")
        client.checkpoints.delete(ckpt.id)


def test_component_fake_server_applies_the_wake_state_rule_and_the_checkpoint_status_codes() -> None:
    sys.path.insert(0, str(EXAMPLES))
    try:
        from _mock import mock_transport
    finally:
        sys.path.remove(str(EXAMPLES))
    from cove_sdk import CoveAPIError, CoveClient

    def refused(call: Callable[[], object], status: int, code: str) -> None:
        with pytest.raises(CoveAPIError) as err:
            call()
        assert (err.value.status, err.value.code) == (status, code)

    with CoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport()) as client:
        for name in ("vm-a", "vm-b"):
            client.vms.create(name=name)
            client.vms.wait_for_state(name, "running", timeout=5, interval=0.001)
        full = client.checkpoints.create("vm-a")
        disk_only = client.checkpoints.create("vm-a", disk_only=True)
        state_409 = (409, "invalid_state_transition")
        # As the server: a full checkpoint wakes only a hibernated VM, a disk-only one only a stopped VM.
        refused(lambda: client.vms.wake("vm-a", checkpoint_id=full.id), *state_409)
        refused(lambda: client.vms.wake("vm-a", checkpoint_id=disk_only.id), *state_409)
        client.vms.stop("vm-a")
        client.vms.wait_for_state("vm-a", "stopped", timeout=5, interval=0.001)
        refused(lambda: client.vms.wake("vm-a", checkpoint_id=full.id), *state_409)
        client.vms.wake("vm-a", checkpoint_id=disk_only.id)
        # A checkpoint that does not exist is a 404; one taken of another VM is a 409.
        missing = "00000000-0000-7000-8000-000000000000"
        refused(lambda: client.vms.wake("vm-b", checkpoint_id=missing), 404, "wake_target_not_found")
        refused(lambda: client.vms.wake("vm-b", checkpoint_id=full.id), *state_409)
        refused(
            lambda: client.vms.clone("vm-b", new_vm_name="copy", source_checkpoint_id=missing),
            404,
            "clone_source_not_found",
        )
        refused(
            lambda: client.vms.clone("vm-b", new_vm_name="copy", source_checkpoint_id=full.id),
            *state_409,
        )


def test_component_fake_server_gives_the_agent_its_key_only_through_the_secrets_route() -> None:
    sys.path.insert(0, str(EXAMPLES))
    try:
        from _mock import mock_transport
    finally:
        sys.path.remove(str(EXAMPLES))
    from cove_sdk import CoveAPIError, CoveClient

    def agent(shell: str) -> list[str]:
        script = 'cd "$1" && claude -p "$2" --permission-mode acceptEdits'
        return [shell, "-lc" if shell == "bash" else "-c", script, "agent", "/root/work", "lowercase"]

    with CoveClient("https://cove.mock", token="cvk_mock", transport=mock_transport()) as client:
        client.vms.create(name="agent-vm")
        client.vms.wait_for_state("agent-vm", "running", timeout=5, interval=0.001)
        client.vms.exec_collect("agent-vm", command=["git", "clone", "https://example.com/demo.git", "/root/work"])
        # No key yet: the fake agent refuses, as the real one does.
        assert client.vms.exec_collect("agent-vm", command=agent("bash")).exit_code == 1
        client.secrets.vm("agent-vm").rotate(
            "ANTHROPIC_API_KEY", value_b64="c2stYW50LXRlc3Qta2V5", exposure="env", target_unit="@login"
        )
        # A plain `sh -c` is no login shell, so the key is not in its environment.
        assert client.vms.exec_collect("agent-vm", command=agent("sh")).exit_code == 1
        # The key's value on a command line is refused.
        with pytest.raises(CoveAPIError) as refused:
            client.vms.exec_collect("agent-vm", command=["echo", "sk-ant-test-key"])
        assert refused.value.status == 400 and "ANTHROPIC_API_KEY" in refused.value.message
        assert client.vms.exec_collect("agent-vm", command=agent("bash")).exit_code == 0


def _snapshot(root: Path) -> dict[str, bytes | None]:
    """Every path under ``root`` with its bytes, so a stray write shows as a difference."""
    return {str(p): p.read_bytes() if p.is_file() else None for p in sorted(root.rglob("*"))}


def test_component_spotlight_git_leaves_a_decoy_repository_alone_under_hook_variables(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    decoy = tmp_path / "decoy.git"
    decoy.mkdir()
    git(decoy, "init", "-q", "--bare")
    before = _snapshot(decoy)
    # What a git hook exports; all of them point at the decoy, never at a real repository.
    hook = {
        "GIT_DIR": decoy,
        "GIT_WORK_TREE": decoy,
        "GIT_INDEX_FILE": decoy / "index",
        "GIT_OBJECT_DIRECTORY": decoy / "objects",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES": decoy / "objects",
        "GIT_COMMON_DIR": decoy,
    }
    for name, path in hook.items():
        monkeypatch.setenv(name, str(path))
    repo = make_repo(tmp_path / "repo")
    assert git(repo, "log", "-1", "--format=%s") == "base"
    proc = run_mock("spotlight.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _snapshot(decoy) == before
