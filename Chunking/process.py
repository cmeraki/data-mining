import argparse
import logging
from utils import *

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main(subtitle_input, audio_input, subtitle_output, audio_output):
    logging.info("Starting processing")

    # Extracting the timestamps and the chunks
    if not os.path.exists(audio_output):
        os.makedirs(audio_output)
        logging.info(f"Created audio output directory: {audio_output}")

    if not os.path.exists(subtitle_output):
        os.makedirs(subtitle_output)
        logging.info(f"Created subtitle output directory: {subtitle_output}")
    
    for filename in os.listdir(subtitle_input):
        logging.info(f"Processing file: {filename}")
        timestamps = extract_timestamps_from_vtt(os.path.join(subtitle_input, filename))
        arr = timestamps
        combined_timestamps = combine_timestamps(arr)
        fname, fe = os.path.splitext(filename)
        fname = fname.replace('.en','')
        output_folder = fname
        fname = fname + '.wav'
        ts = {
            os.path.join(audio_input, fname): combined_timestamps
        }
        chunk_audio_files(timestamps=ts, output_folder=os.path.join(audio_output, output_folder))
        logging.info(f"Chunked audio files for {fname}")

        # Splitting the VTT files
        splits = []
        time_format = []
        for k in combined_timestamps:
            start_format = milliseconds_to_time_format(k[0])
            end_format = milliseconds_to_time_format(k[1])
            time_format.append((start_format, end_format))
        for i in time_format:
            splits.append((parse_vtt_time(i[0]), parse_vtt_time(i[1])))
        process_vtt_file(file_path=os.path.join(subtitle_input, filename), splits=splits, output_folder=f'{subtitle_output}/{output_folder}_split')
        logging.info(f"Processed VTT file: {filename}")

    # Text extraction from VTT files and storing it into a text file
    subtitles_text_dir = os.path.join(subtitle_output, "subtitles_text")
    if not os.path.exists(subtitles_text_dir):
        os.makedirs(subtitles_text_dir)
        logging.info(f"Created subtitles text directory: {subtitles_text_dir}")

    for item in os.listdir(subtitle_output):
        for filename in os.listdir(os.path.join(subtitle_output, item)):
            i = 1
            lines = extract_specific_lines(os.path.join(subtitle_output, item, filename))
            if '<' in lines or '>' in lines:
                for line in lines:
                    text = extract_text_from_vtt_line(line)
                    subtitle_text_folder = os.path.join(subtitles_text_dir, f"subtitles{i}")
                    if not os.path.exists(subtitle_text_folder):
                        os.makedirs(subtitle_text_folder)
                    with open(os.path.join(subtitle_text_folder, filename.replace('.en.vtt', '.txt')), 'a') as f:
                        f.write(text + '\n')
            i += 1
        logging.info(f"Extracted text from VTT files in {item}")

    logging.info("Processing completed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process subtitles and audio files.")
    parser.add_argument("--subtitle_input", required=True, help="Input directory for subtitle files")
    parser.add_argument("--audio_input", required=True, help="Input directory for audio files")
    parser.add_argument("--subtitle_output", required=True, help="Output directory for processed subtitle files")
    parser.add_argument("--audio_output", required=True, help="Output directory for processed audio files")
    parser.add_argument("--log_file", default="processing.log", help="Log file path")
    
    args = parser.parse_args()

    setup_logging(args.log_file)
    
    try:
        main(args.subtitle_input, args.audio_input, args.subtitle_output, args.audio_output)
    except Exception as e:
        logging.exception("An error occurred during processing")
