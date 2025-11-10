from fastapi import APIRouter, Request

from app.core.config import settings
from app.services.auth_validator import ensure_token_valid
from app.services.proxy import forward_request

router = APIRouter()


@router.api_route("/users", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def users_root(request: Request):
    await ensure_token_valid(request)
    return await forward_request(request, settings.USER_SERVICE_URL)


@router.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def users_proxy(request: Request, path: str):
    await ensure_token_valid(request)
    return await forward_request(request, settings.USER_SERVICE_URL, path)

