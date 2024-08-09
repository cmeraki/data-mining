# VTT Processing and OpenAI Batch Processor

This project consists of two Python scripts: one for processing VTT files and generating JSON, and another for sending batch jobs to OpenAI for further processing. The scripts facilitate the extraction and preparation of subtitle data for batch processing with OpenAI's API.

## Features

- **Process VTT Files**: Converts VTT subtitle files to JSON format by removing timestamps and other directives.
- **OpenAI Batch Processor**: Uploads the processed JSON file to OpenAI and initiates a batch job for completion or other tasks.

## Prerequisites

- Python 3.7 or higher
- `openai` library (for interacting with OpenAI API)

You can install the required Python package using pip:

```bash
pip install openai
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

## Usage

### Processing VTT Files

Run the script to process VTT files and create a JSON file:

```bash
python requests.py <directory_with_vtt_files> <output_json_file>
```

- `<directory_with_vtt_files>`: Directory containing the VTT files.
- `<output_json_file>`: Path where the JSON file will be saved.

### Sending Batch Job to OpenAI

Run the script to send a batch job to OpenAI:

```bash
python batch_romanize.py <input_json_file>
```

- `<input_json_file>`: Path to the JSON file created from the VTT processing step.

Ensure that your OpenAI API key is set in your environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

## Logging

Logs are saved in `download.log` and `batch_details.json` for tracking progress and results.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
