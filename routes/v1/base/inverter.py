from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, File, Form, UploadFile
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateInverterModel, UpdateInverterModel, InverterModel, InverterResponseModel, ResponseBasicModel, ErrorResponse
from modules.inverters.inv import retrieve_inverters_by_control_box, retrieve_single_inverter

router = APIRouter(
    prefix="/v1/inverters",
    tags=["v1_inverters"]
)


@router.get("/get_by_control_box/{control_box_id}", response_model=Page[InverterModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_inverters_by_control_box(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), control_box_id: int=0):
    return retrieve_inverters_by_control_box(db=db, control_box_id=control_box_id)

@router.get("/get_single/{inverter_id}", response_model=InverterResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_inverter(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), inverter_id: int = 0):
    return retrieve_single_inverter(db=db, inverter_id=inverter_id)
