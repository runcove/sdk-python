"""Async cancellation propagates unwrapped (async only, so it may use anyio; not mirrored)."""

import anyio
import httpx

from cove_sdk import AsyncCoveClient
from cove_sdk._generated.api.vms import get_vm


def _blocking_client() -> tuple[AsyncCoveClient, list[httpx.Request]]:
    never = anyio.Event()
    reached: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        reached.append(request)
        await never.wait()
        raise AssertionError("the event is never set")

    client = AsyncCoveClient(
        "https://h", token="cvk_c", transport=httpx.MockTransport(handler)
    )
    return client, reached


async def test_component_cancellation_propagates_unwrapped() -> None:
    client, reached = _blocking_client()
    async with client:
        for run in (
            lambda: client._transport.request("GET", "/api/vms"),
            lambda: client._transport.call(get_vm, path={"name": "x"}),
        ):
            # A CoveError (or anything else) raised instead of the cancellation escapes the scope
            # and fails the test; cancelled_caught is True only if the cancellation itself arrived.
            with anyio.move_on_after(0.1) as scope:
                await run()
            assert scope.cancelled_caught
    assert len(reached) == 2  # positive control: both calls really were in flight
