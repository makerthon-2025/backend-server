from fastapi import APIRouter, Request
from src.controller import auth_controller

router = APIRouter()

@router.get("/auth/login")
def login():
    return auth_controller.login_controller()

@router.get('/auth/google/callback')
def google_callback(req: Request):
    return auth_controller.google_callback_controller(req)

