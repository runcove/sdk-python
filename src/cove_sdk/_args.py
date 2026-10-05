"""Argument shaping shared by every resource method (colour-neutral; both clients import it).

Resource methods take keyword arguments: query parameters as named keywords (``None`` = not
given), request bodies as the body's fields (``vms.create(name="web", initial_tags={"k": "v"})``)
or, equally, as one generated model or a plain mapping passed as ``body``. :func:`build_body`
turns either form into the generated request model, refusing a field the model does not have, so
a misspelt keyword fails here instead of travelling to the server as an extra JSON key.
"""

from __future__ import annotations

import datetime
import uuid
from collections.abc import Mapping
from typing import Any, Protocol, Self, TypeVar

import attrs

from ._generated.types import UNSET, Unset


class _Model(Protocol):
    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self: ...

    def to_dict(self) -> dict[str, Any]: ...


M = TypeVar("M", bound=_Model)
T = TypeVar("T")


def opt(value: T | None) -> T | Unset:
    """``None`` (the Python "not given") as the generated calls' ``UNSET``."""
    return UNSET if value is None else value


def _plain(value: Any) -> Any:
    # from_dict parses JSON-shaped data: nested models back to dicts, UUIDs and datetimes to text.
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return value.to_dict()
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def build_body(
    model: type[M], body: M | Mapping[str, Any] | None, fields: Mapping[str, Any]
) -> M:
    """The request model for ``body`` and/or keyword ``fields`` (``fields`` win on a clash).

    Raises ``TypeError`` for a field ``model`` does not declare, for a model instance mixed with
    keyword fields, and for data the model cannot parse (a missing required field, say).
    """
    if isinstance(body, model):
        if fields:
            raise TypeError(
                f"pass either a {model.__name__} or keyword fields, not both "
                f"(got {sorted(fields)})"
            )
        return body
    if body is not None and not isinstance(body, Mapping):
        raise TypeError(
            f"body must be a {model.__name__} or a mapping, got {type(body).__name__}"
        )
    data = {**(body or {}), **fields}
    known = set(attrs.fields_dict(model)) - {"additional_properties"}  # type: ignore[arg-type]
    if unknown := sorted(set(data) - known):
        raise TypeError(
            f"{model.__name__} has no field {', '.join(unknown)}; "
            f"its fields are {', '.join(sorted(known))}"
        )
    try:
        return model.from_dict({k: _plain(v) for k, v in data.items()})
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise TypeError(f"invalid {model.__name__}: {exc!r}") from exc
