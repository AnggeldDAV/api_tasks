import bcrypt
from .settings import get_settings
from datetime import datetime, timedelta, timezone
import jwt


def signJWT(user_id:int):
    settings = get_settings()
    payload ={
        "user_id" : user_id,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return token
    
def decodeJWT(token:str):
    settings = get_settings()
    decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
    return decoded_token
    
    
def hash_password(password:str):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode('utf-8')

def verify_password(password:str,hashed:str):
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
    