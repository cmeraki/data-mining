import logging
import time
import json
import os
from openai import OpenAI

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenAIBatchProcessor:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def download_results(self, batch_details_path):
        # Load batch details from the JSON file
        with open(batch_details_path, 'r') as file:
            batch_details = json.load(file)

        batch_job_id = batch_details['batch_job_id']

        # Retrieve the batch job
        batch_job = self.client.batches.retrieve(batch_job_id)

        # Monitor the batch job status
        while batch_job.status not in ["completed", "failed", "cancelled"]:
            time.sleep(3)  # Wait for 3 seconds before checking the status again
            logging.info(f"Batch job status: {batch_job.status}")
            batch_job = self.client.batches.retrieve(batch_job.id)

        # Download and save the results
        if batch_job.status == "completed":
            result_file_id = batch_job.output_file_id
            result_file = self.client.files.retrieve(result_file_id)

            result_file_name = "batch_job_results.jsonl"
            with open(result_file_name, "wb") as file:
                file.write(result_file.read())

            # Load data from the saved file
            results = []
            with open(result_file_name, "r") as file:
                for line in file:
                    json_object = json.loads(line.strip())
                    results.append(json_object)

            logging.info(results)
            return results
        else:
            logging.error(f"Batch job failed with status: {batch_job.status}")
            return None

# Initialize the OpenAIBatchProcessor
api_key = os.getenv("OPENAI_API_KEY")
processor = OpenAIBatchProcessor(api_key)

# Download the batch job results
batch_details_path = 'batch_details.json'
processor.download_results(batch_details_path)
