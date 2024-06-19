from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateOwnerModel, UpdateOwnerModel, OwnerModel, OwnerResponseModel, ResponseBasicModel, ErrorResponse
from modules.users.base import retrieve_single_owner

router = APIRouter(
    prefix="/v1/owners",
    tags=["v1_owners"]
)

@router.get("/get_single/{owner_id}", response_model=OwnerResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), owner_id: int = 0):
    return retrieve_single_owner(db=db, owner_id=owner_id)
