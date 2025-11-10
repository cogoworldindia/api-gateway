from typing import Any, Dict, Optional


def standard_response(
    *,
    status: str,
    code: int,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[Any] = None,
) -> Dict[str, Any]:
    return {
        "status": status,
        "code": code,
        "message": message,
        "data": data if data is not None else {},
        "error": error,
    }

