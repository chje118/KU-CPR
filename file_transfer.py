"""
Tool to transfer files from multiple local folders to network drive.
Gaps in network connection results in interrupted file transfer, with error message: "An unexpected network error occurred".
Retries if network error occurs. 
"""

import os
import shutil
from pathlib import Path
import time
from tqdm import tqdm

class FileTransfer:
    def __init__(self, retry_delay:int = 5, max_retries:int = 10):
        """ Initialize the FileTransfer object.
        args:
            retry_delay (int): Time in seconds to wait before retrying a failed transfer.
            max_retries (int): Max retries berfore transfer is discontinued. 
        """
        self.retry_delay = retry_delay
        self.max_retries = max_retries
    
    def merge_and_move_folders(self, source_folder:str, destination_folder:Path) -> bool:
        """ Merge source folder into destination folder.
        If the file already exists in the destination folder, it is skipped.

        args:
            source_folder (str): path to source folder
            destination_folder (str): path to destination folder
        returns: 
            bool: True if successful, False otherwise.
        """
        retries = 0
        while retries <= self.max_retries:
            try:
                for src_dir, subdirs, files in os.walk(source_folder):
                    relative_path = os.path.relpath(src_dir, source_folder)
                    dest_dir = os.path.join(destination_folder, relative_path) # Construct the destination path

                    os.makedirs(dest_dir, exist_ok = True) # Create directories in the destination folder, if they don't exist
       
                    for file in files:
                        src_file = os.path.join(src_dir, file)
                        dest_file = os.path.join(dest_dir, file)

                        if os.path.exists(dest_file): # If the file already exists, skip it
                            if os.path.getsize(src_file) == os.path.getsize(dest_file):
                                os.remove(src_file)
                                print(f"Source file '{file}' already exists at destination. Source file deleted.")
                            else:
                                print(f"File '{file}' already exists with different size. Skipping.")
                            continue                        
                        else:
                            shutil.move(src_file, dest_file) # Move the file if it doesn't exist
                            print(f"File '{file}' has been moved.")
                return True
        
            except (shutil.Error, OSError) as e:
                if "network" in str(e).lower(): # Retry if a network error is detected
                    retries += 1
                    if retries > self.max_retries:
                        print("Max retries reached. Failed to merge folders.")
                        return False
                    print(f"Network error occurred. Retry {retries}/{self.max_retries} after {self.retry_delay} seconds.")
                    time.sleep(self.retry_delay)  # Wait before retrying
                    continue
                else:
                    print(f"Error moving file: {e}")
                    return False
        return False 

    def transfer_folder_with_retry(self, source_folder:str, destination_folder:str)->bool:
        """ Transfer a single source folder to the destination folder.
        If the destination folder already exists, merge the folders and move files.

        args:
            source_folder (str): path to source folder
            destination_folder (str): path to destination folder
        returns: 
            bool: True if successful, False otherwise.
        """
        retries = 0
        source = Path(source_folder)
        destination = Path(destination_folder)
        new_destination = destination / source.name # Create destination folder path

        while retries <= self.max_retries:
            try:
                if new_destination.exists():
                    print(f"Destination folder '{new_destination}' already exists. Merging and moving folders.")
                    if not self.merge_and_move_folders(source_folder, new_destination): # Checks return value
                        print("Failed to merge folders. ")
                        return False
                else:
                    shutil.move(source, new_destination) # Move the entire folder                
                    print(f"Successfully moved: {source}")
               
                print("Folder transfer complete.")
                return True
            
            except (shutil.Error, OSError) as e:
                if "network" in str(e).lower(): # Retry if a network error is detected
                    retries += 1
                    print(f"Network error occurred. Retry {retries}/{self.max_retries} after {self.retry_delay} seconds.")
                    time.sleep(self.retry_delay)  # Wait before retrying
                else:
                    print(f"Error moving folder: {e}")
                    return False

        print("Max retries reached. Failed to move folder. ")
        return False

    def transfer_multiple_folders_with_retry(self, source_folders: list[str], destination_folder: str)-> None:
        """ Transfer multiple source folders to the destination folder one by one.
        
        args:
            source_folders(list of strings): list of paths to source folders
            destination_folder(str): path to destination folder
        """
        for source_folder in tqdm(source_folders):
            if not os.path.exists(source_folder): # Check if source folder exists, if not, continue with the next folder
                print(f"Source folder '{source_folder}' does not exist. Skipping.")
                continue
            print(f"\nTransferring folder: {source_folder}")

            if not self.transfer_folder_with_retry(source_folder, destination_folder):
                print(f"Failed to transfer folder: {source_folder}. Moving to next.")
        

if __name__ == "__main__":
    source_folders = [
        "path/to/folders"
    ]
    destination_folder = "path/to/destination"

    transfer_tool = FileTransfer(retry_delay=5, max_retries=15)
    transfer_tool.transfer_multiple_folders_with_retry(source_folders, destination_folder)
