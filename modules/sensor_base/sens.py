from typing import Dict
from database.model import get_all_sensors_by_control_box_id, get_sensor_by_id
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_sensors_by_control_box(db: Session, control_box_id: int=0):
    data = get_all_sensors_by_control_box_id(db=db, control_box_id=control_box_id)
    return paginate(data)

def retrieve_single_sensor(db: Session, sensor_id: int=0):
    sensor = get_sensor_by_id(db=db, id=sensor_id)
    if sensor is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': sensor,
        }