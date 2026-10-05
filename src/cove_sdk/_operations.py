"""Which contract operation each ergonomic method wraps (colour-neutral; read by the coverage test).

A resource method declares its ``operationId`` with :func:`operation`; :func:`wrapped_operations`
walks a client class -- its own methods, every resource class named in its annotations, and every
class named in a resource class's ``__cove_scopes__`` tuple, recursively -- and collects them.
"""

from __future__ import annotations

import typing
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

OPERATION_ATTR = "__cove_operation__"
SCOPES_ATTR = "__cove_scopes__"


def operation(op_id: str) -> Callable[[F], F]:
    """Mark a method as the ergonomic wrapper of contract operation ``op_id``."""

    def mark(fn: F) -> F:
        setattr(fn, OPERATION_ATTR, op_id)
        return fn

    return mark


def _annotated_classes(cls: type) -> list[type]:
    try:
        hints = typing.get_type_hints(cls)
    except (NameError, TypeError):
        hints = {}
    return [
        tp
        for tp in hints.values()
        if isinstance(tp, type) and tp.__module__.startswith("cove_sdk.")
    ]


def wrapped_operations(client_cls: type) -> set[str]:
    """Every ``operationId`` reachable from ``client_cls`` through its resources and their scopes."""
    found: set[str] = set()
    seen: set[type] = set()
    pending: list[type] = [client_cls]
    while pending:
        cls = pending.pop()
        if cls in seen:
            continue
        seen.add(cls)
        for name in dir(cls):
            member = getattr(cls, name, None)
            op_id = getattr(member, OPERATION_ATTR, None)
            if isinstance(op_id, str):
                found.add(op_id)
        pending.extend(_annotated_classes(cls))
        pending.extend(c for c in getattr(cls, SCOPES_ATTR, ()) if isinstance(c, type))
    return found
