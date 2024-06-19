from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List
from modules.authentication.auth import auth
from database.schema import LoginModel, LoginBiomentricModel, AuthResponseModel, UpdateUserModel, UpdateUserPasswordModel, UpdateBiometricModel, ResponseBasicModel, ErrorResponse
from modules.authentication.auth import login_user, login_biometric_user, get_loggedin_user, update_user_details, update_user_password, update_user_biometric_id
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

@router.post("/biometric_login", response_model=AuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def biometric_login(fields: LoginBiomentricModel, db: Session = Depends(get_db)):
    """
    Login
    """
    req = login_biometric_user(db=db, signature=fields.signature)
    return req

@router.get("/details", response_model=AuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def details(user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Loggedin user details
    """
    return get_loggedin_user(db=db, user_id=user['id'])

@router.post("/update", response_model=ResponseBasicModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(fields: UpdateUserModel, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Update user details
    """
    req = update_user_details(db=db, user_id=user['id'], values=dict(fields))
    return req
    
@router.post("/update_password", response_model=ResponseBasicModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_password(fields: UpdateUserPasswordModel, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Update user password
    """
    req = update_user_password(db=db, user_id=user['id'], password=fields.password, password_confirmation=fields.password_confirmation, old_password=fields.old_password)
    return req
    
@router.post("/update_biometric_signature", response_model=ResponseBasicModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_biometric_signature(fields: UpdateBiometricModel, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_db)):
    """
    Update user password
    """
    req = update_user_biometric_id(db=db, user_id=user['id'], signature=fields.signature)
    return req
    