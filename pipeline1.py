#The first part of the pipeline till where requests will be sent to GPT-4o for transliteration
import argparse
import os
from downloadutils import get_youtube_urls, download_youtube_audios_and_transcripts
from compressutils import compress_dir
from subcleanup import process_directory
from chunkingutils import process_files, setup_logging
from requestutils import json_creation
from batch import OpenAIBatchProcessor

def main(channel_url, audio_output_folder, subtitle_output_folder):
    #Get the list of youtube videos for a particular channel
    video_urls = get_youtube_urls(channel_url)  
    #Download the audio and correspoding subtitle for this channel. Modify the language where necessary by changing in the downloadutils.py file
    #audio_output_folder = ChannelName/audio_files
    #subtitle_output_folder = ChannelName/subtitles
    download_youtube_audios_and_transcripts(audio_output_folder, subtitle_output_folder, video_urls)
    #Compressing the audio files
    #audio_compressed_folder = ChannelName/audio_files_compressed
    audio_compressed_folder = audio_output_folder.replace("audio_files","audio_files_commpressed")
    os.makedirs(audio_compressed_folder,exist_ok=True)
    compress_dir(audio_output_folder,audio_compressed_folder)
    os.remove(audio_output_folder)
    #Cleaning the subtitle files
    #subtitle_clean_folder = ChannelName/subtitles_clean
    subtitle_cleanup_folder = subtitle_output_folder("subtitles","subtitles_clean")
    os.makedirs(subtitle_cleanup_folder,exist_ok=True)
    process_directory(subtitle_output_folder,subtitle_cleanup_folder)
    #Performing the chunking on the clean subtitles
    #chunks_folder = ChannelName/chunks
    chunks_folder = audio_output_folder.replace("audio_files","chunks")
    os.makedirs(chunks_folder,exist_ok=True)
    logger = setup_logging(chunks_folder)
    process_files(subtitle_cleanup_folder,audio_compressed_folder,chunks_folder,args.language, args.subtitles,args.category,logger,args.channel)
    #Creating the requests.json to send to GPT
    input_jsonl = f"{chunks_folder}/chunks_metadata.jsonl"
    output_json = f"{chunks_folder}/requests.json"
    json_creation(input_jsonl,output_json)
    #Sending the requests.json file to GPT-4o
    api_key = os.getenv("OPENAI_API_KEY")
    endpoint = "/v1/chat/completions"
    completion_window = "24h"
    processor = OpenAIBatchProcessor(api_key)
    processor.send_batch(output_json,endpoint,completion_window)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and translate chunks based on Hindi-English mapping from GPT-4o results")
    parser.add_argument("--channel_url", required=True, help="Path to the GPT batch_jsonl file")
    parser.add_argument("--audio_output_folder", required=True, help="Path to the original metadata_chunk.josnl file")
    parser.add_argument("--subtitle_output_folder", required=True, help="Path to the new transliterated chunks.josnl file")

    args = parser.parse_args()
    main(args.channel_url, args.audio_output_folder, args.subtitle_output_folder)