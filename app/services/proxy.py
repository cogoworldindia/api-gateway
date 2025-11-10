from typing import Dict

import httpx
from fastapi import HTTPException, Request, Response

_FORWARDED_REQUEST_HEADERS_TO_EXCLUDE = {"host", "content-length"}
_FORWARDED_RESPONSE_HEADERS_TO_EXCLUDE = {
    "content-encoding",
    "transfer-encoding",
    "connection",
}


async def forward_request(request: Request, service_base_url: str, path: str = "") -> Response:
    """
    Proxy the incoming request to a downstream service and return its response.

    Args:
        request: The inbound FastAPI request.
        service_base_url: The downstream service base URL (e.g. http://127.0.0.1:8083).
        path: Optional path suffix to append to the base URL.
    """
    target_url = _build_target_url(service_base_url, path)
    body = await request.body()
    headers = _filter_headers(dict(request.headers), _FORWARDED_REQUEST_HEADERS_TO_EXCLUDE)

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            downstream_response = await client.request(
                request.method,
                target_url,
                params=request.query_params,
                headers=headers,
                content=body or None,
            )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with downstream service: {exc}",
        ) from exc

    response_headers = _filter_headers(
        dict(downstream_response.headers),
        _FORWARDED_RESPONSE_HEADERS_TO_EXCLUDE,
    )

    return Response(
        content=downstream_response.content,
        status_code=downstream_response.status_code,
        headers=response_headers,
        media_type=downstream_response.headers.get("content-type"),
    )


def _build_target_url(service_base_url: str, path: str) -> str:
    base = service_base_url.rstrip("/")
    suffix = path.lstrip("/")
    return f"{base}/{suffix}" if suffix else base


def _filter_headers(headers: Dict[str, str], exclusions: set[str]) -> Dict[str, str]:
    return {k: v for k, v in headers.items() if k.lower() not in exclusions}

