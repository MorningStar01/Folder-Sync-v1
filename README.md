# Folder Sync

Folder Sync is a Python script to synchronize two folders using MD5 hash, ensuring the content of the replica folder matches the content of the source folder. The synchronization is performed periodically, and file creation, copying, and removal operations are logged to a file and console output.

## Requirements

- Python 3.7 or higher

## Installation

1. Clone the repository:
git clone https://github.com/MorningStar01/folder-sync.git

2. Change directory to the `folder-sync` folder

## Usage

To run the script, use the following command:

python folder_sync.py <source_folder> <replica_folder> <interval> <log_folder>
  
- `<source_folder>`: Path to the source folder
- `<replica_folder>`: Path to the replica folder
- `<interval>`: Synchronization interval in seconds
- `<log_folder>`: Path to the folder where the log file should be stored

Example: python folder_sync.py "C:\Users\user\Desktop\Source" "C:\Users\user\Desktop\Replica" 10 "C:\Users\user\Desktop\Logs"
This command will synchronize the "Source" and "Replica" folders every 10 seconds and store the logs in the "Logs" folder.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit pull requests with your changes.

## License
This project is released under the MIT License.
