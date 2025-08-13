import csv
import numpy as np
from huggingface_hub import hf_hub_download
from tqdm import tqdm

# --- 1. Download the training data file ---
print("Downloading 'train.csv'...")
csv_path = hf_hub_download(
    repo_id="sapientinc/sudoku-extreme",
    filename="train.csv",
    repo_type="dataset"
)