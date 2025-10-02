import os
import shutil
from pathlib import Path
import re
import pandas as pd

class FindWSIFolder:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_filename(self, wsi_path):
        """ Extract the filename from a WSI path. """
        return Path(wsi_path).name # e.g., slide1.mrxs or slide1 (2).mrxs

    def get_base_name(self, filename):
        """ Get base name (folder) without extension. """
        return Path(filename).stem  # e.g., slide1 or slide1 (2)

    def find_matching_folders(self, wsi_path):
        """ Find all folders matching the base name of the WSI file. """
        filename = self.get_filename(wsi_path)
        base_name = self.get_base_name(filename)
        search_name = re.sub(r" \(\d+\)$", "", base_name)
        return list(self.base_dir.glob(f"**/{search_name}"))

    def find_folders(self, wsi_path):
        matching_folders = self.find_matching_folders(wsi_path)
        if not matching_folders:
            print(f"No matching folder found for {wsi_path}.")
            return None
        else:
            print(f"Number of matching folders found for {wsi_path}: {len(matching_folders)}")
            return matching_folders
        
    def main(self, df, wsi_column):
        df['matching_folders'] = [self.find_folders(wsi_path) for wsi_path in df[wsi_column]]
        return df

if __name__ == "__main__":
    # Example usage
    df_wsi = pd.read_csv("path/to/wsi_stats.csv")
    
    missing_data = df_wsi[
        (df_wsi["file_size"].isna() | (df_wsi["file_size"] == 0)) | 
        (df_wsi["data_folder_size"].isna() | (df_wsi["data_folder_size"] == 0))
    ]
    
    missing_data = missing_data.reset_index()  # filename becomes a column

    base_directory = Path(r"\\regsj\.intern\appl\Deep_Visual_Proteomics")
    finder = FindWSIFolder(base_directory)
    result_df = finder.main(missing_data, 'filename')
    
    # Remove rows without matching folders
    result_df = result_df[result_df['matching_folders'].notna()]
    
    # Look into files with 1 matching folder
    one_match = result_df[result_df['matching_folders'].apply(lambda x: len(x) == 1)]
    
    # If 1 match, check if folder has any files
    one_match['has_files'] = one_match['matching_folders'].apply(lambda folders: any(f.is_file() for f in folders[0].rglob('*')))
    
    # If no files, remove rows
    one_match = one_match[one_match['has_files']]

    # If has files, check if some have (2) extension
    one_match['has_(2)_files'] = one_match['matching_folders'].apply(
        lambda folders: any(re.search(r" \(\d+\)", f.name) for f in folders[0].rglob('*') if f.is_file())
    )

    # If has (2) files, move all (2) to new folder with (2) suffix
    for idx, row in one_match.iterrows():
        if row['has_(2)_files']:
            original_folder = row['matching_folders'][0]
            new_folder = original_folder.parent / f"{original_folder.name} (2)"
            new_folder.mkdir(exist_ok=True)
            for file in original_folder.rglob('*'):
                if re.search(r" \(\d+\)", file.name) and file.is_file():
                    shutil.move(str(file), new_folder / file.name)
            print(f"Moved (2) files from {original_folder} to {new_folder}")
    
    # If multiple matches, log for manual review
    multiple_matches = result_df[result_df['matching_folders'].apply(lambda x: len(x) > 1)]

    # If a folder does not have files, remove it from the list
    def filter_empty_folders(folders):
        return [f for f in folders if any(file.is_file() for file in f.rglob('*'))]
    multiple_matches['matching_folders'] = multiple_matches['matching_folders'].apply(filter_empty_folders)

    if not multiple_matches.empty:
        print("Multiple matching folders found for some WSIs. Please review manually:")
        print(multiple_matches[['filename', 'matching_folders']])

