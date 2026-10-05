import re

import cove_sdk
import cove_sdk.types as t


def test_unit_types_all_has_no_anonymous_branch_names() -> None:
    assert len(t.__all__) == len(set(t.__all__))
    assert not [n for n in t.__all__ if re.search(r"Type\d+", n)]
    assert "VmDetail" in t.__all__  # positive control: a real schema is exported


def test_unit_tagged_unions_are_exported_under_their_schema_names() -> None:
    # the spec's seven tagged unions, plus VmCreateConflictResponse — one of the four other
    # oneOf schemas — as a control that gen_types.py handles oneOf generically
    for name in (
        "AdminBulkScope",
        "AutoPausePolicy",
        "DeleteAfterStop",
        "DenyReason",
        "IdleKind",
        "InjectSelector",
        "PendingAction",
        "VmCreateConflictResponse",
    ):
        assert name in t.__all__, name


def test_unit_internal_packages_are_not_reexported() -> None:
    for mod in (cove_sdk, t):
        assert not {"_generated", "_async", "_sync"} & set(getattr(mod, "__all__", ()))


def test_unit_stream_types_are_public() -> None:
    import cove_sdk.streams as s
    from cove_sdk._operations import wrapped_operations

    for name in s.__all__:
        assert name in cove_sdk.__all__ and getattr(cove_sdk, name) is getattr(
            s, name
        ), name
    assert "ExecResult" in s.__all__  # positive control
    for client in (cove_sdk.AsyncCoveClient, cove_sdk.CoveClient):
        assert {
            "execVm",
            "streamVmConsole",
            "streamLifecycleEvents",
            "streamAllVmEvents",
            "streamVmEvents",
        } <= wrapped_operations(client), client
