from pymilvus import MilvusClient
import numpy as np
import os
import asyncio
from pymilvus import Collection, connections
from src.helper import embeding_helper
import json

connections.connect(
    alias="default",
    uri=f"http://{os.getenv('MILVUS_HOST')}:{os.getenv('MILVUS_PORT')}",
)

collection = Collection("news")

def search_data(text):
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

    result = collection.search(
        data=[embeding_helper.encode_text(text)], 
        anns_field="vector", 
        param=search_params,  
        limit=4,  
        output_fields=['name', 'link', 'content', 'type'],
        consistency_level="Strong" 
    )

    def hit_to_dict(hit):
        return {
            'id': hit.id,
            'percent': round(hit['distance']*100),
            'data': {
                'name': hit.entity.get('name'),
                'link': hit.entity.get('link'),
                'content': hit.entity.get('content'),
                'type': hit.entity.get('type')
            }
        }

    result_dict = [hit_to_dict(hit) for hit in result[0]]  # result[0] là danh sách các hit trong kết quả

    # Sau đó bạn có thể serialize thành JSON
    json_data = json.dumps(result_dict, ensure_ascii=False, indent=4)
    # print(json_data)

    return json_data

if __name__ == "__main__":
    res = search_data("nghỉ lễ 30/4")

    print(res)