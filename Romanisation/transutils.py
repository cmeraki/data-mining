import re
from collections import OrderedDict
import openai

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

def remove_timestamps_and_directives(input_text):
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
    
    return cleaned_text_with_separators

def transliterate_text(input_text, source_language, target_script):
    """
    Transliterate text using OpenAI GPT-4.
    Args:
    - input_text (str): The text to transliterate.
    - source_language (str): The language of the input text.
    - target_script (str): The script to transliterate the text into.
    """
    openai.api_key = "sk-proj-VOXGggALnfng2POFaOIMT3BlbkFJnUjLveXHsIl9RUFsz4xr"
    prompt = (f"Transliterate the following {source_language} text into {target_script} script:\n\n"
              f"Text: {input_text}\n"
              f"Transliteration:")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that performs transliteration.Just display the words and do not give any other message."},
            {"role": "user", "content": prompt}
        ],

    )
    transliterated_text = response.choices[0].message['content'].strip()
    
    return transliterated_text

def replace_words(input_text, mapping_dict):
    for word1, word2 in mapping_dict.items():
        input_text = input_text.replace(word1,word2)
    return input_text
