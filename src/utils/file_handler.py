"""
File operations and JSON persistence module.

Handles file system operations, directory validation, and JSON data storage.
"""

import os
import glob
import json
<<<<<<< Updated upstream
import sys
=======
>>>>>>> Stashed changes
from pathlib import Path
from typing import Any, Optional, Union


<<<<<<< Updated upstream
def find_jpeg_files(directory):
    """
    Find all .jpeg files in a directory.
=======
def is_file_open(file_path: str, timeout: int = 30) -> bool:
    """Check if a file is currently open by another process.

    Attempts to rename the file to itself to detect if the file is locked
    by another process (common on Windows when files are open in Excel).

    Args:
        file_path: Path to the file to check
        timeout: Maximum wait time in seconds (unused, kept for API compatibility)

    Returns:
        True if the file is currently open/locked, False if available
    """
    if not os.path.exists(file_path):
        return False

    try:
        # Attempt to rename file to itself - fails if file is locked
        os.rename(file_path, file_path)
        return False  # No error: file is available
    except OSError:
        return True  # Error: file is in use


def remove_file(file_path: str) -> None:
    """Remove a file from the filesystem.

    Deletes the specified file and prints a status message indicating
    success or the type of failure encountered.

    Args:
        file_path: Path to the file to delete

    Returns:
        None
    """
    try:
        os.remove(file_path)
        print(f"The file '{file_path}' has been successfully deleted.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_pdf_files(directory: Union[str, Path]) -> list[str]:
    """Find all PDF files in a directory.

    Searches the specified directory for files with .pdf extension
    and prints the list of files found.
>>>>>>> Stashed changes

    Args:
        directory: Directory path to search for PDF files

    Returns:
        List of full paths to PDF files found, empty list if none found
    """
<<<<<<< Updated upstream
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
=======
    pdf_paths = glob.glob(os.path.join(str(directory), '*.pdf'))

    if not pdf_paths:
        print("No PDF files found in the directory.")
        return []

    print("PDF files found:")
    for file in pdf_paths:
        print(file)

    return pdf_paths


def find_valid_directory(directories: list[str]) -> str:
    """Find the first valid directory from a list of candidates.

    Iterates through the provided directory paths and returns the first
    one that exists and is a valid directory.
>>>>>>> Stashed changes

    Args:
        directories: List of directory paths to validate

    Returns:
        The first valid directory path found

    Raises:
        ValueError: If none of the provided directories are valid
    """
    for path in directories:
        if os.path.isdir(path):
            print(f"The directory '{path}' is valid.")
            return path
        else:
            print(f"Error detected: The path '{path}' is not a valid directory.")

    raise ValueError("None of the provided directories are valid.")


def save_json(filepath: Union[str, Path], data: Any) -> None:
    """Save data to a JSON file.

    Serializes the provided data to JSON format and writes it to the
    specified file path with UTF-8 encoding and pretty-printed formatting.

    Args:
        filepath: Path where the JSON file will be saved
        data: Data to serialize (must be JSON-serializable: dict, list, etc.)

    Returns:
        None
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath: Union[str, Path]) -> Any:
    """Load data from a JSON file.

    Reads and deserializes JSON data from the specified file. Returns an
    empty list if the file doesn't exist or contains invalid JSON.

    Args:
        filepath: Path to the JSON file to read

    Returns:
        Deserialized data from the JSON file, or empty list on error
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


def get_category_file_path(category_name: str, categories_dir: Union[str, Path]) -> Optional[Path]:
    """Get the full path to a category JSON file.

    Constructs the path to a category's JSON file within the categories
    directory. Returns None for the special 'break' category name.

    Args:
        category_name: Name of the category (without .json extension)
        categories_dir: Path to the directory containing category files

    Returns:
        Path object to the category JSON file, or None if category_name is 'break'
    """
    if category_name == 'break':
        return None

    return Path(categories_dir) / f"{category_name}.json"


def get_database_json_path(categories_dir: Union[str, Path]) -> Path:
    """Get the path to the Database.json file.

    Constructs the full path to the main database JSON file that contains
    all category definitions and their associated expenses.

    Args:
        categories_dir: Path to the categories directory

    Returns:
        Path object pointing to Database.json
    """
    return Path(categories_dir) / 'Database.json'


def get_id_json_path(categories_dir: Union[str, Path]) -> Path:
    """Get the path to the id.json file.

    Constructs the full path to the ID mapping JSON file that maps
    category indices to their Notion page IDs.

    Args:
        categories_dir: Path to the categories directory

    Returns:
        Path object pointing to id.json
    """
    return Path(categories_dir) / 'id.json'
