from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.settings import settings
from logging import getLogger

oauth2_schema = OAuth2PasswordBearer("/auth/login")

logger = getLogger()

def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    logger.info(f"The payload after decoding token is: {payload}")
    return payload
