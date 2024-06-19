from typing import Dict
from database.model import user_login, user_biometric_login, update_user, get_user_by_id
from modules.utils.tools import process_schema_dictionary
from modules.utils.auth import AuthHandler
from sqlalchemy.orm import Session
import random

auth = AuthHandler()
  
def login_user(db: Session, field: str=None, password: str=None):
    user = user_login(db=db, field=field)
    if user is None:
        return {
            'status': False,
            'message': 'Username or Email not found',
            'data': None,
        }
    else:
        if not auth.verify_password(plain_password=password, hashed_password=user.password):
            return {
                'status': False,
                'message': 'Incorrect Password',
                'data': None,
            }
        else:
            if user.status == 0:
                return {
                    'status': False,
                    'message': 'User has been deactivated',
                    'data': None,
                }
            else:
                if user.deleted_at is not None:
                    return {
                        'status': False,
                        'message': 'User has been deleted',
                        'data': None,
                    }
                else:
                    payload = {
                        'id': user.id,
                        'owner_id': user.owner_id,
                        'username': user.username,
                        'email': user.email,
                    }
                    token = auth.encode_token(user=payload)
                    data = {
                        'access_token': token,
                        'id': user.id,
                        'owner_id': user.owner_id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'created_at': user.created_at,
                    }
                    return {
                        'status': True,
                        'message': 'Login Success',
                        'data': data,
                    }
                
def login_biometric_user(db: Session, signature: str = None):
    user = user_biometric_login(db=db, biometric_id=signature)
    if user is None:
        return {
            'status': False,
            'message': 'Signature is incorrect',
            'data': None
        }
    else:
        if user.status == 0:
            return {
                'status': False,
                'message': 'User has been deactivated',
                'data': None,
            }
        else:
            if user.deleted_at is not None:
                return {
                    'status': False,
                    'message': 'User has been deleted',
                    'data': None,
                }
            else:
                payload = {
                    'id': user.id,
                    'owner_id': user.owner_id,
                    'username': user.username,
                    'email': user.email,
                }
                token = auth.encode_token(user=payload)
                data = {
                    'access_token': token,
                    'id': user.id,
                    'owner_id': user.owner_id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'created_at': user.created_at,
                }
                return {
                    'status': True,
                    'message': 'Login Success',
                    'data': data,
                }

def get_loggedin_user(db: Session, user_id: str=None):
    user = get_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        data = {
            'id': user.id,
            'owner_id': user.owner_id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at,
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data,
        }
    
def update_user_details(db: Session, user_id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_user(db=db, id=user_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def update_user_password(db: Session, user_id: int=0, password: str=None, password_confirmation: str=None, old_password: str = None):
    user_info = get_user_by_id(db=db, id=user_id)
    if user_info is None:
        return {
            'status': False,
            'message': 'Not found'
        }
    else:
        if password != password_confirmation:
            return {
                'status': False,
                'message': 'Password not equal with confirm password',
            }
        else:
            if auth.verify_password(plain_password=old_password, hashed_password=user_info.password) == True:
                password = auth.get_password_hash(password=password)
                da = {
                    'password': password
                }
                update_user(db=db, id=user_id, values=da)
                return {
                    'status': True,
                    'message': 'Success'
                }
            else:
                return {
                    'status': False,
                    'message': 'Old Password Incorrect'
                }

def update_user_biometric_id(db: Session, user_id: int=0, signature: str=None):
    da = {
        'biometric_id': signature
    }
    update_user(db=db, id=user_id, values=da)
    return {
        'status': True,
        'message': 'Success'
    }