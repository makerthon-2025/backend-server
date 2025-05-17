import random
from fastapi import APIRouter, Request
from src.repository import user_repository
from src.repository import milvus_repository
import json
import requests

router = APIRouter()

case = {
    'action': 123,
    'news_query': 321
}

mockNewsName = [
    "Thủ tướng Phạm Minh Chính thăm chính thức Singapore",
    "Giá vàng tăng mạnh, vượt mốc 80 triệu đồng/lượng",
    "Việt Nam đăng cai SEA Games 32",
    "Thời tiết miền Bắc chuyển lạnh đột ngột",
    "Giá xăng dầu giảm từ 15h chiều nay",
    "Hà Nội mở rộng không gian đi bộ phố cổ",
    "Xuất khẩu nông sản đạt kỷ lục trong quý 1",
    "Việt Nam phát triển công nghệ 5G bản địa",
    "Dự báo kinh tế Việt Nam tăng trưởng 6.5%",
    "Khai trương tuyến metro Bến Thành - Suối Tiên"
]

mockData = [
    "AI & Internet",
    "An ninh mạng",
    "An sinh",
    "Bóng đá",
    "Công nghệ",
    "Công sở"
]

def __sort_dict(dict):
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)

async def send_message_action(email: str, req: Request, body: dict):
    news_name = mockNewsName[random.randint(0, len(mockNewsName) - 1)] 
    related_topic = mockData[random.randint(0, len(mockData) - 1)]

    user = user_repository.get_collection_by_email(email)

    if user is None: 
        user_repository.insert_collection({
            'email': email,
            'news_name': {
                news_name: 0
            },
            'related_topic': {
                related_topic: 0
            }
        })

    else:
        if news_name not in user['news_name']:
            user['news_name'][news_name] = 0
        else:
            user['news_name'][news_name] += 1

        if related_topic not in user['related_topic']:
            user['related_topic'][related_topic] = 0
        else:
            user['related_topic'][related_topic] += 1

        sorted_tuple_newsname = __sort_dict(user['news_name'])
        sorted_tuple_relatedtopic = __sort_dict(user['related_topic'])

        user['news_name'] = {}
        user['related_topic'] = {}

        for item in sorted_tuple_newsname:
            user['news_name'][item[0]] = item[1]

        for item in sorted_tuple_relatedtopic:
            user['related_topic'][item[0]] = item[1]
        
        user_repository.update_collection(user)

    return {
        'msg': "success",
    }

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