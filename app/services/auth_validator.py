from typing import Any, Dict

import httpx
from fastapi import HTTPException, Request

from app.core.config import settings

_AUTH_VALIDATE_PATH = "/validate"


async def ensure_token_valid(request: Request) -> Dict[str, Any]:
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    validate_url = _build_validate_url(settings.AUTH_SERVICE_URL)
    headers = {"Authorization": authorization}

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.get(validate_url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error contacting auth service for validation: {exc}",
        ) from exc

    if response.status_code != 200:
        detail = _extract_error_detail(response)
        raise HTTPException(status_code=response.status_code, detail=detail)

    payload = response.json()
    request.state.auth_payload = payload
    return payload


def _build_validate_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    return f"{base}{_AUTH_VALIDATE_PATH}"


def _extract_error_detail(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return "Token validation failed"

    message = payload.get("message")
    if message:
        return message

    error = payload.get("error")
    if isinstance(error, dict):
        return error.get("message", "Token validation failed")
    if isinstance(error, str):
        return error

    return "Token validation failed"

