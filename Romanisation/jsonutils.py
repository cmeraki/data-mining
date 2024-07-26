import re
from collections import OrderedDict
import openai
import json
import os

def clean_text_from_file(file_path):
    '''
    Function to clean text from a file by removing duplicate lines and timestamps.
    params:
        file_path: path to the file to be cleaned
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    pattern = r'.*<\d{2}:\d{2}:\d{2}\.\d{3}><c>.*?</c>.*'
    cleaned_text = re.sub(pattern, '', input_text, flags=re.MULTILINE).strip()
    lines = cleaned_text.splitlines()
    unique_lines = list(OrderedDict.fromkeys(lines))
    cleaned_text_no_duplicates = "\n".join(unique_lines)

    return cleaned_text_no_duplicates

def remove_timestamps_and_directives(input_text,file_path):
    '''
    Function to remove timestamps and formatting directives from the input text.
    params:
        input_text: the text to clean
    '''
    pattern = r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?[\r\n]+|<.*?>'
    text_only = re.sub(pattern, '', input_text).strip()
    lines = text_only.splitlines()
    non_empty_lines = [line.strip() + ':' for line in lines if line.strip()]
    cleaned_text_with_separators = "\n".join(non_empty_lines)
    
    return cleaned_text_with_separators,file_path.replace(".hi.vtt",'')

import json
import os

def json_creation(input_text, file_name):
    new_request = {
        "custom_id": f"{file_name}",
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


