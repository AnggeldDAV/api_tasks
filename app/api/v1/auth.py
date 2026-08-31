from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.auth import UserLogin
from schemas.token import Token
from deps.deps import get_db
from core.security import verify_password, signJWT
from models.user import User

api_router = APIRouter()

@api_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.name == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    verify_pass = verify_password(form_data.password,user.hashed_password)
    if not verify_pass:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = signJWT(user.id)
    return {"access_token":token, "token_type": "bearer"}
