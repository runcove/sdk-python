from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.rotate_summary import RotateSummary
from ...models.scope_denied_body import ScopeDeniedBody
from ...models.set_secret_request import SetSecretRequest
from ...models.sudo_required_body import SudoRequiredBody
from ...types import Response


def _get_kwargs(
    name: str,
    key: str,
    *,
    body: SetSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/vms/{name}/secrets/{key}/rotate".format(
            name=quote(str(name), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody | None
):
    if response.status_code == 200:
        response_200 = RotateSummary.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:

        def _parse_response_401(data: object) -> ApiError | SudoRequiredBody:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_sensitive_op_unauthorized_response_type_0 = (
                    ApiError.from_dict(data)
                )

                return componentsschemas_sensitive_op_unauthorized_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_sensitive_op_unauthorized_response_type_1 = (
                SudoRequiredBody.from_dict(data)
            )

            return componentsschemas_sensitive_op_unauthorized_response_type_1

        response_401 = _parse_response_401(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ScopeDeniedBody.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 503:
        response_503 = ApiError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
]:
    """Rotate a secret with acked push to the running VM

     Unlike `POST /vms/{name}/secrets/{key}`, this delivers to a running VM immediately and waits for the
    guest to acknowledge (`set` stores; `rotate` is the acked live push) — the response reports the
    confirmed count, not just an accepted write. Same request shape as `set`; `--as`/`target_unit` must
    be re-passed on every rotate, since the sink is not remembered from a prior `set`. Like `set`, it
    needs a recent interactive login: a stale one is answered 401 `sudo_required` and the CLI re-
    authenticates and replays.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        key=key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> (
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody | None
):
    """Rotate a secret with acked push to the running VM

     Unlike `POST /vms/{name}/secrets/{key}`, this delivers to a running VM immediately and waits for the
    guest to acknowledge (`set` stores; `rotate` is the acked live push) — the response reports the
    confirmed count, not just an accepted write. Same request shape as `set`; `--as`/`target_unit` must
    be re-passed on every rotate, since the sink is not remembered from a prior `set`. Like `set`, it
    needs a recent interactive login: a stale one is answered 401 `sudo_required` and the CLI re-
    authenticates and replays.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
    """

    return sync_detailed(
        name=name,
        key=key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> Response[
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
]:
    """Rotate a secret with acked push to the running VM

     Unlike `POST /vms/{name}/secrets/{key}`, this delivers to a running VM immediately and waits for the
    guest to acknowledge (`set` stores; `rotate` is the acked live push) — the response reports the
    confirmed count, not just an accepted write. Same request shape as `set`; `--as`/`target_unit` must
    be re-passed on every rotate, since the sink is not remembered from a prior `set`. Like `set`, it
    needs a recent interactive login: a stale one is answered 401 `sudo_required` and the CLI re-
    authenticates and replays.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody]
    """

    kwargs = _get_kwargs(
        name=name,
        key=key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetSecretRequest,
) -> (
    ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody | None
):
    """Rotate a secret with acked push to the running VM

     Unlike `POST /vms/{name}/secrets/{key}`, this delivers to a running VM immediately and waits for the
    guest to acknowledge (`set` stores; `rotate` is the acked live push) — the response reports the
    confirmed count, not just an accepted write. Same request shape as `set`; `--as`/`target_unit` must
    be re-passed on every rotate, since the sink is not remembered from a prior `set`. Like `set`, it
    needs a recent interactive login: a stale one is answered 401 `sudo_required` and the CLI re-
    authenticates and replays.

    Returns **503** with `feature_disabled` when `[secrets] enabled = false`. A VM that does not exist,
    or is not visible to the caller, returns **404** (existence non-leak).

    Args:
        name (str):
        key (str):
        body (SetSecretRequest): Wire body for `POST /vms/{name}/secrets/{key}`.

            Mirrors `cove_api_client::wire_types::SetSecretRequest` exactly:
            base64-encoded value (so non-UTF8 binary survives JSON transport)
            + string-tagged exposure / lifetime split into sibling fields. The
              decoder maps these into the `cove-protocol` enums.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | ApiError | SudoRequiredBody | CliTooOldBody | RotateSummary | ScopeDeniedBody
    """

    return (
        await asyncio_detailed(
            name=name,
            key=key,
            client=client,
            body=body,
        )
    ).parsed
