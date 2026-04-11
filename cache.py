
import os
import json
import logging
from pathlib import Path

def save_cache(cache_data, folder_path, filename):
    """
    Saves a dictionary as a JSON file in the 'cache' folder.
    """
    # 1. Define the directory and ensure it exists
    cache_dir = folder_path / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Define the full file path (DON'T overwrite 'folder_path')
    full_file_path = cache_dir / filename
    
    # 3. Open the file and write
    with open(full_file_path, "w") as o:
        json.dump(cache_data, o, indent=4)
        
    logging.debug(f"{filename} updated correctly")

def fetch_cache(folder_path, filename):
    """
    Reads a JSON file from the 'cache' folder.
    """
    full_file_path = folder_path / "cache" / filename
    
    try:
        with open(full_file_path, "r") as t:
            answer = json.load(t)
        logging.debug(f"{filename} successfully read")
        return answer
    except FileNotFoundError:
        logging.warning(f"Cache {filename} not found.")
        return {}