from fastapi import APIRouter, Depends, status
from app.settings import settings
from pwdlib import PasswordHash
from logging import getLogger
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.exceptions import HTTPException
import jwt
from app.services.auth_service import authenticate_user, create_access_token


logger = getLogger()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    # In later versions, add extracting scopes from request form taky
    username = user_data.username
    password = user_data.password
    payload = authenticate_user(username, password)
    return create_access_token(payload, expire_time=30)
    




#@router.post(/auth/login)
#def login() - app/api/routers/auth

# def verify_password() - app/services/security  -- DONE 
# def authenticate_user() - app/services/security -- DONE
# def create_access_token() - app/services/security -- DONE
# def get_current_user() - app/services/security


    