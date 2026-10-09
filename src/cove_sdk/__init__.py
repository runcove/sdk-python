"""Python client for the Cove API.

``CoveClient`` (sync) and ``AsyncCoveClient`` (async) are the entry points; ``cove_sdk.types``
re-exports the API's models; the events streamed exec and the event streams yield (also in
``cove_sdk.streams``) are exported here; :func:`verify_webhook_signature` checks a webhook delivery;
:func:`has_scope` reads what the caller's credential may do from ``meta.me()``.
"""

from . import types
from ._async._client import AsyncCoveClient
from ._async.resources.keys import SERVICE_KEYS_MIN_API_VERSION
from ._async.resources.vms import EXEC_STDIN_MIN_API_VERSION
from ._meta import API_VERSION
from ._spotlight import DEFAULT_PROTECT as SPOTLIGHT_DEFAULT_PROTECT
from ._spotlight import SpotlightOffResult, SpotlightOnResult, SpotlightStatus
from ._sync._client import CoveClient
from .auth import BearerAuth, CoveAuth, TicketAuth
from .errors import (
    AuthenticationError,
    ConflictError,
    CoveAPIError,
    CoveApiVersionWarning,
    CoveConfigError,
    CoveConnectionError,
    CoveDecodeError,
    CoveError,
    CoveTimeoutError,
    DenyReason,
    DownloadTruncatedError,
    FileNotRegularError,
    FilePathDeniedError,
    FileTooLargeError,
    NotFoundError,
    PayloadTooLargeError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    UnavailableError,
    UpgradeRequiredError,
    ValidationError,
    VmFileNotFoundError,
)
from .files import VmFileStat
from .permissions import has_scope
from .streams import (
    ExecError,
    ExecEvent,
    ExecExit,
    ExecPaused,
    ExecResult,
    ExecStderr,
    ExecStdout,
    LifecycleEvent,
    StreamLagged,
    VmEvent,
)
from .webhook import verify_webhook_signature

__all__ = [
    "API_VERSION",
    "AsyncCoveClient",
    "AuthenticationError",
    "BearerAuth",
    "ConflictError",
    "CoveAPIError",
    "CoveApiVersionWarning",
    "CoveAuth",
    "CoveClient",
    "CoveConfigError",
    "CoveConnectionError",
    "CoveDecodeError",
    "CoveError",
    "CoveTimeoutError",
    "DenyReason",
    "DownloadTruncatedError",
    "EXEC_STDIN_MIN_API_VERSION",
    "ExecError",
    "ExecEvent",
    "ExecExit",
    "ExecPaused",
    "ExecResult",
    "ExecStderr",
    "ExecStdout",
    "FileNotRegularError",
    "FilePathDeniedError",
    "FileTooLargeError",
    "LifecycleEvent",
    "NotFoundError",
    "PayloadTooLargeError",
    "PermissionDeniedError",
    "RateLimitError",
    "SERVICE_KEYS_MIN_API_VERSION",
    "SPOTLIGHT_DEFAULT_PROTECT",
    "ServerError",
    "SpotlightOffResult",
    "SpotlightOnResult",
    "SpotlightStatus",
    "StreamLagged",
    "TicketAuth",
    "UnavailableError",
    "UpgradeRequiredError",
    "ValidationError",
    "VmEvent",
    "VmFileNotFoundError",
    "VmFileStat",
    "has_scope",
    "types",
    "verify_webhook_signature",
]
