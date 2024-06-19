from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List
from modules.authentication.auth import auth
from database.schema import LoginModel, RegisterModel, AuthResponseModel, UpdateAdminModel, UpdateAdminPasswordModel, ResponseBasicModel, ErrorResponse
from modules.authentication.auth import login_user, get_loggedin_user, update_user_details, update_user_password
from database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/v1/auth",
    tags=["v1_auth"]
)

@router.post("/login", response_model=AuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def login(fields: LoginModel, db: Session = Depends(get_db)):
    """
    Login
    """
    req = login_user(db=db, field=fields.field, password=fields.password)
    return req

@router.get("/details", response_model=AuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def details(user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Loggedin user details
    """
    return get_loggedin_user(db=db, user_id=user['id'])

@router.post("/update", response_model=ResponseBasicModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(fields: UpdateAdminModel, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Update admin details
    """
    req = update_user_details(db=db, user_id=user['id'], values=dict(fields))
    return req
    
@router.post("/update_password", response_model=ResponseBasicModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_password(fields: UpdateAdminPasswordModel, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Update admin password
    """
    req = update_user_password(db=db, user_id=user['id'], password=fields.password, password_confirmation=fields.password_confirmation, old_password=fields.old_password)
    return req
    