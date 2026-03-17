import os
import shutil
from datetime import datetime
import logging
from pathlib import Path

def create_backup_directory(base_dir):
    """
    Create a timestamped backup directory under the specified base directory.
    
    Args:
        base_dir (str): The base directory where backups will be stored.
        
    Returns:
        str: The path of the newly created backup directory.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(base_dir, f"zbrush_backup_{timestamp}")
        os.makedirs(backup_dir, exist_ok=True)
        return backup_dir
    except Exception as e:
        print(f"Error creating backup directory: {e}")
        raise

def copy_files_to_backup(source_dir, backup_dir):
    """
    Copy all files from the source directory to the backup directory.
    
    Args:
        source_dir (str): The directory containing ZBrush files to backup.
        backup_dir (str): The directory where files will be copied.
        
    Returns:
        None
    """
    try:
        if not os.path.exists(source_dir):
            print(f"Source directory does not exist: {source_dir}")
            return
        
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            backup_path = os.path.join(backup_dir, item)
            # Check if it's a file or a directory
            if os.path.isfile(source_path):
                shutil.copy2(source_path, backup_path)  # Use copy2 to preserve metadata
                print(f"Copied file: {source_path} to {backup_path}")
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, backup_path)  # Recursively copy directories
                print(f"Copied directory: {source_path} to {backup_path}")
    except Exception as e:
        print(f"Error while copying files: {e}")
        raise

def get_current_timestamp():
    """
    Get the current timestamp formatted as a string.
    
    Returns:
        str: Current timestamp in 'YYYY-MM-DD HH:MM:SS' format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# TODO: Implement logging instead of print statements for better tracking
# TODO: Add functionality to exclude certain file types or directories
# TODO: Consider adding a config file for user preferences (e.g., base directory)
