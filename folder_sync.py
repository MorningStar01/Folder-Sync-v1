import os
import time
import shutil
import hashlib
import argparse
import logging
from pathlib import Path


# Function to get all files in the given folder
def get_all_files(folder_path):
    all_files = set()
    # using "_" will ignore the list of directory names
    for root, _, file_list in os.walk(folder_path):
        for file in file_list:
            full_file_path = os.path.join(root, file)
            relative_file_path = Path(full_file_path).relative_to(folder_path)
            all_files.add(relative_file_path)
    
    return all_files

# Function to calculate the MD5 hash of a file
def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# print(md5("C:\\Users\\danpo\\Desktop\\Veeam\\SSSS\\t2.txt"))

def sync_folders(source, replica):
    source_files = get_all_files(source)
    replica_files = get_all_files(replica)

    # Iterate through source files and update the replica folder
    for file in source_files:
        source_file = source / file
        replica_file = replica / file

        # If the file is not in the replica folder, create it
        if file not in replica_files:
            os.makedirs(replica_file.parent, exist_ok=True)
            try:
                shutil.copy(source_file, replica_file)
                source_file_hash = md5(source_file)
                logging.info(f"Created: {replica_file} (MD5: {source_file_hash})")
            except Exception as e:
                logging.error(f"Error creating {replica_file}: {e}")

        # If the file is in the replica folder but has a different MD5 hash, update it
        else:
            source_file_hash = md5(source_file)
            replica_file_hash = md5(replica_file)
            if source_file_hash != replica_file_hash:
                try:
                    shutil.copy(source_file, replica_file)
                    logging.info(f"Updated: {replica_file} (Old MD5: {replica_file_hash}, New MD5: {source_file_hash})")
                except Exception as e:
                    logging.error(f"Error updating {replica_file}: {e}")

    # Iterate through replica files and remove files that are not in the source folder
    for file in replica_files:
        if file not in source_files:
            replica_file = replica / file
            replica_file_hash = md5(replica_file)
            try:
                os.remove(replica_file)
                logging.info(f"Removed: {replica_file} (MD5: {replica_file_hash})")
            except Exception as e:
                logging.error(f"Error removing {replica_file}: {e}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Synchronize two folders using MD5.")
    parser.add_argument("source", help="Source folder path.")
    parser.add_argument("replica", help="Replica folder path.")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds.")
    parser.add_argument("logfolder", help="Log folder path.")

    args = parser.parse_args()

    # Create the log folder if it doesn't exist
    os.makedirs(args.logfolder, exist_ok=True)

    # Check if logfile.log exists in the log folder, and create it if it doesn't
    log_file_path = os.path.join(args.logfolder, "logfile.log")
    if not os.path.exists(log_file_path):
        open(log_file_path, "w").close()

    # Set up logging
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)

    source = Path(args.source)
    replica = Path(args.replica)

    # Continuously synchronize the folders with the specified interval
    while True:
        sync_folders(source, replica)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
