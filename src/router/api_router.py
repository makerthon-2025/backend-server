from fastapi import APIRouter, Request
from src.controller import api_controller

router = APIRouter()

@router.get('/api/info')
def info(req: Request):
    token = req.headers.get("Authorization")[len("Bearer "):]

    return api_controller.get_info_controller(token)