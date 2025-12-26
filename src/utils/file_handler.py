"""
File operations and JSON persistence module.

Handles file system operations, directory validation, and JSON data storage.
"""

import os
import glob
import json
import sys
from pathlib import Path


def find_jpeg_files(directory):
    """
    Find all .jpeg files in a directory.

    Args:
        directory: Directory path to search

    Returns:
        List of paths to .jpeg files found
    """
    jpeg_paths = glob.glob(os.path.join(directory, '*.jpeg'))

    if not jpeg_paths:
        print("No jpeg files found in the directory.")
        return []

    print("Jpeg files found:")
    for file in jpeg_paths:
        print(file)

    return jpeg_paths


def verify_directory(directory):
    """
    Verify if a directory exists.

    Args:
        directory: Directory path to verify

    Returns:
        Success message if directory is valid

    Raises:
        ValueError: If directory doesn't exist
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The path '{directory}' is not a valid directory.")
    return f"The directory '{directory}' is valid."


def find_valid_directory(directories):
    """
    Try to validate a directory from a list of candidates.
    Returns the first valid directory found.

    Args:
        directories: List of directory paths to try

    Returns:
        First valid directory path found

    Raises:
        ValueError: If none of the directories are valid
    """
    for path in directories:
        try:
            result = verify_directory(path)
            print(result)
            return path
        except ValueError as e:
            print(f"Error detected: {e}")

    raise ValueError("None of the provided directories are valid.")


def save_json(filepath, data):
    """
    Save data to a JSON file.

    Args:
        filepath: File path to save to
        data: Data to save (list, dict, etc.)
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath):
    """
    Load data from a JSON file.

    Args:
        filepath: File path to read from

    Returns:
        Loaded data, or empty list if file not found/corrupted
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"The file {filepath} does not exist, returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"The file {filepath} is empty or corrupted, returning empty list.")
        return []


def get_category_file_path(category_name, categories_dir):
    """
    Get the full path to a category JSON file.

    Args:
        category_name: Name of the category
        categories_dir: Path to categories directory

    Returns:
        Path object to the category file
    """
    if category_name == 'break':
        return None

    return Path(categories_dir) / f"{category_name}.json"


def get_database_json_path(categories_dir):
    """Get path to Database.json file."""
    return Path(categories_dir) / 'Database.json'


def get_id_json_path(categories_dir):
    """Get path to id.json file."""
    return Path(categories_dir) / 'id.json'
