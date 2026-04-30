from secrets import compare_digest

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.core.config import API_KEY

api_key_header = APIKeyHeader(
    name="X-API-Key",
    description="API key configured in the API_KEY environment variable.",
    auto_error=False,
)


def require_api_key(api_key: str | None = Security(api_key_header)) -> None:
    if not api_key or not compare_digest(api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
