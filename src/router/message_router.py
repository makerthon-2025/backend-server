from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def get_user():
    return {"user_id": user, "name": "John Doe"}

