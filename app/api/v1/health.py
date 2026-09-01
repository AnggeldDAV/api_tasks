from fastapi import APIRouter

api_router = APIRouter()
@api_router.get("/")
def health():
    return {"status": "ok"}