import argparse
import json
import os
import logging
from pydub import AudioSegment
import webvtt

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def parse_arguments():
    parser = argparse.ArgumentParser(description="Split audio files based on VTT subtitles and generate JSONL.")
    parser.add_argument("--audio_dir", required=True, help="Directory containing audio files")
    parser.add_argument("--subtitle_dir", required=True, help="Directory containing VTT subtitle files")
    parser.add_argument("--output_dir", required=True, help="Directory to save split audio files")
    parser.add_argument("--jsonl_output", required=True, help="Path to save the output JSONL file")
    parser.add_argument("--log_file", default="process.log", help="Path to save the log file")
    parser.add_argument("--language", default="en", choices=["en", "hi"], help="Language of the audio/subtitles")
    parser.add_argument("--subtitles", default="uploaded", choices=["uploaded", "auto"], help="Source of subtitles")
    parser.add_argument("--category", default="conversation", help="Category of the audio content")
    parser.add_argument("--source", default="unknown", help="Source of the video/audio")
    parser.add_argument("--url", default="", help="URL of the video if available")
    return parser.parse_args()

def split_audio(audio_path, start_time, end_time, output_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        chunk = audio[start_time:end_time]
        chunk.export(output_path, format="wav")
        logging.info(f"Successfully split audio: {output_path}")
    except Exception as e:
        logging.error(f"Error splitting audio {audio_path}: {str(e)}")
        raise

def time_to_milliseconds(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.split('.')
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)

def process_files(args):
    jsonl_data = []
    chunk_id = 1

    for subtitle_file in os.listdir(args.subtitle_dir):
        if not subtitle_file.endswith('.vtt'):
            continue

        logging.info(f"Processing subtitle file: {subtitle_file}")

        # Remove '.hi.vtt' and append '.wav' for audio file name
        base_name = subtitle_file.rsplit('.', 2)[0]
        audio_file = f"{base_name}.wav"
        audio_path = os.path.join(args.audio_dir, audio_file)

        if not os.path.exists(audio_path):
            logging.warning(f"Audio file not found for {subtitle_file}")
            continue

        try:
            vtt = webvtt.read(os.path.join(args.subtitle_dir, subtitle_file))
        except Exception as e:
            logging.error(f"Error reading VTT file {subtitle_file}: {str(e)}")
            continue

        for caption in vtt:
            start_time = time_to_milliseconds(caption.start)
            end_time = time_to_milliseconds(caption.end)
            text = caption.text.replace('\n', ' ')

            output_filename = f"{base_name}_{start_time}_{end_time}.wav"
            output_path = os.path.join(args.output_dir, output_filename)

            try:
                split_audio(audio_path, start_time, end_time, output_path)
            except Exception:
                logging.error(f"Skipping chunk due to split_audio error: {output_filename}")
                continue

            jsonl_entry = {
                "chunk_id": f"{chunk_id:06d}",
                "text": text,
                "audio": os.path.relpath(output_path, args.output_dir),
                "begin_time": start_time,
                "end_time": end_time,
                "audio_id": base_name,
                "url": args.url,
                "source": args.source,
                "language": args.language,
                "subtitles": args.subtitles,
                "category": args.category
            }

            jsonl_data.append(jsonl_entry)
            chunk_id += 1

        logging.info(f"Finished processing {subtitle_file}")

    return jsonl_data

def main():
    args = parse_arguments()
    setup_logging(args.log_file)
    
    logging.info("Starting audio splitting and JSONL generation process")
    
    os.makedirs(args.output_dir, exist_ok=True)
    logging.info(f"Output directory created/verified: {args.output_dir}")

    try:
        jsonl_data = process_files(args)
        logging.info(f"Processed {len(jsonl_data)} chunks in total")

        with open(args.jsonl_output, 'w', encoding='utf-8') as f:
            for entry in jsonl_data:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')
        logging.info(f"JSONL output written to: {args.jsonl_output}")

    except Exception as e:
        logging.error(f"An error occurred during processing: {str(e)}")
    
    logging.info("Process completed")

if __name__ == "__main__":
    main()
