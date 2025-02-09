# Transfer of files from multiple local folders to network drive
# Gaps in network connection results in interrupted file transfer, with error message: "An unexpected network error occurred".

import os
import shutil
from pathlib import Path
import time
from tqdm import tqdm

# Change script to class objects
class FileTransfer: 
    def __init__(self, retry_delay:int =5):
        """ Initialize the FileTransfer object.
        args:
            retry_delay (int): Time in seconds to wait before retrying a failed transfer.
        """
        self.retry_delay = retry_delay
    
    def merge_and_move_folders(self, source_folder:str, destination_folder:str) -> bool:
        """ Merge source folder into destination folder.
        If a file already exists in the destination folder, it is skipped.
        args:
            source_folder(str): path to source folder
            destination_folder(str): path to destination folder
        returns: 
            bool: True if successful, False otherwise.
        """
        try: 
            for src_dir, subdirs, files in os.walk(source_folder):
                relative_path = os.path.relpath(src_dir, source_folder)
                dest_dir = os.path.join(destination_folder, relative_path) # Construct destination path

                os.makedirs(dest_dir, exist_ok = True) # Create directories in the destination folder if they don't exist
            
                for file in tqdm(files, desc=f"Merging files in {src_dir}"):
                    src_file = os.path.join(src_dir, file)
                    dest_file = os.path.join(dest_dir, file)

                    if os.path.exists(dest_file): # If the file already exists, skip it
                        print(f"File '{dest_file}' already exists. Skipping.")
                        continue
                
                    shutil.move(src_file, dest_file) # Move the file if it doesn't exist
                    print(f"File '{src_file}' has been moved.")
            
            return True
        
        except shutil.Error as e:
            if "network" in str(e).lower(): # Retry if a network error is detected
                print(f"Network error occurred. Retrying after {self.retry_delay} seconds.")
                time.sleep(self.retry_delay) # Wait before retrying
                return False
            
            else:
                print(f"Error moving folder: {e}")
                return False # Exit the loop if it's not a network error

    def transfer_folder_with_retry(self, source_folder:str, destination_folder:str)->bool:
        """ Transfer a single source folder to the destination folder.
        Retry if a network-related error occurs during transfer.
        args:
            source_folder (str): path to source folder
            destination_folder (str): path to destination folder
        """
        source = Path(source_folder)
        destination = Path(destination_folder) / source.name # Create destination folder path
                
        while True:
            try:
                if destination.exists(): #Merge folder, if folder already exists
                    print(f"Folder '{destination}' already exists. Merging folders.")
                    if not self.merge_and_move_folders(source_folder, destination): # Checks return value
                        print("Transfer failed. Error while merging folders.")
                        return
                else:
                    shutil.move(source, destination) # Move the entire folder to the destination
                    print(f"Successfully moved: {source}")

                print("Folder transfer complete.")
                return

            except (shutil.Error) as e:
                if "network" in str(e).lower(): # Retry if a network error is detected
                    print(f"Network error occurred. Retrying after {self.retry_delay} seconds.")
                    time.sleep(self.retry_delay) # Wait before retrying
                else: 
                    print(f"Error moving folder: {e}")
                    return

    def transfer_multiple_folders_with_retry(self, source_folders: list[str], destination_folder: str):
        """ Transfer multiple source folders to the destination folder one by one.
        args:
            source_folders(list of strings): list of paths to source folders
            destination_folder(str): path to destination folder
        """
        for source_folder in tqdm(source_folders, , desc="Transferring folders"):
            if not os.path.exists(source_folder): # Check if source folder exists, if not, continue with the next folder
                print(f"Source folder '{source_folder}' does not exist. Skipping.")
                continue
        
            print(f"\nTransferring folder: {source_folder}")
            self.transfer_folder_with_retry(source_folder, destination_folder)     

# Example usage. Script executes if run directly (not when imported as a module).
if __name__ == "__main__":
    source_folders = [
        "/Path/To/Folder/1",
        "/Path/To/Folder/2",
        "/Path/To/Folder/3"
        ]
    destination_folder = "/Path/To/Destination/Folder"

    # Create an instance of FolderTransfer with a retry delay of 5 seconds
    transfer_tool = FileTransfer(retry_delay=5)
    transfer_tool.transfer_multiple_folders_with_retry(source_folders, destination_folder)
