from fastapi import HTTPException, Security
from fastapi.security import APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN

API_KEY = "1234567"
API_KEY_NAME = "api_key"

api_key_query = APIKeyQuery(name=API_KEY_NAME,auto_error=True)


def get_api_key(api_key: str = Security(api_key_query)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API Key"
        )