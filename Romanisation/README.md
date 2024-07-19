# Subtitle Processing Tool

This tool is designed to process subtitle files, specifically `.vtt` files, to clean, transliterate, and remove duplicates and formatting directives. It's particularly useful for preparing subtitles for further processing or analysis.

## Features

- **Clean Subtitles**: Removes specific patterns and duplicate lines from subtitle files.
- **Remove Timestamps and Formatting**: Strips out timestamps and any HTML-like formatting directives.
- **Transliterate Text**: Supports transliteration of text from one script to another, utilizing OpenAI's GPT-4 for accurate results.

## Requirements

- Python 3.x
- `re` module for regular expressions
- `collections.OrderedDict` for maintaining order while removing duplicates
- OpenAI's GPT-4 API for transliteration (API key required)

## Setup

1. Ensure Python 3.x is installed on your system.
2. Obtain an API key from OpenAI for GPT-4 access.
3. Clone this repository or download the script files to your local machine.

## Usage

1. Place your `.vtt` subtitle files in a directory.
2. Run the script with the directory as an argument:

```bash
python process.py <directory_path>
