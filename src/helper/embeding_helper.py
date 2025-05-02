from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("resources/model")

def encode_text(text):
    return model.encode(text)

if __name__ == "__main__":
    print(encode_text("bro hello hello"))