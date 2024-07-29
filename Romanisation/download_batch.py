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

            # Log the first few lines of the file for debugging
            with open(result_file_name, "r") as file:
                for i, line in enumerate(file):
                    if i < 5:  # Log the first 5 lines
                        logging.info(f"Line {i+1}: {line.strip()}")

            # Load data from the saved file
            results = []
            with open(result_file_name, "r") as file:
                for line in file:
                    try:
                        json_object = json.loads(line.strip())
                        results.append(json_object)
                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decode error: {e}")

            logging.info("Batch job completed successfully.")
            return results
        else:
            logging.error("Output file ID not found in the batch job details.")
            return None
    else:
        logging.error(f"Batch job failed with status: {batch_job.get('status')}")
        return None
