from typing import Dict
from database.model import get_all_control_boxes_by_asset_id, get_control_box_by_id
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate


def retrieve_control_boxes_by_asset(db: Session, asset_id: int=0):
    data = get_all_control_boxes_by_asset_id(db=db, asset_id=asset_id)
    return paginate(data)

def retrieve_single_control_box(db: Session, control_box_id: int=0):
    control_box = get_control_box_by_id(db=db, id=control_box_id)
    if control_box is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': control_box,
        }