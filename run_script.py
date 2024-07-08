import subprocess
import json
from pytube import YouTube
from pydub import AudioSegment
import os
import yt_dlp
from pydub import AudioSegment
import re
from datetime import datetime, timedelta

#Obataining the URLS for a Youtube Channel
def get_youtube_urls(channel_url):
    command = ['yt-dlp', '-j', '--flat-playlist', channel_url]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        return []
    
    video_urls = []
    for line in result.stdout.strip().split('\n'):
        video_data = json.loads(line)
        video_url = f"https://www.youtube.com/watch?v={video_data['id']}"
        video_urls.append(video_url)
    
    return video_urls

channel_url = 'https://www.youtube.com/@NotJustBikes/videos'
video_urls = get_youtube_urls(channel_url)

#Downloading the audio from the Youtube Channel into MP3 Format
def download_audio_from_youtube(video_url, output_path):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(only_audio=True).first()
        download_path = video_stream.download(output_path=output_path)

        audio = AudioSegment.from_file(download_path)
        mp3_path = os.path.splitext(download_path)[0] + '.mp3'
        audio.export(mp3_path, format="mp3")

        os.remove(download_path)

        print(f"Downloaded and converted audio saved at: {mp3_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

i = 0 
for video_url in video_urls:
    output_path = f"test{i}.mp3"
    download_audio_from_youtube(video_url, output_path)
    i += 1
count = i

#Obtaining the VTT Subtitle files for the Youtube Videos
def extract_transcript(video_url):
    ydl_opts = {
        'skip_download': True, 
        'writeautomaticsub': True, 
        'subtitleslangs': ['en','en-CA'],  
        'subtitlesformat': 'vtt',  
        'outtmpl': 'subtitles/%(id)s.%(ext)s',  
        'quiet': True, 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

for video_url in video_urls:
    extract_transcript(video_url)

#Getting the timestamp splits, Splitting VTT functions
def parse_vtt_time(time_str):
    """Convert a VTT time string to a timedelta."""
    hours, minutes, seconds,milliseconds = map(float, re.split('[:.]', time_str))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def split_vtt_by_timestamps(vtt_content, splits):
    """Split VTT content based on given start and end timestamps."""
    lines = vtt_content.split('\n')
    split_contents = [[] for _ in splits]
    current_split_index = 0
    start_time = None

    for line in lines:
        if '-->' in line:
            start_time_str, end_time_str = re.findall(r'\d{2}:\d{2}:\d{2}\.\d{3}', line)
            start_time = parse_vtt_time(start_time_str)
            # Check if the current caption falls within the current split range
            if start_time >= splits[current_split_index][1]:
                current_split_index += 1
            if current_split_index >= len(splits):
                break  # All splits are processed
        if start_time is not None and current_split_index < len(splits) and start_time >= splits[current_split_index][0]:
            split_contents[current_split_index].append(line)

    return split_contents

def write_splits_to_files(split_contents, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, content in enumerate(split_contents):
        file_path = os.path.join(output_folder, f'split_{i+1}.vtt')
        with open(file_path, 'w') as f:
            f.write('WEBVTT\nKind: captions\nLanguage: en\n\n')
            f.write('\n'.join(content))

def process_vtt_file(file_path, splits, output_folder):
    with open(file_path, 'r') as file:
        vtt_content = file.read()
    split_contents = split_vtt_by_timestamps(vtt_content, splits)
    write_splits_to_files(split_contents, output_folder)

def chunk_audio_files(timestamps, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file, chunks in timestamps.items():
        audio = AudioSegment.from_file(file)
        for i, (start, end) in enumerate(chunks):
            chunk = audio[start:end]
            chunk_filename = os.path.join(output_folder, f"{os.path.basename(file).rsplit('.', 1)[0]}_chunk{i}.mp3")
            chunk.export(chunk_filename, format="mp3")
            print(f"Exported {chunk_filename}")

def extract_timestamps_from_vtt(filename):
    timestamp_regex = r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})'
    
    timestamps = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = re.findall(timestamp_regex, content)
        for start, end in matches:
            start_ms = int(timedelta(hours=int(start[0:2]), minutes=int(start[3:5]), seconds=int(start[6:8]), milliseconds=int(start[9:])).total_seconds() * 1000)
            end_ms = int(timedelta(hours=int(end[0:2]), minutes=int(end[3:5]), seconds=int(end[6:8]), milliseconds=int(end[9:])).total_seconds() * 1000)
            timestamps.append((start_ms, end_ms))
    return timestamps

def combine_timestamps(timestamps):
    combined_timestamps = []
    i = 0
    while i < len(timestamps) - 6:
        combined_timestamps.append((timestamps[i][0], timestamps[i + 6][1]))
        i += 7
    while i < len(timestamps):
        combined_timestamps.append(timestamps[i])
        i += 1
    return combined_timestamps

def milliseconds_to_time_format(milliseconds):
    # Calculate hours, minutes, seconds and milliseconds
    hours = milliseconds // (1000 * 60 * 60)
    milliseconds_remaining = milliseconds % (1000 * 60 * 60)
    minutes = milliseconds_remaining // (1000 * 60)
    milliseconds_remaining %= (1000 * 60)
    seconds = milliseconds_remaining // 1000
    milliseconds_remaining %= 1000
    
    # Format the time string
    time_format = f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds_remaining:03}"
    
    return time_format

#Chunking the audio files and splitting the VTT files
j=0
for filename in os.listdir('subtitles'):
    timestamps = extract_timestamps_from_vtt(os.path.join('subtitles',filename))
    arr = timestamps
    combined_timestamps = combine_timestamps(arr)
    #print(timestamps)
    for i in range(0,count):
        timestamps = {
            f'test{i}.mp3/test{i}.mp3': combined_timestamps}
        output_folder = f'final_outputs/output{i}'
        chunk_audio_files(timestamps, output_folder)
    # Splitting the VTT files
    splits = []
    time_format = []
    for k in combined_timestamps:
        start_format = milliseconds_to_time_format(i[0])
        end_format = milliseconds_to_time_format(i[1])
        time_format.append((start_format, end_format))
    for i in time_format:
        splits.append((parse_vtt_time(i[0]), parse_vtt_time(i[1])))
    process_vtt_file(os.path.join('subtitles',filename), splits,f'subtitles_split{j}')
    j = j+1

#Text Extraction from the VTT files and storing it into a text file
def extract_specific_lines(vtt_filename):
    pattern = re.compile(r'.*<\d{2}:\d{2}:\d{2}\.\d{3}><c>.*</c>.*')
    
    with open(vtt_filename, 'r', encoding='utf-8') as file:
        for line in file:
            if re.match(pattern, line):
                print(line.strip())

def extract_text_from_vtt_line(line):
    text_only = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>|<c>|</c>', '', line)
    return text_only

matching_directories = []
for item in os.listdir('.'):
    if os.path.isdir(item) and 'subtitles_split' in item:
        matching_directories.append(item)

for filedir in matching_directories:
    for file in filedir:
        extracted_text = extract_specific_lines(os.path.join(filedir,file))
        text_only = extract_text_from_vtt_line(extracted_text)
        file_path = f'{filedir}/{file}.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_only)
