"""VmDetail.permissions: a permission name this SDK does not know reads, it does not raise."""

from cove_sdk.types import VmDetail


def _vm(permissions: list[str]) -> dict[str, object]:
    return {
        "vm_id": "0192aaaa-8888-7000-8000-000000000002",
        "name": "dev-01",
        "state": "running",
        "image": "fedora-44",
        "mac_address": "52:54:00:aa:bb:cc",
        "vcpus": 2,
        "memory_mb": 2048,
        "disk_size_gb": 20,
        "auto_pause_policy": {"type": "always_on"},
        "created_at": "2026-10-12T00:00:00Z",
        "updated_at": "2026-10-12T00:00:00Z",
        "permissions": permissions,
    }


def test_unit_vm_detail_reads_an_unknown_permission() -> None:
    # An owner holds every permission, so one a newer server adds reaches
    # every owner: reading the VM must not fail on it.
    vm = VmDetail.from_dict(_vm(["vm.view", "vm.teleport", "vm.power"]))
    assert vm.permissions == ["vm.view", "vm.teleport", "vm.power"]
    assert "vm.power" in vm.permissions
