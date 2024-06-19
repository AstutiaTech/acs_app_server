from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, File, Form, UploadFile
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreatePortModel, UpdatePortModel, PortModel, PortResponseModel, ResponseBasicModel, ErrorResponse
from modules.port_base.por import retrieve_ports_by_control_box, retrieve_single_port

router = APIRouter(
    prefix="/v1/ports",
    tags=["v1_ports"]
)


@router.get("/get_by_control_box/{control_box_id}", response_model=Page[PortModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_by_control_box(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), control_box_id: int=0):
    return retrieve_ports_by_control_box(db=db, control_box_id=control_box_id)

@router.get("/get_single/{port_id}", response_model=PortResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), port_id: int = 0):
    return retrieve_single_port(db=db, port_id=port_id)
