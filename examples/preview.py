#!/usr/bin/env python3
"""A preview for every pull request: when a pull request opens, create a VM tagged with its
number, check out its branch, start the app, and publish the app's port; the URL is what you post
on the pull request. When it closes, delete every VM with that tag. Your CI or your forge's
webhook calls the two functions; this program calls both in turn.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... \\
      PREVIEW_REPO_URL=https://example.com/your/repo.git PR_NUMBER=123 PR_BRANCH=my-change \\
      python examples/preview.py
    python examples/preview.py --mock     # offline, against an in-process fake server

Needs git, python3 and curl in the VM's image, and the app's port in the host's allowed list.
The app is ``python3 -m http.server``, serving the checkout; start yours with its own command.
"""

from __future__ import annotations

import os
import sys

from cove_sdk import CoveAPIError, CoveClient

# The port the app listens on. The host refuses a port that is not in its allowed list.
PORT = 8080


def main() -> int:
    mock = "--mock" in sys.argv
    repo_url = "https://example.com/demo.git" if mock else env("PREVIEW_REPO_URL")
    pr = "123" if mock else env("PR_NUMBER")
    branch = "my-change" if mock else env("PR_BRANCH")
    with make_client(mock) as client:
        try:
            url = opened(client, pr, branch, repo_url, mock)
            print(f"preview for pull request {pr}: {url}")
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
            # Here at once, so a demo run leaves nothing; for real, when the pull request closes.
            closed(client, pr)
    return 0


def opened(client: CoveClient, pr: str, branch: str, repo_url: str, mock: bool) -> str:
    """The pull request opened: build its preview and return the URL."""
    name = client.vms.create(name=f"pr-{pr}", initial_tags={"pr": pr}).name
    print(f"created {name}")
    client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)

    run(client, name, ["git", "clone", "--depth", "1", "--branch", branch, repo_url, "/root/app"])
    # `setsid -f` starts the server in the background, in a session of its own, so it keeps
    # running after this command returns. Then wait until it answers, retrying for about 10 s.
    run(
        client,
        name,
        ["sh", "-c", f"setsid -f python3 -m http.server {PORT} --directory /root/app > /root/app.log 2>&1"],
    )
    run(
        client,
        name,
        ["curl", "-fsS", "--retry", "10", "--retry-delay", "1", "--retry-connrefused", "-o", "/dev/null", f"http://127.0.0.1:{PORT}/"],
    )
    print(f"app is up on port {PORT}")

    # Publish the port: the host proxies HTTPS to it. Only you, the people you share the VM
    # with and administrators can open the URL, after signing in, until you make it public or
    # send an invite link.
    client.vms.add_port(name, PORT)
    info = client.vms.get_url(name)
    for published in info.ports:
        if published.port == PORT:
            return published.url
    raise RuntimeError(f"port {PORT} is not in {name}'s URLs")


def closed(client: CoveClient, pr: str) -> None:
    """The pull request closed: delete every VM tagged with its number."""
    names = [vm.name for vm in client.vms.iter(tag=f"pr={pr}")]
    for name in names:
        client.vms.delete(name)
        print(f"deleted {name}")


def run(client: CoveClient, vm: str, command: list[str]) -> None:
    """Run a command in the VM and fail if it fails."""
    out = client.vms.exec_collect(vm, command=command, timeout_secs=600)
    if out.exit_code != 0:
        raise RuntimeError(f"{' '.join(command)} failed (exit {out.exit_code}): {out.stderr}")


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
