import os
import argparse
from jsonutils import *

def process_vtt_files(dir, json_path):
    for filename in os.listdir(dir):
        if filename.endswith(".vtt"):
            file_path = os.path.join(dir, filename)
            clean_text = clean_text_from_file(file_path)
            cleaned_text_with_separators, _ = remove_timestamps_and_directives(clean_text, file_path)
            json_creation(cleaned_text_with_separators, json_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process VTT files and create JSON.")
    parser.add_argument('dir', type=str, help="Directory containing VTT files")
    parser.add_argument('json_path', type=str, help="Path for the output JSON file")
    
    args = parser.parse_args()
    process_vtt_files(args.dir, args.json_path)
