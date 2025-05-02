import os
import json

def save_file(file_path, content):    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception:
        return None