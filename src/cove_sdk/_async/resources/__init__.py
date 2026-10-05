"""The client's resource groups (``client.vms``, ``client.secrets``, ...), written once for the async
client and mirrored to the sync one by unasync.

Every method follows one pattern: it declares the contract operation it wraps with
:func:`cove_sdk._operations.operation`, passes path arguments as ``path={...}`` (guarded by the
transport's ``check_segment`` before anything is sent), query parameters as keywords with ``None``
meaning "not given", a request body built by :func:`cove_sdk._args.build_body`, and the caller's
``timeout=``. It returns the generated model the operation documents, or ``None`` for an empty
response.
"""
