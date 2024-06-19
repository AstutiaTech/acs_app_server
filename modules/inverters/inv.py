from typing import Dict
from database.model import get_all_inverters_by_control_box_id, get_inverter_by_id
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_inverters_by_control_box(db: Session, control_box_id: int=0):
    data = get_all_inverters_by_control_box_id(db=db, control_box_id=control_box_id)
    return paginate(data)

def retrieve_single_inverter(db: Session, inverter_id: int=0):
    inverter = get_inverter_by_id(db=db, id=inverter_id)
    if inverter is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': inverter,
        }