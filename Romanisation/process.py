import os
import argparse
import logging
from transutils import *

def setup_logging(log_file="script.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def process_subtitle_file(file_path):
    logging.info(f"Starting to process file: {file_path}")
    
    try:
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
        
        logging.info(f"Finished processing file: {file_path}")
        return output_text
    
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return None

def process_directory(directory):
    output_directory = f"{directory}_trans"
    os.makedirs(output_directory, exist_ok=True)
    logging.info(f"Created output directory: {output_directory}")
    
    for filename in os.listdir(directory):
        if filename.endswith(".vtt"):
            file_path = os.path.join(directory, filename)
            output_text = process_subtitle_file(file_path)
            if output_text:
                output_file_path = os.path.join(output_directory, filename.replace('.vtt', '_final.vtt'))
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(output_text)
                logging.info(f"Processed {file_path} -> {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a directory of subtitle files.")
    parser.add_argument("directory", type=str, help="Directory containing subtitle files")
    args = parser.parse_args()

    setup_logging()
    process_directory(args.directory)
