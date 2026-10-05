"""Every wrapped method's docstring names the scope the contract requires, exactly."""

import importlib
import inspect
import pathlib
import pkgutil
import re
from types import ModuleType

from ruamel.yaml import YAML

from cove_sdk._async import resources as async_resources
from cove_sdk._sync import resources as sync_resources
from cove_sdk._operations import OPERATION_ATTR

SPEC = pathlib.Path(__file__).parents[2] / "openapi.yaml"
METHODS = ("get", "put", "post", "delete", "patch", "head", "options", "trace")
# The docstring form every method uses: "Scope ``vms:write``." (a note may follow in parens).
SCOPE_LINE = re.compile(r"\bScope ``([^`]+)``")


def _contract_scopes() -> dict[str, str | None]:
    """operationId -> x-required-scope (None when the operation declares none)."""
    spec = YAML(typ="safe").load(SPEC.read_text())
    scopes: dict[str, str | None] = {}
    for item in spec["paths"].values():
        for method in METHODS:
            op = item.get(method)
            if op is not None:
                scopes[op["operationId"]] = op.get("x-required-scope")
    return scopes


def _wrapped_methods(resources: ModuleType) -> list[tuple[str, str, str]]:
    """(qualified name, operationId, docstring) of every @operation method in a resources package."""
    found: list[tuple[str, str, str]] = []
    for mod in pkgutil.iter_modules(resources.__path__):
        module = importlib.import_module(f"{resources.__name__}.{mod.name}")
        for cls_name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != module.__name__:
                continue
            for name, member in vars(cls).items():
                op_id = getattr(member, OPERATION_ATTR, None)
                if isinstance(op_id, str):
                    found.append((f"{cls_name}.{name}", op_id, inspect.getdoc(member) or ""))
    return found


def test_unit_async_docstring_scope_lines_match_the_contract() -> None:
    _check(async_resources)


def test_unit_sync_docstring_scope_lines_match_the_contract() -> None:
    """The shipped sync twins are held directly, not only through the generator."""
    _check(sync_resources)


def _check(resources: ModuleType) -> None:
    contract = _contract_scopes()
    methods = _wrapped_methods(resources)
    assert len(methods) > 100, "found too few @operation methods; the walk is broken"
    problems: list[str] = []
    for qualname, op_id, doc in sorted(methods):
        assert op_id in contract, f"{qualname}: {op_id} is not in the contract"
        stated = SCOPE_LINE.findall(doc)
        expected = contract[op_id]
        if expected is None:
            if stated:
                problems.append(f"{qualname} ({op_id}): names {stated} but the contract requires no scope")
        elif stated != [expected]:
            problems.append(
                f"{qualname} ({op_id}): docstring says {stated or 'no scope'}, contract requires {expected}"
            )
    assert not problems, "\n".join(problems)
