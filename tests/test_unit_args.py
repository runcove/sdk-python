"""build_body() and opt(): how resource methods turn keyword arguments into a generated call."""

import uuid

import pytest

from cove_sdk._args import build_body, opt
from cove_sdk._generated.models import (
    CreateVmRequest,
    ExecWithSecretsRequest,
    InjectSelectorType1,
    UpdateAutoPauseRequest,
    WakeRequest,
)
from cove_sdk._generated.types import UNSET


def test_unit_opt_maps_none_to_unset_and_keeps_falsy_values() -> None:
    assert opt(None) is UNSET
    assert opt(0) == 0 and opt("") == "" and opt(False) is False


def test_unit_build_body_from_keywords_mapping_or_model() -> None:
    from_kw = build_body(
        CreateVmRequest, None, {"name": "w", "initial_tags": {"k": "v"}}
    )
    assert from_kw.to_dict() == {"name": "w", "initial_tags": {"k": "v"}}
    from_map = build_body(CreateVmRequest, {"name": "w", "cpus": 2}, {"cpus": 4})
    assert from_map.to_dict() == {"name": "w", "cpus": 4}  # keywords win on a clash
    model = CreateVmRequest(name="w")
    assert build_body(CreateVmRequest, model, {}) is model
    assert build_body(WakeRequest, None, {}).to_dict() == {}


def test_unit_build_body_takes_nested_models_and_uuids() -> None:
    sel = InjectSelectorType1.from_dict({"kind": "subset", "names": ["A"]})
    req = build_body(
        ExecWithSecretsRequest, None, {"command": ["true"], "selector": sel}
    )
    assert req.to_dict() == {
        "command": ["true"],
        "selector": {"kind": "subset", "names": ["A"]},
    }
    cid = uuid.UUID("0199a000-0000-7000-8000-000000000001")
    assert build_body(WakeRequest, None, {"checkpoint_id": cid}).to_dict() == {
        "checkpoint_id": str(cid)
    }
    pol = build_body(UpdateAutoPauseRequest, None, {"policy": {"type": "always_on"}})
    assert pol.to_dict() == {"policy": {"type": "always_on"}}


def test_unit_build_body_refuses_unknown_fields_and_mixed_forms() -> None:
    with pytest.raises(TypeError, match="has no field vm_name"):
        build_body(CreateVmRequest, None, {"vm_name": "w"})
    with pytest.raises(TypeError, match="has no field additional_properties"):
        build_body(CreateVmRequest, {"additional_properties": {}}, {})
    with pytest.raises(TypeError, match="not both"):
        build_body(CreateVmRequest, CreateVmRequest(name="w"), {"cpus": 1})
    with pytest.raises(TypeError, match="mapping"):
        build_body(CreateVmRequest, ["name"], {})  # type: ignore[arg-type]


def test_unit_build_body_reports_a_missing_required_field_as_type_error() -> None:
    with pytest.raises(TypeError, match="invalid ExecWithSecretsRequest"):
        build_body(ExecWithSecretsRequest, None, {"command": ["true"]})
    with pytest.raises(TypeError, match="invalid ExecWithSecretsRequest"):
        build_body(
            ExecWithSecretsRequest,
            None,
            {"command": ["x"], "selector": {"kind": "bogus"}},
        )
