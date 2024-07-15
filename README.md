# Scraping Audio data with its paralell text

# Timestamp Helper Functions

This Python script provides a set of helper functions designed to work with video or audio timestamps. It includes functionality for extracting timestamps from files, combining them into groups, and converting milliseconds to a human-readable time format.

## Features

- **Timestamp Extraction**: Extract start and end timestamps from files based on a predefined regex pattern.
- **Combine Timestamps**: Group timestamps into sets of 7 for batch processing or analysis.
- **Milliseconds to Time Format**: Convert durations in milliseconds to a standard time format (HH:MM:SS:MMM).

## Usage

1. **Extracting Timestamps**: To extract timestamps from a file, ensure the file contains timestamps in a recognizable format. The function reads the entire file content and extracts timestamps based on the specified regex pattern.

    ```python
    timestamps = extract_timestamps('path/to/your/file.txt')
    ```

2. **Combining Timestamps**: After extracting timestamps, you can combine them into groups of 7. This is useful for processing or analyzing timestamps in batches.

    ```python
    combined_timestamps = combine_timestamps(timestamps)
    ```

3. **Milliseconds to Time Format**: Convert any duration in milliseconds to a readable time format. This can be used to display durations or timestamps in a user-friendly manner.

    ```python
    time_format = milliseconds_to_time_format(123456789)
    ```

## Requirements

- Python 3.x
- No external libraries are required for the main functionality. However, logging is used for informational purposes.

## Installation

No installation is required. Simply download the `helper_functions.py` script and include it in your Python project.

## Workflow

1. **Download Audio and Transcripts**: The script starts by downloading audio files and transcripts for a predefined list of YouTube video URLs.
2. **Prepare Output Directories**: It ensures that directories for storing audio outputs and subtitle outputs are created.
3. **Process Subtitles**: For each subtitle file, it extracts timestamps, combines them into groups, and prepares them for chunking.
4. **Chunk Audio**: Audio files are then chunked based on the combined timestamps.
5. **Split Subtitles**: Corresponding subtitle files are split into segments to match the audio chunks.

## Contributing

Contributions to improve the script or add new features are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.
