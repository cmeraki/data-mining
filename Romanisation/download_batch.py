import logging
import time
import json
import os
import requests

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

        # Log the batch job details for debugging
        logging.info(f"Batch job details: {batch_job}")

        # Monitor the batch job status
        while batch_job.get('status') not in ["completed", "failed", "cancelled"]:
            time.sleep(3)  # Wait for 3 seconds before checking the status again
            logging.info(f"Batch job status: {batch_job.get('status')}")
            batch_job = self._retrieve_batch_job(batch_job_id)

        # Download and save the results
        if batch_job.get('status') == "completed":
            result_file_id = batch_job.get('output_file_id')  # Use this key to get the file ID
            if result_file_id:
                result_file_name = "batch_job_results.jsonl"
                self._download_file(result_file_id, result_file_name)

                # Load data from the saved file
                results = []
                with open(result_file_name, "r") as file:
                    for line in file:
                        json_object = json.loads(line.strip())
                        results.append(json_object)

                logging.info("Batch job completed successfully.")
                return results
            else:
                logging.error("Output file ID not found in the batch job details.")
                return None
        else:
            logging.error(f"Batch job failed with status: {batch_job.get('status')}")
            return None

    def _retrieve_batch_job(self, batch_job_id):
        response = requests.get(f"{self.base_url}/batches/{batch_job_id}",
                                headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        return response.json()

    def _download_file(self, file_id, output_file_name):
        # Retrieve the file using its ID
        file_url = f"{self.base_url}/files/{file_id}"
        response = requests.get(file_url, headers={"Authorization": f"Bearer {self.api_key}"})
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
