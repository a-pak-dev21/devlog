from fastapi import APIRouter, Depends
from logging import getLogger
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.services.auth_service import authenticate_user, create_access_token


logger = getLogger()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    # In later versions, add extracting scopes from request form
    username = user_data.username
    password = user_data.password
    payload = authenticate_user(username, password)
    return create_access_token(payload, expire_time=30)

    