import os
import shutil
import hashlib
import logging


def synchronize_folders(source, replica):
    """
    :param source: Path to the source directory that contains the files to be synchronized.
    :param replica: Path to the replica directory where the files should be synchronized to.
    :return: None
    """
    create_directories(source, replica)
    process_files(source, replica)
    clean_replica(source, replica)


def calculate_md5(file_path):
    """
    :param file_path: The path to the file for which the MD5 checksum needs to be calculated.
    :return: The MD5 checksum of the file as a hexadecimal string.
    """
    hash_md5 = hashlib.md5()
    # Open the file in binary read mode
    with open(file_path, "rb") as f:
        # Read the file in chunks of 4096 bytes
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_directories(source, replica):
    """
    :param source: The path to the source directory tree that will be mirrored.
    :param replica: The path to the replica directory where the directory structure will be created.
    :return: None
    """
    for dirpath, _, _ in os.walk(source):
        # Construct the relative path from source to current directory
        relative_path = os.path.relpath(dirpath, source)
        # Construct the corresponding path in the replica folder
        replica_dir = os.path.join(replica, relative_path)
        # Create directories in the replica folder if they don't exist
        os.makedirs(replica_dir, exist_ok=True)


def process_files(source, replica):
    """
    :param source: The directory where the source files are located.
    :param replica: The directory where the files should be replicated.
    :return: None
    """
    for dirpath, _, filenames in os.walk(source):
        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            replica_file = os.path.join(replica, os.path.relpath(source_file, source))
            # Check if the file needs to be copied or updated
            if not os.path.exists(replica_file) or \
                    calculate_md5(source_file) != calculate_md5(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied: {source_file} to {replica_file}")


def clean_replica(source, replica):
    """
    :param source: The source directory path containing the original files.
    :param replica: The replica directory path which needs to be cleaned based on the source directory.
    :return: None
    """
    for replica_dirpath, dirnames, filenames in os.walk(replica, topdown=False):
        source_dirpath = os.path.join(source, os.path.relpath(replica_dirpath, replica))
        remove_files_not_in_source(source_dirpath, replica_dirpath, filenames)
        remove_dirs_not_in_source(source_dirpath, replica_dirpath, dirnames)


def remove_files_not_in_source(source_dir, replica_dir, filenames):
    """
    :param source_dir: Directory path of the source directory containing the original files.
    :param replica_dir: Directory path of the replica directory from which files will be removed if they do not exist in the source directory.
    :param filenames: List of filenames to check for existence in the source directory.
    :return: None
    """
    for filename in filenames:
        replica_file = os.path.join(replica_dir, filename)
        source_file = os.path.join(source_dir, filename)
        if not os.path.exists(source_file):
            os.remove(replica_file)
            logging.info(f"Removed: {replica_file}")


def remove_dirs_not_in_source(source_dir, replica_dir, dirnames):
    """
    :param source_dir: Path to the source directory.
    :param replica_dir: Path to the replica directory.
    :param dirnames: List of directory names to check.
    :return: None
    """
    for dirname in dirnames:
        replica_subdir = os.path.join(replica_dir, dirname)
        source_subdir = os.path.join(source_dir, dirname)
        if not os.path.exists(source_subdir):
            shutil.rmtree(replica_subdir)
            logging.info(f"Removed directory: {replica_subdir}")


def setup_logging(log_file):
    """
    :param log_file: The path to the file where logs will be written.
    :return: None
    """
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


# Example usage
if __name__ == "__main__":
    setup_logging("sync_log.txt")
    synchronize_folders("path/to/source", "path/to/replica")
