from helper_functions import *

#Extracting the youtube video URLS when a channel is inputted
video_urls = get_youtube_urls("https://www.youtube.com/c/NotJustBikes/videos")

#Downloading the videos into a wav format
download_youtube_audios("channel_1",video_urls)

#Extracting the transcripts
extract_transcript(video_urls=video_urls,output_dir='subtitles')

#Extracting the timestamps and the chunks
if not os.path.exists('audio_outputs'):
    os.makedirs('audio_outputs')

if not os.path.exists('subtitle_outputs'):
    os.makedirs('subtitle_outputs')
    
for filename in os.listdir('subtitles'):
    timestamps = extract_timestamps_from_vtt(os.path.join('subtitles',filename))
    arr = timestamps
    combined_timestamps = combine_timestamps(arr)
    fname , fe = os.path.splitext(filename)
    fname = fname.replace('.en','')
    print(fname)
    output_folder = fname
    fname = fname+'.wav'
    ts = {
        os.path.join('channel_1',fname) : combined_timestamps
    }
    chunk_audio_files(timestamps=ts,output_folder=os.path.join('audio_outputs',output_folder))

    # Splitting the VTT files
    splits = []
    time_format = []
    for k in combined_timestamps:
        start_format = milliseconds_to_time_format(k[0])
        end_format = milliseconds_to_time_format(k[1])
        time_format.append((start_format, end_format))
    for i in time_format:
        splits.append((parse_vtt_time(i[0]), parse_vtt_time(i[1])))
    process_vtt_file(file_path=os.path.join('subtitles',filename), splits=splits,output_folder=f'subtitle_outputs/{output_folder}_split')

#Text extraction from VTT files and storing it into a text file
if not os.path.exists("subtitles_text"):
    os.makedirs("subtitles_text")
for item in os.listdir('subtitle_outputs'):
    for filename in os.listdir(os.path.join('subtitle_outputs',item)):
        i=1
        lines = extract_specific_lines(os.path.join("subtitle_outputs",item,filename))
        if '<' or '>' in lines:
            for line in lines:
                text = extract_text_from_vtt_line(line)
                if not os.path.exists(f"subtitles_text/subtitles{i}"):
                    os.makedirs(f"subtitles_text/subtitles{i}")
                with open(f'subtitles_text/subtitles{i}/'+filename.replace('.en.vtt','.txt'),'a') as f:
                    f.write(text+'\n')
        i=i+1
