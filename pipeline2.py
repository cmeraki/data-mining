import json
import argparse
from json.decoder import JSONDecodeError

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except JSONDecodeError:
                print(f"Error parsing line in {file_path}: {line}")
    return data

def main(batch_jsonl_path, og_chunks_path, mod_chunks_path):
    # Load batch data and create a dictionary for quick lookup
    batch_data = {item['custom_id']: item['response']['body']['choices'][0]['message']['content'] 
                  for item in load_jsonl(batch_jsonl_path)}
    
    # Process chunks and write directly to output file
    with open(og_chunks_path, 'r') as input_file, open(mod_chunks_path, 'w') as output_file:
        for line in input_file:
            chunk = json.loads(line.strip())
            custom_id = chunk['chunk_id']
            if custom_id in batch_data:
                chunk['text'] = batch_data[custom_id]
            json.dump(chunk, output_file)
            output_file.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and translate chunks based on Hindi-English mapping from GPT-4 results")
    parser.add_argument("--batch_jsonl_path", required=True, help="Path to the GPT batch_jsonl file")
    parser.add_argument("--og_chunks_path", required=True, help="Path to the original metadata_chunk.jsonl file")
    parser.add_argument("--mod_chunks_path", required=True, help="Path to the new transliterated chunks.jsonl file")
    args = parser.parse_args()
    main(args.batch_jsonl_path, args.og_chunks_path, args.mod_chunks_path)