"""Static hygiene of the hand-written layer, by ast walks over the source tree.

Each checker is a plain function, and each test also runs it over a source it must flag, so a
checker that silently matches nothing fails here rather than passing vacuously.
"""

import ast
import pathlib
import re

PKG = pathlib.Path(__file__).parents[1]
SRC = PKG / "src" / "cove_sdk"
TESTS = PKG / "tests"
GENERATED_API = "cove_sdk._generated.api"

COLOUR_PRIMITIVES = {"asyncio", "anyio", "trio", "threading", "time"}
SSE_MODULES = (
    f"{GENERATED_API}.monitoring.exec_vm",
    f"{GENERATED_API}.monitoring.stream_vm_console",
    f"{GENERATED_API}.events",
)
GENERATED_CALLS = {"asyncio_detailed", "asyncio", "sync_detailed", "sync"}


def _package_of(path: pathlib.Path) -> str:
    rel = path.relative_to(SRC.parent).with_suffix("")
    parts = list(rel.parts)
    return ".".join(
        parts[:-1]
    )  # a module's package; for __init__.py, the package itself


def _resolve(module: str | None, level: int, package: str) -> str:
    if level == 0:
        return module or ""
    base = package.split(".")
    base = base[: len(base) - (level - 1)]
    return ".".join(base + ([module] if module else []))


def _imports(tree: ast.AST, package: str) -> list[tuple[str, str, int]]:
    """(dotted target, bound local name, line) for every import; a ``from`` import yields module.name."""
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out.append((a.name, a.asname or a.name.split(".")[0], node.lineno))
        elif isinstance(node, ast.ImportFrom):
            mod = _resolve(node.module, node.level, package)
            out.append((mod, "", node.lineno))
            for a in node.names:
                out.append((f"{mod}.{a.name}", a.asname or a.name, node.lineno))
    return out


def _py_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)


def _hand_written() -> list[pathlib.Path]:
    return [p for p in _py_files(SRC) if "_generated" not in p.relative_to(SRC).parts]


# -- 1. colour primitives ------------------------------------------------------------------------


def colour_primitives(source: str) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.add(node.module.split(".")[0])
    return found & COLOUR_PRIMITIVES


def test_unit_async_layer_imports_no_colour_primitive() -> None:
    files = _py_files(SRC / "_async") + _py_files(TESTS / "_async")
    assert len(files) >= 4
    offenders = {
        str(p.relative_to(PKG)): sorted(found)
        for p in files
        if (found := colour_primitives(p.read_text()))
    }
    assert not offenders, (
        f"colour-specific imports under _async/ (move them to _colour.py): {offenders}"
    )
    # positive control: the colour-neutral module really does import them
    assert colour_primitives((SRC / "_colour.py").read_text()) >= {"anyio", "time"}
    assert colour_primitives("from asyncio import sleep\nimport threading.local\n") == {
        "asyncio",
        "threading",
    }


# -- 2. the generated SSE modules ----------------------------------------------------------------


def sse_imports(source: str, package: str) -> list[str]:
    return [
        f"line {line}: {target}"
        for target, _, line in _imports(ast.parse(source), package)
        if any(target == m or target.startswith(m + ".") for m in SSE_MODULES)
    ]


def test_unit_no_handwritten_import_of_generated_sse_modules() -> None:
    files = _hand_written()
    assert files
    offenders = {
        str(p.relative_to(PKG)): hits
        for p in files
        if (hits := sse_imports(p.read_text(), _package_of(p)))
    }
    assert not offenders, (
        f"hand-written code imports a generated SSE module: {offenders}"
    )
    for flagged in (
        "from cove_sdk._generated.api.monitoring import exec_vm\n",
        "from ..._generated.api.events.stream_vm_events import asyncio_detailed\n",
        "import cove_sdk._generated.api.monitoring.stream_vm_console as c\n",
    ):
        assert sse_imports(flagged, "cove_sdk._async.resources"), flagged
    assert not sse_imports(
        "from cove_sdk._generated.api.monitoring import get_vm_stats\n", "cove_sdk"
    )


# -- 3. generated calls go through the transport -------------------------------------------------


def direct_generated_calls(source: str, package: str) -> list[str]:
    tree = ast.parse(source)
    generated = {
        local
        for target, local, _ in _imports(tree, package)
        if local and target.startswith(GENERATED_API + ".")
    }
    hits = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in GENERATED_CALLS
        ):
            receiver = node.func.value
            on_generated = isinstance(receiver, ast.Name) and receiver.id in generated
            if on_generated or node.func.attr.endswith("_detailed"):
                hits.append(f"line {node.lineno}: .{node.func.attr}()")
    return hits


def test_unit_generated_calls_only_through_transport_call() -> None:
    files = [p for p in _hand_written() if p.name != "_transport.py"]
    assert files
    offenders = {
        str(p.relative_to(PKG)): hits
        for p in files
        if (hits := direct_generated_calls(p.read_text(), _package_of(p)))
    }
    assert not offenders, (
        f"call generated operations through the transport's call(): {offenders}"
    )
    flagged = "from cove_sdk._generated.api.vms import get_vm\nasync def f(c):\n    return await get_vm.asyncio(name='x', client=c)\n"
    assert direct_generated_calls(flagged, "cove_sdk._async.resources")
    assert direct_generated_calls(
        "def f(m, c):\n    return m.sync_detailed(client=c)\n", "cove_sdk"
    )
    # the transport itself is the one allowed caller, and it really does call it
    assert direct_generated_calls(
        (SRC / "_sync" / "_transport.py").read_text(), "cove_sdk._sync"
    )


# -- 4. path parameters go through call(path=...) ------------------------------------------------


def _url_params(module: str) -> set[str]:
    path = SRC.parent / (module.replace(".", "/") + ".py")
    m = re.search(r'"url": "([^"]*)"', path.read_text())
    assert m, f"no url template in {path}"
    return set(re.findall(r"\{(\w+)\}", m.group(1)))


def path_param_problems(source: str, package: str) -> tuple[int, list[str]]:
    tree = ast.parse(source)
    modules = {
        local: target
        for target, local, _ in _imports(tree, package)
        if local
        and target.startswith(GENERATED_API + ".")
        and target.count(".") == GENERATED_API.count(".") + 2
    }
    checked, problems = 0, []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "call"
        ):
            continue
        where = f"line {node.lineno}"
        first = node.args[0] if node.args else None
        if not (isinstance(first, ast.Name) and first.id in modules):
            problems.append(
                f"{where}: call()'s first argument is not a module imported from {GENERATED_API}"
            )
            continue
        params = _url_params(modules[first.id])
        kws = {k.arg: k.value for k in node.keywords if k.arg}
        path = kws.get("path")
        if path is None:
            keys: set[str] = set()
        elif isinstance(path, ast.Dict) and all(
            isinstance(k, ast.Constant) and isinstance(k.value, str) for k in path.keys
        ):
            keys = {k.value for k in path.keys if isinstance(k, ast.Constant)}
        else:
            problems.append(f"{where}: path= must be a dict literal with string keys")
            continue
        if keys != params:
            problems.append(
                f"{where}: {first.id} takes path {sorted(params)}, path= has {sorted(keys)}"
            )
        if plain := sorted(params & (set(kws) - {"path"})):
            problems.append(
                f"{where}: path parameters passed as plain keywords: {plain}"
            )
        checked += 1
    return checked, problems


def test_unit_path_params_are_passed_as_path() -> None:
    resources = SRC / "_async" / "resources"
    checked = 0
    problems: dict[str, list[str]] = {}
    for p in _py_files(resources) if resources.exists() else []:
        n, found = path_param_problems(p.read_text(), _package_of(p))
        checked += n
        if found:
            problems[str(p.relative_to(PKG))] = found
    assert not problems, problems
    if resources.exists():
        assert checked >= 1, "resources/ exists but no call() site was checked"
    # positive controls
    head = "from cove_sdk._generated.api.vms import get_vm, list_vms\n"
    good = (
        head
        + "async def f(t):\n    await t.call(get_vm, path={'name': 'x'})\n    await t.call(list_vms)\n"
    )
    assert path_param_problems(good, "cove_sdk._async.resources") == (2, [])
    for bad in (
        "async def f(self):\n    await self._t.call(self._ops.list)\n",
        head + "async def f(t):\n    await t.call(get_vm, name='x')\n",
        head + "async def f(t, p):\n    await t.call(get_vm, path=p)\n",
        head + "async def f(t):\n    await t.call(list_vms, path={'name': 'x'})\n",
    ):
        assert path_param_problems(bad, "cove_sdk._async.resources")[1], bad


# -- 5. the test mirror --------------------------------------------------------------------------


def test_unit_every_async_test_has_a_sync_mirror() -> None:
    async_tests = sorted((TESTS / "_async").glob("test_*.py"))
    assert len(async_tests) >= 2  # positive control: the walk found the async suite
    missing = [p.name for p in async_tests if not (TESTS / "_sync" / p.name).is_file()]
    assert not missing, (
        f"no tests/_sync mirror (run scripts/sync-sdk-python.sh): {missing}"
    )
