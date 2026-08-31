from sqlalchemy.orm import Session
from schemas.task import TaskCreate
from models.task import Task


def create_task(db:Session,task:TaskCreate,user_id:int) ->Task:
    db_task = Task(
        title = task.title,
        description = task.description,
        state = task.state,
        priority = task.priority,
        date = task.date,
        user_id = user_id  
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def search_tasks_by_user(db:Session,user_id:int):
    return db.query(Task).filter(Task.user_id==user_id).all()

def search_task(db:Session, task_id:int)-> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    return task

def update_task(db:Session, task:Task,data:TaskCreate):   
    for key, value in data.dict().items():
        setattr(task,key,value)
    db.commit()
    db.refresh(task)
    return task

def remove_task(db:Session,task:Task):
    db.delete(task)
    db.commit()
    return task