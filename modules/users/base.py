from typing import Dict
from database.model import get_owner_by_id, get_users_by_owner_id, get_users_by_owner_id_and_status, get_user_by_id
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.auth import AuthHandler

auth = AuthHandler()

def retrieve_single_owner(db: Session, owner_id: int=0):
    owner = get_owner_by_id(db=db, id=owner_id)
    if owner is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': owner
        }
    
def retrieve_users_by_owners(db: Session, owner_id: int=0):
    data = get_users_by_owner_id(db=db, owner_id=owner_id)
    return paginate(data)

def retrieve_users_by_owners_and_status(db: Session, owner_id: int=0, status: int=0):
    data = get_users_by_owner_id_and_status(db=db, owner_id=owner_id, status=status)
    return paginate(data)

def retrieve_single_user(db: Session, user_id: int=0):
    user = get_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': user
        }
    
