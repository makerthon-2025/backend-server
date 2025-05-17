label_data = ['clear_history', 'find_api', 'find_history', 'log_in', 'log_out']
import torch
from transformers import AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

tokenizer = AutoTokenizer.from_pretrained("./resources/final_model")
model = AutoModelForSequenceClassification.from_pretrained("./resources/final_model")

def api_classification(text):
    # Tokenize văn bản
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Dự đoán với mô hình
    with torch.no_grad():
        outputs = model(**inputs)

    # Lấy kết quả dự đoán (logits)
    logits = outputs.logits

    # Lấy nhãn dự đoán (với argmax)
    predicted_label = logits.argmax(dim=-1).item()

    return label_data[predicted_label]
