import os
import re
import argparse
from datetime import datetime
from pycaption import WebVTTReader

def time_difference(start, end):
    fmt = '%H:%M:%S.%f'
    d1 = datetime.strptime(start, fmt)
    d2 = datetime.strptime(end, fmt)
    diff = d2 - d1
    return diff.total_seconds()

def convert_vtt_to_custom_format(input_vtt, output_txt):
    with open(input_vtt, 'r', encoding='utf-8') as vtt_file:
        vtt_content = vtt_file.read()
    
    if vtt_content.count("<c>") > 0:    
        caption_set =  WebVTTReader(time_shift_milliseconds=0).read(vtt_content,lang='hi')
        #print(caption_set)
        #print(caption_set.get_languages())
        #print(caption_set.get_captions(lang='hi'))
        with open(output_txt, 'w', encoding='utf-8') as out_file:
            for caption in caption_set.get_captions(lang='hi'):
                #print(str(caption))
                caption = str(caption)
                caption = caption.replace("'","")
                parts = caption.split("\\n")
                if len(parts) == 3:
                    text = parts[0]+"\n"+parts[-1]
                    out_file.write(text+"\n")
    else:
        print("Skipping file")
        with open(output_txt, 'w', encoding='utf-8') as out_file:
            out_file.write(vtt_content)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.vtt'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            
            convert_vtt_to_custom_format(input_file,output_file)
    
            print(f'Processed file: {input_file}')