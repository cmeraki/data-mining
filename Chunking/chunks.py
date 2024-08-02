import os
import re
import argparse
from pydub import AudioSegment

def parse_vtt(vtt_content):
    captions = []
    pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)(?=\n\n|\Z)'
    matches = re.findall(pattern, vtt_content, re.DOTALL)
    
    for start, end, text in matches:
        captions.append({
            'start': start,
            'end': end,
            'text': text.strip()
        })
    
    return captions

def time_to_milliseconds(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.split('.')
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)

def process_files(subtitle_dir, audio_dir, output_base_dir):
    for subtitle_file in os.listdir(subtitle_dir):
        if subtitle_file.endswith('.vtt'):
            base_name = os.path.splitext(subtitle_file)[0]
            audio_file = os.path.join(audio_dir, f"{base_name}.mp3")
            
            if not os.path.exists(audio_file):
                print(f"Audio file not found for {subtitle_file}. Skipping.")
                continue
            
            output_dir = os.path.join(output_base_dir, base_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # Process subtitle file
            with open(os.path.join(subtitle_dir, subtitle_file), 'r', encoding='utf-8') as file:
                vtt_content = file.read()
            
            captions = parse_vtt(vtt_content)
            
            # Copy original subtitle file to output directory
            with open(os.path.join(output_dir, subtitle_file), 'w', encoding='utf-8') as file:
                file.write(vtt_content)
            
            # Load audio file
            audio = AudioSegment.from_file(audio_file, format="mp3")
            
            for i, caption in enumerate(captions):
                # Create text file for each caption
                text_filename = f'chunk_{i+1:04d}.txt'
                with open(os.path.join(output_dir, text_filename), 'w', encoding='utf-8') as file:
                    file.write(f"Start: {caption['start']}\n")
                    file.write(f"End: {caption['end']}\n")
                    file.write(f"Text: {caption['text']}\n")
                
                # Extract audio segment
                start_ms = time_to_milliseconds(caption['start'])
                end_ms = time_to_milliseconds(caption['end'])
                audio_segment = audio[start_ms:end_ms]
                
                # Export audio segment
                audio_filename = f'chunk_{i+1:04d}.mp3'
                audio_segment.export(os.path.join(output_dir, audio_filename), format="mp3")
            
            print(f"Processed {subtitle_file}")

def main():
    parser = argparse.ArgumentParser(description='Process subtitle and audio files.')
    parser.add_argument('subtitle_dir', help='Directory containing subtitle files')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('output_dir', help='Directory for output')
    
    args = parser.parse_args()
    
    process_files(args.subtitle_dir, args.audio_dir, args.output_dir)

if __name__ == "__main__":
    main()
