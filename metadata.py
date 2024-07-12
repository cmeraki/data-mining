import yt_dlp
import csv

def fetch_channel_videos_info(channel_url):
    """
    Fetches and stores video links, names, and durations for a YouTube channel.
    params:
        channel_url (str): The URL of the YouTube channel.
    Returns:
        list of dict: A list containing dictionaries with video information.
    """
    videos_info = []

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        if 'entries' in result:
            for video in result['entries']:
                if video:  # Ensure the video information is not None
                    video_info = {
                        'url': f"https://www.youtube.com/watch?v={video['id']}",
                        'title': video.get('title'),
                        'duration': video.get('duration')  # Duration in seconds
                    }
                    videos_info.append(video_info)

    return videos_info

def write_videos_info_to_csv(videos_info, csv_filename):
    """
    Writes video information to a CSV file.
    params:
        videos_info (list of dict): A list containing dictionaries with video information.
        csv_filename (str): The filename of the CSV file to write to.
    """
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'url', 'duration'])
        writer.writeheader()
        for video in videos_info:
            writer.writerow(video)

# Example usage
channel_url = 'https://www.youtube.com/@TEDEd/videos'
videos_info = fetch_channel_videos_info(channel_url)
write_videos_info_to_csv(videos_info, 'metadata/Ted_ED.csv')

