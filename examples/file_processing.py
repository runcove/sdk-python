#!/usr/bin/env python3
"""A file-processing job: copy a batch of input files into a throwaway VM, run the processing
there (here, totalling order quantities with awk, where your own converter or an untrusted tool
would go), and read the result back. Nothing the job runs touches your machine, and the VM is
deleted at the end.

    COVE_URL=http://127.0.0.1:8090 COVE_TOKEN=cvk_... python examples/file_processing.py
    python examples/file_processing.py --mock     # offline, against an in-process fake server
"""

from __future__ import annotations

import os
import sys

from cove_sdk import CoveAPIError, CoveClient

# The batch: file name -> contents. Read your own with pathlib.Path.read_text.
INPUTS = {
    "orders-monday.csv": "apples,5\npears,2\n",
    "orders-tuesday.csv": "apples,7\npears,3\n",
}

# Sums the second column per first column over every input file, sorted by item.
PROCESS = (
    "cat /root/in/*.csv | awk -F, '{ t[$1] += $2 } END { for (k in t) print k \",\" t[k] }'"
    " | sort > /root/out/totals.csv"
)


def main() -> int:
    mock = "--mock" in sys.argv
    with make_client(mock) as client:
        name = client.vms.create().name
        print(f"created {name}")
        try:
            client.vms.wait_for_state(name, "running", timeout=300, interval=0.01 if mock else 1.0)
            print(f"{name} is running")

            for file, content in INPUTS.items():
                write_file(client, name, f"/root/in/{file}", content)
            print(f"uploaded {len(INPUTS)} files to /root/in")

            job = client.vms.exec_collect(
                name,
                command=["sh", "-c", f"mkdir -p /root/out && {PROCESS}", "sum-orders"],
                timeout_secs=600,
            )
            if job.exit_code != 0:
                raise RuntimeError(f"processing failed (exit {job.exit_code}): {job.stderr}")

            # download_bytes reads the whole file; `vms.files.download` streams a large one instead.
            result = client.vms.files.download_bytes(name, "/root/out/totals.csv")
            print("totals.csv:")
            sys.stdout.write(result.decode())
        except CoveAPIError as err:
            print(f"API error {err.status} {err.code}: {err.message}", file=sys.stderr)
            return 1
        finally:
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
