from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, File, Form, UploadFile
from modules.authentication.auth import auth
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from database.schema import CreateAssetModel, UpdateAssetModel, CreateAssetFileBase64Model, UpdateAssetFileBase64Model, AssetModel, AssetFileModel, AssetResponseModel, AssetFileResponseModel, AssetWithFileModel, AssetWithFilesResponseModel, ResponseBasicModel, ErrorResponse
from modules.assets.asset_main import retrieve_assets_by_owners, retrieve_assets_by_owners_with_files, retrieve_single_asset, retrieve_single_asset_with_files, retrieve_all_asset_files_by_asset, retrieve_single_asset_file

router = APIRouter(
    prefix="/v1/assets",
    tags=["v1_assets"]
)

@router.get("/get_by_owner/{owner_id}", response_model=Page[AssetModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_by_owner(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), owner_id: int=0):
    return retrieve_assets_by_owners(db=db, owner_id=owner_id)

@router.get("/get_by_owner_with_files/{owner_id}", response_model=Page[AssetWithFileModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all_with_files(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), owner_id: int=0):
    return retrieve_assets_by_owners_with_files(db=db, owner_id=owner_id)

@router.get("/get_single/{asset_id}", response_model=AssetResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), asset_id: int = 0):
    return retrieve_single_asset(db=db, asset_id=asset_id)

@router.get("/get_single_with_file/{asset_id}", response_model=AssetWithFilesResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_with_file(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), asset_id: int = 0):
    return retrieve_single_asset_with_files(db=db, asset_id=asset_id)

@router.get("/files/get_by_asset/{asset_id}", response_model=Page[AssetFileModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def files_get_all(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), asset_id: int=0):
    return retrieve_all_asset_files_by_asset(db=db, asset_id=asset_id)

@router.get("/files/get_single/{file_id}", response_model=AssetResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def files_get_single(request: Request, user=Depends(auth.auth_user_wrapper), db: Session = Depends(get_session), file_id: int = 0):
    return retrieve_single_asset_file(db=db, file_id=file_id)
