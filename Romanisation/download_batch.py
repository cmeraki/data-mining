import argparse
import logging
import time
import json
import os
from openai import OpenAI

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenAIBatchProcessor:
    def __init__(self, api_key):
        client = OpenAI(api_key=api_key)
        self.client = client

    def send_batch(self, input_file_path, endpoint, completion_window):
        # Upload the input file
        with open(input_file_path, "rb") as file:
            uploaded_file = self.client.files.create(
                file=file,
                purpose="batch"
            )

        # Create the batch job
        batch_job = self.client.batches.create(
            input_file_id=uploaded_file.id,
            endpoint=endpoint,
            completion_window=completion_window
        )

        # Save batch job details to a file
        batch_details = {
            "batch_job_id": batch_job.id,
            "input_file_id": uploaded_file.id
        }
        with open("batch_details.json", "w") as file:
            json.dump(batch_details, file)

        logging.info(f"Batch job created with ID: {batch_job.id}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Send a batch job with OpenAI.')
parser.add_argument('input_file', type=str, help='Path to the input JSON file')
args = parser.parse_args()

# Initialize the OpenAIBatchProcessor
api_key = os.getenv("OPENAI_API_KEY")
processor = OpenAIBatchProcessor(api_key)

# Send the batch job
input_file_path = args.input_file
endpoint = "/v1/chat/completions"
completion_window = "24h"

processor.send_batch(input_file_path, endpoint, completion_window)
