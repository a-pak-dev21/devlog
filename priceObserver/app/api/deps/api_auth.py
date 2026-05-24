from fastapi import Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from app.settings import settings
from logging import getLogger
from app.api.schemas import PayloadOut

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

logger = getLogger()

def get_current_user(token: Annotated[str, Depends(oauth2_schema)]) -> PayloadOut:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return PayloadOut(**payload)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token is expired, login again")
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication token",
                            headers={"WWW-Authenticate":"Bearer"})
