#Number of files of type .mrxs
#Scan 100.000 slides of type .mrxs
#Script to keep status of scanned number of slides

import os

def count_mrxs_files(directory_path):
    '''Count number of files of type .mrxs in specified directory, including subdirectories'''
    
    # Traverse the directory and count .mrxs files, including in subdirectories
    mrxs_count = 0
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.mrxs'):
                mrxs_count += 1

    return mrxs_count


# Example usage
directory_path = 'path/to/directory'

# Run program
if __name__ == '__main__':
    mrxs_file_count = count_mrxs_files(directory_path)
    print(f"Number of .mrxs files: {mrxs_file_count}")

