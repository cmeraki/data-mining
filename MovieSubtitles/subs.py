import subprocess
import json
import requests
import logging
import os

# Configure logging
logging.basicConfig(filename='process.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_js_script(js_file_path, movie_name):
    """Run a JavaScript file using Node.js and return the output."""
    try:
        logging.info(f'Running JavaScript file: {js_file_path} with movie_name: {movie_name}')
        result = subprocess.run(['node', js_file_path, movie_name], capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info('JavaScript file executed successfully.')
            return result.stdout.strip()
        else:
            logging.error(f'Error executing JavaScript file. Return code: {result.returncode}')
            logging.error(result.stderr)
            return None
    except Exception as e:
        logging.exception('Exception occurred while running JavaScript file.')
        return None

def download_file(url, local_filename):
    """Download a file from a URL and save it locally."""
    try:
        logging.info(f'Downloading file from URL: {url}')
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logging.info(f'File downloaded and saved as {local_filename}')
        else:
            logging.error(f'Failed to download file. Status code: {response.status_code}')
    except Exception as e:
        logging.exception('Exception occurred while downloading file.')

def main():
    js_file_path = 'script2.mjs'
    
    with open('movielist.txt', 'r') as file:
            movies = [line.strip() for line in file if line.strip()]
    subtitle_base_url = 'https://dl.subdl.com'

    for movie_name in movies:
        raw_output = run_js_script(js_file_path, movie_name)
        if raw_output:
            subtitle_url = f'{subtitle_base_url}{raw_output}'
            local_filename = f'movie_subs/{movie_name}.zip'
            download_file(subtitle_url, local_filename)
        else:
            logging.error('No subtitle URL was obtained from JavaScript script.')

if __name__ == '__main__':
    main()
