import os
import re
import argparse
from datetime import datetime

def time_difference(start, end):
    fmt = '%H:%M:%S.%f'
    d1 = datetime.strptime(start, fmt)
    d2 = datetime.strptime(end, fmt)
    diff = d2 - d1
    return diff.total_seconds()

def clean_vtt_content(vtt_content):
    # Remove <c> tags and their content
    cleaned_content = re.sub(r'<c>[^<]*<\/c>', '', vtt_content)
    
    # Remove inline timestamps within the lines
    cleaned_content = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', cleaned_content)

    # Split the content into lines
    lines = cleaned_content.splitlines()
    cleaned_lines = []
    previous_text = ""
    
    for i, line in enumerate(lines):
        timestamp_match = re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line.strip())
        if timestamp_match:
            timestamps = timestamp_match.group().split(' --> ')
            start, end = timestamps[0], timestamps[1]
            if i + 1 < len(lines) and not re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', lines[i + 1].strip()):
                text = lines[i + 1].strip()
                
                # Check the duration and duplicate text
                if time_difference(start, end) >= 0.1 and text != previous_text:
                    cleaned_lines.append(f"{start} --> {end}")
                    cleaned_lines.append(text)
                    previous_text = text

    return '\n'.join(cleaned_lines)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.vtt'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            
            with open(input_file, 'r', encoding='utf-8') as file:
                vtt_content = file.read()
            
            cleaned_content = clean_vtt_content(vtt_content)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            
            print(f'Processed file: {input_file}')