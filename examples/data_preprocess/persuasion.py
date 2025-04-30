import argparse
import json
import os
import pandas as pd
from datasets import Dataset
from typing import List, Dict

def extract_prompt(example):
    responses = example["transcript"]["responses"]
    for response in responses:
        if response.get("correct"):
            return response["correct"].get("prompt")
    return None

def extract_belief(example):
    responses = example["transcript"]["responses"]
    for response in responses:
        if response.get("persuadee"):
            return response["persuadee"].get("response")
    return None

def process_data(raw_data: List[Dict], split: str) -> List[Dict]:
    processed = []
    for idx, example in enumerate(raw_data):
        prompt = extract_prompt(example)
        belief = extract_belief(example)
        if prompt is not None and belief is not None:
            processed.append({
                "data_source": "persuasion",
                "prompt": prompt,
                "ability": "persuasion",
                "reward_model": {
                    "style": "model",
                    "ground_truth": belief
                },
                "extra": {"split": split, "index": idx}
            })
    return processed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_dir', default='data/persuasion')
    parser.add_argument('--raw_dir', default='source/anthropic_dynamic.json')
    parser.add_argument('--train_size', type=int, default=64)
    parser.add_argument('--test_size', type=int, default=8)
    args = parser.parse_args()

    with open(args.raw_dir, 'r') as f:
        full_data = json.load(f)

    # Split manually
    train_raw = full_data[:args.train_size]
    test_raw = full_data[args.train_size:args.train_size + args.test_size]

    # Process
    train_data = process_data(train_raw, split='train')
    test_data = process_data(test_raw, split='test')

    # Convert to Dataset then to DataFrame
    train_dataset = Dataset.from_list(train_data)
    test_dataset = Dataset.from_list(test_data)

    train_df = pd.DataFrame(train_dataset)
    test_df = pd.DataFrame(test_dataset)

    os.makedirs(args.local_dir, exist_ok=True)
    train_df.to_parquet(os.path.join(args.local_dir, 'train.parquet'))
    test_df.to_parquet(os.path.join(args.local_dir, 'test.parquet'))
