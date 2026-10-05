"""``client.vms.files``: single-file transfer in and out of a running VM.

``GET``, ``PUT`` and ``HEAD`` on ``/api/vms/{name}/files``. ``stat`` and ``upload`` are plain calls;
``download`` is context-managed like the SSE streams (nothing is sent until the block is entered,
leaving it closes the response) and checks the body against its ``Content-Length``: a body that
ends short is a failed download (:class:`~cove_sdk.errors.DownloadTruncatedError`), never a
complete one.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, AsyncIterable, AsyncIterator, Iterable
from contextlib import AbstractAsyncContextManager
from datetime import datetime
from types import TracebackType
from typing import IO, Self, cast

import httpx

from ..._colour import async_read_chunk
from ..._generated.models import FileUploaded
from ..._operations import operation
from ...errors import (
    CoveConnectionError,
    CoveDecodeError,
    CoveError,
    CoveTimeoutError,
    DownloadTruncatedError,
)
from ...files import HEAD_IMPLIED_CODES, VmFileStat, file_query, stat_of, wire_mode
from .._transport import (
    CLIENT_DEFAULT,
    AsyncCoveTransport,
    CallTimeout,
    TimeoutArg,
    api_path,
)

CHUNK = 64 * 1024
"""Bytes read from a file object per chunk of an upload."""

UploadData = (
    bytes
    | bytearray
    | memoryview
    | str
    | IO[bytes]
    | AsyncIterable[bytes]
    | Iterable[bytes]
)
"""What ``upload`` sends: bytes (or a ``str``, sent as UTF-8), a binary file object, or an iterable
of ``bytes`` chunks (sync or async on the async client)."""


class FileDownload:
    """``vms.files.download``'s result: use it in a ``with`` block, then iterate it for ``bytes``
    chunks (or ``read()`` the rest). ``size``, ``mode`` and ``mtime`` are set on entering the block.

    Iteration raises :class:`~cove_sdk.errors.DownloadTruncatedError` when the body ends before
    ``size`` bytes, runs past them, or the connection breaks mid-body. The ``timeout`` given to
    ``download`` bounds the idle time between chunks (by default only the connect phase is
    bounded).
    """

    def __init__(
        self, transport: AsyncCoveTransport, path: str, *, timeout: TimeoutArg
    ) -> None:
        self._t = transport
        self._path = path
        self._timeout = timeout
        self._cm: AbstractAsyncContextManager[httpx.Response] | None = None
        self._response: httpx.Response | None = None
        self._entered = False
        self._inside = False
        self._chunks: AsyncGenerator[bytes, None] | None = None
        self._stat: VmFileStat | None = None

    @property
    def size(self) -> int:
        """The file's size in bytes (``Content-Length``)."""
        return self._require_stat().size

    @property
    def mode(self) -> int | None:
        """The file's permission bits as a number, or ``None`` when the response did not say."""
        return self._require_stat().mode

    @property
    def mtime(self) -> datetime | None:
        """The file's modification time (``Last-Modified``), or ``None`` when the response did not
        say."""
        return self._require_stat().mtime

    def _require_stat(self) -> VmFileStat:
        if self._stat is None:
            raise CoveError("use the download in a with block")
        return self._stat

    async def __aenter__(self) -> Self:
        if self._entered:
            raise CoveError("a download can be entered once")
        self._entered = True
        # identity: Content-Length must count the bytes this download yields, which a
        # content-encoded (compressed) body would not.
        cm = self._t.stream(
            "GET",
            self._path,
            timeout=self._timeout,
            accept="application/octet-stream",
            headers={"Accept-Encoding": "identity"},
        )
        response = await cm.__aenter__()
        self._cm, self._response = cm, response
        try:
            self._stat = stat_of(response.headers, "GET")
        except BaseException:
            await self._close()
            raise
        self._inside = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._inside = False
        chunks, self._chunks = self._chunks, None
        try:
            if chunks is not None:
                await chunks.aclose()
        finally:
            await self._close()

    async def _close(self) -> None:
        cm, self._cm, self._response = self._cm, None, None
        if cm is not None:
            await cm.__aexit__(None, None, None)

    def __aiter__(self) -> AsyncIterator[bytes]:
        if not self._inside or self._response is None:
            raise CoveError("use the download in a with block")
        if self._chunks is None:
            self._chunks = self._iterate(self._response)
        return self._chunks

    async def _iterate(self, response: httpx.Response) -> AsyncGenerator[bytes, None]:
        expected = self.size
        received = 0
        try:
            async for chunk in response.aiter_bytes():
                received += len(chunk)
                if received > expected:
                    raise DownloadTruncatedError(expected, received)
                yield chunk
        except httpx.TimeoutException as exc:
            raise CoveTimeoutError(f"download timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise DownloadTruncatedError(expected, received) from exc
        if received != expected:
            raise DownloadTruncatedError(expected, received)

    async def read(self) -> bytes:
        """The rest of the file as one ``bytes``, checked against ``size``."""
        parts = [chunk async for chunk in self]
        return b"".join(parts)


def _size_mismatch(size: int, got: str) -> CoveError:
    return CoveError(f"upload body does not match its declared size of {size} bytes ({got})")


def _checked_chunk(chunk: object, failure: list[CoveError]) -> bytes:
    if not isinstance(chunk, (bytes, bytearray, memoryview)):
        failure.append(CoveError("an upload iterable must yield bytes"))
        raise failure[-1]
    return bytes(chunk)


async def _assert_empty(chunks: AsyncIterator[bytes]) -> None:
    """Confirm a body declared as 0 bytes yields none, before the request goes out: with
    ``Content-Length: 0`` the server has the whole file once it has the headers."""
    failure: list[CoveError] = []
    async for chunk in chunks:
        if _checked_chunk(chunk, failure):
            raise _size_mismatch(0, "it ran past it")


async def _sized(
    chunks: AsyncIterator[bytes], size: int, failure: list[CoveError]
) -> AsyncIterator[bytes]:
    """``chunks``, counted against ``size``: a mismatch raises before the server has all ``size``
    bytes.

    The chunk that reaches ``size`` is held back until the source is exhausted: the server commits
    as soon as it has ``Content-Length`` bytes, so a later chunk could no longer fail the upload.
    The error is also kept in ``failure``, since httpx may report the broken body as its own
    transport error.
    """
    sent = 0
    held: bytes | None = None
    async for chunk in chunks:
        data = _checked_chunk(chunk, failure)
        if not data:
            continue
        sent += len(data)
        if sent > size:
            failure.append(_size_mismatch(size, "it ran past it"))
            raise failure[-1]
        if sent == size:
            held = data
        else:
            yield data
    if sent != size:
        failure.append(_size_mismatch(size, f"it ended after {sent}"))
        raise failure[-1]
    if held is not None:
        yield held


async def _from_file(file: IO[bytes]) -> AsyncIterator[bytes]:
    while True:
        chunk = await async_read_chunk(file, CHUNK)
        if not chunk:
            return
        yield chunk


async def _from_iterable(chunks: Iterable[bytes]) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk


def _remaining(file: IO[bytes]) -> int | None:
    """Bytes from ``file``'s position to its end, or ``None`` when it cannot seek."""
    try:
        if not file.seekable():
            return None
        start = file.tell()
        end = file.seek(0, 2)
        file.seek(start)
    except (OSError, ValueError, AttributeError):
        return None
    return max(end - start, 0)


class Files:
    """``client.vms.files`` -- move single files in and out of a running VM.

    ``path`` is the file's absolute path in the VM. Scopes ``files:read`` (``stat``,
    ``download``) and ``files:write`` (``upload``); both are in a new key's default set. The
    caller also needs SSH access to the VM. A transfer holds one of the guest's transfer slots
    while it runs; when they are all taken the server answers 503 ``unavailable``
    (:class:`~cove_sdk.errors.UnavailableError`): retry.

    Errors common to all three: 400 ``validation_failed`` for a path that is not absolute or has
    an empty, ``.`` or ``..`` component; 403 ``file_path_denied`` (``FilePathDeniedError``) for a
    deny-listed or pseudo-filesystem path; 404 ``vm_not_found`` (``NotFoundError``) or
    ``file_not_found`` (``VmFileNotFoundError``); 409 for a VM that is not running, or whose guest
    agent predates file transfer (``guest_agent_too_old``: restart the VM); 413 ``file_too_large``
    (``FileTooLargeError``); 422 ``file_not_regular`` (``FileNotRegularError``) for a directory,
    a device or a symlink anywhere in the path.
    """

    def __init__(self, transport: AsyncCoveTransport) -> None:
        self._t = transport

    @operation("statVmFile")
    async def stat(
        self, name: str, path: str, *, timeout: CallTimeout = CLIENT_DEFAULT
    ) -> VmFileStat:
        """Size, mode and modification time of one file, without reading it.

        Scope ``files:read``.

        A ``HEAD`` error has no body; the server names its code in ``X-Cove-Error-Code``, which
        picks the error class as a ``GET`` body's ``code`` would: a 404 is ``NotFoundError``
        (``vm_not_found``) or ``VmFileNotFoundError`` (``file_not_found``), a 403
        ``FilePathDeniedError`` (``file_path_denied``) or ``PermissionDeniedError``
        (``scope_denied``). Without the header (an older server), the status alone picks: 413 is
        ``FileTooLargeError``, 422 ``FileNotRegularError``, 503 ``UnavailableError``, and a 403 or
        404 stays ``PermissionDeniedError`` / ``NotFoundError`` with ``code`` ``None``.
        """
        target = api_path("/api/vms/{name}/files", name=name) + file_query(path)
        response = await self._t.request(
            "HEAD", target, timeout=timeout, implied_codes=HEAD_IMPLIED_CODES
        )
        return stat_of(response.headers, "HEAD")

    @operation("downloadVmFile")
    def download(
        self, name: str, path: str, *, timeout: TimeoutArg = None
    ) -> FileDownload:
        """Stream one file out of the VM. Scope ``files:read``.

        Use the result in a ``with`` block: ``size`` and ``mode`` are set on entering it, and
        iterating it yields ``bytes`` chunks, raising ``DownloadTruncatedError`` if they stop short
        of ``size``. Nothing is sent until the block is entered. ``timeout`` bounds the idle time
        between chunks; by default only the connect phase is bounded. The server ends a download
        slower than an average 256 KiB/s (60 s at least), which arrives as a short body.
        """
        target = api_path("/api/vms/{name}/files", name=name) + file_query(path)
        return FileDownload(self._t, target, timeout=timeout)

    async def download_bytes(
        self, name: str, path: str, *, timeout: TimeoutArg = None
    ) -> bytes:
        """:meth:`download`, read to the end: the whole file as ``bytes``. Scope ``files:read``.

        Raises ``DownloadTruncatedError`` rather than return fewer bytes than the file holds.
        """
        async with self.download(name, path, timeout=timeout) as download:
            return await download.read()

    @operation("uploadVmFile")
    async def upload(
        self,
        name: str,
        path: str,
        data: UploadData,
        *,
        mode: int | str | None = None,
        size: int | None = None,
        timeout: CallTimeout = CLIENT_DEFAULT,
    ) -> FileUploaded:
        """Write ``data`` to one file in the VM, creating it or replacing it whole.

        Scope ``files:write``, which is as strong as ``vms:exec``: a file written as root can run
        code. The guest renames the file into place only once every byte has arrived, so a failed
        upload leaves the old file untouched. The file is owned by root, with ``mode`` (an int such
        as ``0o755``, or the octal string ``"0755"``, within ``0o777``), else the replaced file's
        bits, else ``0644``.

        ``data`` is bytes (a ``str`` is sent as UTF-8), a binary file object (read from its
        position to its end), or an iterable of ``bytes`` chunks. The server needs the size before
        the upload starts and refuses a chunked body, so an iterable, or a file object that cannot
        seek, needs ``size``; a body that yields a different number of bytes raises ``CoveError``
        before the server commits anything. A file object is read in a worker thread on the
        async client.

        Statuses beyond those on :class:`Files`: 400 for a body shorter than its size, 413
        ``file_too_large`` for a file over the host's limit, 503 ``unavailable`` with a message
        starting ``file transfer too slow`` for an upload slower than an average 256 KiB/s, and
        507 ``guest_disk_full`` when it would leave the guest under 128 MiB free.
        """
        wire = None if mode is None else wire_mode(mode)
        if size is not None and (
            isinstance(size, bool) or not isinstance(size, int) or size < 0
        ):
            raise CoveError(f"an upload size must be a non-negative int, got {size!r}")
        target = api_path("/api/vms/{name}/files", name=name) + file_query(path, wire)

        content: bytes | AsyncIterable[bytes]
        failure: list[CoveError] = []
        if isinstance(data, str):
            data = data.encode()
        if isinstance(data, (bytes, bytearray, memoryview)):
            body = bytes(data)
            if size is not None and size != len(body):
                raise CoveError(
                    f"an upload size of {size} contradicts the body's {len(body)} bytes"
                )
            content, length = body, len(body)
        else:
            chunks: AsyncIterator[bytes]
            if hasattr(data, "read"):
                file = cast(IO[bytes], data)
                known = _remaining(file)
                if size is not None and known is not None and size != known:
                    raise CoveError(
                        f"an upload size of {size} contradicts the file's {known} remaining bytes"
                    )
                chunks = _from_file(file)
                size = known if size is None else size
            elif isinstance(data, AsyncIterable):
                chunks = aiter(data)
            elif isinstance(
                data, Iterable
            ):  # unreachable in the sync mirror; harmless there
                chunks = _from_iterable(data)
            else:
                raise CoveError(
                    f"cannot upload a {type(data).__name__}: pass bytes, a file object or an "
                    "iterable of bytes"
                )
            if size is None:
                raise CoveError(
                    "uploading a stream needs size=: the server needs the file's size before the "
                    "upload starts and refuses a chunked body"
                )
            if size == 0:
                await _assert_empty(chunks)
                content, length = b"", 0
            else:
                content, length = _sized(chunks, size, failure), size

        try:
            response = await self._t.request(
                "PUT",
                target,
                content=content,
                headers={
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(length),
                },
                timeout=timeout,
            )
        except CoveConnectionError:
            if failure:
                raise failure[-1] from None
            raise
        try:
            return FileUploaded.from_dict(response.json())
        except (ValueError, KeyError, TypeError) as exc:
            raise CoveDecodeError(
                response.status_code,
                f"could not decode the uploadVmFile response body: {exc!r}",
                response.text,
            ) from exc


__all__ = ["CHUNK", "FileDownload", "Files", "UploadData"]
