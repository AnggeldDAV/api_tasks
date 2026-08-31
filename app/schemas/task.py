from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    state: str
    priority : bool
    date : datetime
    
class TaskResponse(BaseModel):
    id : int
    title: str
    description: str
    state: str
    priority : bool
    date : datetime
    user_id : int
    
    class Config:
        orm_mode = True