from typing import Dict
import jwt 
from fastapi import HTTPException, Security, Header, Request, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext 
from datetime import datetime, timedelta 
import dateparser
import time
from settings.config import load_env_config
from database.model import create_auth_token, get_last_login_auth_token_by_user_id, ping_auth_token, get_last_login_auth_token_by_admin_id, get_user_by_id
from database.db import session
import hashlib

config = load_env_config()


def get_next_few_minutes(minutes: int=0):
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=minutes)
    return future_time.strftime("%Y-%m-%d %H:%M:%S")

def check_if_time_as_pass_now(time_str: str = None):
    date_parsed = dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
    time_tz = time.mktime(date_parsed.timetuple())
    time_tz = int(time_tz)
    current_tz = int(time.time())
    if current_tz >= time_tz:
        return True
    else:
        return False

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = config['secret_key']
    db = session

    def get_password_hash(self, password: str = None):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str=None, hashed_password: str=None):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user: Dict={}):
        payload = {
            'exp': datetime.now() + timedelta(days=365, minutes=5),
            'iat': datetime.now(),
            'sub': user
        }
        expired_at = (datetime.now() + timedelta(days=365, minutes=5)).strftime("%Y/%m/%d %H:%M:%S")
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        user_id = user['id']
        create_auth_token(db=self.db, user_id=user_id, token=token, status=1, expired_at=expired_at)
        return token

    def decode_token(self, token: str = None):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            user_id = payload['sub']['id']
            admin = get_user_by_id(db=self.db, id=user_id)
            if admin is None:
                raise HTTPException(status_code=401, detail='User does not exist')
            else:
                auth_token = get_last_login_auth_token_by_user_id(db=self.db, user_id=user_id)
                if auth_token is None:
                    raise HTTPException(status_code=401, detail='Empty Auth Token')
                else:
                    if auth_token.token != token:
                        raise HTTPException(status_code=401, detail='Invalid Auth Token')
                    else:
                        if auth_token.status == 0:
                            raise HTTPException(status_code=401, detail='Token Expired')
                        else:
                            deleted_at = admin.deleted_at
                            if deleted_at is not None:
                                raise HTTPException(status_code=401, detail='Admin is deleted')
                            else:
                                ping_auth_token(db=self.db, id=auth_token.id)
                                return payload['sub']
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    # def auth_admin_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
    #     user = self.decode_token(auth.credentials)
    #     return user
    
    def auth_user_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        user = self.decode_token(auth.credentials)
        return user
