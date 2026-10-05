"""The selector shapes `vms.exec_with_secrets` documents must be accepted by the generated types."""

import inspect
import json
import re

from cove_sdk._args import build_body
from cove_sdk._async.resources.vms import Vms
from cove_sdk._generated.models import ExecWithSecretsRequest


def _documented_selectors() -> list[dict[str, object]]:
    doc = inspect.getdoc(Vms.exec_with_secrets) or ""
    # Inline literals like ``{"kind": "all"}``, one per double-backtick span.
    spans = re.findall(r"``(\{\"kind\".*?\})``", doc)
    return [json.loads(s) for s in spans]


def test_unit_exec_with_secrets_docstring_documents_all_three_selector_kinds() -> None:
    kinds = {s["kind"] for s in _documented_selectors()}
    assert kinds == {"all", "subset", "setup_tag"}


def test_unit_exec_with_secrets_docstring_selectors_build_a_valid_request() -> None:
    for selector in _documented_selectors():
        req = build_body(
            ExecWithSecretsRequest, None, {"command": ["true"], "selector": selector}
        )
        assert req.to_dict()["selector"] == selector
