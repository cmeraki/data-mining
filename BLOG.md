# Youtube video scraping and data chunking

Let's dive into the data flow and code flow of this comprehensive Python script designed to download YouTube videos, extract audio, process subtitles, and manage audio splitting. Here's a step-by-step explanation of how the functions work together:

## Step 1: Obtaining YouTube URLs
The script begins by defining a function get_youtube_urls(channel_url) which takes the URL of a YouTube channel and retrieves all video URLs from that channel. It uses the yt-dlp command-line tool to fetch a playlist in JSON format and extracts video IDs to construct individual video URLs.

## Step 2: Downloading Audio
Next, the download_audio_from_youtube(video_url, output_path) function is responsible for downloading the audio from each YouTube video. Using the pytube library, it filters to get only the audio stream, downloads it, converts it to MP3 format using the pydub library, and saves it. The original file is then deleted to save space.

## Step 3: Obtaining VTT Subtitle Files
To extract subtitles, the extract_transcript(video_url) function uses yt_dlp again with specific options to download automatic subtitles in VTT format. These subtitles are saved in a designated directory.

## Step 4: Parsing and Splitting VTT Files
The script includes multiple functions to handle the parsing and splitting of VTT subtitle files:

parse_vtt_time(time_str) converts a VTT timestamp into a timedelta object.
split_vtt_by_timestamps(vtt_content, splits) splits the VTT file into chunks based on provided timestamp ranges.
write_splits_to_files(split_contents, output_folder) saves these chunks into separate VTT files.

## Step 5: Processing VTT Files
The process_vtt_file(file_path, splits, output_folder) function reads the VTT file, splits it using split_vtt_by_timestamps, and writes the split contents to new files.

## Step 6: Chunking Audio Files
To manage audio chunks, the script defines:

chunk_audio_files(timestamps, output_folder) which takes timestamp ranges and splits the audio files accordingly. Each chunk is saved as an individual MP3 file.
extract_timestamps_from_vtt(filename) extracts timestamp pairs from the VTT file.
combine_timestamps(timestamps) combines these timestamps into larger chunks.

## Step 7: Converting Milliseconds to Time Format
The milliseconds_to_time_format(milliseconds) function is a utility to convert milliseconds into a formatted time string, which is useful for handling timestamp data.

## Step 8: Chunking Audio and Splitting VTT Files
The script iterates over subtitle files and extracts timestamps, combines them, and splits both audio and VTT files. The timestamps are used to split the audio files into chunks using chunk_audio_files, and VTT files are split using process_vtt_file.

## Step 9: Extracting Text from VTT Files
Finally, to extract specific lines from the VTT files, the script uses:

extract_specific_lines(vtt_filename) which identifies lines matching a particular pattern.
extract_text_from_vtt_line(line) which removes unwanted tags from the lines to extract clean text.

## Summary
The overall flow of the script involves:

Fetching video URLs from a YouTube channel.
Downloading and converting audio from these videos.
Downloading subtitle files for the videos.
Parsing and splitting both the audio and subtitle files based on timestamps.
Extracting and cleaning text from subtitle files.
This modular approach ensures that each task is handled by a dedicated function, making the script efficient and easy to manage. The final outcome is a set of chunked audio files and corresponding subtitle segments, with clean text extracted from the subtitles for further use.
