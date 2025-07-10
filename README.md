KU-CPR: Novo Nordisk Foundation Center for Protein Research. Project 100k. 

FileTransfer_MultipleFolders.py
This script is designed to transfer files from multiple local folders to a network drive, ensuring reliable transfer despite network interruptions.

Features:
- Merges and moves folders, avoiding duplication of existing files.
- Retries file transfer in case of network errors.
- Provides a progress bar for the transfer process using tqdm.

Functions:
- merge_and_move_folders(src_folder, dest_folder)
Merges the contents of the source folder into the destination folder. If a file already exists in the destination folder, it is skipped.

- transfer_folder_with_retry(source_folder, destination_folder, max_retries, retry_delay)
Transfers a source folder to the destination folder with retries in case of network-related errors.

- transfer_multiple_folders_with_retry(source_folders, destination_folder)
Transfers multiple source folders to the destination folder, one by one, with retries in case of network-related errors.

Usage:
The script can be executed directly, specifying the source folders and the destination folder. The example below shows how to use the script:

source_folders = [
  "/Path/To/Folder/1",
  "/Path/To/Folder/2",
  "/Path/To/Folder/3"
]
destination_folder = "/Path/To/Destination/Folder"
transfer_multiple_folders_with_retry(source_folders, destination_folder)

Dependencies:
- os
- shutil
- pathlib
- time
- tqdm
