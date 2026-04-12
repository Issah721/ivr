from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config.settings import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header_str: str = Security(api_key_header)):
    if api_key_header_str == settings.api_secret_key:
        return api_key_header_str
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
