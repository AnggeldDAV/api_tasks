from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import UserLogin
from schemas.token import Token
from deps.deps import get_db
from core.security import verify_password, signJWT
from models.user import User

api_router = APIRouter()

@api_router.post("/login", response_model=Token)
def login(login_user:UserLogin,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.name == login_user.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    verify_pass = verify_password(login_user.password,user.hashed_password)
    if not verify_pass:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = signJWT(user.id)
    return {"access_token":token, "token_type": "bearer"}
