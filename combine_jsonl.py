import json
import glob
import os
import argparse

def combine_jsonl_files(input_directory):
    # Create the output file path
    output_file = os.path.join(input_directory, "combined_output.jsonl")
    
    # Get all .jsonl files in the input directory
    input_pattern = os.path.join(input_directory, "*.jsonl")
    
    with open(output_file, 'w') as outfile:
        for filename in glob.glob(input_pattern):
            # Skip the output file if it already exists
            if filename == output_file:
                continue
            with open(filename, 'r') as infile:
                for line in infile:
                    outfile.write(line)
    
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine multiple JSONL files in a directory into a single JSONL file")
    parser.add_argument("input_directory", help="Directory containing input JSONL files")
    args = parser.parse_args()

    output_file = combine_jsonl_files(args.input_directory)
    print(f"Combined JSONL files into {output_file}")