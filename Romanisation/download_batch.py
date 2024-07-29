import logging
import time
import json
import os
import requests  # Use requests to download file contents

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenAIBatchProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"

    def download_batch_output(self, batch_details_file):
        # Load batch details from the file
        with open(batch_details_file, "r") as file:
            batch_details = json.load(file)

        batch_job_id = batch_details["batch_job_id"]

        # Retrieve the batch job
        batch_job = self._retrieve_batch_job(batch_job_id)

        # Monitor the batch job status
        while batch_job['status'] not in ["completed", "failed", "cancelled"]:
            time.sleep(3)  # Wait for 3 seconds before checking the status again
            logging.info(f"Batch job status: {batch_job['status']}")
            batch_job = self._retrieve_batch_job(batch_job_id)

        # Download and save the results
        if batch_job['status'] == "completed":
            result_file_url = batch_job['output_file_url']
            result_file_name = "batch_job_results.jsonl"
            self._download_file(result_file_url, result_file_name)

            # Load data from the saved file
            results = []
            with open(result_file_name, "r") as file:
                for line in file:
                    json_object = json.loads(line.strip())
                    results.append(json_object)

            logging.info("Batch job completed successfully.")
            return results
        else:
            logging.error(f"Batch job failed with status: {batch_job['status']}")
            return None

    def _retrieve_batch_job(self, batch_job_id):
        # Replace with actual request to OpenAI's API to retrieve batch job
        response = requests.get(f"{self.base_url}/batches/{batch_job_id}",
                                headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        return response.json()

    def _download_file(self, file_url, output_file_name):
        response = requests.get(file_url)
        response.raise_for_status()
        with open(output_file_name, "wb") as file:
            file.write(response.content)

# Initialize the OpenAIBatchProcessor
api_key = os.getenv("OPENAI_API_KEY")
processor = OpenAIBatchProcessor(api_key)

# Download the batch output
batch_details_file = "batch_details.json"
results = processor.download_batch_output(batch_details_file)

# Log the results
logging.info(results)
