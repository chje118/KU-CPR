#Transfer of files from multiple local folders to network drive
#Gaps in network connection results in interrupted file transfer, with error message: "An unexpected network error occurred".

import os
import shutil
from pathlib import Path
import time

def merge_and_move_folders(src_folder, dest_folder):
    '''Move source folder into destination folder.
    Merge folders if destination folder already exists.
    If a file already exists in the destination folder, it is skipped.

    args:
        src_folder(str): path to source folder
        dest_folder(str): path to destination folder
    
    '''
    
    # If folder exists, merge the contents
    for src_dir, subdirs, files in os.walk(src_folder):

        # Construct the destination path for the current directory
        relative_path = os.path.relpath(src_dir, src_folder)
        dest_dir = os.path.join(dest_folder, relative_path)
        
        # Create directories in the destination folder if they don't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Move files from the source to the destination directory
        for file in files:
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)
            
            # If the file already exists, skip it
            if os.path.exists(dest_file):
                print(f"File '{dest_file}' already exists. Skipping.")
                continue
            else:
                # Move the file if it doesn't exist
                shutil.move(src_file, dest_file)
                print(f"File '{src_file}' has been moved.")

    # Once all files have been moved, remove the source folder
    shutil.rmtree(src_folder)
    print(f"Source folder '{src_folder}' has been removed.")
    return True


def transfer_folder_with_retry(source_folder, destination_folder, max_retries, retry_delay):
    '''Transfer a single source folder to the destination folder.
    Retry if a network-related error occurs during transfer.
    If the destination folder already exists, merge the folders and move files.
    
    args:
        source_folder (str): path to source folder
        destination_folder (str): path to destination folder
        max_retries (int): number of retries before process is stopped
        retry_delay (float): delay in seconds from error to transfer is retried
        
    '''
    
    retry_count = 0
    while retry_count <= max_retries:
        try:
            # Convert to Path objects for easier handling
            source = Path(source_folder)
            destination = Path(destination_folder)

            # Create destination folder path
            new_destination = destination / source.name

            #Merge folder, if folder already exists
            if new_destination.exists():
                print(f"Destination folder '{new_destination}' already exists. Merging and moving folders.")

                #Checks return value of the merge_and_move_folders()
                if not merge_and_move_folders(source_folder, new_destination):
                    print("Transfer canceled by user.")
                    break
            else:
                # Move the entire folder to the destination
                shutil.move(source, new_destination)
                print(f"Successfully moved: {source} to {new_destination}")

            print("Folder transfer complete.")
            break  # Exit the loop if the transfer was successful

        except shutil.Error as e:
            # Retry if a network error is detected
            if "network error" in str(e).lower():
                retry_count = retry_count + 1
                if retry_count <= max_retries:
                    print(f"Network error occurred. Retrying {retry_count}/{max_retries} after {retry_delay} seconds.")
                    time.sleep(retry_delay)  # Wait before retrying
                else:
                    print(f"Exceeded maximum retries ({max_retries}). Transfer failed.")
                    raise e  # Raise the exception after the final attempt
            else:
                print(f"Error moving folder: {e}")
                break  # Exit the loop if it's not a network error

def transfer_multiple_folders_with_retry(source_folders, destination_folder, max_retries, retry_delay):
    '''Transfer multiple source folders to the destination folder one by one.
    Retry if a network-related error occurs during transfer for each folder.
    
    args:
        source_folders(list of strings): list of paths to source folders
        destination_folder(str): path to destination folder
        max_retries(int): number of retries before process is stopped
        retry_delay(float): delay in seconds from error to transfer is retried
        
    '''
    for source_folder in source_folders:
        # Check if source folder exists, if not, continue with the next folder
        if not os.path.exists(source_folder):
            print(f"Source folder '{source_folder}' does not exist. Skipping.")
            continue
        
        print(f"\nTransferring folder: {source_folder}")
        transfer_folder_with_retry(source_folder, destination_folder, max_retries, retry_delay)

# Example usage
source_folders = [
    "/Path/To/Folder/1",
    "/Path/To/Folder/2",
    "/Path/To/Folder/3"
]
destination_folder = "/Path/To/Destination/Folder"
max_retries = 10
retry_delay = 5

transfer_multiple_folders_with_retry(source_folders, destination_folder, max_retries, retry_delay)
