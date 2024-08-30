import os
import yt_dlp
import logging

# Setup logging
logging.basicConfig(filename='download.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Scraping log')

def download_youtube_audios_and_transcripts(output_audio_dir, output_transcript_dir, youtube_links):
    """
    Downloads and extracts audio and transcripts from a list of YouTube URLs and saves them in the specified output directories.
    Each file is named after its YouTube video ID.
    params:
        output_audio_dir : str : The directory where the extracted audio files will be saved.
        output_transcript_dir : str : The directory where the transcript files will be saved.
        youtube_links : list : A list of YouTube URLs to download audio and extract transcripts from.
    """
    # Ensure output directories exist
    os.makedirs(output_audio_dir, exist_ok=True)
    os.makedirs(output_transcript_dir, exist_ok=True)

    for link in youtube_links:
        # Define options for downloading audio
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',  
                'preferredquality': '192', 
            }],
            'outtmpl': os.path.join(output_audio_dir, '%(id)s.%(ext)s'),  # Use video ID for filename
        }

        # Define options for downloading subtitles
        ydl_opts_transcript = {
            'writesubtitles': True,
            'subtitleslangs': ['hi',],  # Change 'en' to your preferred language code
            'writeautomaticsub': True,
            'skip_download': True,
            'outtmpl': os.path.join(output_transcript_dir, '%(id)s.%(ext)s'),  # Use video ID for filename
        }

        try:
            # Download audio
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download([link])
            logger.info(f"Download completed for audio with ID {link.split('=')[-1]}.wav.")

            # Download transcript
            with yt_dlp.YoutubeDL(ydl_opts_transcript) as ydl:
                ydl.download([link])
            logger.info(f"Download completed for transcript with ID {link.split('=')[-1]}.")

        except Exception as e:
            logger.error(f"Failed to download for {link}. Error: {e}")
