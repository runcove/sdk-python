"""The built wheel: its runtime dependencies, its typing marker and its Python floor.

Run by scripts/test-sdk-python.sh, which builds the wheel, installs it on its own and sets
COVE_SDK_WHEEL and COVE_SDK_SITE; tests/ci/test-test-sdk-python.sh asserts these ran there
rather than skipped. A plain `pytest` run (no wheel built) skips them, with that reason.
"""

import email.message
import email.parser
import os
import zipfile

import pytest

WHEEL = os.environ.get("COVE_SDK_WHEEL")
pytestmark = pytest.mark.skipif(
    not WHEEL, reason="run by scripts/test-sdk-python.sh, which builds the wheel"
)


def _metadata() -> email.message.Message:
    assert WHEEL
    with zipfile.ZipFile(WHEEL) as z:
        name = next(n for n in z.namelist() if n.endswith(".dist-info/METADATA"))
        return email.parser.Parser().parsestr(z.read(name).decode())


def test_packaging_requires_dist_is_exactly_the_runtime_set() -> None:
    names = sorted(
        r.split(";")[0].split("<")[0].split(">")[0].split("=")[0].strip().lower()
        for r in _metadata().get_all("Requires-Dist") or []
    )
    assert names == ["anyio", "attrs", "httpx", "typing-extensions"]


def test_packaging_wheel_ships_py_typed_and_requires_python() -> None:
    assert WHEEL
    with zipfile.ZipFile(WHEEL) as z:
        assert "cove_sdk/py.typed" in z.namelist()
    assert _metadata()["Requires-Python"] == ">=3.11"


def test_packaging_suite_imports_the_installed_wheel() -> None:
    import cove_sdk

    assert cove_sdk.__file__ is not None
    assert cove_sdk.__file__.startswith(os.environ["COVE_SDK_SITE"]), cove_sdk.__file__
