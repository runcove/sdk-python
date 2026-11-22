"""RamCapacity.committed_mb: an answer from a server that predates the field still reads."""

from cove_sdk.types import RamCapacity
from cove_sdk._generated.types import UNSET


def _ram(**extra: object) -> dict[str, object]:
    return {
        "host_total_mb": 131072,
        "reserved_mb": 8192,
        "reservation_mb": 512,
        "headroom_mb": 300000,
        "mem_available_mb": 100000,
        "pending_resize_mb": 0,
        "swap_total_mb": 0,
        "swap_used_mb": 0,
        "psi_mem_avg10_pct": 0.0,
        "ratio": 2.5,
        **extra,
    }


def test_unit_ram_capacity_without_committed_mb_reads() -> None:
    # An older daemon sends no committed_mb: the answer reads, the field is
    # unset, and writing it back does not invent one.
    ram = RamCapacity.from_dict(_ram())
    assert ram.committed_mb is UNSET
    assert ram.reservation_mb == 512
    assert "committed_mb" not in ram.to_dict()


def test_unit_ram_capacity_reads_committed_mb() -> None:
    ram = RamCapacity.from_dict(_ram(committed_mb=24576))
    assert ram.committed_mb == 24576
    assert ram.to_dict()["committed_mb"] == 24576
