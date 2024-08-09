# Subtitle and Audio Chunk Processor

This Python script processes subtitle and audio files to create chunks of audio and text, extracting and exporting them into separate files. The chunks are based on rules derived from subtitle text, and metadata is saved in a JSON Lines (JSONL) file. This tool is particularly useful for managing and analyzing large amounts of subtitle and audio data.

## Features

- **Subtitle Parsing**: Reads and parses `.hi_final.vtt` subtitle files to extract text and timing information.
- **Audio Chunking**: Splits audio files into chunks based on the parsed subtitle timings and text rules.
- **Metadata Generation**: Creates a JSONL file containing metadata for each audio chunk, including text, timings, and file paths.
- **Logging**: Logs the processing details to a file and console for monitoring and debugging purposes.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- `pydub` (for audio processing)
- `re` (for regular expressions)
- `argparse` (for command-line argument parsing)
- `logging` (for logging)
- `json` (for JSON handling)
- `os` (for file system operations)

You can install the required package using pip:

```bash
pip install pydub
```

Make sure you also have `ffmpeg` or `libav` installed on your system, as `pydub` depends on it for handling audio files.

## Usage

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. **Run the Script**

   Use the following command to run the script:

   ```bash
   python script_name.py <subtitle_dir> <audio_dir> <output_dir> [--channel CHANNEL] [--language LANGUAGE] [--subtitles SUBTITLES] [--category CATEGORY]
   ```

   - `<subtitle_dir>`: Directory containing `.hi_final.vtt` subtitle files.
   - `<audio_dir>`: Directory containing corresponding `.wav` audio files.
   - `<output_dir>`: Directory where output files and logs will be saved.
   - `--channel`: Optional channel name (default: 'base').
   - `--language`: Optional language of the subtitles (default: 'en').
   - `--subtitles`: Optional subtitle source ('uploaded' or 'auto', default: 'auto').
   - `--category`: Optional category of the content (default: 'general').

## Example

```bash
python script_name.py ./subtitles ./audio ./output --channel my_channel --language es --subtitles uploaded --category conversation
```

This command will process subtitle and audio files in the `./subtitles` and `./audio` directories, respectively, and save the processed files and metadata in the `./output` directory. It will also log the process details and handle Spanish language subtitles with a channel name `my_channel` and category `conversation`.

## Files Created

- **Audio Chunks**: `.wav` files in the `audio_chunks` subdirectory.
- **Text Chunks**: `.txt` files in the `subtitle_chunks` subdirectory.
- **Metadata File**: `chunks_metadata.jsonl` containing JSON lines with chunk metadata.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or comments, please contact Subhash
