from fastapi import APIRouter, Request
from src.repository import milvus_repository
import json
import requests

router = APIRouter()

case = {
    'action': 123,
    'news_query': 321
}

async def send_message_action(email: str, req: Request, body: dict):
    type = body['type']
    news_name = body['news_name']

    

async def send_message(req: Request):
    # email = req.state.email
    body = await req.json()

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
    scripts = f"[rag respond]= {rag_data} \n [system]: trả lời khách quan cấm thảo mai, cấm nói từ ạ, dạ,... bạn là chat bot gợi ý tin tức cho hệ thống, sau khi user hỏi qua [user prompt], dựa vào thông tin từ [rag respond],hãy dùng dữ liệu từ [rag respond] và dự vào các thông sốm trả về kết quả (lấy văn bản thôi lấy content, đừng lấy link, đừng lặp lại tiêu đề cố gắng nói chi tiết nội dung bài báo) cho user, câu trả lời văn bản tiếng việt! Không quá 250 ký tự. Cố gắng trả lời nhiệt tình như một nhân viên tư vấn. Không kí tự đặc biệt như \n **!!!!. Hôm nay là ngày {datetime.today().strftime('%Y-%m-%d')}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": scripts}
                ]
            }
        ]
    }

    response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}", json=body)

    return response.json()['candidates'][0]['content']['parts'][0]['text']