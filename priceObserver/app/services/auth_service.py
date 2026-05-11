from pwdlib import PasswordHash
from app.settings import settings
from fastapi import status
from fastapi.exceptions import HTTPException
from datetime import timedelta, datetime, timezone
import jwt


def verify_password(password: str) -> bool:
    # In later versions update to check password from User DB

    pwd_hash = PasswordHash.recommended()
    
    return pwd_hash.verify(password, settings.admin_password_hash.get_secret_value())
        
    
def create_access_token(data: dict, expire_time: int | None):
    payload = data.copy()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong or empty input")
    if expire_time is not None and expire_time < 0: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Token expiration time can't be less then 0")
    elif expire_time is None or expire_time == 0:
        token_expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
    else:
        token_expiration = datetime.now(timezone.utc) + timedelta(minutes=expire_time)
    payload["exp"] = token_expiration
    token = jwt.encode(payload, settings.jwt_secret_key, settings.jwt_algorithm)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def authenticate_user(username: str, password: str):
    # In Later versions add parameter scope to check if scope from user's db is valid and same
    
    if username != settings.admin_username or not verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    else:
        return {
            #to add id which will be after adding middleware and data from User DB,
            # for now it's just hardcoded datas
            "name": username,
            "role": "admin"
            }
