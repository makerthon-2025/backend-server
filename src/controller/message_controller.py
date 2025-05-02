from fastapi import APIRouter, Request
from src.repository import milvus_repository
import json
import requests

router = APIRouter()

case = {
    'action': 123,
    'news_query': 321
}

async def send_message(req: Request):
    email = req.state.email
    body = await req.json()

    if body['type'] == 'action':
        pass
    if body['type'] == 'news_query':
        response = milvus_repository.search_data(body['prompt'])

    data = {
        'data': json.loads(response)
    }

    str_data = json.dumps(data, ensure_ascii=False)

    res = __gemini_call(body['prompt'], str_data)
    data['prompt'] = res

    return data

# ==================================================================
# ===================== PRIVATE ===================================
import os
from datetime import datetime

def __gemini_call(prompt, rag_data):
    scripts = f"[user prompt]: {prompt} \n [rag respond]: {rag_data} \n [system]: bạn là chat bot đọc báo cho hệ thống, bạn tên là mavBot, sau khi user hỏi qua [user prompt], hệ thống sẽ truy vấn RAG và hiển thị dữ liệu qua [rag respond], hãy dùng dữ liệu từ [rag respond] và dự vào các thông sốm trả về kết quả cho user, câu trả lời văn bản tiếng việt! Không quá 50 ký tự. Cố gắng trả lời nhiệt tình như một nhân viên tư vấn. Không kí tự đặc biệt!!!!. Hôm nay là ngày {datetime.today().strftime('%Y-%m-%d')}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}", json=body)

    return response.json()['candidates'][0]['content']['parts'][0]['text']