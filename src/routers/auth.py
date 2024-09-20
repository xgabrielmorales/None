from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.schemas.auth import AuthGrantedData, CreatedUserData, CreateUser
from src.services.users import create_user, user_login

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: CreateUser,
    db: Session = Depends(get_db),
) -> CreatedUserData:
    user = await create_user(db=db, user_data=user_data)

    return user


@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
)
async def login(
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> AuthGrantedData:
    access_token = await user_login(db=db, auth_data=auth_data)

    return AuthGrantedData(access_token=access_token, refresh_token=None)
