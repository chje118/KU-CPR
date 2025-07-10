"""
Count number of files of a given type in a list of directories.
"""

import os

class FileCounter:
    """Class to count files in a list of directories."""
    def __init__(self, directories: list[str], file_type: str):
        self.directories = directories
        self.file_type = file_type

    def get_file_count(self)-> None:
        """ Print total number of files. """
        count = self.file_count()
        return print(f'Total number of {self.file_type} files: {count}')     
    
    def file_count(self) -> int:
        """ Count total number of files in the list of directories."""
        total_count = 0
        for directory in self.directories:
            subcount = self._count_in_directory(directory)
            total_count += subcount
        return total_count

    def _count_in_directory(self, path: str) -> int:
        """ Count files in given directory path. """
        count = 0
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(self.file_type):
                        count += 1
        except (PermissionError, FileNotFoundError) as e:
            print(f"Skipping {path}: {e}")
        print(f"Number of files in {path}: {count}") 
        return count
    
if __name__ == '__main__':
    directory_paths = [
        'path/to/directory'
    ]

    file_type = '.mrxs'

    MRXScounter = FileCounter(directory_paths, file_type)
    MRXScounter.get_file_count()