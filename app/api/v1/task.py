from fastapi import APIRouter,HTTPException, Depends, status
from schemas.task import TaskCreate, TaskResponse
from crud.task import create_task, search_tasks_by_user, search_task, update_task, remove_task
from crud.user import search_user
from deps.deps import get_db, get_current_user
from sqlalchemy.orm import Session

api_router = APIRouter()


@api_router.post("/",response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_task(task:TaskCreate,db:Session = Depends(get_db),user = Depends(get_current_user)):
    user_exists = search_user(db, user.id)
    if not user_exists:
        raise HTTPException(status_code=400, detail="User not found")
    return create_task(db,task,user.id)


@api_router.get("/",response_model=list[TaskResponse])
def get_tasks(db:Session = Depends(get_db), user = Depends(get_current_user)):
    return search_tasks_by_user(db,user.id)

@api_router.get("/{id}", response_model=TaskResponse)
def get_task(id:int,db:Session = Depends(get_db), user = Depends(get_current_user)):
    task = search_task(db,id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    return task

@api_router.put("/{id}",response_model=TaskResponse)
def put_task(id:int,data:TaskCreate,db:Session = Depends(get_db),user = Depends(get_current_user)):
    task = search_task(db,id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    modified_task = update_task(db,task,data)
    return modified_task
    
@api_router.delete("/{id}")
def delete_task(id:int,db:Session = Depends(get_db),user = Depends(get_current_user)):
    task = search_task(db,id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    remove_task(db,task)
    return {"message":"Task removed correctly"}