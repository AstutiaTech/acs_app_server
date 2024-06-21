from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, File, Form, UploadFile
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateControlBoxModel, UpdateControlBoxModel, ControlBoxModel, ControlBoxResponseModel, ResponseBasicModel, ErrorResponse
from modules.boxes.control import retrieve_control_boxes_by_asset, retrieve_single_control_box

router = APIRouter(
    prefix="/v1/control_boxes",
    tags=["v1_control_boxes"]
)

@router.get("/get_by_asset/{asset_id}", response_model=Page[ControlBoxModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_control_boxes_by_asset(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), asset_id: int=0):
    return retrieve_control_boxes_by_asset(db=db, asset_id=asset_id)

@router.get("/get_single/{control_box_id}", response_model=ControlBoxResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_control_box(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), control_box_id: int = 0):
    return retrieve_single_control_box(db=db, control_box_id=control_box_id)
