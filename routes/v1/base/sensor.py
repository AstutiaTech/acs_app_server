from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, File, Form, UploadFile
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateSensorModel, UpdateSensorModel, SensorModel, SensorResponseModel, ResponseBasicModel, ErrorResponse
from modules.sensor_base.sens import retrieve_sensors_by_control_box, retrieve_single_sensor

router = APIRouter(
    prefix="/v1/sensors",
    tags=["v1_sensors"]
)

@router.get("/get_by_control_box/{control_box_id}", response_model=Page[SensorModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_sensors_by_control_box(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), control_box_id: int=0):
    return retrieve_sensors_by_control_box(db=db, control_box_id=control_box_id)

@router.get("/get_single/{sensor_id}", response_model=SensorResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_sensor(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), sensor_id: int = 0):
    return retrieve_single_sensor(db=db, sensor_id=sensor_id)
