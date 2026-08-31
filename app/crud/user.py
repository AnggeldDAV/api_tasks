from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User
from core.security import hash_password


def create_user(db:Session, user:UserCreate) -> User:
    db_user= User(
        name = user.name,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def search_user_by_name(db:Session,username:str):
    user = db.query(User).filter(User.name==username).first()
    return user
    
def search_user(db:Session,user_id:int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    return user

def search_users(db:Session):
    return db.query(User).all()

def update_user(db:Session,user:User,data:UserCreate):
    user.name = data.name
    user.hashed_password = hash_password(data.password)
    db.commit()
    db.refresh(user)
    return user

def remove_user(db:Session,user:User):
    db.delete(user)
    db.commit()
    return user
    
