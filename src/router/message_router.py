from fastapi import APIRouter, Request
from src.controller import message_controller

router = APIRouter()

@router.post("/api/send_message")
async def send_message(req: Request):
    return await message_controller.send_message(req)

@router.post("/api/top_article/{type_value}")
async def send_message(type_value: str):
    return await message_controller.top_article_action(type_value)

@router.post("/api/log_type/{email}")
async def send_message_action(email: str, req: Request):
    body = await req.json()

    return await message_controller.send_message_action(email, req, body)
