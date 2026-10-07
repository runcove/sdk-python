from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.broadcast_lag_entry import BroadcastLagEntry
    from ..models.snapshot_image_usage import SnapshotImageUsage
    from ..models.snapshot_reap_summary import SnapshotReapSummary


T = TypeVar("T", bound="AdminHostStateResponse")


@_attrs_define
class AdminHostStateResponse:
    """Admin host-page gauge body. Surfaces:
    * `ttl_pending_count` — VMs satisfying either TTL sweep predicate at
      query time (delete_after_stop grace expired or max_lifetime cap exceeded).
    * `audit_emit_failed_total` — process-lifetime count of best-effort
      audit INSERT failures. Sourced from the process-global counter in
      `cove_service::event_bus`. Useful for detecting persistent audit-log
      outages without a full Prometheus scrape.
    * `broadcast_lag` — per-(channel, consumer) process-lifetime totals of
      `Lagged(n)` events from the two daemon broadcast channels (`VmEvent`,
      `LifecycleEvent`). Sourced from `cove_server::broadcast_lag`. Lets an
      operator see which consumer is falling behind (and by how much) under
      multi-host fan-in without a Prometheus scrape.

      Attributes:
          audit_emit_failed_total (int):
          broadcast_lag (list[BroadcastLagEntry]): Per-(channel, consumer) broadcast-lag totals this process.
          orphaned_checkpoint_bytes (int): Total on-disk bytes for the orphaned checkpoints counted above
              (best-effort fs scan; same informational-gauge contract as
              `snapshot_images`).
          orphaned_checkpoint_count (int): Count of `Available` checkpoints whose source VM is gone
              (`checkpoints.vm_id IS NULL`) — the disk cost of the
              admin-checkpoint-reclamation gap this handler's sibling
              `GET /admin/checkpoints[?orphaned=true]` closes.
          snapshot_images (list[SnapshotImageUsage]): Per-image snapshot disk usage (version-dir count + bytes).
          ttl_pending_count (int):
          embedded_agent_version (None | str | Unset): Version of the guest agent this daemon embeds for hot-patching, or
              `None` when the build embeds none (`embedded_agent_version`). The admin
              Guest Agents page compares each VM's reported version against it.
          key_presentations_ignored_total (int | Unset): Presentations to `POST /api/api-keys/revoke` this process
              answered
              that revoked nothing (not a key, no matching key, already revoked).
              They write no audit row, so this counter is where they show. Not
              `required` in the schema: a daemon that predates it omits it, and the
              generated SDKs must still decode that daemon's answer.
          snapshot_last_reap (None | SnapshotReapSummary | Unset):
    """

    audit_emit_failed_total: int
    broadcast_lag: list[BroadcastLagEntry]
    orphaned_checkpoint_bytes: int
    orphaned_checkpoint_count: int
    snapshot_images: list[SnapshotImageUsage]
    ttl_pending_count: int
    embedded_agent_version: None | str | Unset = UNSET
    key_presentations_ignored_total: int | Unset = UNSET
    snapshot_last_reap: None | SnapshotReapSummary | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.snapshot_reap_summary import SnapshotReapSummary

        audit_emit_failed_total = self.audit_emit_failed_total

        broadcast_lag = []
        for broadcast_lag_item_data in self.broadcast_lag:
            broadcast_lag_item = broadcast_lag_item_data.to_dict()
            broadcast_lag.append(broadcast_lag_item)

        orphaned_checkpoint_bytes = self.orphaned_checkpoint_bytes

        orphaned_checkpoint_count = self.orphaned_checkpoint_count

        snapshot_images = []
        for snapshot_images_item_data in self.snapshot_images:
            snapshot_images_item = snapshot_images_item_data.to_dict()
            snapshot_images.append(snapshot_images_item)

        ttl_pending_count = self.ttl_pending_count

        embedded_agent_version: None | str | Unset
        if isinstance(self.embedded_agent_version, Unset):
            embedded_agent_version = UNSET
        else:
            embedded_agent_version = self.embedded_agent_version

        key_presentations_ignored_total = self.key_presentations_ignored_total

        snapshot_last_reap: dict[str, Any] | None | Unset
        if isinstance(self.snapshot_last_reap, Unset):
            snapshot_last_reap = UNSET
        elif isinstance(self.snapshot_last_reap, SnapshotReapSummary):
            snapshot_last_reap = self.snapshot_last_reap.to_dict()
        else:
            snapshot_last_reap = self.snapshot_last_reap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "audit_emit_failed_total": audit_emit_failed_total,
                "broadcast_lag": broadcast_lag,
                "orphaned_checkpoint_bytes": orphaned_checkpoint_bytes,
                "orphaned_checkpoint_count": orphaned_checkpoint_count,
                "snapshot_images": snapshot_images,
                "ttl_pending_count": ttl_pending_count,
            }
        )
        if embedded_agent_version is not UNSET:
            field_dict["embedded_agent_version"] = embedded_agent_version
        if key_presentations_ignored_total is not UNSET:
            field_dict["key_presentations_ignored_total"] = (
                key_presentations_ignored_total
            )
        if snapshot_last_reap is not UNSET:
            field_dict["snapshot_last_reap"] = snapshot_last_reap

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.broadcast_lag_entry import BroadcastLagEntry
        from ..models.snapshot_image_usage import SnapshotImageUsage
        from ..models.snapshot_reap_summary import SnapshotReapSummary

        d = dict(src_dict)
        audit_emit_failed_total = d.pop("audit_emit_failed_total")

        broadcast_lag = []
        _broadcast_lag = d.pop("broadcast_lag")
        for broadcast_lag_item_data in _broadcast_lag:
            broadcast_lag_item = BroadcastLagEntry.from_dict(broadcast_lag_item_data)

            broadcast_lag.append(broadcast_lag_item)

        orphaned_checkpoint_bytes = d.pop("orphaned_checkpoint_bytes")

        orphaned_checkpoint_count = d.pop("orphaned_checkpoint_count")

        snapshot_images = []
        _snapshot_images = d.pop("snapshot_images")
        for snapshot_images_item_data in _snapshot_images:
            snapshot_images_item = SnapshotImageUsage.from_dict(
                snapshot_images_item_data
            )

            snapshot_images.append(snapshot_images_item)

        ttl_pending_count = d.pop("ttl_pending_count")

        def _parse_embedded_agent_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        embedded_agent_version = _parse_embedded_agent_version(
            d.pop("embedded_agent_version", UNSET)
        )

        key_presentations_ignored_total = d.pop(
            "key_presentations_ignored_total", UNSET
        )

        def _parse_snapshot_last_reap(
            data: object,
        ) -> None | SnapshotReapSummary | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                snapshot_last_reap_type_1 = SnapshotReapSummary.from_dict(data)

                return snapshot_last_reap_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SnapshotReapSummary | Unset, data)

        snapshot_last_reap = _parse_snapshot_last_reap(
            d.pop("snapshot_last_reap", UNSET)
        )

        admin_host_state_response = cls(
            audit_emit_failed_total=audit_emit_failed_total,
            broadcast_lag=broadcast_lag,
            orphaned_checkpoint_bytes=orphaned_checkpoint_bytes,
            orphaned_checkpoint_count=orphaned_checkpoint_count,
            snapshot_images=snapshot_images,
            ttl_pending_count=ttl_pending_count,
            embedded_agent_version=embedded_agent_version,
            key_presentations_ignored_total=key_presentations_ignored_total,
            snapshot_last_reap=snapshot_last_reap,
        )

        admin_host_state_response.additional_properties = d
        return admin_host_state_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
