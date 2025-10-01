import os
import shutil
from pathlib import Path
import re
import pandas as pd

data_dir = Path(r"//regsj\.intern/appl/Deep_Visual_Proteomics\")
# wsi_files = TODO, FILES FROM CODE

# Extract filename without path
def get_filename(wsi_path):
    return Path(wsi_path).name # e.g., slide1.mrxs or slide1 (2).mrxs

# Get base name without extension
def get_base_name(filename):
    return Path(filename).stem  # e.g., slide1 or slide1 (2)

# Process each WSI file
def find_matching_folders(wsi_path):
    filename = get_filename(wsi_path)
    base_name = get_base_name(filename)
    search_name = re.sub(r" \(\d+\)$", "", base_name)
    return list(data_dir.glob(f"**/{search_name}"))

# Add a column to the DataFrame with all matched folders for each WSI file
df['matching_folders'] = [find_matching_folders(wsi_path) for wsi_path in df.index]