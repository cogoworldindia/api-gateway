from fastapi import APIRouter, Request

from app.core.config import settings
from app.services.proxy import forward_request

router = APIRouter()


@router.api_route("/auth", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_root(request: Request):
    return await forward_request(request, settings.AUTH_SERVICE_URL)


@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_proxy(request: Request, path: str):
    return await forward_request(request, settings.AUTH_SERVICE_URL, path)

