import os
import argparse
from transutils import *

def process_subtitle_file(file_path):
    # Text extraction
    clean_text = clean_text_from_file(file_path)
    text_only = remove_timestamps_and_directives(clean_text)
    lines_list = text_only.split(':')
    lines_list = [element.replace('\n', '') for element in lines_list]

    # Transliteration
    source_language = "Hindi"
    target_script = "Roman"
    transliterated_text = transliterate_text(text_only, source_language, target_script)

    translines = transliterated_text.split(':')
    translines = [element.replace('\n', '') for element in translines]

    # Mapping and replacement
    mapping = dict(zip(lines_list, translines))
    input_text = clean_text
    output_text = replace_words(input_text, mapping)
    
    return output_text

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".vtt"):
            file_path = os.path.join(directory, filename)
            output_text = process_subtitle_file(file_path)
            output_file_path = os.path.join(directory, filename.replace('.vtt', '_final.vtt'))
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(output_text)
            print(f"Processed {file_path} -> {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a directory of subtitle files.")
    parser.add_argument("directory", type=str, help="Directory containing subtitle files")
    args = parser.parse_args()

    process_directory(args.directory)
