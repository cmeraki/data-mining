import re
from collections import OrderedDict
import openai
import json
import os

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except JSONDecodeError:
                print(f"Error parsing line in {file_path}: {line}")
    return data

def json_creation(input_jsonl_path,output_json_path):
    jsonl_data = load_jsonl(input_jsonl_path)
    for item in jsonl_data:
        input_text = item['text']
        new_request = {
            "custom_id": item['chunk_id'],
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that performs transliteration. Just display the words and do not give any other message."
                    },
                    {
                        "role": "user",
                        "content": f"Transliterate the following Hindi Text into English Text:\n{input_text}\nTransliteration"
                    }
                ],
            }
        }
    
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                pass 
    
        # Append the new request as a new line in the JSON file
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(json.dumps(new_request, ensure_ascii=False) + '\n')