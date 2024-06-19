from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, File, Form, UploadFile
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateBatteryModel, UpdateBatteryModel, BatteryModel, BatteryResponseModel, ResponseBasicModel, ErrorResponse
from modules.batteries.bat import retrieve_batteries_by_control_box, retrieve_single_battery

router = APIRouter(
    prefix="/v1/batteries",
    tags=["v1_batteries"]
)

@router.get("/get_by_control_box/{control_box_id}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_by_control_box(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), control_box_id: int=0):
    return retrieve_batteries_by_control_box(db=db, control_box_id=control_box_id)

@router.get("/get_single/{battery_id}", response_model=BatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), battery_id: int = 0):
    return retrieve_single_battery(db=db, battery_id=battery_id)
