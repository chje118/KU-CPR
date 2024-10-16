# Transfer of files from multiple local folders to network drive
# Gaps in network connection results in interrupted file transfer, with error message: "An unexpected network error occurred".

import os
import shutil
from pathlib import Path
import time
from tqdm import tqdm

def merge_and_move_folders(src_folder, dest_folder):
    """ Move source folder into destination folder.
    Merge folders if destination folder already exists.
    If a file already exists in the destination folder, it is skipped.

    args:
        src_folder(str): path to source folder
        dest_folder(str): path to destination folder
    """
    
    try: 
        # If folder exists, merge the contents
        for src_dir, subdirs, files in os.walk(src_folder):

            # Construct the destination path for the current directory
            relative_path = os.path.relpath(src_dir, src_folder)
            dest_dir = os.path.join(dest_folder, relative_path)
        
            # Create directories in the destination folder if they don't exist
            os.makedirs(dest_dir, exist_ok = True)
        
            # Move files from the source to the destination directory
            # tqdm is used to show a progress bar for the file transfer for each folder
            for file in tqdm(files, desc=f"Moving files in {src_folder}",leave = False):
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
        return True # Return True to indicate complete process

    except KeyboardInterrupt:
        print("Process interrupted by user.")
        return False  # Return False to indicate an incomplete process


def transfer_folder_with_retry(source_folder, destination_folder, max_retries, retry_delay):
    """ Transfer a single source folder to the destination folder.
    Retry if a network-related error occurs during transfer.
    If the destination folder already exists, merge the folders and move files.
    
    args:
        source_folder (str): path to source folder
        destination_folder (str): path to destination folder
        max_retries (int): number of retries before process is stopped, default 10
        retry_delay (float): delay in seconds from error to transfer is retried, default 5 seconds
    """
    
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

                # Checks return value of the merge_and_move_folders()
                if not merge_and_move_folders(source_folder, new_destination):
                    print("Transfer failed. Error while merging folders.")
                    break
            else:
                # Move the entire folder to the destination
                shutil.move(source, new_destination)
                print(f"Successfully moved: {source} to {new_destination}")

            print("Folder transfer complete.")
            break  # Exit the loop if the transfer was successful

        except (shutil.Error) as e:
            if "network error" not in e:
                print(f"Error moving folder: {e}")    
                break # Exit the loop if it's not a network error
            
            retry_count += 1
            time.sleep(retry_delay)  # Wait before retrying
            
            if retry_count > max_retries:
                print(f"Exceeded maximum retries. Transfer failed.")
                raise e # Raise the exception after the final attempt
            
        except KeyboardInterrupt:
            print("Process interrupted by user.")
            return False

def transfer_multiple_folders_with_retry(source_folders, destination_folder, max_retries, retry_delay):
    """ Transfer multiple source folders to the destination folder one by one.
    Retry if a network-related error occurs during transfer for each folder.
    
    args:
        source_folders(list of strings): list of paths to source folders
        destination_folder(str): path to destination folder
        max_retries(int): number of retries before process is stopped, default 10
        retry_delay(float): delay in seconds from error to transfer is retried, default 5 seconds
        
    """
    try:
        with tqdm(total=len(source_folders), desc="Transferring Folders", unit="folder") as folder_pbar:
        
            for source_folder in source_folders:
                # Check if source folder exists, if not, continue with the next folder
                if not os.path.exists(source_folder):
                    print(f"Source folder '{source_folder}' does not exist. Skipping.")
                    folder_pbar.update(1)   # Increase progress bar with 1
                    continue
        
                print(f"\nTransferring folder: {source_folder}")
                if transfer_folder_with_retry(source_folder, destination_folder, max_retries, retry_delay):
                    folder_pbar.update(1)
                else:
                    break

    except KeyboardInterrupt:
        print("Process interrupted by user.")


# Example usage. Script only executes if run directly (not when imported as a module).
if __name__ == "__main__":
    source_folders = [
        "/Path/To/Folder/1",
        "/Path/To/Folder/2",
        "/Path/To/Folder/3"
    ]
    destination_folder = "/Path/To/Destination/Folder"

transfer_multiple_folders_with_retry(source_folders, destination_folder, max_retries = 10, retry_delay = 5)
