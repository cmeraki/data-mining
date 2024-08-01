import re
import json
import logging
import argparse
from collections import OrderedDict
from transutils import replace_words

# Configure logging to write to a file
logging.basicConfig(
    filename='trans.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_text(input_text, current_content, current_custom_id):
    pattern = r'.*<\d{2}:\d{2}:\d{2}\.\d{3}><c>.*?</c>.*'
    cleaned_text = re.sub(pattern, '', input_text, flags=re.MULTILINE).strip()
    lines = cleaned_text.splitlines()
    unique_lines = list(OrderedDict.fromkeys(lines))
    cleaned_text_no_duplicates = "\n".join(unique_lines)

    input_text = cleaned_text_no_duplicates
    pattern = r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?[\r\n]+|<.*?>'
    text_only = re.sub(pattern, '', input_text).strip()
    lines = text_only.splitlines()
    non_empty_lines = [line.strip() + ':' for line in lines if line.strip()]
    cleaned_text_with_separators = "\n".join(non_empty_lines)

    lines_list = cleaned_text_with_separators.split(':')
    lines_list = [element.replace('\n', '') for element in lines_list]

    translines = current_content.split(':')
    mapping = dict(zip(lines_list, translines))
    output_text = replace_words(input_text=input_text, mapping_dict=mapping)

    trans_path = current_custom_id + '.vtt'
    trans_path = trans_path.replace('subtitles', 'subtitles_trans')
    
    # Write to file and log the operation
    with open(f'{trans_path}', 'w', encoding='utf-8') as output_file:
        output_file.write(output_text)
    
    logging.info(f'Generated VTT file: {trans_path}')

def process_jsonl_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            item = json.loads(line)
            current_custom_id = item.get('custom_id')
            current_content = item.get('response', {}).get('body', {}).get('choices', [{}])[0].get('message', {}).get('content')

            input_text_path = current_custom_id + '.hi.vtt'
            with open(input_text_path, 'r', encoding='utf-8') as input_file:
                input_text = input_file.read()

            process_text(input_text, current_content, current_custom_id)

def main():
    parser = argparse.ArgumentParser(description='Process a JSONL file to generate VTT files.')
    parser.add_argument('jsonl_file_path', type=str, help='Path to the input JSONL file')
    args = parser.parse_args()
    
    process_jsonl_file(args.jsonl_file_path)

if __name__ == '__main__':
    main()
