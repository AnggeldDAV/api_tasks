from fastapi import APIRouter,HTTPException, Depends, status
from schemas.user import UserResponse,UserCreate
from crud.user import create_user, search_user, search_users, update_user, remove_user, search_user_by_name
from deps.deps import get_db, get_current_user
from sqlalchemy.orm import Session


api_router = APIRouter()

@api_router.get("/{id}",response_model=UserResponse)
def get_user(id : int,db:Session = Depends(get_db), user= Depends(get_current_user)):
    searched_user = search_user(db,id)
    if searched_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    if user.id != searched_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized")
    return searched_user

@api_router.get("/",response_model=list[UserResponse])
def get_users(db:Session = Depends(get_db), user= Depends(get_current_user)):
    return search_users(db)
    

@api_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_user(user:UserCreate,db:Session = Depends(get_db)):
    user_exists = search_user_by_name(db,user.name)
    if user_exists:
        raise HTTPException(status_code=409, detail="User already exists")
    return create_user(db,user)


@api_router.put("/{id}",response_model=UserResponse)
def put_user(id:int,data:UserCreate,db:Session = Depends(get_db), current_user = Depends(get_current_user)):
     user = search_user(db,id)
     if not user:
         raise HTTPException(status_code=404,detail="User not found")
     if current_user.id != user.id:
         raise HTTPException(status_code=403,detail="Not Authorized")
     modified_user = update_user(db,user,data)
     return modified_user
 
@api_router.delete("/{id}")
def delete_user(id:int,db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = search_user(db,id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if current_user.id != user.id:
        raise HTTPException(status_code=403,detail="Not Authorized")
    remove_user(db,user)
    return {"message":"User removed correctly"}