
from core.settings import get_settings, Settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from core.security import decodeJWT
import jwt
from crud.user import search_user
from db.database import get_session_factory, create_tables
from db.database import Base

def get_db(settings:Settings = Depends(get_settings)):
    session_factory = get_session_factory(settings.DATABASE_URL)
    create_tables()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
       
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
 
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    cred_exep = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Not Authenticated",
        headers={"WWW-Authenticate":"Bearer"}
        )
    try:
        payload = decodeJWT(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise cred_exep
    except jwt.exceptions.PyJWTError:
        raise cred_exep
    user = search_user(db,user_id)
    if not user:
        raise cred_exep
    return user