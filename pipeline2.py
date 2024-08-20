#The second part of the pipeline that will transliterate the chunks file from hindi to english for the corresponding chunks created
import json
import re
from json.decoder import JSONDecodeError

#Load a json/jsonl file into an array
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except JSONDecodeError:
                print(f"Error parsing line in {file_path}: {line}")
    return data
    
#Replacing the hindi chunks with English chunks
def main(batch_jsonl_path,og_chunks_path,mod_chunks_path):
    batch_data = load_jsonl(batch_jsonl_path)
    chunks_data = load_jsonl(og_chunks_path)
    chunks_mod = []
    for chunk in chunk_data:
        custom_id = chunk['chunk_id']
        for batch in batch_data:
            if batch['custom_id'] == custom_id:
                text = batch['response']['body']['choices'][0]['message']['content']
                chunk['text'] = text
                chunk_mod.append(chunk)
    with open(mod_chunks_path,'w') as file:
        for item in chunk_mod:
            json.dump(item,file)
            file.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and translate chunks based on Hindi-English mapping from GPT-4o results")
    parser.add_argument("--batch_jsonl_path", required=True, help="Path to the GPT batch_jsonl file")
    parser.add_argument("--og_chunks_path", required=True, help="Path to the original metadata_chunk.josnl file")
    parser.add_argument("--mod_chunks_path", required=True, help="Path to the new transliterated chunks.josnl file")

    args = parser.parse_args()
    main(args.batch_jsonl_path, args.og_chunks_path, args.mod_chunks_path)