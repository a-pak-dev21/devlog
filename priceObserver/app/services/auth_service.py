from pwdlib import PasswordHash
from app.settings import settings
from fastapi import status
from fastapi.exceptions import HTTPException
from datetime import timedelta, datetime, timezone
import jwt
from app.settings import settings


pwd_hash = PasswordHash.recommended()

def verify_password(password: str) -> bool:
    # In later versions update to check password from User DB
    return pwd_hash.verify(password, settings.admin_password_hash.get_secret_value())
        
    
def create_access_token(data: dict, expire_time: int | None):

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong or empty input")
    
    payload = data.copy()
    token_expiration = expire_time or settings.access_token_expire_minutes

    if token_expiration <= 0: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Token expiration time can't be less then 0")
    
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=token_expiration)
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
            "sub": username,
            "role": "admin"
            }
