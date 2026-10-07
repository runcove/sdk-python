from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.cli_too_old_body import CliTooOldBody
from ...models.get_openapi_document_response_200 import GetOpenapiDocumentResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openapi.json",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | CliTooOldBody | GetOpenapiDocumentResponse200 | None:
    if response.status_code == 200:
        response_200 = GetOpenapiDocumentResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 426:
        response_426 = CliTooOldBody.from_dict(response.json())

        return response_426

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | CliTooOldBody | GetOpenapiDocumentResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ApiError | CliTooOldBody | GetOpenapiDocumentResponse200]:
    """This API description

     Returns the OpenAPI 3.1 description of the operations this server exposes, generated from the
    server's own source. Byte-equal to the `sdk/openapi.yaml` shipped with the matching release, modulo
    the JSON/YAML encoding.

    Anonymous: an SDK generator fetches the contract before it has a credential.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | GetOpenapiDocumentResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> ApiError | CliTooOldBody | GetOpenapiDocumentResponse200 | None:
    """This API description

     Returns the OpenAPI 3.1 description of the operations this server exposes, generated from the
    server's own source. Byte-equal to the `sdk/openapi.yaml` shipped with the matching release, modulo
    the JSON/YAML encoding.

    Anonymous: an SDK generator fetches the contract before it has a credential.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | GetOpenapiDocumentResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ApiError | CliTooOldBody | GetOpenapiDocumentResponse200]:
    """This API description

     Returns the OpenAPI 3.1 description of the operations this server exposes, generated from the
    server's own source. Byte-equal to the `sdk/openapi.yaml` shipped with the matching release, modulo
    the JSON/YAML encoding.

    Anonymous: an SDK generator fetches the contract before it has a credential.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | CliTooOldBody | GetOpenapiDocumentResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> ApiError | CliTooOldBody | GetOpenapiDocumentResponse200 | None:
    """This API description

     Returns the OpenAPI 3.1 description of the operations this server exposes, generated from the
    server's own source. Byte-equal to the `sdk/openapi.yaml` shipped with the matching release, modulo
    the JSON/YAML encoding.

    Anonymous: an SDK generator fetches the contract before it has a credential.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | CliTooOldBody | GetOpenapiDocumentResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
