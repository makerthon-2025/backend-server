from fastapi import APIRouter, Request
from src.controller import message_controller

router = APIRouter()

@router.post("/api/send_message")
async def send_message(req: Request):
    return await message_controller.send_message(req)

