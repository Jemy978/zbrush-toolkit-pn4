import os
import shutil
import datetime
import sys
from pathlib import Path

def create_backup(source_dir, backup_root):
    """
    Create a backup of ZBrush project files from the source_dir to the backup_root directory
    with a timestamped folder.
    
    Args:
        source_dir (str): The directory containing ZBrush project files to back up.
        backup_root (str): The root directory where backups will be stored.
    """
    if not os.path.exists(source_dir):
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return
    
    if not os.path.isdir(source_dir):
        print(f"Error: The source path '{source_dir}' is not a directory.")
        return
    
    if not os.path.exists(backup_root):
        os.makedirs(backup_root)
        print(f"Created backup root directory: {backup_root}")

    # Create a timestamped folder for the backup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_root, f"backup_{timestamp}")
    
    try:
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")
        
        # Copy files from source_dir to the backup_dir
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            destination_path = os.path.join(backup_dir, item)
            
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
                print(f"Copied directory: {source_path} to {destination_path}")
            else:
                shutil.copy2(source_path, destination_path)  # preserves metadata
                print(f"Copied file: {source_path} to {destination_path}")
                
    except Exception as e:
        print(f"An error occurred during backup: {e}")
        return

def main():
    if len(sys.argv) != 3:
        print("Usage: python backup_automator.py <source_dir> <backup_root>")
        return
    
    source_dir = sys.argv[1]
    backup_root = sys.argv[2]
    
    create_backup(source_dir, backup_root)

if __name__ == "__main__":
    main()

# TODO: 
# - Add logging to a file instead of print statements.
# - Implement a way to compress backup directories.
# - Allow scheduling of backups using a cron job or similar.
