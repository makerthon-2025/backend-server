import random
from fastapi import APIRouter, Request
from src.repository import user_repository
from src.repository import milvus_repository, news_repository
from src.helper.api_classification_helper import api_classification
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
    "Chính trị",
    "Xã hội",
    "An sinh",
    "Xã hội",
    "Công nghệ",
    "Tổ chức bộ máy"
]

async def top_article_action(type: str):
    # Giả sử get_top_n_by_count(limit) là async và trả về danh sách bài báo
    data = news_repository.get_top_n_by_count(type, 4)
    # suggest_news = await news_repository.get_top_n_by_count(limit=2)
    result = {
        'data': data
    }

    return result

async def send_message_action(email: str, req: Request, body):
    news_name = body['news_name']
    related_topic = body['type']

    user = user_repository.get_collection_by_email(email)
    news = news_repository.get_collection_by_name(news_name)

    if news is None:
        news_repository.insert_collection({
            'name': news_name,
            'type': related_topic,
            'count': 1,
            'created_at': datetime.now()
        })
    else:
        news_repository.update_collection({
            'name': news_name,
            'type': related_topic,
            'count': news['count'] + 1,
        })

    if user is None: 
        user_repository.insert_collection({
            'email': email,
            'related_topic': {
                related_topic: 1
            }
        })

    else:
        if related_topic not in user['related_topic']:
            user['related_topic'][related_topic] = 1
        else:
            user['related_topic'][related_topic] += 1

        sorted_tuple_relatedtopic = __sort_dict(user['related_topic'])

        user['related_topic'] = {}

        for item in sorted_tuple_relatedtopic:
            user['related_topic'][item[0]] = item[1]
        
        user_repository.update_collection(user)

    return {
        'msg': "success",
    }


async def send_message(req: Request):
    # email = req.state.email
    body = await req.json()

    response = json.loads(milvus_repository.search_data(body['prompt']))

    suggest_news = __handle_response(response, "khang.tran@gmail.com", api_classification(body['prompt']))

    data = {
        'data': response[:4],
        'suggest_news': suggest_news[:3]
    }

    print(body)
    print(data)

    str_data = json.dumps(data, ensure_ascii=False)

    res = __gemini_call(body['prompt'], str_data)
    data['prompt'] = res

    return data

# ==================================================================
# ===================== PRIVATE ===================================
import os
from datetime import datetime

def __handle_response(response, email, related_topic):
    user = user_repository.get_collection_by_email(email)

    if user is None: 
        user = {
            'email': email,
            'related_topic': {
                related_topic: 1
            }
        }

        user_repository.insert_collection(user)
    
    related_topic = user['related_topic']

    max_size = 3

    suggest_news = []

    for item in response[4:]:
        if max_size == 0:
            break

        if item['data']['type'] in related_topic:
            suggest_news.append(item)
            max_size -= 1
        else:
            print(f"not in related topic: {item['data']['type']}")

    return suggest_news

def __sort_dict(dict):
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)

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