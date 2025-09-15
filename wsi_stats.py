import os
import pickle
from datetime import datetime
import pandas as pd

ROOT_DIR = "/path/to/wsi/folder"
CACHE_FILE = "/path/to/wsi/cache"

class WSIStats:
    def __init__(self, filename):
        self.filename = filename
        self.rekvnr = os.path.basename(filename)[:8]
        self.file_size = os.path.getsize(filename)
        self.date_modified = datetime.fromtimestamp(os.path.getmtime(filename))
        self.data_folder = os.path.splitext(filename)[0]
        self.data_folder_size = self.get_folder_size(self.data_folder) if os.path.isdir(self.data_folder) else 0

    @staticmethod
    def get_folder_size(folder):
        total = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total += os.path.getsize(fp)
        return total

    def to_dict(self):
        return {
            "filename": self.filename,
            "rekvnr": self.rekvnr,
            "file_size": self.file_size,
            "data_folder_size": self.data_folder_size,
            "date_modified": self.date_modified,
        }

class WSIStatsCache:
    def __init__(self, root_dir, cache_file):
        self.root_dir = root_dir
        self.cache_file = cache_file
        self.stats = []

    def scan_files(self):
        # Build a set of already cached file paths
        cached_files = set(stat.filename for stat in self.stats)
        new_stats = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for fname in filenames:
                if fname.lower().endswith('.mrxs'):
                    fpath = os.path.join(dirpath, fname)
                    if fpath not in cached_files:
                        new_stats.append(WSIStats(fpath))
        if new_stats:
            print(f"Found {len(new_stats)} new files.")
        self.stats.extend(new_stats)

    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.stats, f)

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                self.stats = pickle.load(f)
            return True
        return False

    def get_stats_dicts(self):
        return [stat.to_dict() for stat in self.stats]

def main():
    cache = WSIStatsCache(ROOT_DIR, CACHE_FILE)
    cache.load_cache()
    cache.scan_files()  # Always scan for new files
    cache.save_cache()
    stats_dicts = cache.get_stats_dicts()
    # Create DataFrame with filenames as index
    df = pd.DataFrame(stats_dicts)
    df.set_index("filename", inplace=True)
    print(df.head())

if __name__ == "__main__":
    main()