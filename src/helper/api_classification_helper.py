import random
import torch
from transformers import AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

tokenizer = AutoTokenizer.from_pretrained("./resources/final_model")
model = AutoModelForSequenceClassification.from_pretrained("./resources/final_model")

label_data = ['AI & Internet','An ninh mạng','An sinh','Bóng đá','Bất động sản',
 'Chuyện của tôi','Chuyện nghề','Chính sách','Chính trị','Chợ online',
 'Chứng khoán','Công nghệ','Công sở','Cộng đồng','Cộng đồng xe',
 'Doanh nghiệp','Du học','Du lịch','Dự án','Gia dụng thông minh',
 'Gia đình','Giao thông','Giáo dục','Giáo dục - Nghề nghiệp','Giải trí',
 'Giới trẻ','Góc phụ huynh','Gương sáng','Hậu trường','Học tập Bác',
 'Hồ sơ vụ án','Khoa học','Khoa học & đời sống','Khuyến học','Khám phá',
 'Khỏe đẹp','Khởi nghiệp','Kinh doanh','Kinh nghiệm - Tư vấn',
 'Kiến thức giới tính','Kiều bào','Kỷ nguyên mới','Làm giàu',
 'Món ngon - Điểm đẹp','Môi trường','Mỹ thuật - Sân khấu',
 'Ngoại thần kinh - Cột sống','Nhà đất','Nhân lực mới','Nhịp sống đô thị',
 'Nóng trên mạng','Nội thất','Nội vụ','Pháp đình','Phân tích - Bình luận',
 'Pickleball','Quân sự','Sách hay','Sản phẩm & Cộng đồng','Sống khỏe',
 'Sống xanh','Sức khỏe','Tennis','Thượng lưu','Thế giới',
 'Thế giới tự nhiên','Thế giới đó đây','Thể thao','Thị trường',
 'Thị trường xe','Thời trang','Tin tức','Tiêu dùng','Tiền lương',
 'Tour hay - Khuyến mại','Tuyển sinh','Tài chính','Tình yêu','Tư vấn',
 'Tổ chức bộ máy','Ung thư','Video - Ảnh','Việc làm',
 'Võ thuật - Các môn khác','Vũ trụ','Vượt lên số phận','Xe ++','Xe điện',
 'Xã hội','Âm nhạc','Điện ảnh','Đánh giá','Đời sống']

def api_classification(text):
    # Tokenize văn bản
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Dự đoán với mô hình
        with torch.no_grad():
            outputs = model(**inputs)

        # Lấy kết quả dự đoán (logits)
        logits = outputs.logits

        # Lấy nhãn dự đoán (với argmax)
        predicted_label = logits.argmax(dim=-1).item()

        return label_data[predicted_label]
    except Exception as e:
        print("Lỗi \n\n\n")
        return label_data[random.randint(0, len(label_data) - 1)]

if __name__ == "__main__":
    res = api_classification("tôi muốn xóa lịch sử")
    print(res)
