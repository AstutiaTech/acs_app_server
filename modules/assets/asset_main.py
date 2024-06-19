from typing import Dict
from database.model import get_all_assets_paginated, get_all_assets_paginated_with_files, get_assets_by_owner_id, get_assets_by_owner_id_with_files, get_all_asset_files, get_all_asset_files_by_asset_id, get_asset_by_id, get_asset_by_id_with_files, get_asset_file_by_id
from sqlalchemy.orm import Session
from fastapi import UploadFile
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_assets_by_owners(db: Session, owner_id: int=0):
    data = get_assets_by_owner_id(db=db, owner_id=owner_id)
    return paginate(data)

def retrieve_assets_by_owners_with_files(db: Session, owner_id: int=0):
    data = get_assets_by_owner_id_with_files(db=db, owner_id=owner_id)
    return paginate(data)

def retrieve_single_asset(db: Session, asset_id: int=0):
    asset = get_asset_by_id(db=db, id=asset_id)
    if asset is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': asset
        }
    
def retrieve_single_asset_with_files(db: Session, asset_id: int=0):
    asset = get_asset_by_id_with_files(db=db, id=asset_id)
    if asset is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': asset
        }
    
def retrieve_all_asset_files_by_asset(db: Session, asset_id: int=0):
    data = get_all_asset_files_by_asset_id(db=db, asset_id=asset_id)
    return paginate(data)

def retrieve_single_asset_file(db: Session, file_id: int=0):
    asset_file = get_asset_file_by_id(db=db, id=file_id)
    if asset_file is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': asset_file
        }