"""Every bearer-reachable operation is wrapped by both clients, or named on the allowlist."""

import pathlib
import re

from coverage_allowlist import NOT_YET_WRAPPED

from cove_sdk import AsyncCoveClient, CoveClient
from cove_sdk._operations import operation, wrapped_operations

SPEC = pathlib.Path(__file__).parents[2] / "openapi.yaml"
METHODS = ("get", "put", "post", "delete", "patch", "head", "options", "trace")


def _operations(text: str) -> list[tuple[str, list[str]]]:
    """(operationId, x-listeners) for every operation under ``paths:``, read line by line.

    The contract prints each path at two spaces, each method at four, and the method's
    ``operationId:`` and ``x-listeners:`` (one ``- <listener>`` per line) at six.
    """
    lines = text.splitlines()
    assert "paths:" in lines, "no top-level paths: block"
    ops: list[tuple[str, list[str]]] = []
    op_id: str | None = None
    listeners: list[str] = []
    in_listeners = False
    in_op = False

    def flush() -> None:
        if in_op:
            assert op_id is not None, "an operation without an operationId"
            ops.append((op_id, listeners))

    for line in lines[lines.index("paths:") + 1 :]:
        if line and not line.startswith(" "):
            break  # the next top-level key ends paths:
        if re.match(r"^  \S", line) or re.match(
            rf"^    (?:{'|'.join(METHODS)}):\s*$", line
        ):
            flush()
            in_op = bool(re.match(r"^    \S", line))
            op_id, listeners, in_listeners = None, [], False
            continue
        if not in_op:
            continue
        if m := re.match(r"^      operationId:\s*(\S+)\s*$", line):
            op_id, in_listeners = m.group(1), False
        elif re.match(r"^      x-listeners:\s*$", line):
            in_listeners = True
        elif in_listeners and (m := re.match(r"^      - (\S+)\s*$", line)):
            listeners.append(m.group(1))
        elif re.match(r"^      \S", line):
            in_listeners = False
    flush()
    return ops


OPS = _operations(SPEC.read_text())
ALL_IDS = {op_id for op_id, _ in OPS}
COVERAGE = {op_id for op_id, listeners in OPS if "external" in listeners}


def _check_client(cls: type) -> None:
    wrapped = wrapped_operations(cls)
    unwrapped = COVERAGE - wrapped
    missing = sorted(unwrapped - NOT_YET_WRAPPED)
    stale = sorted(NOT_YET_WRAPPED - unwrapped)
    assert not missing, (
        f"{cls.__name__} wraps none of these and they are not allowlisted: {missing}"
    )
    assert not stale, (
        f"allowlisted for {cls.__name__} but wrapped or not in the coverage set: {stale}"
    )


def test_unit_coverage_async_client() -> None:
    _check_client(AsyncCoveClient)


def test_unit_coverage_sync_client() -> None:
    _check_client(CoveClient)


def test_unit_wrapped_ids_exist_in_the_contract() -> None:
    for cls in (AsyncCoveClient, CoveClient):
        unknown = sorted(wrapped_operations(cls) - ALL_IDS)
        assert not unknown, (
            f"{cls.__name__} declares operationIds the contract lacks: {unknown}"
        )


def test_unit_wrapped_operations_leave_the_allowlist() -> None:
    for cls in (AsyncCoveClient, CoveClient):
        both = sorted(wrapped_operations(cls) & NOT_YET_WRAPPED)
        assert not both, (
            f"{cls.__name__} wraps these, so drop them from NOT_YET_WRAPPED: {both}"
        )


def test_unit_coverage_set_is_real() -> None:
    # positive control: the parser found the contract's operations, not an empty set
    assert len(COVERAGE) >= 128 and "getVm" in COVERAGE
    assert len(ALL_IDS) == len(OPS), "duplicate operationIds in the contract"
    assert (
        "revokeSession" in ALL_IDS and "revokeSession" not in COVERAGE
    )  # internal-only: an API key never changes its owner's sessions


def test_unit_allowlist_has_no_stale_entries() -> None:
    assert not sorted(NOT_YET_WRAPPED - COVERAGE)


def test_unit_walker_finds_methods_resources_and_scopes() -> None:
    # positive control for wrapped_operations: an empty result above proves nothing on its own
    class Scope:
        @operation("listVmSecrets")
        def list(self) -> None: ...

    class Inner:
        __cove_scopes__ = (Scope,)

        @operation("getVm")
        def get(self) -> None: ...

    class Client:
        inner: Inner

        @operation("health")
        def health(self) -> None: ...

    Scope.__module__ = Inner.__module__ = Client.__module__ = "cove_sdk.fake"
    assert wrapped_operations(Client) == {"health", "getVm", "listVmSecrets"}


def test_unit_readme_names_exactly_the_unwrapped_operations() -> None:
    """The README's "What is covered" counts and names the allowlist, so neither can drift."""
    readme = (pathlib.Path(__file__).parents[1] / "README.md").read_text()
    section = readme.split("## What is covered", 1)[1].split("\n## ", 1)[0]
    words = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
    n = len(NOT_YET_WRAPPED)
    phrase = "the operation in" if n == 1 else f"{words.get(n, str(n))} operations in"
    assert phrase in " ".join(section.split()), section
    named = set(re.findall(r"`([a-z][A-Za-z]+)`", section))
    assert named == set(NOT_YET_WRAPPED), section
