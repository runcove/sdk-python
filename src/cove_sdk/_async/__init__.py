# The _async package is hand-written and async-first; the _sync package is generated from it by
# unasync (scripts/sync-sdk-python.sh). Code in _async never imports `asyncio` or `anyio`:
# `_colour.py` holds the colour-specific primitives.
