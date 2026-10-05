"""check_segment and api_path: the dot-segment guard every path argument passes through."""

import pytest

from cove_sdk._async._transport import api_path, check_segment
from cove_sdk.errors import CoveError


@pytest.mark.parametrize("bad", ["", ".", ".."])
def test_unit_segment_guard_rejects(bad: str) -> None:
    with pytest.raises(CoveError):
        check_segment(bad)


def test_unit_segment_guard_accepts_what_the_call_encodes() -> None:
    assert check_segment("a b/c") == "a b/c" and check_segment(7) == "7"
    assert (
        check_segment("...") == "..."
    )  # only the exact dot segments retarget a request


def test_unit_api_path_encodes_and_guards_every_segment() -> None:
    assert api_path("/api/vms/{name}/exec", name="a b/c") == "/api/vms/a%20b%2Fc/exec"
    with pytest.raises(CoveError):
        api_path("/api/vms/{name}/exec", name="..")
