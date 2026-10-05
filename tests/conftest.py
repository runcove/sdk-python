"""Shared pytest configuration: async tests run on anyio's asyncio backend."""

import inspect

import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # Mark every coroutine test for anyio here, so tests carry no async-only marker and the
    # unasync mirror of a test module is a plain sync module.
    for item in items:
        func = getattr(item, "function", None)
        if func is not None and inspect.iscoroutinefunction(func):
            item.add_marker(pytest.mark.anyio)
