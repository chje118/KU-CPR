#Transfer of files from multiple local folders to network drive
#Gaps in network connection results in interrupted file transfer, with error message: "An unexpected network error occurred".

import os
import shutil
from pathlib import Path
import time
from tqdm import tqdm


def merge_and_move_folders(source_folder, destination_folder):
    ''' Move source folder into destination folder.
    Merge folders if destination folder already exists.
    If a file already exists in the destination folder, it is skipped.

    args:
        source_folder(str): path to source folder
        destination_folder(str): path to destination folder
    '''
    max_retries = 3
    retries = 0
    
    while retries <= max_retries:
        try:   
            for src_dir, subdirs, files in os.walk(source_folder):
       
                relative_path = os.path.relpath(src_dir, source_folder)
                dest_dir = os.path.join(destination_folder, relative_path) # Construct the destination path
               
                os.makedirs(dest_dir, exist_ok = True) # Create directories in the destination folder, if they don't exist
       
                for file in tqdm(files):
                    src_file = os.path.join(src_dir, file)
                    dest_file = os.path.join(dest_dir, file)
           
                    if os.path.exists(dest_file): # If the file already exists, skip it
                        print(f"File '{dest_file}' already exists. Skipping.")
                        continue
           
                    else:
                        shutil.move(src_file, dest_file) # Move the file if it doesn't exist
                        print(f"File '{src_file}' has been moved.")

        except shutil.Error as e:
            if "network" in str(e).lower(): # Retry if a network error is detected
                print(f"Network error occurred. Retrying after {retry_delay} seconds.")
                retries += 1
                time.sleep(retry_delay)  # Wait before retrying

            else:
                print(f"Error moving folder: {e}")
                break  # Exit the loop if it's not a network error


def transfer_folder_with_retry(source_folder, destination_folder, retry_delay = 5):
    '''Transfer a single source folder to the destination folder.
    Retry if a network-related error occurs during transfer.
    If the destination folder already exists, merge the folders and move files.
   
    args:
        source_folder (str): path to source folder
        destination_folder (str): path to destination folder
        retry_delay (float): delay in seconds from error to transfer is retried
    '''
   
    while True:
        try:
            source = Path(source_folder)
            destination = Path(destination_folder)
           
            new_destination = destination / source.name # Create destination folder path

            if new_destination.exists():
                print(f"Destination folder '{new_destination}' already exists. Merging and moving folders.")
                if not merge_and_move_folders(source_folder, new_destination): # Checks return value
                    print("Merging folders failed. ")
                    break
            else:
                shutil.move(source, new_destination) # Move the entire folder                
                print(f"Successfully moved: {source}")
               
            print("Folder transfer complete.")
            break  # Exit the loop if the transfer was successful
       
        except shutil.Error as e:
            if "network" in str(e).lower(): # Retry if a network error is detected
                print(f"Network error occurred. Retrying after {retry_delay} seconds.")
                time.sleep(retry_delay)  # Wait before retrying

            else:
                print(f"Error moving folder: {e}")
                break  # Exit the loop if it's not a network error


def transfer_multiple_folders_with_retry(source_folders, destination_folder):
    '''Transfer multiple source folders to the destination folder one by one.
    Retry if a network-related error occurs during transfer for each folder.
   
    args:
        source_folders(list of strings): list of paths to source folders
        destination_folder(str): path to destination folder
    '''
   
    for source_folder in tqdm(source_folders):
        if not os.path.exists(source_folder): # Check if source folder exists, if not, continue with the next folder
            print(f"Source folder '{source_folder}' does not exist. Skipping.")
            continue
       
        print(f"\nTransferring folder: {source_folder}")
       
        transfer_folder_with_retry(source_folder, destination_folder)
       

if __name__ == "__main__":
    source_folders = [
    "K:/Slides 04.03.2025",
    "K:/Slides 27.02.2025",
    "J:/Slides 25.02.2025",
    "J:/Slides 11.02.2025",
    "J:/Slides 28.02.2025"
    ]
    destination_folder = "PATH"

    transfer_multiple_folders_with_retry(source_folders, destination_folder)
