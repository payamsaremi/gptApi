from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN
# from config import Settings, get_settings
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    GENOAI_API_KEY: str = 'GENOAI_API_KEY'

    class Config:
        env_file = ".env"

# New decorator for cache
@lru_cache()
def get_settings():
    return Settings()

api_key_header = APIKeyHeader(name="access-token", auto_error=False)

async def get_api_key(settings: Settings = Depends(get_settings), api_key_header: str = Security(api_key_header)):
    print(settings, api_key_header)
    if api_key_header == str(settings.GENOAI_API_KEY):
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )