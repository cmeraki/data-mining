import json
import torch
import torchaudio
import os
from datasets import load_dataset
from ttsutils import convert_audio
from datalib import Dataset
from torio.io import CodecConfig
from tqdm import tqdm
from tokenlib import AUDIO
import soundfile as sf

def stream_samples_from_jsonl(jsonl_file):
    with open(jsonl_file, 'r') as f:
        for line in f:
            item = json.loads(line)
            yield item

def make_dataset(jsonl_file, hf_repo_id):
    dataset = Dataset(repo_id=hf_repo_id)

    for item in tqdm(stream_samples_from_jsonl(jsonl_file)):
        sample = dataset.create_sample(id=item['chunk_id'])

        sample.raw_text = item['text']

        audio_path = item['audio']
        audio_path = os.path.join("/mnt/disks/audio-data-2/Data/SandeepMaheshwari/chunks",audio_path)
        audio_array, sr = torchaudio.load(audio_path)

        audio_array = convert_audio(audio_array,
                                     sr=sr,
                                     target_sr=16000,
                                     target_channels=1)

        torchaudio.save(dataset.get_absolute_path(sample.audio_path),
                          audio_array,
                          sample_rate=16000,
                          format='mp3',
                          encoding='PCM_S',
                          bits_per_sample=16,
                          backend='ffmpeg',
                          compression=CodecConfig(bit_rate=64000))

        dataset.add_sample(sample)

    dataset.upload(hf_repo_id=hf_repo_id)

def tokenize(hf_repo_id):
    dataset = Dataset(repo_id=hf_repo_id)

    import audiotoken
    tokenizer = audiotoken.AudioToken(tokenizer='semantic_s', device='cpu')

    tokenizer.encode_batch_files(audio_dir=dataset.dirs[AUDIO],
                                 outdir='/tmp/test/',
                                 num_workers=4,
                                 batch_size=32)

def test_dataset(hf_repo_id):
    dataset = Dataset(repo_id=hf_repo_id)
    for item in tqdm(dataset.iter_dataset()):
        pass

# Replace 'path_to_your_jsonl_file' with the actual path to your JSONL file
jsonl_file = '/mnt/disks/audio-data-2/Data/SandeepMaheshwari/chunks/chunks.jsonl'

# Replace 'new_repo_name' with the desired name for your Hugging Face repository
hf_repo_id = 'youtube_sandeepmaheshwari_hi_raw'

make_dataset(jsonl_file, hf_repo_id)
tokenize(hf_repo_id)
test_dataset(hf_repo_id)