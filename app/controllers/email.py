from fastapi import APIRouter, Request

from app.core.config import settings
from app.services.proxy import forward_request

router = APIRouter()


@router.api_route("/mail", methods=["POST"])
async def send_email(request: Request):
    return await forward_request(request, settings.EMAIL_SERVICE_URL)


@router.api_route("/mail/{path:path}", methods=["GET", "POST"])
async def email_proxy(request: Request, path: str):
    return await forward_request(request, settings.EMAIL_SERVICE_URL, path)

