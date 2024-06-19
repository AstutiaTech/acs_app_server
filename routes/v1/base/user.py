from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateUserModel, UpdateUserModel, UserModel, UserResponseModel, ResponseBasicModel, ErrorResponse
from modules.users.base import retrieve_users_by_owners, retrieve_users_by_owners_and_status, retrieve_single_user

router = APIRouter(
    prefix="/v1/users",
    tags=["v1_users"]
)

@router.get("/get_by_owners/{owner_id}", response_model=Page[UserModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_by_owners(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), owner_id: int = 0):
    return retrieve_users_by_owners(db=db, owner_id=owner_id)

@router.get("/get_by_owners_and_status/{owner_id}/{status}", response_model=Page[UserModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_by_owners_and_status(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), owner_id: int = 0, status: int = 0):
    return retrieve_users_by_owners_and_status(db=db, owner_id=owner_id, status=status)

@router.get("/get_single/{user_id}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), user_id: int = 0):
    return retrieve_single_user(db=db, user_id=user_id)
