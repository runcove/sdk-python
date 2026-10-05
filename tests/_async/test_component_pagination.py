"""paginate(): the one cursor loop every iter_* method uses (mirrored to the sync helper)."""

from types import SimpleNamespace
from typing import Any

from cove_sdk._async._pagination import paginate
from cove_sdk._generated.types import UNSET


def _pages(*pages: Any) -> tuple[list[str | None], Any]:
    calls: list[str | None] = []
    queue = list(pages)

    async def fetch(cursor: str | None) -> Any:
        calls.append(cursor)
        return queue.pop(0)

    return calls, fetch


async def test_component_paginate_follows_next_cursor_to_the_end() -> None:
    calls, fetch = _pages(
        SimpleNamespace(items=[1, 2], next_cursor="c1"),
        SimpleNamespace(items=[3], next_cursor=None),
    )
    assert [x async for x in paginate(fetch, "items")] == [1, 2, 3]
    assert calls == [None, "c1"]


async def test_component_paginate_stops_on_an_empty_or_unset_cursor() -> None:
    for last in ("", UNSET):
        calls, fetch = _pages(
            SimpleNamespace(items=["a"], next_cursor="c1"),
            SimpleNamespace(items=["b"], next_cursor=last),
            SimpleNamespace(items=["never"], next_cursor=None),
        )
        assert [x async for x in paginate(fetch, "items")] == ["a", "b"], last
        assert calls == [None, "c1"]


async def test_component_paginate_starts_from_a_given_cursor() -> None:
    calls, fetch = _pages(SimpleNamespace(vms=["v"], next_cursor=None))
    assert [x async for x in paginate(fetch, "vms", cursor="c9")] == ["v"]
    assert calls == ["c9"]


async def test_component_paginate_fetches_lazily() -> None:
    calls, fetch = _pages(
        SimpleNamespace(items=[1], next_cursor="c1"),
        SimpleNamespace(items=[2], next_cursor=None),
    )
    it = paginate(fetch, "items").__aiter__()
    assert await it.__anext__() == 1
    assert calls == [None]  # the second page is not fetched until the first is consumed
