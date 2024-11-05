import argparse  # For parsing command-line arguments
import time  # For delays between synchronization intervals
import os  # For interacting with the operating system
from sync_functions import setup_logging, synchronize_folders  # Import custom functions for logging and syncing

SYNC_INTERVAL = 5  # Default synchronization interval in seconds


def synchronize_folders_continuously(source, replica):
    """
    :param source: The directory path for the source folder to be synchronized.
    :param replica: The directory path for the replica folder where changes will be mirrored.
    :return: None
    """
    while True:
        if not os.path.exists(source):
            # Check if the source folder exists; if not, print an error message and exit the loop
            print(f"Source folder '{source}' does not exist.")
            break
        synchronize_folders(source, replica)  # Synchronize the source and replica folders
        print(f"Synchronized '{source}' to '{replica}'.")  # Indicate successful synchronization
        time.sleep(SYNC_INTERVAL)  # Wait for the specified interval before the next synchronization


def main(source_folder, replica_folder, log_file):
    """
    :param source_folder: The path to the source directory that needs to be synchronized.
    :param replica_folder: The path to the target directory where the content will be replicated.
    :param log_file: The path to the log file where synchronization logs will be stored.
    :return: None
    """
    setup_logging(log_file)  # Set up logging to the specified log file
    synchronize_folders_continuously(source_folder, replica_folder)  # Start continuous synchronization


# Example usage
if __name__ == "__main__":
    # Set up argument parser for command-line execution
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder")  # Path to the source folder
    parser.add_argument("replica", help="Path to the replica folder")  # Path to the replica folder
    parser.add_argument("log_file", help="Path to the log file")  # Path to the log file
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds",
                        default=SYNC_INTERVAL)  # Sync interval
    args = parser.parse_args()  # Parse the command-line arguments

    # Call the main function with parsed arguments
    main(args.source, args.replica, args.log_file)