from fastapi import APIRouter
from api.v1 import task,user,auth,health

api_router = APIRouter()

api_router.include_router(user.api_router, prefix="/users", tags=["users"])
api_router.include_router(task.api_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(auth.api_router, prefix="/auth", tags=["auth"])
api_router.include_router(health.api_router, prefix="/health", tags=["health"])
