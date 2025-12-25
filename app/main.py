from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from contextlib import asynccontextmanager
from app.controllers import router as api_router
import uvicorn
from app.utils.response import standard_response

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown lifecycle events."""

    # Redis initialization 
    # await redis_client.init_redis()

    yield  # App runs while inside this context

    # Shutdown: close Redis connection
    # await redis_client.close_redis()

    print(" Shutting down, cleaning up resources...")


app = FastAPI(
    title="API Gateway",
    description="Handles routing for microservices.",
    version="1.0.0",
)

# Include routers
app.include_router(api_router, prefix="/v1", tags=["Application"])

# Health check route
@app.get("/health", tags=["Health"])
def health_check():
    return standard_response(
        status="success",
        code=200,
        message="Gateway is healthy",
        data={"service": "api_gateway"},
        error=None,
    )

# Exception handlers to enforce gateway-originated response shape
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    message = str(exc.detail) if exc.detail else "Request failed"
    body = standard_response(
        status="error",
        code=exc.status_code,
        message=message,
        data={},
        error=None,
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = standard_response(
        status="error",
        code=422,
        message="Validation error",
        data={},
        error=None,
    )
    return JSONResponse(status_code=422, content=body)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    body = standard_response(
        status="error",
        code=500,
        message="Internal server error",
        data={},
        error=None,
    )
    return JSONResponse(status_code=500, content=body)

# Entry point for running app
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=int(settings.APP_PORT),  # read from .env or settings
        reload=True
    )